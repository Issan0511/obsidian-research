"""Step U — 500 タスク定常性分析（走ゼロ）

mt_U1_bareK1_500tasks_v2_lr{tag}.npz を 5 窓 (tasks 200-260, 261-320, 321-380, 381-440,
441-500) で集計:
- zbar_width (q90-q10 of alive)
- zbar_med
- N_alive
- near_frac (zbar > -0.5)
- deep_frac (zbar ≤ -2.5)

判定:
- 5 窓の zbar_width が概ね一定なら **定常** (260 タスクが十分)
- 中間 η で峰が徐々に平坦化 or 高 η 側にシフトなら **過渡** (S_a 混入・500 タスクでも足りない)

段 0 check: session19 mt_v2 の task 0-260 と一致 (差 < 1e-6)

出力:
  session20_out/step_U_5window_stats.csv
  session20_out/step_U_report.md
"""
import numpy as np, os, sys, csv

OUT = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session20_out'
SESSION19 = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session19_out'
ETAS = [0.000156, 0.0002, 0.0005, 0.001, 0.0025]
TAGS = ['0156', '02', '05', '10', '25']
WINDOWS = [
    ('W1_200_260', 200, 260),   # matches session19 endpoint
    ('W2_261_320', 261, 320),
    ('W3_321_380', 321, 380),
    ('W4_381_440', 381, 440),
    ('W5_441_500', 441, 500),
]


def analyze(tag, eta):
    d = np.load(os.path.join(OUT, f'mt_U1_bareK1_500tasks_v2_lr{tag}.npz'))
    kon = d['kon']    # (501, 10, 100)
    zbar = d['zbar']  # (501, 10, 100)
    stats = []
    for wname, ts, te in WINDOWS:
        kw = kon[ts:te + 1]        # (window, 10, 100)
        zw = zbar[ts:te + 1]
        alive = kw > 0
        n_alive_per_task = alive.sum(axis=(1, 2)) / 10.0  # per seed 平均、100 unit 中の alive
        n_alive_mean = float(n_alive_per_task.mean())
        pool = zw[alive]
        if len(pool) < 10:
            stats.append(dict(window=wname, ts=ts, te=te, n_alive=n_alive_mean,
                              zbar_med=float('nan'), zbar_width=float('nan'),
                              near_frac=float('nan'), deep_frac=float('nan'),
                              h_u=float('nan')))
            continue
        zbar_med = float(np.median(pool))
        q90 = float(np.quantile(pool, 0.9))
        q10 = float(np.quantile(pool, 0.1))
        zbar_width = q90 - q10
        near_frac = float((pool > -0.5).mean())
        deep_frac = float((pool <= -2.5).mean())
        # h(u): 危険率 = task 間で dead になった unit の割合 / task
        # ここでは alive → dead 遷移数 / alive の数 で近似
        transitions_alive_to_dead = 0
        alive_count = 0
        for t in range(ts, te):
            alive_t = kon[t] > 0
            dead_tp1 = kon[t + 1] == 0
            transitions_alive_to_dead += int((alive_t & dead_tp1).sum())
            alive_count += int(alive_t.sum())
        h_u = transitions_alive_to_dead / max(alive_count, 1)
        stats.append(dict(window=wname, ts=ts, te=te, n_alive=n_alive_mean,
                          zbar_med=zbar_med, zbar_width=zbar_width,
                          near_frac=near_frac, deep_frac=deep_frac, h_u=h_u))
    return stats


def stage0_check(tag):
    """session19 mt_v2 の task 0-260 と mt_500 の task 0-260 が一致するか検算 (max diff)."""
    a = np.load(os.path.join(SESSION19, f'mt_U1_bareK1_v2_lr{tag}.npz'))
    b = np.load(os.path.join(OUT, f'mt_U1_bareK1_500tasks_v2_lr{tag}.npz'))
    # kon (261, 10, 100) vs (501,10,100)
    d_kon = int(np.abs(a['kon'] - b['kon'][:261]).max())
    d_zbar = float(np.abs(a['zbar'].astype(np.float64) - b['zbar'][:261].astype(np.float64)).max())
    return dict(diff_kon=d_kon, diff_zbar=d_zbar)


