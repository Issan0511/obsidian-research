"""Step T — T_0 の (k_on, z̄) joint 分布抽出（走ゼロ）

第 19 回 mt_U1_bareK1_v2_lr*.npz の 5 ファイルを読み、per-task per-unit の
kick_i + offset_i (= T_0) を kon_pre × zbar_pre の 2D bin で集計する。

出力:
  session20_out/step_T_T0_joint_distribution.npz
    T0_mean:  (5 η, 22 zbar_bin, 5 kon_group)
    T0_std:   (5 η, 22 zbar_bin, 5 kon_group)
    T0_count: (5 η, 22 zbar_bin, 5 kon_group)  int32
    T0_skew:  (5 η, 22 zbar_bin, 5 kon_group)
    T0_kurt:  (5 η, 22 zbar_bin, 5 kon_group)
    zbar_bin_edges: (23,)
    kon_group_labels: 5 個の文字列
    eta_values: (5,)

  session20_out/step_T_report.md
"""
import numpy as np, os, sys

OUT = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session20_out'
SESSION19 = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session19_out'
ETAS = [0.000156, 0.0002, 0.0005, 0.001, 0.0025]
TAGS = ['0156', '02', '05', '10', '25']
WINDOW_TASKS = (200, 260)  # 末尾窓
ZBAR_EDGES = np.arange(-8.0, 3.0 + 1e-9, 0.5)   # 23 edges → 22 bins
NBIN_Z = len(ZBAR_EDGES) - 1
KON_GROUPS = [
    ('kon0', lambda k: k == 0),
    ('kon1', lambda k: k == 1),
    ('kon2', lambda k: k == 2),
    ('kon3_5', lambda k: (k >= 3) & (k <= 5)),
    ('kon6p', lambda k: k >= 6),
]
NKON = len(KON_GROUPS)


def one_eta(tag):
    d = np.load(os.path.join(SESSION19, f'mt_U1_bareK1_v2_lr{tag}.npz'))
    # kon: (261, 10, 100), zbar: (261, 10, 100)
    # kick_i: (260, 10, 100), offset_i: (260, 10, 100)
    kon = d['kon']
    zbar = d['zbar']
    kick = d['kick_i']
    off = d['offset_i']
    T0 = kick + off  # per-task per-unit の kick+offset = T_0(k_on_pre, zbar_pre)
    t0_all = []
    kon_pre_all = []
    zbar_pre_all = []
    t_start, t_end = WINDOW_TASKS
    for t in range(t_start, t_end):
        # task t の遷移: pre state は kon[t], zbar[t]; T0 の第 t 項は kick_i[t]+offset_i[t]
        kp = kon[t]         # (10, 100)
        zp = zbar[t]        # (10, 100)
        alive = kp > 0      # dead は SGD で動かないので、SGD 前で alive のもの → ではなく、
                            # T_0 は kick で起こる幾何量なので dead unit にも定義される
        # ただし解析の目的は「T_0 の分布」なので、alive/dead は分けずに全 unit を集計する
        # 各 group はどうせ kon_pre で切る
        t0_all.append(T0[t].reshape(-1))
        kon_pre_all.append(kp.reshape(-1))
        zbar_pre_all.append(zp.reshape(-1))
    t0_all = np.concatenate(t0_all)
    kon_pre_all = np.concatenate(kon_pre_all)
    zbar_pre_all = np.concatenate(zbar_pre_all)
    return t0_all, kon_pre_all, zbar_pre_all


def bin_stats(vals):
    """mean, std, count, skew, kurt over the array. Return NaN if empty."""
    n = vals.size
    if n == 0:
        return np.nan, np.nan, 0, np.nan, np.nan
    m = float(vals.mean())
    s = float(vals.std())
    if n < 3 or s < 1e-30:
        return m, s, n, 0.0, 0.0
    skew = float(((vals - m) ** 3).mean() / (s ** 3))
    kurt = float(((vals - m) ** 4).mean() / (s ** 4) - 3.0)
    return m, s, n, skew, kurt


