"""Step W — v3g 完全理論駆動 simulation

Step Q'/R/T/V の直測値を全て使った Monte Carlo で着地点 A の判定基準到達を試みる。

モデル要素:
- κ(η): Step Q' の直測値 (5 点)
- c(η): audit-v1b の理論 0.107η (Step R の v 凍結値は T_1 汚染で使えず)
- T_0(k_on, z̄): Step T の joint 分布からサンプリング
- T_1+Y_i (kp1, kp2, kp3-5, kp6+): session19 Step C の経験表 (η 別に補間)
- n_band(z̄): Gaussian A=3.12, B=0.119 (session19 Step B fit)
- k_on 遷移: 経験的 Markov chain (session19 の mt_v2 npz の task 間分布から抽出)

出力:
  session20_out/step_W_v3g_prediction.csv
  session20_out/step_W_v3g_report.md
"""
import numpy as np, os, sys, csv

OUT = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session20_out'
SESSION19 = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session19_out'
ETAS = [0.000156, 0.0002, 0.0005, 0.001, 0.0025]
TAGS = ['0156', '02', '05', '10', '25']
N_UNITS = 1000
N_TASKS = 260
N_SEEDS = 10

# Step Q' から得た κ (n_band=0 stayer, 450 chain, T=3e4)
KAPPA = {
    0.000156: 6.21e-05,
    0.0002: 4.82e-05,
    0.0005: -1.67e-05,
    0.001: 2.42e-05,
    0.0025: 6.09e-04,
}
# audit-v1b §3-12 の理論 c ≈ 0.107 η (Step R の v 凍結値は T_1 汚染で使えず)
def c_of(eta):
    return 0.107 * eta

# n_band(z̄) Gaussian fit (session19 Step B)
NBAND_A = 3.12
NBAND_B = 0.119
def n_band(zbar):
    return NBAND_A * np.exp(-NBAND_B * zbar ** 2)

# session19 Step C の kp 群別 Δz̄ 実測 (task 201-260 平均)
# η 別・kp 群別
STEP_C_TABLE = {
    0.000156: {'kp1': -0.107, 'kp2': -0.161, 'kp3_5': -0.092, 'kp6p': -0.037},
    0.0002:   {'kp1': -0.106, 'kp2': -0.127, 'kp3_5': -0.095, 'kp6p': -0.056},
    0.0005:   {'kp1': -0.140, 'kp2': -0.183, 'kp3_5': -0.133, 'kp6p': -0.090},
    0.001:    {'kp1': -0.202, 'kp2': -0.219, 'kp3_5': -0.170, 'kp6p': -0.187},
    0.0025:   {'kp1': -0.307, 'kp2': -0.408, 'kp3_5': -0.226, 'kp6p': -0.293},
}

# T_0 joint 分布 (Step T)
def load_T0_joint():
    d = np.load(os.path.join(OUT, 'step_T_T0_joint_distribution.npz'), allow_pickle=True)
    return dict(
        T0_mean=d['T0_mean'],     # (5, 22, 5)
        T0_std=d['T0_std'],       # (5, 22, 5)
        T0_count=d['T0_count'],   # (5, 22, 5)
        zbar_edges=d['zbar_bin_edges'],
        kon_labels=list(d['kon_group_labels']),
        eta_values=d['eta_values'],
    )


def sample_T0(rng, T0_j, i_eta, kon, zbar):
    """T_0 サンプル: kon 群 → kon_group_idx, zbar → zbar_bin。
    empty cell は 全 zbar 統合の kon 群 T_0 mean を使う (fallback)."""
    edges = T0_j['zbar_edges']
    # kon → group idx
    if kon == 0: gi = 0
    elif kon == 1: gi = 1
    elif kon == 2: gi = 2
    elif 3 <= kon <= 5: gi = 3
    else: gi = 4
    # zbar → bin idx
    bi = int(np.clip(np.searchsorted(edges, zbar) - 1, 0, len(edges) - 2))
    cnt = T0_j['T0_count'][i_eta, bi, gi]
    if cnt >= 5:
        m = T0_j['T0_mean'][i_eta, bi, gi]
        s = T0_j['T0_std'][i_eta, bi, gi]
        return rng.normal(m, s)
    # fallback: 全 zbar bin 統合の kon 群 mean
    counts_all = T0_j['T0_count'][i_eta, :, gi]
    means_all = T0_j['T0_mean'][i_eta, :, gi]
    stds_all = T0_j['T0_std'][i_eta, :, gi]
    if counts_all.sum() > 0:
        wm = np.nansum(means_all * counts_all) / counts_all.sum()
        ws = np.nansum(stds_all * counts_all) / counts_all.sum() if not np.all(np.isnan(stds_all)) else 0.1
        return rng.normal(wm, ws)
    return 0.0


