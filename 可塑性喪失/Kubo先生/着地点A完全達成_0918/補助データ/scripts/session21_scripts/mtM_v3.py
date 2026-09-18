"""mtM_v3.py — session19/session20 の mtM_v2 を継承した session21 版

追加: per-task per-seed の δ' (flip 直後・SGD 開始前) を保存

δ'_r(task=t, seed=s) := yhat(x_r; W(t-1)) - y_r
  - x_r  : task t の flip 後 32 支持点 (Xc after make_X(S))
  - y_r  : teacher output at 32 支持点 (Y after make_X(S))
  - W(t-1): task t 開始時 (flip 直後・SGD 前) の Wb, v, c

保存 shape: dprime (T, C, 32) float32

seed_rng を v2 と揃えれば、rng 呼び出し順序は SGD ループ前後で不変なので
zbar など既存 field は bit-exact に v2 の同じ tag の npz と一致するはず.
"""
import numpy as np, sys, time, json, os
sys.path.insert(0, '/home/kubo/project/Nakatsuka/claude/hole1_scripts')
from sim_act import load_ck, make_act
from model import support, oracle_g, teacher, FREE

U = ''
NBAND_THR = 0.3


def run(ckpath, seeds, eta, ntask, T=10000, seed_rng=0, freeze_dead_W=False, freeze_v=False,
        log_every=1, resume=None, kappa_dead=1.0, maintain=False, kahan=False):
    net, Tt, fs, rm, act, alpha = load_ck(ckpath); phi_f, dphi_f = make_act(act, alpha)
    C = len(seeds)
    if resume is None:
        W = np.stack([net['W'][s] for s in seeds]); b = np.stack([net['b'][s] for s in seeds])
        v = np.stack([net['v'][s] for s in seeds]); c = np.array([net['c'][s] for s in seeds])
        S = np.stack([fs[s] for s in seeds]).astype(int)
        Wb = np.concatenate([W, b[:, :, None]], 2)
    else:
        R = np.load(resume); Wb = R['Wb_final'].copy(); v = R['v_final'].copy(); c = R['c_final'].copy(); S = R['S_final'].copy()
    rng = np.random.default_rng(seed_rng); ar = np.arange(C)
    if resume is not None and 'rng_state' in R.files:
        rng.bit_generator.state = json.loads(str(R['rng_state']))
    if (kappa_dead != 1.0 or maintain) and resume is None:
        Xc0 = np.zeros((C, 32, 21))
        for i, s in enumerate(seeds):
            g = oracle_g(int(S[i].sum())); X = support(S[i].astype(float))
            Xc0[i] = np.concatenate([X - g, np.ones((32, 1))], 1)
        z0 = np.einsum('cru,chu->crh', Xc0, Wb).max(1); dead0 = (np.einsum('cru,chu->crh', Xc0, Wb) > 0).sum(1) == 0
        Wb[:, :, :20] *= np.where(dead0[:, :, None], kappa_dead, 1.0)
        z1 = np.einsum('cru,chu->crh', Xc0, Wb).max(1); Wb[:, :, 20] += np.where(dead0, z0 - z1, 0.0)
        tn = np.linalg.norm(Wb[:, :, :20], axis=2); coh = dead0.copy()
    if resume is not None and maintain:
        tn = R['tn'].copy(); coh = R['coh'].copy()

    def make_X(S):
        Xc = np.zeros((C, 32, 21)); Y = np.zeros((C, 32))
        for i, s in enumerate(seeds):
            g = oracle_g(int(S[i].sum())); X = support(S[i].astype(float))
            Xc[i] = np.concatenate([X - g, np.ones((32, 1))], 1); Y[i] = teacher(Tt, s, X)
        return Xc, Y
    zall = lambda Xs, Wb: np.einsum('cru,chu->crh', Xs, Wb)
    rec = {k: [] for k in ('kon', 'zmax', 'zbar', 'loss', 'kon_kick', 'zmax_kick', 'wflip_abs',
                            'wnorm', 'zmax_kick_prevW', 'zmax_kick_prevW_bonly', 'nband',
                            'kick_i', 'offset_i',
                            'zbar_kick',
                            'm_fac', 'm_n',
                            'dprime',
                            'z_kick',
                            'n_active',   # (C,) per task: number of "on" bits in S (post-flip)
                            'kp_hist')}    # (C,) per task: index of flipped bit
    Wb_start = Wb.copy()
    Xc, Y = make_X(S); z = zall(Xc, Wb)
    rec['kon'].append((z > 0).sum(1)); rec['zmax'].append(z.max(1)); rec['zbar'].append(z.mean(1))
    rec['nband'].append((np.abs(z) < NBAND_THR).sum(1).astype(np.int32))

    Wb_err = np.zeros_like(Wb) if kahan else None
    v_err = np.zeros_like(v) if kahan else None
    c_err = np.zeros_like(c) if kahan else None

    t0 = time.time()
    for task in range(1, ntask + 1):
        kp = rng.integers(0, 15, C); eps = 1 - 2 * S[ar, kp]; S[ar, kp] = 1 - S[ar, kp]
        Xc, Y = make_X(S)
        z_post = zall(Xc, Wb)
        rec['kon_kick'].append((z_post > 0).sum(1)); rec['zmax_kick'].append(z_post.max(1))
        rec['zbar_kick'].append(z_post.mean(1))
        rec['zmax_kick_prevW'].append(zall(Xc, Wb_start).max(1))
        Wb_bonly = Wb_start.copy(); Wb_bonly[:, :, 20] = Wb[:, :, 20]
        rec['zmax_kick_prevW_bonly'].append(zall(Xc, Wb_bonly).max(1))
        S_old = S.copy(); S_old[ar, kp] = 1 - S_old[ar, kp]
        n_old = S_old.sum(1); n_new = S.sum(1)
        dg = oracle_g(n_new) - oracle_g(n_old)
        Wsum = Wb[:, :, :20].sum(2)
        W_flip = Wb[ar, :, kp]
        rec['kick_i'].append(eps[:, None] * W_flip)
        rec['offset_i'].append(-dg[:, None] * Wsum)

        # === session21 additive: δ' per-event + z_kick per-event ===
        # 定義: δ'_r = yhat(x_r; W(t-1)) - y_r at flip 直後・SGD 開始前
        # ここで Wb は task 開始時 (前 task の SGD 完了直後) の重み = W(t-1) の役割
        # Xc, Y は make_X(S) で flip 後の supports/teacher で更新済み
        phi_post = phi_f(z_post)  # (C, 32, H)
        yhat_post = np.einsum('crh,ch->cr', phi_post, v) + c[:, None]  # (C, 32)
        dprime = yhat_post - Y  # (C, 32)
        rec['dprime'].append(dprime)
        # z_kick_full: (C, 32, H) — flip 直後・SGD 前の per-support per-unit z. Step C の φ'_{i,r} に必要
        rec['z_kick'].append(z_post)
        rec['n_active'].append(n_new.astype(np.int32).copy())  # (C,)
        rec['kp_hist'].append(kp.astype(np.int32).copy())      # (C,)
        # ==========================================================

        Wb_start = Wb.copy()
        dead_pre = (rec['kon'][-1] == 0)
        if freeze_dead_W == 'noncross':
            dead_pre = dead_pre & (rec['kon_kick'][-1] == 0)
        mask = np.ones((C, 100, 21))
        if freeze_dead_W:
            mask[:, :, :20] = np.where(dead_pre[:, :, None], 0.0, 1.0)
        for t in range(T):
            r = rng.integers(0, 32, C); x = Xc[ar, r]
            zz = np.einsum('cu,chu->ch', x, Wb); phi = phi_f(zz); dphi = dphi_f(zz)
            yh = (phi * v).sum(1) + c; d = yh - Y[ar, r]; gz = 2 * d[:, None] * v * dphi
            upd = eta * gz[:, :, None] * x[:, None, :]
            if freeze_dead_W:
                upd *= mask
            if kahan:
                y_k = (-upd) - Wb_err; t_k = Wb + y_k; Wb_err = (t_k - Wb) - y_k; Wb = t_k
                if not freeze_v:
                    uv = eta * 2 * d[:, None] * phi
                    y_k = (-uv) - v_err; t_k = v + y_k; v_err = (t_k - v) - y_k; v = t_k
                uc = eta * 2 * d
                y_k = (-uc) - c_err; t_k = c + y_k; c_err = (t_k - c) - y_k; c = t_k
            else:
                Wb -= upd
                if not freeze_v:
                    v -= eta * 2 * d[:, None] * phi
                c -= eta * 2 * d
        if maintain:
            z = zall(Xc, Wb); dnow = coh & ((z > 0).sum(1) == 0); zm = z.max(1)
            cur = np.linalg.norm(Wb[:, :, :20], axis=2); fac = np.where(dnow, tn / np.maximum(cur, 1e-12), 1.0)
            rec['m_fac'].append(np.where(dnow, fac, np.nan)); rec['m_n'].append(dnow.sum(1))
            Wb[:, :, :20] *= fac[:, :, None]; z1 = zall(Xc, Wb).max(1); Wb[:, :, 20] += np.where(dnow, zm - z1, 0.0)
            if kahan:
                Wb_err = np.zeros_like(Wb)
        z = zall(Xc, Wb); phi = phi_f(z); yh = np.einsum('crh,ch->cr', phi, v) + c[:, None]
        rec['kon'].append((z > 0).sum(1)); rec['zmax'].append(z.max(1)); rec['zbar'].append(z.mean(1))
        rec['loss'].append(((yh - Y) ** 2).mean(1))
        rec['wflip_abs'].append(np.abs(Wb[:, :, :15]).mean(2)); rec['wnorm'].append(np.linalg.norm(Wb[:, :, :20], axis=2))
        rec['nband'].append((np.abs(z) < NBAND_THR).sum(1).astype(np.int32))
        if task % log_every == 0 and task % 50 == 0:
            dead = rec['kon'][-1] == 0
            print(f"task {task:4d}  {time.time()-t0:6.0f}s  n_alive {100-dead.sum(1).mean():5.1f}  dead zmax med {np.median(rec['zmax'][-1][dead]):+.3f}  loss med {np.median(rec['loss'][-1]):.2e}", flush=True)
    out = {k: np.array(v) for k, v in rec.items()}
    for k in ['kon', 'zmax', 'zbar', 'loss', 'kon_kick', 'zmax_kick', 'wflip_abs', 'wnorm',
              'zmax_kick_prevW', 'zmax_kick_prevW_bonly', 'nband', 'kick_i', 'offset_i',
              'zbar_kick', 'dprime', 'z_kick']:
        if k in out and out[k].dtype not in (np.int32, np.int64):
            out[k] = out[k].astype(np.float32)
    out['S_final'] = S; out['Wb_final'] = Wb.astype(np.float32); out['v_final'] = v.astype(np.float32); out['c_final'] = c.astype(np.float32)
    if maintain:
        out['tn'] = tn.astype(np.float32); out['coh'] = coh
    out['rng_state'] = np.array(json.dumps(rng.bit_generator.state))
    return out


if __name__ == '__main__':
    ck = sys.argv[1]; eta = float(sys.argv[2]); ntask = int(sys.argv[3]); tag = sys.argv[4]
    kw = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {}
    o = run(U + ck, range(10), eta, ntask, **kw)
    o = {k: v for k, v in o.items() if not (isinstance(v, np.ndarray) and v.size == 0)}
    out_dir = os.environ.get('MTM_OUT_DIR', '.')
    os.makedirs(out_dir, exist_ok=True)
    outpath = os.path.join(out_dir, f'mt_{tag}.npz')
    np.savez_compressed(outpath, **o); print('saved', outpath, 'tasks', len(o['loss']))