def main():
    log_lines = []
    def log(m):
        print(m, flush=True); log_lines.append(m)
    log('=== Step U — 500 タスク定常性分析 ===')
    log(f'Windows: {[(w, ts, te) for w, ts, te in WINDOWS]}')

    all_rows = []
    for tag, eta in zip(TAGS, ETAS):
        log(f'\n---- η={eta:g} tag={tag} ----')
        # 段 0 check
        s0 = stage0_check(tag)
        log(f'  段 0 check (vs session19 mt_v2 task 0-260): diff_kon={s0["diff_kon"]}, diff_zbar={s0["diff_zbar"]:.2e}')
        # 5 窓分析
        stats = analyze(tag, eta)
        for s in stats:
            log(f'  {s["window"]}: N_alive={s["n_alive"]:.2f}, zbar_width={s["zbar_width"]:.3f}, zbar_med={s["zbar_med"]:+.3f}, near_frac={s["near_frac"]:.3f}, deep_frac={s["deep_frac"]:.3f}, h(u)={s["h_u"]:.3f}')
            s2 = dict(s)
            s2['eta'] = eta
            s2['tag'] = tag
            all_rows.append(s2)

    csv_path = os.path.join(OUT, 'step_U_5window_stats.csv')
    fields = ['eta', 'tag', 'window', 'ts', 'te', 'n_alive', 'zbar_med', 'zbar_width', 'near_frac', 'deep_frac', 'h_u']
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        for r in all_rows:
            w.writerow(r)
    log(f'\nSaved {csv_path}')

    # markdown report
    md = ['# Step U — 500 タスク定常性分析\n\n']
    md.append('5 窓 × 5 η の zbar_width 時系列で定常性を判定。\n\n')
    md.append('## zbar_width の 5 窓時系列\n\n')
    md.append('| η | W1 (200-260) | W2 (261-320) | W3 (321-380) | W4 (381-440) | W5 (441-500) | ΔW/W1 |\n')
    md.append('|---:|---:|---:|---:|---:|---:|---:|\n')
    from collections import defaultdict
    grouped = defaultdict(dict)
    for r in all_rows:
        grouped[r['eta']][r['window']] = r
    for eta in ETAS:
        row = grouped[eta]
        ws = [row[w[0]]['zbar_width'] for w in WINDOWS]
        w1 = ws[0]
        rel_change = (ws[-1] - w1) / w1 if w1 != 0 else float('nan')
        md.append(f"| {eta:g} | {ws[0]:.3f} | {ws[1]:.3f} | {ws[2]:.3f} | {ws[3]:.3f} | {ws[4]:.3f} | {rel_change:+.3f} |\n")

    md.append('\n## N_alive の 5 窓時系列\n\n')
    md.append('| η | W1 | W2 | W3 | W4 | W5 |\n')
    md.append('|---:|---:|---:|---:|---:|---:|\n')
    for eta in ETAS:
        row = grouped[eta]
        ws = [row[w[0]]['n_alive'] for w in WINDOWS]
        md.append(f"| {eta:g} | {ws[0]:.1f} | {ws[1]:.1f} | {ws[2]:.1f} | {ws[3]:.1f} | {ws[4]:.1f} |\n")

    md.append('\n## Spearman(zbar_width, α_ref) の窓別変化\n\n')
    alpha_ref = {0.000156: +0.389, 0.0002: +0.607, 0.0005: +0.540, 0.001: +0.186, 0.0025: -1.540}
    alphas = [alpha_ref[e] for e in ETAS]
    try:
        from scipy.stats import spearmanr
    except ImportError:
        spearmanr = None
    md.append('| Window | Spearman ρ | p-value |\n')
    md.append('|---|---:|---:|\n')
    for w in WINDOWS:
        widths = [grouped[e][w[0]]['zbar_width'] for e in ETAS]
        if spearmanr is not None:
            rho, p = spearmanr(widths, alphas)
            md.append(f'| {w[0]} | {rho:+.3f} | {p:.3f} |\n')

    md.append('\n## 定常性判定\n\n')
    stationary = True
    for eta in ETAS:
        row = grouped[eta]
        ws = [row[w[0]]['zbar_width'] for w in WINDOWS]
        rel_range = (max(ws) - min(ws)) / max(min(ws), 1e-6)
        if rel_range > 0.30:
            stationary = False
        md.append(f'- η={eta:g}: 5 窓の相対変動 (max-min)/min = {rel_range:.3f}  ({"定常" if rel_range < 0.15 else "軽度過渡" if rel_range < 0.30 else "過渡"})\n')
    md.append(f'\n**総合判定: {"定常 (260 タスクで十分)" if stationary else "過渡 (500 タスクでも peak が動く可能性)"}**\n')

    with open(os.path.join(OUT, 'step_U_report.md'), 'w') as f:
        f.writelines(md)

    with open(os.path.join(OUT, 'step_U_analyze.log'), 'w') as f:
        f.write('\n'.join(log_lines))
    print('Saved step_U_report.md')


if __name__ == '__main__':
    main()
