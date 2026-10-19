import sys, json, math, time, argparse
import torch, torch.nn as nn, torch.nn.functional as F

p = argparse.ArgumentParser()
p.add_argument("--data", required=True); p.add_argument("--out", required=True)
p.add_argument("--arm", required=True, choices=["A","B","C"])
p.add_argument("--d", type=int, default=128); p.add_argument("--L", type=int, default=4)
p.add_argument("--H", type=int, default=4); p.add_argument("--T", type=int, default=128)
p.add_argument("--B", type=int, default=32); p.add_argument("--steps", type=int, default=1200)
p.add_argument("--warmup", type=int, default=300); p.add_argument("--warmdown", type=int, default=350)
p.add_argument("--eval_every", type=int, default=50); p.add_argument("--seed", type=int, default=0)
p.add_argument("--threads", type=int, default=1)
p.add_argument("--lr", type=float, default=None); p.add_argument("--act", default=None)
a = p.parse_args()
torch.set_num_threads(a.threads); torch.manual_seed(a.seed)

text = open(a.data, encoding="utf-8").read()
chars = sorted(set(text)); stoi = {c:i for i,c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in text], dtype=torch.long)
n = int(0.9*len(data)); tr, va = data[:n], data[n:]
V = len(chars)
g = torch.Generator().manual_seed(1234)
def batch(src, B, gen=None):
    ix = torch.randint(len(src)-a.T-1, (B,), generator=gen)
    x = torch.stack([src[i:i+a.T] for i in ix]); y = torch.stack([src[i+1:i+a.T+1] for i in ix])
    return x, y
xv, yv = batch(va, 64, g)  # fixed eval batch

# recipe
if a.arm in ("A","C"):
    ln_bias, lin_bias, drop, act = False, False, 0.0, "relu"
else:  # B: ViT-like training recipe, activation matched (ReLU)
    ln_bias, lin_bias, drop, act = True, True, 0.1, "relu"
if a.act: act = a.act

class Rotary(nn.Module):
    def __init__(s, dim):
        super().__init__(); s.register_buffer("inv", 1.0/(10000**(torch.arange(0,dim,2).float()/dim)))
    def forward(s, T):
        f = torch.outer(torch.arange(T).float(), s.inv); return f.cos()[None,:,None,:], f.sin()[None,:,None,:]
def rope(x, c, s_):
    d = x.shape[3]//2; x1, x2 = x[...,:d], x[...,d:]
    return torch.cat([x1*c + x2*s_, -x1*s_ + x2*c], 3)

