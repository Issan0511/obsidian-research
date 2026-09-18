"""step_C_t1_theory.py — T_1 theory per-event 計算

audit-v1b §3-10 の 1 次予言:
    T_1(unit i, task t) = -v_i · Σ_r m_r · δ'_r · φ'_{i,r}

0 次近似: ζ = δ' (audit-v1b §3-10 参照; 1 次補正は future work)

- m_r = tilde_x_r · tilde_μ where tilde_x_r = X_r - g (per-support), tilde_μ = mean over r of tilde_x
- φ'_{i,r} = 1 if z_{i,r}(flip 直後) > 0 else a = 0.03 (LRa0p03 leaky)
- v_i: session20 v2 npz の v_final (tail 窓では概ね一定と仮定)

入力:
  session21_out/mt_U1_bareK1_dprime_v3_lr*.npz  (dprime, z_kick, n_active, kp_hist, v_final)

出力:
  session21_out/step_C_t1_theory_per_event.npz  (per-event arrays)
"""
import numpy as np, sys, os, json, time
sys.path.insert(0, '/home/kubo/project/Nakatsuka/claude/hole1_scripts')
from model import FREE, oracle_g

OUT = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session21_out'
ETAS = {'0156': 0.000156, '02': 0.0002, '05': 0.0005, '10': 0.001, '25': 0.0025}
TAGS = list(ETAS.keys())
ALPHA = 0.03  # LRa0p03 leaky slope

# FREE (32, 5) — 5-bit combinatorial part of support
# support(S) = [S[0..14], FREE[r, 0..4]]  each r ∈ 0..31
# X (32, 20) : rows are supports, columns are 20 input dims


def compute_m_r_all_tasks(n_active_hist):
    """
    n_active_hist: (T, C) int — per task per seed n_new (after flip)
    Returns m_r_hist: (T, C, 32) float — m_r for each task/seed/support

    Derivation:
      support = concat([repeat(S, 32, axis=0), FREE], axis=1)   -> (32, 20)
      Xc = support - g   (broadcasted scalar g)                  -> (32, 20)
      tilde_x_r = Xc[r]                                          -> (20,)
      tilde_mu = Xc.mean(axis=0)                                 -> (20,)
        = concat([S - g, FREE.mean(0) - g])
        = concat([S - g, 0.5 * ones(5) - g])   (since FREE is balanced Boolean)

      m_r = tilde_x_r · tilde_mu
          = Σ_j (S[j] - g)^2  (over j=0..14)  +  Σ_k (FREE[r, k] - g)(0.5 - g)  (over k=0..4)

      For binary S[j] ∈ {0,1}: (S[j] - g)^2 = S[j] - 2g·S[j] + g^2 = S[j](1-2g) + g^2
        Σ_j = n(1-2g) + 15 g^2   (constant across r; only depends on n)

      Second term: (0.5-g) Σ_k (FREE[r,k] - g) = (0.5-g) (f_r - 5g)  where f_r := FREE[r].sum()
    """
    T, C = n_active_hist.shape
    n = n_active_hist.astype(np.float64)  # (T, C)
    g = oracle_g(n)                        # (T, C)
    f_r = FREE.sum(axis=1)                 # (32,)

    const_term = n * (1 - 2*g) + 15 * g**2  # (T, C)  — constant across r
    r_term_scale = (0.5 - g)                 # (T, C)
    # (T, C, 32) = const_term[:, :, None] + r_term_scale[:, :, None] * (f_r[None, None, :] - 5*g[:, :, None])
    m = const_term[:, :, None] + r_term_scale[:, :, None] * (f_r[None, None, :] - 5*g[:, :, None])
    return m.astype(np.float32)


def compute_T1_per_event(dprime, z_kick, v, m, alpha=ALPHA, eta=None, T_sgd=10000):
    """
    audit-v1b §3-9/§3-10 の 1 次 T_1 予言 (0-th order):
        T_1_i(t) = -(2 η T / 32) · v_i · Σ_r m_r · δ'_r · φ'_{i,r}
      where prefactor comes from ζ = ℱ(𝒦) δ' ≈ (2 η T / 32) δ' at 0-th order (A^t ≈ I)

    dprime: (T, C, 32)
    z_kick: (T, C, 32, H)
    v:      (C, H)
    m:      (T, C, 32)
    eta:    float — SGD learning rate (required for scale factor)
    T_sgd:  int — number of SGD steps per task (default 10000)
    Returns T_1_bare (no scale), T_1_scaled (with 0-th order operator scale) : (T, C, H)
    """
    # phi_prime_i(r) = 1 if z_i,r > 0 else alpha  (leaky slope)
    phi_prime = np.where(z_kick > 0, 1.0, alpha).astype(np.float32)  # (T, C, 32, H)
    common = m * dprime            # (T, C, 32) elementwise
    inner = np.einsum('tcr,tcrh->tch', common, phi_prime)  # (T, C, H)
    T_1_bare = (-v[None, :, :] * inner).astype(np.float32)
    if eta is None:
        return T_1_bare, T_1_bare
    scale_op = 2.0 * eta * T_sgd / 32.0    # 0-th order operator response
    T_1_scaled = (scale_op * T_1_bare).astype(np.float32)
    return T_1_bare, T_1_scaled


