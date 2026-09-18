# Step F — Markov 遷移確率 (LRa0p03)


## lr0156 (η=0.000156)  n=400000  window tasks [100, 500)
  kp0     n=  323965  mean zbar_pre=-5.825  →  kp0:  99.9%  kp1:   0.1%  kp2:   0.0%  kp3+:   0.0%
  kp1     n=   33839  mean zbar_pre=-4.238  →  kp0:  22.3%  kp1:  70.3%  kp2:   5.8%  kp3+:   1.7%
  kp2     n=    7384  mean zbar_pre=-3.506  →  kp0:   4.3%  kp1:  22.3%  kp2:  60.6%  kp3+:  12.8%
  kp3-5   n=    7475  mean zbar_pre=-2.824  →  kp0:   0.6%  kp1:   7.0%  kp2:  13.2%  kp3+:  79.2%
  kp6+    n=   27337  mean zbar_pre=+0.853  →  kp0:   0.0%  kp1:   0.2%  kp2:   0.4%  kp3+:  99.4%

## lr02 (η=0.0002)  n=400000  window tasks [100, 500)
  kp0     n=  327783  mean zbar_pre=-5.834  →  kp0:  99.9%  kp1:   0.1%  kp2:   0.0%  kp3+:   0.0%
  kp1     n=   31688  mean zbar_pre=-4.227  →  kp0:  26.2%  kp1:  65.0%  kp2:   6.5%  kp3+:   2.2%
  kp2     n=    7001  mean zbar_pre=-3.513  →  kp0:   6.3%  kp1:  23.5%  kp2:  56.3%  kp3+:  13.9%
  kp3-5   n=    7007  mean zbar_pre=-2.769  →  kp0:   1.4%  kp1:   8.8%  kp2:  13.3%  kp3+:  76.5%
  kp6+    n=   26521  mean zbar_pre=+0.881  →  kp0:   0.0%  kp1:   0.2%  kp2:   0.6%  kp3+:  99.2%

## lr05 (η=0.0005)  n=400000  window tasks [100, 500)
  kp0     n=  339782  mean zbar_pre=-5.892  →  kp0:  99.8%  kp1:   0.1%  kp2:   0.0%  kp3+:   0.0%
  kp1     n=   26719  mean zbar_pre=-4.296  →  kp0:  34.2%  kp1:  55.1%  kp2:   6.6%  kp3+:   4.0%
  kp2     n=    5117  mean zbar_pre=-3.404  →  kp0:  14.2%  kp1:  24.5%  kp2:  42.8%  kp3+:  18.4%
  kp3-5   n=    5806  mean zbar_pre=-2.768  →  kp0:   4.7%  kp1:  13.4%  kp2:  13.4%  kp3+:  68.5%
  kp6+    n=   22576  mean zbar_pre=+0.574  →  kp0:   0.1%  kp1:   0.8%  kp2:   1.2%  kp3+:  97.9%

## lr10 (η=0.001)  n=400000  window tasks [100, 500)
  kp0     n=  360161  mean zbar_pre=-5.964  →  kp0:  99.7%  kp1:   0.2%  kp2:   0.0%  kp3+:   0.0%
  kp1     n=   23159  mean zbar_pre=-4.419  →  kp0:  40.7%  kp1:  50.1%  kp2:   5.4%  kp3+:   3.8%
  kp2     n=    3665  mean zbar_pre=-3.520  →  kp0:  20.6%  kp1:  26.7%  kp2:  33.7%  kp3+:  19.0%
  kp3-5   n=    3688  mean zbar_pre=-2.784  →  kp0:  10.0%  kp1:  14.8%  kp2:  16.1%  kp3+:  59.2%
  kp6+    n=    9327  mean zbar_pre=+0.279  →  kp0:   0.4%  kp1:   1.9%  kp2:   2.4%  kp3+:  95.3%

## lr25 (η=0.0025)  n=400000  window tasks [100, 500)
  kp0     n=  366122  mean zbar_pre=-5.922  →  kp0:  99.7%  kp1:   0.3%  kp2:   0.0%  kp3+:   0.0%
  kp1     n=   23268  mean zbar_pre=-4.523  →  kp0:  49.2%  kp1:  42.8%  kp2:   4.4%  kp3+:   3.6%
  kp2     n=    2699  mean zbar_pre=-3.662  →  kp0:  30.5%  kp1:  28.2%  kp2:  25.0%  kp3+:  16.3%
  kp3-5   n=    2593  mean zbar_pre=-2.895  →  kp0:  15.0%  kp1:  20.1%  kp2:  15.1%  kp3+:  49.8%
  kp6+    n=    5318  mean zbar_pre=-0.134  →  kp0:   0.8%  kp1:   2.9%  kp2:   3.5%  kp3+:  92.8%

saved /home/kubo/project/Nakatsuka/claude/hole1_scripts/session21_out/step_F_markov_transitions.csv

## audit-v1b §3-11 LRoff0 reference (kp1 の終点):
  LRoff0: kp0=37%, kp≥3=13%  (η=0.01)
  LRa0p03 対応 (per-arm):
  lr0156 η=0.000156:  kp1 →  kp0: 22.3%  kp1: 70.3%  kp2: 5.8%  kp3+: 1.7%
  lr02 η=0.0002:  kp1 →  kp0: 26.2%  kp1: 65.0%  kp2: 6.5%  kp3+: 2.2%
  lr05 η=0.0005:  kp1 →  kp0: 34.2%  kp1: 55.1%  kp2: 6.6%  kp3+: 4.0%
  lr10 η=0.001:  kp1 →  kp0: 40.7%  kp1: 50.1%  kp2: 5.4%  kp3+: 3.8%
  lr25 η=0.0025:  kp1 →  kp0: 49.2%  kp1: 42.8%  kp2: 4.4%  kp3+: 3.6%