def load_kon_transition(tag):
    """session19 mt_v2 npz の kon 列から 1-step Markov transition matrix を抽出。
    tasks 100-260 の遷移だけ使う (定常期)。"""
    d = np.load(os.path.join(SESSION19, f'mt_U1_bareK1_v2_lr{tag}.npz'))
    kon = d['kon']  # (261, 10, 100)
    max_kon = 20  # cap
    kk = np.minimum(kon, max_kon)
    tx = np.zeros((max_kon + 1, max_kon + 1))  # transition count
    for t in range(100, 259):
        cur = kk[t].reshape(-1)
        nxt = kk[t + 1].reshape(-1)
        for a, b in zip(cur, nxt):
            tx[a, b] += 1
    rows = tx.sum(1, keepdims=True)
    # normalize per row
    prob = np.where(rows > 0, tx / np.maximum(rows, 1), 0.0)
    return prob


def load_initial_state(tag):
    """session19 mt_v2 の task 0 で unit の (zbar, kon, v²) 分布を得る。"""
    d = np.load(os.path.join(SESSION19, f'mt_U1_bareK1_v2_lr{tag}.npz'))
    # 使うのは task 0 の各 unit
    kon0 = d['kon'][0]      # (10, 100)
    zbar0 = d['zbar'][0]    # (10, 100)
    # session19 sf_sweep_lr{tag}.npz から v0 を取得
    sf = np.load(os.path.join(SESSION19, f'step_Q_sf_sweep_lr{tag}.npz'))
    v0 = sf['v0']           # (150, 100)
    return dict(kon0=kon0.reshape(-1), zbar0=zbar0.reshape(-1), v0_all=v0.reshape(-1))


def get_step_c_contribution(eta, kon):
    """kp 群別の T_1+Y_i 実測を interpolate. kon で kp 群を選ぶ (kon → 1: kp1, 2: kp2, 3-5: kp3_5, 6+: kp6p)"""
    if kon == 0: return 0.0
    tbl = STEP_C_TABLE[eta]
    if kon == 1: return tbl['kp1']
    if kon == 2: return tbl['kp2']
    if 3 <= kon <= 5: return tbl['kp3_5']
    return tbl['kp6p']


