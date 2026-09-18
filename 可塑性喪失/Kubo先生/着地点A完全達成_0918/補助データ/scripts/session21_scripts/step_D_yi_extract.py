"""step_D_yi_extract.py — Y_i per-event 抽出

R = Δzbar_meas - kick - offset - T_4_theory - T_5_theory
Y_i = R - T_1_theory

理論式 (per-unit-5term-verification-and-v3e-success-0917.md §1-1):
  T_4 = κ(η) · (-z̄)                                 with κ(η) = a² · e^{1.604} · η^{1.352}
  T_5 = -c(η) · v² · n_band                          with c(η) = (0.11/0.01) · (0.97/0.90) · η

  a² = 0.09 (LRoff0 a=0.1 → LRa0p03 a=0.03 ⇒ a²=9e-4 vs LRoff0 a²=0.01. 実は audit-v1b §3-8 では
             κ ∝ a² で LRa0p03 は 0.09 倍。ここで κ_theory = 0.09 × κ_LRoff0 の scaling。)

入力: session21_out/step_C_t1_theory_per_event.npz
出力: session21_out/step_D_y_per_event.npz
"""
import numpy as np, sys, os

sys.path.insert(0, '/home/kubo/project/Nakatsuka/claude/hole1_scripts')

OUT = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session21_out'
ETAS = {'0156': 0.000156, '02': 0.0002, '05': 0.0005, '10': 0.001, '25': 0.0025}
TAGS = list(ETAS.keys())

# From per-unit-5term §1-1:
#   κ(η) = a² · exp(1.604) · η^{1.352}   (LRa0p03: a² = 0.09 scaling from LRoff0)
#   c(η) = (0.11 / 0.01) · (0.97 / 0.90) · η
A2 = 0.09   # (a_LRa0p03 / a_LRoff0)² = (0.03/0.1)² = 0.09
KAPPA_A = A2 * np.exp(1.604)
KAPPA_B = 1.352
C_COEFF = (0.11 / 0.01) * (0.97 / 0.90)


def kappa_theory(eta):
    return KAPPA_A * eta ** KAPPA_B


def c_theory(eta):
    return C_COEFF * eta


def main():
    log = []
    def L(s):
        print(s, flush=True); log.append(s)

    L('=== Step D: Y_i per-event 抽出 ===')

    inp = os.path.join(OUT, 'step_C_t1_theory_per_event.npz')
    if not os.path.exists(inp):
        raise SystemExit(f'not found: {inp}. Run step_C_t1_theory.py first.')
    d = np.load(inp)

    out = {}
    for tag in TAGS:
        eta = ETAS[tag]
        pref = f'{tag}__'
        keys = [k for k in d.files if k.startswith(pref)]
        if not keys:
            L(f'  arm lr{tag}: missing — skip')
            continue

        def g(k):
            return d[pref + k]

        T_1 = g('T_1')                     # (T, C, H)
        dzbar = g('dzbar_meas')            # (T, C, H)
        kick_i = g('kick_i')               # (T, C, H)
        offset_i = g('offset_i')           # (T, C, H)
        zbar_pre = g('zbar_pre')           # (T, C, H)
        nband_pre = g('nband_pre').astype(np.float32)  # (T, C, H)
        v_bcast = g('v')                   # (T, C, H)
        v2 = g('v2')                       # (T, C, H)
        kon_kick = g('kon_kick')           # (T, C, H)

        # T_4 theory: κ(η) × (-z̄_pre)
        kappa = kappa_theory(eta)
        T_4_th = kappa * (-zbar_pre)                # (T, C, H)

        # T_5 theory: -c(η) × v² × n_band_pre
        c_v = c_theory(eta)
        T_5_th = -c_v * v2 * nband_pre              # (T, C, H)

        # R = Δzbar_meas - kick - offset - T_4 - T_5
        R = dzbar - kick_i - offset_i - T_4_th - T_5_th

        # Y_i = R - T_1
        Y = R - T_1

        # group summary by kon_kick
        L(f'  arm lr{tag} (η={eta:g}):  κ_th={kappa:.4e}  c_th={c_v:.4e}')
        for label, mask in [
            ('kp0', kon_kick == 0),
            ('kp1', kon_kick == 1),
            ('kp2', kon_kick == 2),
            ('kp3-5', (kon_kick >= 3) & (kon_kick <= 5)),
            ('kp6+', kon_kick >= 6),
        ]:
            if mask.sum() == 0:
                continue
            n = int(mask.sum())
            R_mean = R[mask].mean()
            T_1_mean = T_1[mask].mean()
            Y_mean = Y[mask].mean()
            T_4_mean = T_4_th[mask].mean()
            T_5_mean = T_5_th[mask].mean()
            L(f'    {label:6s} n={n:>7d}  R={R_mean:+.4f}  T_1_th={T_1_mean:+.4f}  Y_i={Y_mean:+.4f}   (T_4_th={T_4_mean:+.4f}, T_5_th={T_5_mean:+.4f})')

        out[f'{tag}__T_1'] = T_1
        out[f'{tag}__T_4_th'] = T_4_th.astype(np.float32)
        out[f'{tag}__T_5_th'] = T_5_th.astype(np.float32)
        out[f'{tag}__R'] = R.astype(np.float32)
        out[f'{tag}__Y'] = Y.astype(np.float32)
        out[f'{tag}__dzbar_meas'] = dzbar
        out[f'{tag}__kick_i'] = kick_i
        out[f'{tag}__offset_i'] = offset_i
        out[f'{tag}__zbar_pre'] = zbar_pre
        out[f'{tag}__nband_pre'] = nband_pre.astype(np.int16)
        out[f'{tag}__v'] = v_bcast
        out[f'{tag}__v2'] = v2
        out[f'{tag}__kon_kick'] = kon_kick.astype(np.int16)
        out[f'{tag}__eta'] = np.float32(eta)
        # copy from step_C for E:
        for pass_k in ['sum_dprime_on', 'sgn_pred', 'zmax_kick', 'zbar_kick', 'dprime_mean']:
            key = f'{tag}__{pass_k}'
            if key in d.files:
                out[key] = d[key]

    outpath = os.path.join(OUT, 'step_D_y_per_event.npz')
    np.savez_compressed(outpath, **out)
    L(f'\nsaved {outpath}')

    with open(os.path.join(OUT, 'step_D_log.txt'), 'w') as f:
        f.write('\n'.join(log))


if __name__ == '__main__':
    main()
