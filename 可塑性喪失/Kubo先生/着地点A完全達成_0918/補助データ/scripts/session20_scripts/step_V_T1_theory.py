"""Step V — T_1 の飽和形理論式の検証 (LRa0p03 arm・kp1 unit)

audit-v1b §3-10 の T_1 = -0.45 · v_i · <ζ, m ⊙ φ'_i> 飽和式を LRa0p03 で検証する。
- ζ は本来 F(K) δ' だが、時間発展を無視した最も単純な近似として ζ ≈ δ' を採用する
  (audit-v1b §3-10 は「跨いだ点の残差だけで sign 70% 予測」と report しており、
   ζ の伝播はまず切って基本形を試す)。
- m_r = row-mean of K matrix (K = X_new X_new^T / 32)
- φ'_{i,r} = 1 if z_post[i,r] > 0, α=0.03 else
- T_1_theory = -sat · v_i · Σ_r ζ_r · m_r · φ'_{i,r}, sat = 0.45 (audit-v1b の飽和 factor)

kp1 unit は kon_pre=0 AND kon0=1 で識別 (flip 直後に丁度 1 個 active になった unit)。

実測 T_1 + Y_i = Δz̄ - T_0 - T_4 - T_5, where
  T_0 = kick + offset
  T_4 = κ(η) × (-zbar_pre)  (Step Q' の κ を使う)
  T_5 = c(η) × v_i^2 × n_band_i  (audit-v1b の理論 c ≈ 0.107 η を使う)

session19 sf_sweep_lr*.npz を入力とする。checkpoint LRa0p03_1216_step5000000.pt から
Wb, v, c, fs, Tt を取り直す。

出力:
  session20_out/step_V_T1_verification.csv
  session20_out/step_V_T1_verification.md
"""
import numpy as np, os, sys, csv
sys.path.insert(0, '/home/kubo/project/Nakatsuka/claude/hole1_scripts')
from sim_act import load_ck, make_act
from model import support, oracle_g, teacher

CKPATH = '/home/kubo/project/Nakatsuka/data/act_sweep_hole1_0910_local/ckpts/LRa0p03_1216_step5000000.pt'
SF_DIR = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session19_out'
OUT = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session20_out'
TAGS = ['0156', '02', '05', '10', '25']
ETAS = [0.000156, 0.0002, 0.0005, 0.001, 0.0025]
REC_AT = [100, 1000, 5000, 10000]
SAT = 0.45  # saturation factor from audit-v1b §3-10 (実測 slope 0.42-0.48)

# Step Q' で得た κ (n_band=0 stayer 中心値・450 chain・T=3e4)
KAPPA_QPRIME = {
    0.000156: 6.21e-05,
    0.0002: 4.82e-05,
    0.0005: -1.67e-05,
    0.001: 2.42e-05,
    0.0025: 6.09e-04,
}


def compute_perunit_geom(net, Tt, fs, chain_seed, chain_kp, act, alpha):
    """checkpoint から chain 別の post-flip の (Xc, Y, z_post, z_hat_post, phi_deriv, K, m_r, delta_prime) を計算。
    Returns dict of arrays with C-first indexing."""
    C = len(chain_seed)
    phi_f, dphi_f = make_act(act, alpha)
    Wb_full = np.zeros((C, net['W'].shape[1], 21))
    v_full = np.zeros((C, net['v'].shape[1]))
    c_full = np.zeros(C)
    Xc = np.zeros((C, 32, 21))
    Y = np.zeros((C, 32))
    for i in range(C):
        s = int(chain_seed[i])
        kp = int(chain_kp[i])
        Wb_full[i, :, :20] = net['W'][s]
        Wb_full[i, :, 20] = net['b'][s]
        v_full[i] = net['v'][s]
        c_full[i] = net['c'][s]
        fs2 = fs[s].copy()
        fs2[kp] = 1 - fs2[kp]
        n1 = int(fs2.sum())
        g1 = oracle_g(n1)
        X = support(fs2)
        Xc[i] = np.concatenate([X - g1, np.ones((32, 1))], 1)
        Y[i] = teacher(Tt, s, X)
    # z_post = Xc · Wb.T (C, 32, H)
    z_post = np.einsum('cru,chu->crh', Xc, Wb_full)
    phi_post = phi_f(z_post)
    dphi_post = dphi_f(z_post)  # φ' at post-flip (1 if z>0 else α)
    # y_hat_post: (C, 32)
    y_hat_post = np.einsum('crh,ch->cr', phi_post, v_full) + c_full[:, None]
    delta_prime = y_hat_post - Y  # (C, 32) residual at post-flip pre-SGD
    # K_c[r,s] = Xc[c,r] · Xc[c,s]  (C, 32, 32) then m_r = row-mean over s
    K_full = np.einsum('cru,csu->crs', Xc, Xc) / 32.0  # normalized to be image-space similarity
    m_r = K_full.mean(axis=2)  # (C, 32) row-mean of K
    return dict(Xc=Xc, Y=Y, z_post=z_post, phi_post=phi_post, dphi_post=dphi_post,
                y_hat_post=y_hat_post, delta_prime=delta_prime, m_r=m_r, K=K_full,
                v=v_full, c=c_full, Wb=Wb_full)