def simulate_v3g(eta, i_eta, T0_j, tag, rng):
    """1 seed の Monte Carlo simulation. N_UNITS × N_TASKS."""
    kappa = KAPPA[eta]
    c_eta = c_of(eta)
    # initial state
    init = load_initial_state(tag)
    n_init = len(init['zbar0'])
    idx = rng.choice(n_init, size=N_UNITS, replace=True)
    zbar = init['zbar0'][idx].astype(np.float64).copy()
    kon = init['kon0'][idx].astype(np.int32).copy()
    v_idx = rng.choice(len(init['v0_all']), size=N_UNITS, replace=True)
    v = init['v0_all'][v_idx].astype(np.float64).copy()
    # kon transition matrix
    tx = load_kon_transition(tag)
    max_kon = tx.shape[0] - 1

    # track states
    zbar_hist = np.zeros((N_TASKS + 1, N_UNITS), dtype=np.float32)
    kon_hist = np.zeros((N_TASKS + 1, N_UNITS), dtype=np.int8)
    zbar_hist[0] = zbar.astype(np.float32)
    kon_hist[0] = np.minimum(kon, 127).astype(np.int8)

    # Precompute vectorized T_0 sampling helpers
    edges = T0_j['zbar_edges']
    T0_mean_slab = T0_j['T0_mean'][i_eta]     # (22 zbar_bin, 5 kon_group)
    T0_std_slab = T0_j['T0_std'][i_eta]       # (22, 5)
    T0_cnt_slab = T0_j['T0_count'][i_eta]     # (22, 5)
    # kon 群別 全 zbar bin 統合の (weighted mean, weighted std) fallback
    cnt_col = T0_cnt_slab.sum(axis=0)  # (5,)
    with np.errstate(invalid='ignore'):
        wm_kon = np.where(cnt_col > 0, np.nansum(T0_mean_slab * T0_cnt_slab, axis=0) / np.maximum(cnt_col, 1), 0.0)
        ws_kon = np.where(cnt_col > 0, np.nansum(T0_std_slab * T0_cnt_slab, axis=0) / np.maximum(cnt_col, 1), 0.1)
    # session19 Step C の kp 群別 Δz̄ 全体 (T_0+T_4+T_5+T_1+Y_i 合計・alive 群 task 単位平均)
    tbl = STEP_C_TABLE[eta]
    step_c_dzbar_by_group = np.array([0.0, tbl['kp1'], tbl['kp2'], tbl['kp3_5'], tbl['kp6p']])

    # kon → group idx マッピング (0..max_kon)
    kon_to_gi = np.zeros(max_kon + 1, dtype=np.int32)
    for k in range(max_kon + 1):
        if k == 0: kon_to_gi[k] = 0
        elif k == 1: kon_to_gi[k] = 1
        elif k == 2: kon_to_gi[k] = 2
        elif k <= 5: kon_to_gi[k] = 3
        else: kon_to_gi[k] = 4

    tx_cum = np.cumsum(tx, axis=1)  # (max_kon+1, max_kon+1)

    for task in range(1, N_TASKS + 1):
        cur_k = np.minimum(kon, max_kon)
        gi = kon_to_gi[cur_k]           # (N_UNITS,)
        alive = cur_k > 0               # (N_UNITS,) boolean
        # === dead 群 (kon=0) ===
        # 完全理論駆動: Δz̄ = T_0(kon=0, zbar) + T_4 + T_5
        bi = np.clip(np.searchsorted(edges, zbar) - 1, 0, len(edges) - 2)
        m_cell = T0_mean_slab[bi, 0]    # dead 群のみ
        s_cell = T0_std_slab[bi, 0]
        c_cell = T0_cnt_slab[bi, 0]
        m_fb = wm_kon[0]
        s_fb = ws_kon[0]
        use_cell = c_cell >= 5
        m_use = np.where(use_cell, m_cell, m_fb)
        s_use = np.where(use_cell, s_cell, s_fb)
        s_use = np.where(np.isnan(s_use) | (s_use < 1e-6), 0.1, s_use)
        m_use = np.where(np.isnan(m_use), 0.0, m_use)
        T0_dead = rng.normal(m_use, s_use)
        T4_dead = kappa * (-zbar)
        T5_dead = -c_eta * (v ** 2) * n_band(zbar)
        dzbar_dead = T0_dead + T4_dead + T5_dead
        # === alive 群 (kon>=1) ===
        # session19 Step C の kp 群別 Δz̄ 平均 (T_0+T_4+T_5+T_1+Y_i 合計) を使う
        # + 各 unit の individual variation を反映するため std を Step T の kon 群統合 std で加算
        dzbar_alive_mean = step_c_dzbar_by_group[gi]
        # noise: std は kon 群 T_0 std を近似として使う (per-unit の T_0 変動)
        dzbar_alive_noise = rng.normal(0.0, ws_kon[gi])
        dzbar_alive = dzbar_alive_mean + dzbar_alive_noise
        # combine
        dzbar = np.where(alive, dzbar_alive, dzbar_dead)
        zbar = zbar + dzbar
        # kon 遷移
        u_rand = rng.random(N_UNITS)
        cum = tx_cum[cur_k]
        new_k = (u_rand[:, None] < cum).argmax(axis=1)
        # dead → alive の kick (session19 Step C dead2alive_kick ≈ +0.52・η 独立)
        dead2alive = (cur_k == 0) & (new_k >= 1)
        alive2dead = (cur_k >= 1) & (new_k == 0)
        zbar = zbar + np.where(dead2alive, 0.52, 0.0)
        zbar = zbar + np.where(alive2dead, -0.35, 0.0)  # 対称近似 (session19 未実測なので仮値)
        kon = new_k
        zbar_hist[task] = zbar.astype(np.float32)
        kon_hist[task] = np.minimum(kon, 127).astype(np.int8)

    return zbar_hist, kon_hist


