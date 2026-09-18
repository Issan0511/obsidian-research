"""step_F_markov.py — 1 タスク内 k_on 動態の Markov 遷移確率

session20 の 500-task v2 npz (kon, kon_kick) からタスク遷移を集計:
  p(kon_next | kon_pre, kon_kick, η) を per-η per-kp 群で

各 kp 群 (kp0, kp1, kp2, kp3-5, kp6+) の終点分布 (kp0/kp1/kp2/kp3+) を集計。
audit-v1b §3-11「LRoff0: k=1 の終点は k=0 が 37%・k≥3 が 13%」の LRa0p03 版。

入力: session20_out/mt_U1_bareK1_500tasks_v2_lr*.npz
出力:
  session21_out/step_F_markov_transitions.csv
  session21_out/step_F_report.md
"""
import numpy as np, sys, os, csv

OUT_DIR = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session21_out'
S20_DIR = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session20_out'
ETAS = {'0156': 0.000156, '02': 0.0002, '05': 0.0005, '10': 0.001, '25': 0.0025}
TAGS = list(ETAS.keys())


def group_label(k):
    if k == 0: return 'kp0'
    if k == 1: return 'kp1'
    if k == 2: return 'kp2'
    if k <= 5: return 'kp3-5'
    return 'kp6+'


def next_bucket(kn):
    if kn == 0: return 'kp0'
    if kn == 1: return 'kp1'
    if kn == 2: return 'kp2'
    return 'kp3+'


def main():
    log = ['# Step F — Markov 遷移確率 (LRa0p03)', '']
    def L(s):
        print(s, flush=True); log.append(s)

    rows = []  # (tag, eta, kp_kick_group, next_bucket, count, frac, mean_zbar_pre)
    for tag in TAGS:
        eta = ETAS[tag]
        v2path = os.path.join(S20_DIR, f'mt_U1_bareK1_500tasks_v2_lr{tag}.npz')
        if not os.path.exists(v2path):
            L(f'\n## lr{tag}: MISSING {v2path}')
            continue
        d = np.load(v2path)
        kon = d['kon']              # (T+1, C, H)  = (501, 10, 100)
        kon_kick = d['kon_kick']    # (T, C, H)    = (500, 10, 100)
        zbar = d['zbar']            # (T+1, C, H)

        T = kon_kick.shape[0]
        # For each task t, event (c, i) has:
        #   kon_pre  = kon[t]         (start of task = end of prev task's SGD)
        #   kon_kick = kon_kick[t]    (right after flip, before SGD)
        #   kon_next = kon[t+1]       (end of task after SGD)
        #   zbar_pre = zbar[t]

        # Use tail window 100..T (skip warmup)
        WARMUP = 100
        kp_pre = kon[WARMUP:T].ravel()          # (n,)  actually indexes t = WARMUP..T-1  matching kon_kick[WARMUP:T]
        kp_kick = kon_kick[WARMUP:T].ravel()    # (n,)
        kn_next = kon[WARMUP+1:T+1].ravel()     # (n,)  end of task t
        zb_pre = zbar[WARMUP:T].ravel()         # (n,)

        n_total = kp_kick.size
        L(f'\n## lr{tag} (η={eta:g})  n={n_total}  window tasks [{WARMUP}, {T})')

        # group by kp_kick (post-flip); track kn_next distribution
        kp_kick_int = kp_kick.astype(int)
        kn_next_int = kn_next.astype(int)

        for kp_g in ['kp0', 'kp1', 'kp2', 'kp3-5', 'kp6+']:
            if kp_g == 'kp0': gm = kp_kick_int == 0
            elif kp_g == 'kp1': gm = kp_kick_int == 1
            elif kp_g == 'kp2': gm = kp_kick_int == 2
            elif kp_g == 'kp3-5': gm = (kp_kick_int >= 3) & (kp_kick_int <= 5)
            else: gm = kp_kick_int >= 6
            n_g = int(gm.sum())
            if n_g == 0:
                continue
            # bucketize kn_next
            nn = kn_next_int[gm]
            zb_g = zb_pre[gm]
            b_counts = dict(kp0=0, kp1=0, kp2=0, **{'kp3+': 0})
            for k in nn:
                b = next_bucket(int(k))
                b_counts[b] += 1
            L(f'  {kp_g:6s}  n={n_g:>8d}  mean zbar_pre={zb_g.mean():+.3f}  →  ' +
              '  '.join(f'{b}: {b_counts[b]/n_g*100:>5.1f}%' for b in ['kp0','kp1','kp2','kp3+']))
            for b in ['kp0', 'kp1', 'kp2', 'kp3+']:
                rows.append(dict(tag=tag, eta=eta, kp_kick_group=kp_g, next_bucket=b,
                                 count=b_counts[b], frac=b_counts[b]/n_g,
                                 mean_zbar_pre=float(zb_g.mean()), n_g=n_g))

    csvpath = os.path.join(OUT_DIR, 'step_F_markov_transitions.csv')
    with open(csvpath, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['tag','eta','kp_kick_group','next_bucket','count','frac','mean_zbar_pre','n_g'])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    L(f'\nsaved {csvpath}')

    # LRoff0 §3-11 reference
    L('\n## audit-v1b §3-11 LRoff0 reference (kp1 の終点):')
    L('  LRoff0: kp0=37%, kp≥3=13%  (η=0.01)')
    L('  LRa0p03 対応 (per-arm):')
    for tag in TAGS:
        eta = ETAS[tag]
        rr = [r for r in rows if r['tag'] == tag and r['kp_kick_group'] == 'kp1']
        if not rr:
            continue
        frac = {r['next_bucket']: r['frac'] for r in rr}
        L(f'  lr{tag} η={eta:g}:  kp1 →  kp0: {frac.get("kp0",0)*100:.1f}%  kp1: {frac.get("kp1",0)*100:.1f}%  kp2: {frac.get("kp2",0)*100:.1f}%  kp3+: {frac.get("kp3+",0)*100:.1f}%')

    with open(os.path.join(OUT_DIR, 'step_F_report.md'), 'w') as f:
        f.write('\n'.join(log))
    L(f'\nsaved step_F_report.md')


if __name__ == '__main__':
    main()