class Attn(nn.Module):
    def __init__(s):
        super().__init__(); s.qkv = nn.Linear(a.d, 3*a.d, bias=lin_bias); s.o = nn.Linear(a.d, a.d, bias=lin_bias)
        s.rot = Rotary(a.d//a.H); s.drop = drop
    def forward(s, x):
        B,T,C = x.shape; q,k,v = s.qkv(x).split(C, 2)
        q,k,v = [t.view(B,T,a.H,C//a.H) for t in (q,k,v)]; c,sn = s.rot(T); q,k = rope(q,c,sn), rope(k,c,sn)
        y = F.scaled_dot_product_attention(q.transpose(1,2),k.transpose(1,2),v.transpose(1,2),is_causal=True,
                                           dropout_p=s.drop if s.training else 0.0)
        return F.dropout(s.o(y.transpose(1,2).reshape(B,T,C)), s.drop, s.training)

class MLP(nn.Module):
    def __init__(s):
        super().__init__(); s.up = nn.Linear(a.d, 4*a.d, bias=lin_bias); s.down = nn.Linear(4*a.d, a.d, bias=lin_bias)
        s.z = None; s.xin = None
    def forward(s, x):
        if not s.training: s.xin = x.detach()
        z = s.up(x)
        if not s.training: s.z = z.detach()
        h = F.relu(z) if act=="relu" else F.gelu(z)
        return F.dropout(s.down(h), drop, s.training)

class Block(nn.Module):
    def __init__(s):
        super().__init__(); s.n1 = nn.LayerNorm(a.d, bias=ln_bias); s.n2 = nn.LayerNorm(a.d, bias=ln_bias)
        s.attn = Attn(); s.mlp = MLP(); s.sc = 1/math.sqrt(2*a.L)
    def forward(s, x):
        x = x + s.sc*s.attn(s.n1(x)); return x + s.mlp(s.n2(x))

class GPT(nn.Module):
    def __init__(s):
        super().__init__(); s.wte = nn.Embedding(V, a.d); s.h = nn.ModuleList([Block() for _ in range(a.L)])
        s.nf = nn.LayerNorm(a.d, bias=ln_bias); s.head = nn.Linear(a.d, V, bias=False); s.wte.weight = s.head.weight
    def forward(s, x, y=None):
        h = F.dropout(s.wte(x), drop, s.training)
        for b in s.h: h = b(h)
        lg = s.head(s.nf(h)); return lg, (F.cross_entropy(lg.view(-1,V), y.view(-1)) if y is not None else None)

m = GPT()

def ns5(G, steps=5, eps=1e-7):
    A_, B_, C_ = 3.4445, -4.7750, 2.0315
    X = G.bfloat16()/(G.norm()+eps); tr_ = G.size(0) > G.size(1)
    if tr_: X = X.T
    for _ in range(steps):
        A = X @ X.T; Bm = A @ X; X = A_*X + B_*Bm + C_*A @ Bm
    if tr_: X = X.T
    return X.to(G.dtype)
class Muon(torch.optim.Optimizer):
    def __init__(s, params, lr, momentum=0.95): super().__init__(params, dict(lr=lr, momentum=momentum))
    @torch.no_grad()
    def step(s):
        for gr in s.param_groups:
            for p_ in gr["params"]:
                if p_.grad is None: continue
                st = s.state[p_]; buf = st.setdefault("buf", torch.zeros_like(p_.grad))
                buf.mul_(gr["momentum"]).add_(p_.grad); g_ = p_.grad.add(buf, alpha=gr["momentum"])
                if g_.size(0) == 3*g_.size(1):
                    g_ = torch.cat([ns5(t) for t in g_.split(g_.size(1))]); sc = g_.size(1)**0.5
                else:
                    g_ = ns5(g_); sc = max(g_.size(0), g_.size(1))**0.5
                p_.add_(g_, alpha=-gr["lr"]*sc)

if a.arm == "A":
    base = 0.005
    mu = [p_ for n_,p_ in m.named_parameters() if n_.startswith("h.") and p_.ndim==2]
    ad = [p_ for n_,p_ in m.named_parameters() if not (n_.startswith("h.") and p_.ndim==2)]
    opts = [(torch.optim.AdamW(ad, lr=base, betas=(0.9,0.95), weight_decay=0.0), base),
            (Muon(mu, lr=0.1*base), 0.1*base)]
elif a.arm == "C":
    base = 1e-3
    opts = [(torch.optim.AdamW(m.parameters(), lr=base, betas=(0.9,0.95), weight_decay=0.0), base)]
else:
    base = a.lr if a.lr else 1e-4
    opts = [(torch.optim.Adam(m.parameters(), lr=base), base)]

def mult(t):
    if t < a.warmup: return (t+1)/a.warmup
    if t < a.steps - a.warmdown: return 1.0
    return (a.steps - t)/a.warmdown

@torch.no_grad()
def evaluate(t):
    m.eval(); _, loss = m(xv, yv); rows = []
    for li, b in enumerate(m.h):
        z = b.mlp.z.reshape(-1, 4*a.d)            # tokens x units
        mu_u = z.mean(0); sd_u = z.std(0)+1e-8
        rec = dict(layer=li, neg_frac=(z<0).float().mean().item(),
                   units_mean_neg=(mu_u<0).float().mean().item(),
                   med_mean_over_sd=(mu_u/sd_u).median().item(),
                   dead_units=((z>0).float().mean(0)==0).float().mean().item())
        if lin_bias:
            bpart = b.mlp.up.bias
            rec["bias_mean"] = bpart.mean().item()
            rec["frac_mean_from_bias"] = (bpart.abs().sum()/(mu_u.abs().sum()+1e-8)).item()
        rows.append(rec)
    m.train(); return dict(step=t, val_loss=loss.item(), layers=rows)

log = [evaluate(0)]; t0 = time.time()
for t in range(a.steps):
    x, y = batch(tr, a.B); _, loss = m(x, y); loss.backward()
    k = mult(t)
    for o, b0 in opts:
        for gr in o.param_groups: gr["lr"] = b0*k
        o.step(); o.zero_grad(set_to_none=True)
    if (t+1) % a.eval_every == 0 or t+1 == a.steps:
        r = evaluate(t+1); r["sec"] = time.time()-t0; log.append(r)
        print(a.arm, t+1, f"loss {r['val_loss']:.3f}", "neg", [round(l['neg_frac'],3) for l in r['layers']], f"{r['sec']:.0f}s", flush=True)
        json.dump(dict(args=vars(a), log=log), open(a.out, "w"))