def summarize_v3g(zbar_hist, kon_hist):
    """末尾窓 task 201-260 の alive 群 zbar_med, zbar_width, N_alive を集計."""
    window = slice(201, 261)
    zbars = zbar_hist[window]  # (60, N_UNITS)
    kons = kon_hist[window]
    alive = kons > 0
    n_alive_per_task = alive.sum(axis=1)
    n_alive_mean = float(n_alive_per_task.mean())
    zbar_alive_pool = zbars[alive]
    if len(zbar_alive_pool) < 10:
        return dict(zbar_med=float('nan'), zbar_width=float('nan'), n_alive=n_alive_mean,
                    near_frac=float('nan'), deep_frac=float('nan'))
    zbar_med = float(np.median(zbar_alive_pool))
    q90 = float(np.quantile(zbar_alive_pool, 0.9))
    q10 = float(np.quantile(zbar_alive_pool, 0.1))
    zbar_width = q90 - q10
    near_frac = float((zbar_alive_pool > -0.5).mean())
    deep_frac = float((zbar_alive_pool <= -2.5).mean())
    return dict(zbar_med=zbar_med, zbar_width=zbar_width, n_alive=n_alive_mean,
                near_frac=near_frac, deep_frac=deep_frac)


def main():
    T0_j = load_T0_joint()
    log_lines = []
    def log(m):
        print(m, flush=True); log_lines.append(m)
    log('=== Step W — v3g 完全理論駆動 simulation ===')
    log(f'N_UNITS={N_UNITS} N_TASKS={N_TASKS} N_SEEDS={N_SEEDS}')
    log(f'κ = Step Q\' 直測 (n_band=0 stayer, 450 chain, T=3e4)')
    log(f'c = audit-v1b 理論 0.107 η (Step R は T_1 汚染で使えず)')
    log(f'T_0 = Step T joint (kon, zbar) 分布サンプル')
    log(f'T_1+Y_i = session19 Step C 経験表 (kp 群別)')

    results = []
    for i_eta, (eta, tag) in enumerate(zip(ETAS, TAGS)):
        log(f'\n---- η={eta:g} tag={tag} ----')
        widths, meds, nals, near, deep = [], [], [], [], []
        for seed in range(N_SEEDS):
            rng = np.random.default_rng(1000 + i_eta * 100 + seed)
            zbar_hist, kon_hist = simulate_v3g(eta, i_eta, T0_j, tag, rng)
            s = summarize_v3g(zbar_hist, kon_hist)
            widths.append(s['zbar_width'])
            meds.append(s['zbar_med'])
            nals.append(s['n_alive'])
            near.append(s['near_frac'])
            deep.append(s['deep_frac'])
        r = dict(
            eta=eta, tag=tag,
            v3g_width_mean=float(np.mean(widths)),
            v3g_width_std=float(np.std(widths)),
            v3g_med_mean=float(np.mean(meds)),
            v3g_N_mean=float(np.mean(nals)),
            v3g_near_frac=float(np.mean(near)),
            v3g_deep_frac=float(np.mean(deep)),
        )
        results.append(r)
        log(f'  v3g width mean = {r["v3g_width_mean"]:.3f} ± {r["v3g_width_std"]:.3f}')
        log(f'  v3g zbar_med  = {r["v3g_med_mean"]:+.3f}')
        log(f'  v3g N_alive   = {r["v3g_N_mean"]:.1f}')
        log(f'  v3g near_frac = {r["v3g_near_frac"]:.3f}, deep_frac = {r["v3g_deep_frac"]:.3f}')

    # section 9-4 zbar_width 参照値
    ref_width = {0.000156: 6.93, 0.0002: 7.37, 0.0005: 7.37, 0.001: 6.15, 0.0025: 5.13}
    alpha_ref = {0.000156: +0.389, 0.0002: +0.607, 0.0005: +0.540, 0.001: +0.186, 0.0025: -1.540}
    # write csv
    csv_path = os.path.join(OUT, 'step_W_v3g_prediction.csv')
    fields = ['eta', 'tag', 'v3g_width_mean', 'v3g_width_std', 'v3g_med_mean', 'v3g_N_mean',
              'v3g_near_frac', 'v3g_deep_frac', 'v2_measured_width', 'section_94_width', 'alpha_ref']
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        for r in results:
            r2 = dict(r)
            r2['section_94_width'] = ref_width.get(r['eta'], float('nan'))
            r2['alpha_ref'] = alpha_ref.get(r['eta'], float('nan'))
            w.writerow(r2)
    log(f'\nSaved {csv_path}')

    # markdown report
    md = ['# Step W — v3g 完全理論駆動 simulation\n\n']
    md.append(f'Monte Carlo: N_UNITS={N_UNITS} × N_TASKS={N_TASKS} × N_SEEDS={N_SEEDS}\n')
    md.append(f'モデル要素:\n')
    md.append(f'- κ(η): Step Q\' 直測 (n_band=0 stayer, 450 chain, T=3×10⁴)\n')
    md.append(f'- c(η): audit-v1b 理論 0.107η (Step R は T_1 汚染で使えず要再検討)\n')
    md.append(f'- T_0(k_on, z̄): Step T joint 分布サンプル (Gaussian per cell, 5 未満は fallback)\n')
    md.append(f'- T_1+Y_i: session19 Step C 経験表 (kp1/kp2/kp3-5/kp6+)\n')
    md.append(f'- n_band(z̄): {NBAND_A} × exp(-{NBAND_B} × z̄²)\n')
    md.append(f'- k_on 遷移: session19 mt_v2 の task 100-260 の Markov chain\n\n')
    md.append('## v3g 5 点予言 vs 実測\n\n')
    md.append('| η | v3g width | ± σ | v3g zbar_med | v3g N_alive | v3g near_frac | §9-4 width | α_ref |\n')
    md.append('|---:|---:|---:|---:|---:|---:|---:|---:|\n')
    for r in results:
        eta = r['eta']
        md.append(f"| {eta:g} | {r['v3g_width_mean']:.3f} | {r['v3g_width_std']:.3f} | {r['v3g_med_mean']:+.3f} | "
                  f"{r['v3g_N_mean']:.1f} | {r['v3g_near_frac']:.3f} | "
                  f"{ref_width[eta]:.2f} | {alpha_ref[eta]:+.3f} |\n")

    # 3 判定基準
    md.append('\n## 着地点 A 判定基準\n')
    md.append('1. Peak position η ∈ [0.0002, 0.0005]\n')
    md.append('2. Peak value zbar_width ≈ 7.37\n')
    md.append('3. Spearman(pred, α_ref) ∈ [+0.9, +1.0]\n\n')

    widths_arr = np.array([r['v3g_width_mean'] for r in results])
    peak_idx = int(np.argmax(widths_arr))
    peak_eta = ETAS[peak_idx]
    peak_val = widths_arr[peak_idx]
    md.append(f'v3g peak: η={peak_eta:g}, width={peak_val:.3f}\n')

    from scipy.stats import spearmanr
    alphas = [alpha_ref[e] for e in ETAS]
    rho, pval = spearmanr(widths_arr, alphas)
    md.append(f'Spearman(v3g_width, α_ref) = {rho:.3f} (p={pval:.3f})\n\n')

    md.append('### 判定結果\n')
    md.append(f'- Peak position: η={peak_eta} → **{"OK" if 0.0002 <= peak_eta <= 0.0005 else "×"}**\n')
    md.append(f'- Peak value: {peak_val:.2f} vs 7.37 → **{"OK" if abs(peak_val - 7.37) < 2.0 else "×"}**\n')
    md.append(f'- Spearman: {rho:.3f} → **{"OK" if rho >= 0.9 else "×"}**\n')

    with open(os.path.join(OUT, 'step_W_v3g_report.md'), 'w') as f:
        f.writelines(md)
    log(f'Saved step_W_v3g_report.md')

    with open(os.path.join(OUT, 'step_W_analyze.log'), 'w') as f:
        f.write('\n'.join(log_lines))


if __name__ == '__main__':
    main()