def analyze_one(tag, eta):
    d = np.load(os.path.join(SF_DIR, f'step_Q_sf_sweep_lr{tag}.npz'))
    net, Tt, fs, rm, act, alpha = load_ck(CKPATH)
    C, H = d['zbar_pre'].shape
    kon_pre = d['kon_pre']
    kon0 = d['kon0']
    zbar_pre = d['zbar_pre']
    zbarT = d['zbarT']
    kick = d['kick']
    offset = d['offset']
    v0 = d['v0']
    # nband 平均
    nband = np.mean(np.stack([d[f'nband_t{t}'] for t in REC_AT], 0).astype(np.float64), axis=0)

    # per-unit geometric quantities (Xc, delta_prime, m_r, dphi_post) via checkpoint
    geom = compute_perunit_geom(net, Tt, fs, d['chain_seed'], d['chain_kp'], act, alpha)
    delta_prime = geom['delta_prime']       # (C, 32)
    m_r = geom['m_r']                       # (C, 32)
    dphi_post = geom['dphi_post']           # (C, 32, H)

    # T_1_theory (per unit): -SAT · v_i · Σ_r (δ'_r · m_r · φ'_{i,r})
    # ζ ≈ δ' (時間発展を無視する第 0 次近似)
    inner = np.einsum('cr,cr,crh->ch', delta_prime, m_r, dphi_post)  # (C, H)
    T1_theory = -SAT * v0 * inner  # (C, H)

    # 実測 T_1 + Y_i = Δz̄ - T_0 - T_4 - T_5
    kappa_eta = KAPPA_QPRIME[eta]
    T0 = kick + offset
    T4 = kappa_eta * (-zbar_pre)  # (C, H)
    c_theory = 0.107 * eta        # audit-v1b §3-12
    T5 = -c_theory * (v0 ** 2) * nband  # (C, H)
    dzbar = zbarT - zbar_pre
    T1_measured = dzbar - T0 - T4 - T5  # T_1 + Y_i

    # kp1 unit の識別
    mask_kp1 = (kon_pre == 0) & (kon0 == 1)
    mask_kp2 = (kon_pre == 0) & (kon0 == 2)

    result = dict(eta=eta, tag=tag)

    for label, mask in [('kp1', mask_kp1), ('kp2', mask_kp2)]:
        n = int(mask.sum())
        result[f'n_{label}'] = n
        if n < 30:
            continue
        theo = T1_theory[mask]
        meas = T1_measured[mask]
        # correlation
        corr = float(np.corrcoef(theo, meas)[0, 1]) if n > 1 else float('nan')
        result[f'corr_{label}'] = corr
        # linear regression measured ~ slope * theory + intercept
        num = float(((theo - theo.mean()) * (meas - meas.mean())).sum())
        den = float(((theo - theo.mean()) ** 2).sum())
        slope = num / den if den > 0 else float('nan')
        intercept = float(meas.mean() - slope * theo.mean())
        result[f'slope_{label}'] = slope
        result[f'intercept_{label}'] = intercept
        # R²
        pred = slope * theo + intercept
        ss_res = float(((meas - pred) ** 2).sum())
        ss_tot = float(((meas - meas.mean()) ** 2).sum())
        result[f'R2_{label}'] = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
        # means
        result[f'mean_theory_{label}'] = float(theo.mean())
        result[f'mean_measured_{label}'] = float(meas.mean())
        # residual = measured - theory (attempted attribution to Y_i)
        result[f'residual_Y_{label}'] = float((meas - theo).mean())
    return result


