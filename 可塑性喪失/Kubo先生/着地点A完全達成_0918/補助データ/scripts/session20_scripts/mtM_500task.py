"""Step U — mtM_v2.py の 500 タスク版

session19 mtM_v2.py と同じ設定で ntask=500・default kappa_dead=1.0・maintain=False。

出力: session20_out/mt_U1_bareK1_500tasks_v2_lr{tag}.npz
"""
import numpy as np, sys, os, json, time
sys.path.insert(0, '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session19_scripts')
from mtM_v2 import run

CKPATH = '/home/kubo/project/Nakatsuka/data/act_sweep_hole1_0910_local/ckpts/LRa0p03_1216_step5000000.pt'
OUT = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session20_out'
ETAS = [0.000156, 0.0002, 0.0005, 0.001, 0.0025]
TAGS = ['0156', '02', '05', '10', '25']
NTASK = 500
T_STEPS = 10000


def main(only_tag=None):
    os.makedirs(OUT, exist_ok=True)
    for eta, tag in zip(ETAS, TAGS):
        if only_tag is not None and tag != only_tag:
            continue
        print(f'[mtM_500task] η={eta:g} tag={tag} ntask={NTASK}  starting ...', flush=True)
        t0 = time.time()
        out = run(CKPATH, list(range(10)), eta, NTASK, T=T_STEPS,
                  freeze_dead_W=False, freeze_v=False,
                  kappa_dead=1.0, maintain=False, kahan=False)
        out = {k: v for k, v in out.items() if not (isinstance(v, np.ndarray) and v.size == 0)}
        outpath = os.path.join(OUT, f'mt_U1_bareK1_500tasks_v2_lr{tag}.npz')
        np.savez_compressed(outpath, **out)
        dt = time.time() - t0
        size = os.path.getsize(outpath)
        print(f'  saved {outpath}  walltime {dt:.0f}s  size {size/1e6:.1f}MB', flush=True)


if __name__ == '__main__':
    only = sys.argv[1] if len(sys.argv) > 1 else None
    main(only)