def main():
    log = []
    def L(s):
        print(s, flush=True); log.append(s)

    L(f'=== Step C: T_1 theory per-event ===')
    all_records = {}
    t0 = time.time()

    for tag in TAGS:
        eta = ETAS[tag]
        v3path = os.path.join(OUT, f'mt_U1_bareK1_dprime_v3_lr{tag}.npz')
        if not os.path.exists(v3path):
            L(f'  arm lr{tag}: MISSING {v3path} — skipping')
            continue
        d = np.load(v3path)
        needed = ['dprime', 'z_kick', 'n_active', 'v_final', 'kick_i', 'offset_i',
                  'zbar', 'zbar_kick', 'kon_kick', 'nband']
        missing = [k for k in needed if k not in d.files]
        if missing:
            L(f'  arm lr{tag}: MISSING fields {missing} — skipping')
            continue

        dprime = d['dprime'].astype(np.float32)          # (T, C, 32)
        z_kick = d['z_kick'].astype(np.float32)          # (T, C, 32, H)
        n_active = d['n_active'].astype(np.int32)        # (T, C)
        v = d['v_final'].astype(np.float32)              # (C, H)
        kick_i = d['kick_i'].astype(np.float32)          # (T, C, H)
        offset_i = d['offset_i'].astype(np.float32)      # (T, C, H)
        zbar = d['zbar'].astype(np.float32)              # (T+1, C, H)
        zbar_kick = d['zbar_kick'].astype(np.float32)    # (T, C, H)
        kon_kick = d['kon_kick'].astype(np.int32)        # (T, C, H)
        nband = d['nband'].astype(np.int32)              # (T+1, C, H)

        T, C, R = dprime.shape[0], dprime.shape[1], 32
        H = v.shape[1]

        # m_r per (t, c, r)
        m = compute_m_r_all_tasks(n_active)             # (T, C, 32)

        # T_1 per (t, c, i) — both bare and 0-th order scaled
        T_1_bare, T_1 = compute_T1_per_event(dprime, z_kick, v, m, eta=eta, T_sgd=10000)  # (T, C, H)

        # derived quantities
        v_bcast = np.broadcast_to(v[None, :, :], (T, C, H)).copy()  # (T, C, H)
        v2 = v_bcast ** 2
        # zbar_pre = zbar_kick (before SGD) — approx pre-flip zbar is zbar[t] but we can use both
        # Δzbar_meas = zbar[t+1] - zbar[t]   (per-task per-unit)
        dzbar_meas = zbar[1:] - zbar[:-1]                # (T, C, H)  = zbar[t+1] - zbar[t]

        # sign(v · Σ_{r∈on} dprime_r) predictor per event (audit-v1b §3-10)
        on_mask = (z_kick > 0).astype(np.float32)        # (T, C, 32, H)
        sum_dprime_on = np.einsum('tcr,tcrh->tch', dprime, on_mask)  # (T, C, H)
        sgn_pred = np.sign(v_bcast * sum_dprime_on)      # (T, C, H)  ∈ {-1, 0, +1}

        L(f'  arm lr{tag}  T={T}  C={C}  H={H}')
        L(f'    T_1  median|·|={np.median(np.abs(T_1)):.4f}  p99={np.quantile(np.abs(T_1), 0.99):.4f}')
        L(f'    Δzbar_meas  median|·|={np.median(np.abs(dzbar_meas)):.4f}  p99={np.quantile(np.abs(dzbar_meas), 0.99):.4f}')
        L(f'    kick_i  median|·|={np.median(np.abs(kick_i)):.4f}')
        L(f'    offset_i median|·|={np.median(np.abs(offset_i)):.4f}')
        L(f'    kon_kick per-event distribution:  0: {(kon_kick==0).mean()*100:.1f}%  1: {(kon_kick==1).mean()*100:.1f}%  2: {(kon_kick==2).mean()*100:.1f}%  3-5: {((kon_kick>=3)&(kon_kick<=5)).mean()*100:.1f}%  6+: {(kon_kick>=6).mean()*100:.1f}%')

        all_records[tag] = dict(
            eta=np.float32(eta),
            T_1=T_1,
            T_1_bare=T_1_bare,
            dzbar_meas=dzbar_meas,
            kick_i=kick_i,
            offset_i=offset_i,
            zbar_pre=zbar[:-1].astype(np.float32),
            zbar_post=zbar[1:].astype(np.float32),
            zbar_kick=zbar_kick,
            kon_kick=kon_kick.astype(np.int16),
            nband_pre=nband[:-1].astype(np.int16),
            v=v_bcast,
            v2=v2,
            sum_dprime_on=sum_dprime_on,
            sgn_pred=sgn_pred.astype(np.int8),
            dprime_mean=dprime.mean(axis=-1).astype(np.float32),      # (T, C) per-event dprime mean
            zmax_kick=d['zmax_kick'].astype(np.float32),               # (T, C, H)
        )

    # Save
    out_dict = {}
    for tag, rec in all_records.items():
        for k, v in rec.items():
            out_dict[f'{tag}__{k}'] = v
    outpath = os.path.join(OUT, 'step_C_t1_theory_per_event.npz')
    np.savez_compressed(outpath, **out_dict)
    L(f'\nsaved {outpath}  elapsed {time.time()-t0:.0f}s')

    with open(os.path.join(OUT, 'step_C_log.txt'), 'w') as f:
        f.write('\n'.join(log))


if __name__ == '__main__':
    main()