def main():
    os.makedirs(OUT, exist_ok=True)
    T0_mean = np.full((5, NBIN_Z, NKON), np.nan)
    T0_std = np.full((5, NBIN_Z, NKON), np.nan)
    T0_count = np.zeros((5, NBIN_Z, NKON), dtype=np.int32)
    T0_skew = np.full((5, NBIN_Z, NKON), np.nan)
    T0_kurt = np.full((5, NBIN_Z, NKON), np.nan)

    lines = []
    lines.append('# Step T — T_0 の (k_on, z̄) joint 分布抽出\n')
    lines.append('走ゼロ・session19 の mt_U1_bareK1_v2_lr*.npz を集計。\n')
    lines.append(f'末尾窓 task {WINDOW_TASKS[0]}-{WINDOW_TASKS[1]-1}・zbar_bin edges = np.arange(-8, 3+ε, 0.5) → {NBIN_Z} bin。\n')
    lines.append(f'kon groups: {[g[0] for g in KON_GROUPS]}\n')

    for i, (eta, tag) in enumerate(zip(ETAS, TAGS)):
        t0, kp, zp = one_eta(tag)
        for gi, (gn, gf) in enumerate(KON_GROUPS):
            mg = gf(kp)
            for bi in range(NBIN_Z):
                zlo, zhi = ZBAR_EDGES[bi], ZBAR_EDGES[bi + 1]
                mz = (zp >= zlo) & (zp < zhi)
                m = mg & mz
                if m.sum() == 0:
                    continue
                mean, std, cnt, sk, ku = bin_stats(t0[m])
                T0_mean[i, bi, gi] = mean
                T0_std[i, bi, gi] = std
                T0_count[i, bi, gi] = cnt
                T0_skew[i, bi, gi] = sk
                T0_kurt[i, bi, gi] = ku
        # per-eta summary: kon_pre=0 の T_0 mean を zbar_bin 別に表示
        lines.append(f'\n## η = {eta}\n')
        lines.append('### T_0 mean of kon_pre=0 群 (幾何量: kick + offset)\n')
        lines.append('| zbar_bin | count | T_0 mean | T_0 std | T_0 skew | T_0 kurt |\n')
        lines.append('|---:|---:|---:|---:|---:|---:|\n')
        for bi in range(NBIN_Z):
            cnt = T0_count[i, bi, 0]
            if cnt == 0:
                continue
            zc = 0.5 * (ZBAR_EDGES[bi] + ZBAR_EDGES[bi + 1])
            lines.append(f'| [{ZBAR_EDGES[bi]:.1f}, {ZBAR_EDGES[bi+1]:.1f}) '
                         f'| {cnt} | {T0_mean[i,bi,0]:+.5f} | {T0_std[i,bi,0]:.5f} | {T0_skew[i,bi,0]:+.3f} | {T0_kurt[i,bi,0]:+.3f} |\n')
        # kon group summary
        lines.append('\n### 各 kon 群の (全 zbar 統合) T_0 mean・std\n')
        lines.append('| kon 群 | count | T_0 mean | T_0 std |\n')
        lines.append('|---|---:|---:|---:|\n')
        for gi, (gn, gf) in enumerate(KON_GROUPS):
            mg = gf(kp)
            n = int(mg.sum())
            if n == 0:
                lines.append(f'| {gn} | 0 | — | — |\n')
                continue
            tv = t0[mg]
            lines.append(f'| {gn} | {n} | {tv.mean():+.5f} | {tv.std():.5f} |\n')

    np.savez(os.path.join(OUT, 'step_T_T0_joint_distribution.npz'),
             T0_mean=T0_mean, T0_std=T0_std, T0_count=T0_count,
             T0_skew=T0_skew, T0_kurt=T0_kurt,
             zbar_bin_edges=ZBAR_EDGES,
             kon_group_labels=np.array([g[0] for g in KON_GROUPS]),
             eta_values=np.array(ETAS))

    # 予期される所見の議論
    lines.append('\n## 予期される所見の照合\n')
    lines.append('- kon_pre=0 & zbar_pre 深部 (-6 以下) で T_0 mean ≈ +0.019 が保持されるか (§9-4 の LRoff0 arm 値+0.034 とは異なる LRa0p03 arm 値 +0.0193)。\n')
    lines.append('- kon_pre≥1 で T_0 mean が負に振れるか (crosser で kick が下向き)。\n')
    lines.append('- 分布形が Gaussian でなく双峰性を示すか (kick+ と kick- の混合)。\n')

    with open(os.path.join(OUT, 'step_T_report.md'), 'w') as f:
        f.writelines(lines)
    print('Saved step_T_T0_joint_distribution.npz and step_T_report.md')


if __name__ == '__main__':
    main()