def main():
    log_lines = []
    def log(m):
        print(m, flush=True); log_lines.append(m)
    log('=== Step V — T_1 saturated 理論式 検証 (LRa0p03) ===')
    log(f'sat={SAT}  ζ ≈ δ\'  (時間発展無視の最も単純な近似)')
    log(f'κ used = Step Q\' 値: {KAPPA_QPRIME}')
    log(f'c used = audit-v1b 理論 0.107 × η')
    results = []
    for tag, eta in zip(TAGS, ETAS):
        r = analyze_one(tag, eta)
        results.append(r)
        log(f'\n---- η={eta:g} tag={tag} ----')
        for label in ['kp1', 'kp2']:
            n = r.get(f'n_{label}', 0)
            log(f'  {label}: n={n}')
            if n < 30:
                continue
            log(f'    corr(T_1_theo, T_1_meas) = {r.get(f"corr_{label}"):+.3f}')
            log(f'    slope                     = {r.get(f"slope_{label}"):+.3f}')
            log(f'    R²                        = {r.get(f"R2_{label}"):+.3f}')
            log(f'    mean_theory  = {r.get(f"mean_theory_{label}"):+.4f}')
            log(f'    mean_measured= {r.get(f"mean_measured_{label}"):+.4f}')
            log(f'    residual_Y   = {r.get(f"residual_Y_{label}"):+.4f}')
    # csv
    csv_path = os.path.join(OUT, 'step_V_T1_verification.csv')
    fields = ['eta', 'tag',
              'n_kp1', 'corr_kp1', 'slope_kp1', 'intercept_kp1', 'R2_kp1',
              'mean_theory_kp1', 'mean_measured_kp1', 'residual_Y_kp1',
              'n_kp2', 'corr_kp2', 'slope_kp2', 'intercept_kp2', 'R2_kp2',
              'mean_theory_kp2', 'mean_measured_kp2', 'residual_Y_kp2']
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        for r in results:
            w.writerow(r)
    log(f'\nSaved {csv_path}')

    md_lines = ['# Step V — T_1 飽和形理論式の検証 (LRa0p03)\n\n']
    md_lines.append(f'audit-v1b §3-10: $T_1 = -0.45 \\cdot v_i \\langle\\zeta, m\\odot\\varphi\'_i\\rangle$\n')
    md_lines.append(f'ここでは ζ ≈ δ\' (flip 直後の残差) の 0 次近似で試験。sat = {SAT}\n')
    md_lines.append('m_r = row-mean of K/32 (K = Xc Xc^T).  φ\' = 1 for z_post>0, α=0.03 else.\n\n')
    md_lines.append('## 実測 T_1+Y_i vs 理論 T_1 の照合 (kp1・kp2 群)\n\n')
    md_lines.append('| η | kp1 n | corr | slope | R² | mean_theo | mean_meas | Y_residual | kp2 n | corr | slope | R² |\n')
    md_lines.append('|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n')
    for r in results:
        md_lines.append(f"| {r['eta']:g} | "
                        f"{r.get('n_kp1', 0)} | {r.get('corr_kp1', float('nan')):+.3f} | {r.get('slope_kp1', float('nan')):+.3f} | {r.get('R2_kp1', float('nan')):+.3f} | "
                        f"{r.get('mean_theory_kp1', float('nan')):+.4f} | {r.get('mean_measured_kp1', float('nan')):+.4f} | {r.get('residual_Y_kp1', float('nan')):+.4f} | "
                        f"{r.get('n_kp2', 0)} | {r.get('corr_kp2', float('nan')):+.3f} | {r.get('slope_kp2', float('nan')):+.3f} | {r.get('R2_kp2', float('nan')):+.3f} |\n")

    md_lines.append('\n## 判定条件\n')
    md_lines.append('- Correlation > 0.5 なら T_1 式が LRa0p03 で成立 (audit-v1b の LRoff0 は 0.55-0.68)\n')
    md_lines.append('- Slope が 0.45 近傍 (sat の乗算前の実測値・sat = 1 の場合に相当) なら飽和 factor が LRa0p03 でも同じ\n')
    md_lines.append('- Y_i 残差 |Y| < 0.02 なら T_1 単独で crosser 群を説明できる\n')

    with open(os.path.join(OUT, 'step_V_T1_verification.md'), 'w') as f:
        f.writelines(md_lines)

    with open(os.path.join(OUT, 'step_V_analyze.log'), 'w') as f:
        f.write('\n'.join(log_lines))
    print('Saved step_V_T1_verification.md')


if __name__ == '__main__':
    main()
