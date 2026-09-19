# Step E — Y_i の関数形 fitting

入力: step_D_y_per_event.npz

## lr0156 (η=0.000156)  n=250000
### kp0  n=197173  Y_mean=-0.0010  Y_std=0.6952
  (i)  v²                         slope=-0.0007  R²=+0.0000
  (ii) |v|                        slope=-0.0011  R²=+0.0000
  (iii) v²·z_max_kick             slope=+0.0043  R²=+0.0002
  (iv) v²·sgn(v·Σδ'_on)           slope=+0.0000  R²=+0.0000
  (v) v·Σδ'_on                    slope=+0.0000  R²=+0.0000
  (vi) v²·z̄_kick                 slope=+0.0004  R²=+0.0000
  Spearman(Y, sgn_pred)=+nan
### kp1  n=28621  Y_mean=+0.1355  Y_std=1.5493
  (i)  v²                         slope=+0.1315  R²=+0.0064
  (ii) |v|                        slope=+0.2332  R²=+0.0052
  (iii) v²·z_max_kick             slope=+0.2637  R²=+0.0111
  (iv) v²·sgn(v·Σδ'_on)           slope=+0.7871  R²=+0.4489
  (v) v·Σδ'_on                    slope=+0.9388  R²=+0.7892
  (vi) v²·z̄_kick                 slope=-0.0236  R²=+0.0050
  Spearman(Y, sgn_pred)=+0.6765
### kp2  n=6263  Y_mean=+0.1513  Y_std=2.1262
  (i)  v²                         slope=+0.2887  R²=+0.0126
  (ii) |v|                        slope=+0.4406  R²=+0.0087
  (iii) v²·z_max_kick             slope=+0.2177  R²=+0.0119
  (iv) v²·sgn(v·Σδ'_on)           slope=+1.3815  R²=+0.5283
  (v) v·Σδ'_on                    slope=+0.9366  R²=+0.8991
  (vi) v²·z̄_kick                 slope=-0.0721  R²=+0.0123
  Spearman(Y, sgn_pred)=+0.7592
### kp3-5  n=5395  Y_mean=+0.2517  Y_std=3.1128
  (i)  v²                         slope=+0.3814  R²=+0.0083
  (ii) |v|                        slope=+0.5851  R²=+0.0074
  (iii) v²·z_max_kick             slope=+0.2335  R²=+0.0118
  (iv) v²·sgn(v·Σδ'_on)           slope=+2.4187  R²=+0.5488
  (v) v·Σδ'_on                    slope=+0.9231  R²=+0.9548
  (vi) v²·z̄_kick                 slope=-0.1457  R²=+0.0118
  Spearman(Y, sgn_pred)=+0.7771
### kp6+  n=12548  Y_mean=+0.2174  Y_std=7.2019
  (i)  v²                         slope=+0.5988  R²=+0.0020
  (ii) |v|                        slope=+0.9155  R²=+0.0020
  (iii) v²·z_max_kick             slope=+0.1190  R²=+0.0014
  (iv) v²·sgn(v·Σδ'_on)           slope=+7.0229  R²=+0.3669
  (v) v·Σδ'_on                    slope=+0.9000  R²=+0.9941
  (vi) v²·z̄_kick                 slope=-0.1459  R²=+0.0005
  Spearman(Y, sgn_pred)=+0.8398
### all  n=250000  Y_mean=+0.0348  Y_std=1.8939
  (i)  v²                         slope=+0.0160  R²=+0.0001
  (ii) |v|                        slope=+0.0337  R²=+0.0001
  (iii) v²·z_max_kick             slope=+0.0303  R²=+0.0012
  (iv) v²·sgn(v·Σδ'_on)           slope=+1.4249  R²=+0.1531
  (v) v·Σδ'_on                    slope=+0.9050  R²=+0.8673
  (vi) v²·z̄_kick                 slope=+0.0010  R²=+0.0000
  Spearman(Y, sgn_pred)=+0.4437

## lr02 (η=0.0002)  n=250000
### kp0  n=197960  Y_mean=-0.0015  Y_std=0.9181
  (i)  v²                         slope=-0.0016  R²=+0.0000
  (ii) |v|                        slope=-0.0032  R²=+0.0000
  (iii) v²·z_max_kick             slope=+0.0052  R²=+0.0001
  (iv) v²·sgn(v·Σδ'_on)           slope=+0.0000  R²=+0.0000
  (v) v·Σδ'_on                    slope=+0.0000  R²=+0.0000
  (vi) v²·z̄_kick                 slope=+0.0006  R²=+0.0000
  Spearman(Y, sgn_pred)=+nan
### kp1  n=27592  Y_mean=+0.1795  Y_std=2.1186
  (i)  v²                         slope=+0.1684  R²=+0.0064
  (ii) |v|                        slope=+0.3116  R²=+0.0052
  (iii) v²·z_max_kick             slope=+0.3633  R²=+0.0138
  (iv) v²·sgn(v·Σδ'_on)           slope=+1.0240  R²=+0.4706
  (v) v·Σδ'_on                    slope=+1.2416  R²=+0.8134
  (vi) v²·z̄_kick                 slope=-0.0306  R²=+0.0052
  Spearman(Y, sgn_pred)=+0.7028
### kp2  n=6514  Y_mean=+0.2247  Y_std=2.5927
  (i)  v²                         slope=+0.3981  R²=+0.0147
  (ii) |v|                        slope=+0.5608  R²=+0.0102
  (iii) v²·z_max_kick             slope=+0.3501  R²=+0.0177
  (iv) v²·sgn(v·Σδ'_on)           slope=+1.7187  R²=+0.4865
  (v) v·Σδ'_on                    slope=+1.2113  R²=+0.9003
  (vi) v²·z̄_kick                 slope=-0.1083  R²=+0.0168
  Spearman(Y, sgn_pred)=+0.7399
### kp3-5  n=5420  Y_mean=+0.3823  Y_std=4.0323
  (i)  v²                         slope=+0.7536  R²=+0.0162
  (ii) |v|                        slope=+1.0861  R²=+0.0132
  (iii) v²·z_max_kick             slope=+0.4533  R²=+0.0196
  (iv) v²·sgn(v·Σδ'_on)           slope=+3.2666  R²=+0.5251
  (v) v·Σδ'_on                    slope=+1.1926  R²=+0.9624
  (vi) v²·z̄_kick                 slope=-0.2495  R²=+0.0164
  Spearman(Y, sgn_pred)=+0.8006
### kp6+  n=12514  Y_mean=+0.2912  Y_std=10.1391
  (i)  v²                         slope=+0.6618  R²=+0.0013
  (ii) |v|                        slope=+0.9140  R²=+0.0012
  (iii) v²·z_max_kick             slope=+0.2250  R²=+0.0022
  (iv) v²·sgn(v·Σδ'_on)           slope=+9.9886  R²=+0.4335
  (v) v·Σδ'_on                    slope=+1.1547  R²=+0.9957
  (vi) v²·z̄_kick                 slope=+0.1044  R²=+0.0001
  Spearman(Y, sgn_pred)=+0.8463
### all  n=250000  Y_mean=+0.0473  Y_std=2.6165
  (i)  v²                         slope=+0.0190  R²=+0.0001
  (ii) |v|                        slope=+0.0434  R²=+0.0001
  (iii) v²·z_max_kick             slope=+0.0444  R²=+0.0013
  (iv) v²·sgn(v·Σδ'_on)           slope=+1.9172  R²=+0.1568
  (v) v·Σδ'_on                    slope=+1.1630  R²=+0.8809
  (vi) v²·z̄_kick                 slope=+0.0017  R²=+0.0000
  Spearman(Y, sgn_pred)=+0.4544

## lr05 (η=0.0005)  n=250000
### kp0  n=201442  Y_mean=-0.0057  Y_std=2.7730
  (i)  v²                         slope=-0.0041  R²=+0.0000
  (ii) |v|                        slope=-0.0077  R²=+0.0000
  (iii) v²·z_max_kick             slope=+0.0104  R²=+0.0001
  (iv) v²·sgn(v·Σδ'_on)           slope=+0.0000  R²=+0.0000
  (v) v·Σδ'_on                    slope=+0.0000  R²=+0.0000
  (vi) v²·z̄_kick                 slope=+0.0014  R²=+0.0000
  Spearman(Y, sgn_pred)=+nan
### kp1  n=25382  Y_mean=+0.5820  Y_std=7.2857
  (i)  v²                         slope=+0.2605  R²=+0.0020
  (ii) |v|                        slope=+0.6493  R²=+0.0020
  (iii) v²·z_max_kick             slope=+0.8613  R²=+0.0142
  (iv) v²·sgn(v·Σδ'_on)           slope=+2.5926  R²=+0.5027
  (v) v·Σδ'_on                    slope=+3.3230  R²=+0.8679
  (vi) v²·z̄_kick                 slope=-0.0481  R²=+0.0015
  Spearman(Y, sgn_pred)=+0.7678
### kp2  n=5047  Y_mean=+0.8183  Y_std=10.0486
  (i)  v²                         slope=+0.5551  R²=+0.0044
  (ii) |v|                        slope=+1.3309  R²=+0.0044
  (iii) v²·z_max_kick             slope=+0.5909  R²=+0.0087
  (iv) v²·sgn(v·Σδ'_on)           slope=+4.0811  R²=+0.5318
  (v) v·Σδ'_on                    slope=+3.2470  R²=+0.9478
  (vi) v²·z̄_kick                 slope=-0.1652  R²=+0.0047
  Spearman(Y, sgn_pred)=+0.8128
### kp3-5  n=5110  Y_mean=+0.7984  Y_std=15.2333
  (i)  v²                         slope=+0.4522  R²=+0.0011
  (ii) |v|                        slope=+0.9012  R²=+0.0009
  (iii) v²·z_max_kick             slope=+0.2025  R²=+0.0007
  (iv) v²·sgn(v·Σδ'_on)           slope=+6.8750  R²=+0.5450
  (v) v·Σδ'_on                    slope=+3.0926  R²=+0.9804
  (vi) v²·z̄_kick                 slope=-0.1397  R²=+0.0007
  Spearman(Y, sgn_pred)=+0.8456
### kp6+  n=13019  Y_mean=+1.6032  Y_std=51.2474
  (i)  v²                         slope=+1.1942  R²=+0.0006
  (ii) |v|                        slope=+2.5707  R²=+0.0007
  (iii) v²·z_max_kick             slope=+0.3840  R²=+0.0013
  (iv) v²·sgn(v·Σδ'_on)           slope=+23.1369  R²=+0.4410
  (v) v·Σδ'_on                    slope=+2.9151  R²=+0.9982
  (vi) v²·z̄_kick                 slope=+0.5408  R²=+0.0008
  Spearman(Y, sgn_pred)=+0.8604
### all  n=250000  Y_mean=+0.1708  Y_std=12.4619
  (i)  v²                         slope=+0.0723  R²=+0.0000
  (ii) |v|                        slope=+0.1897  R²=+0.0001
  (iii) v²·z_max_kick             slope=+0.1644  R²=+0.0014
  (iv) v²·sgn(v·Σδ'_on)           slope=+6.7548  R²=+0.1873
  (v) v·Σδ'_on                    slope=+2.9336  R²=+0.9520
  (vi) v²·z̄_kick                 slope=+0.0140  R²=+0.0001
  Spearman(Y, sgn_pred)=+0.5073

## lr10 (η=0.001)  n=250000
### kp0  n=208096  Y_mean=-0.0223  Y_std=6.2019
  (i)  v²                         slope=-0.0181  R²=+0.0000
  (ii) |v|                        slope=-0.0420  R²=+0.0000
  (iii) v²·z_max_kick             slope=+0.0364  R²=+0.0002
  (iv) v²·sgn(v·Σδ'_on)           slope=+0.0000  R²=+0.0000
  (v) v·Σδ'_on                    slope=+0.0000  R²=+0.0000
  (vi) v²·z̄_kick                 slope=+0.0049  R²=+0.0000
  Spearman(Y, sgn_pred)=+nan
### kp1  n=24380  Y_mean=+1.4852  Y_std=18.6895
  (i)  v²                         slope=+0.3548  R²=+0.0009
  (ii) |v|                        slope=+1.0360  R²=+0.0009
  (iii) v²·z_max_kick             slope=+1.4510  R²=+0.0113
  (iv) v²·sgn(v·Σδ'_on)           slope=+5.0442  R²=+0.5251
  (v) v·Σδ'_on                    slope=+6.7998  R²=+0.8879
  (vi) v²·z̄_kick                 slope=-0.0457  R²=+0.0003
  Spearman(Y, sgn_pred)=+0.7807
### kp2  n=4150  Y_mean=+2.7565  Y_std=28.1442
  (i)  v²                         slope=+0.5989  R²=+0.0012
  (ii) |v|                        slope=+1.8006  R²=+0.0013
  (iii) v²·z_max_kick             slope=+0.6295  R²=+0.0027
  (iv) v²·sgn(v·Σδ'_on)           slope=+7.4464  R²=+0.5674
  (v) v·Σδ'_on                    slope=+6.6341  R²=+0.9576
  (vi) v²·z̄_kick                 slope=-0.1447  R²=+0.0010
  Spearman(Y, sgn_pred)=+0.8317
### kp3-5  n=4337  Y_mean=+3.6508  Y_std=45.7977
  (i)  v²                         slope=+1.1101  R²=+0.0017
  (ii) |v|                        slope=+3.0232  R²=+0.0015
  (iii) v²·z_max_kick             slope=+0.6231  R²=+0.0023
  (iv) v²·sgn(v·Σδ'_on)           slope=+11.6133  R²=+0.5453
  (v) v·Σδ'_on                    slope=+6.2363  R²=+0.9856
  (vi) v²·z̄_kick                 slope=-0.3221  R²=+0.0013
  Spearman(Y, sgn_pred)=+0.8481
### kp6+  n=9037  Y_mean=+6.9106  Y_std=128.9665
  (i)  v²                         slope=+2.9333  R²=+0.0015
  (ii) |v|                        slope=+7.8954  R²=+0.0015
  (iii) v²·z_max_kick             slope=+0.8705  R²=+0.0025
  (iv) v²·sgn(v·Σδ'_on)           slope=+33.9616  R²=+0.4647
  (v) v·Σδ'_on                    slope=+5.8475  R²=+0.9981
  (vi) v²·z̄_kick                 slope=+0.6434  R²=+0.0005
  Spearman(Y, sgn_pred)=+0.8633
### all  n=250000  Y_mean=+0.4851  Y_std=26.8124
  (i)  v²                         slope=+0.3039  R²=+0.0003
  (ii) |v|                        slope=+0.7310  R²=+0.0002
  (iii) v²·z_max_kick             slope=+0.4381  R²=+0.0033
  (iv) v²·sgn(v·Σδ'_on)           slope=+11.8159  R²=+0.2391
  (v) v·Σδ'_on                    slope=+5.9091  R²=+0.9459
  (vi) v²·z̄_kick                 slope=+0.0380  R²=+0.0001
  Spearman(Y, sgn_pred)=+0.4954

## lr25 (η=0.0025)  n=250000
### kp0  n=215993  Y_mean=-0.0876  Y_std=15.6593
  (i)  v²                         slope=-0.0395  R²=+0.0000
  (ii) |v|                        slope=-0.1196  R²=+0.0000
  (iii) v²·z_max_kick             slope=+0.1185  R²=+0.0005
  (iv) v²·sgn(v·Σδ'_on)           slope=+0.0000  R²=+0.0000
  (v) v·Σδ'_on                    slope=+0.0000  R²=+0.0000
  (vi) v²·z̄_kick                 slope=+0.0141  R²=+0.0001
  Spearman(Y, sgn_pred)=+nan
### kp1  n=22578  Y_mean=+5.7082  Y_std=47.4746
  (i)  v²                         slope=+1.1462  R²=+0.0019
  (ii) |v|                        slope=+3.9294  R²=+0.0023
  (iii) v²·z_max_kick             slope=+4.0232  R²=+0.0156
  (iv) v²·sgn(v·Σδ'_on)           slope=+11.4365  R²=+0.5170
  (v) v·Σδ'_on                    slope=+17.0530  R²=+0.8905
  (vi) v²·z̄_kick                 slope=-0.1978  R²=+0.0013
  Spearman(Y, sgn_pred)=+0.7865
### kp2  n=3512  Y_mean=+10.3038  Y_std=72.5725
  (i)  v²                         slope=+1.3959  R²=+0.0011
  (ii) |v|                        slope=+5.5395  R²=+0.0018
  (iii) v²·z_max_kick             slope=+0.8962  R²=+0.0009
  (iv) v²·sgn(v·Σδ'_on)           slope=+17.9261  R²=+0.5567
  (v) v·Σδ'_on                    slope=+16.4573  R²=+0.9570
  (vi) v²·z̄_kick                 slope=-0.3874  R²=+0.0014
  Spearman(Y, sgn_pred)=+0.8237
### kp3-5  n=3122  Y_mean=+14.2651  Y_std=122.0229
  (i)  v²                         slope=+3.1893  R²=+0.0023
  (ii) |v|                        slope=+10.6084  R²=+0.0025
  (iii) v²·z_max_kick             slope=+2.1633  R²=+0.0048
  (iv) v²·sgn(v·Σδ'_on)           slope=+28.2150  R²=+0.5566
  (v) v·Σδ'_on                    slope=+15.5165  R²=+0.9845
  (vi) v²·z̄_kick                 slope=-0.8862  R²=+0.0018
  Spearman(Y, sgn_pred)=+0.8474
### kp6+  n=4795  Y_mean=+14.7672  Y_std=348.7134
  (i)  v²                         slope=+3.8132  R²=+0.0004
  (ii) |v|                        slope=+11.0324  R²=+0.0004
  (iii) v²·z_max_kick             slope=+0.9452  R²=+0.0005
  (iv) v²·sgn(v·Σδ'_on)           slope=+75.9793  R²=+0.4924
  (v) v·Σδ'_on                    slope=+14.7299  R²=+0.9977
  (vi) v²·z̄_kick                 slope=-0.0117  R²=+0.0000
  Spearman(Y, sgn_pred)=+0.8637
### all  n=250000  Y_mean=+1.0460  Y_std=54.9337
  (i)  v²                         slope=+0.4462  R²=+0.0002
  (ii) |v|                        slope=+1.2787  R²=+0.0002
  (iii) v²·z_max_kick             slope=+0.7105  R²=+0.0024
  (iv) v²·sgn(v·Σδ'_on)           slope=+24.0184  R²=+0.2430
  (v) v·Σδ'_on                    slope=+14.9309  R²=+0.9172
  (vi) v²·z̄_kick                 slope=+0.0323  R²=+0.0000
  Spearman(Y, sgn_pred)=+0.4466

## η 依存 (log-log fit of |slope|)  — form (v2)
  kp1: slope(v2) [values = [0.13149955339755556, 0.1684222836369301, 0.2604904196522648, 0.35480502765430083, 1.1461589108399066]], mean R²=0.004
    → |slope| ∝ η^0.72  C = exp(+4.20) = 6.672e+01
  kp2: slope(v2) [values = [0.2886826071270426, 0.39806737753469945, 0.5551193310667715, 0.5989011244888524, 1.3959296805127908]], mean R²=0.007
    → |slope| ∝ η^0.50  C = exp(+3.15) = 2.344e+01
  kp3-5: slope(v2) [values = [0.38142418654421395, 0.7536347417391436, 0.4521565351263434, 1.1101210906833647, 3.1893305514322092]], mean R²=0.006
    → |slope| ∝ η^0.64  C = exp(+4.67) = 1.064e+02
  kp6+: slope(v2) [values = [0.598806878896621, 0.661787159986507, 1.1941619033576563, 2.9333142286582086, 3.8131776324655156]], mean R²=0.001
    → |slope| ∝ η^0.72  C = exp(+5.80) = 3.296e+02

## η 依存 (log-log fit of |slope|)  — form (v_sumdprime_on)
  kp1: slope(v_sumdprime_on) [values = [0.9388417687427837, 1.2416360956615442, 3.3229919574266416, 6.799790143852132, 17.052992635733613]], mean R²=0.850
    → |slope| ∝ η^1.05  C = exp(+9.12) = 9.177e+03
  kp2: slope(v_sumdprime_on) [values = [0.9366326458411631, 1.2112627962020186, 3.2469536539662402, 6.634140218630844, 16.45728806415743]], mean R²=0.932
    → |slope| ∝ η^1.04  C = exp(+9.04) = 8.427e+03
  kp3-5: slope(v_sumdprime_on) [values = [0.9231080248429526, 1.19256679290109, 3.092591735799698, 6.236329025216342, 15.51654905766509]], mean R²=0.974
    → |slope| ∝ η^1.02  C = exp(+8.86) = 7.038e+03
  kp6+: slope(v_sumdprime_on) [values = [0.9000106043281518, 1.154656778797772, 2.9151004571772723, 5.847514614939033, 14.729933284750691]], mean R²=0.997
    → |slope| ∝ η^1.01  C = exp(+8.73) = 6.172e+03

## η 依存 (log-log fit of |slope|)  — form (v2_zmax)
  kp1: slope(v2_zmax) [values = [0.2637178247352579, 0.3633183997134269, 0.8613343834637203, 1.4510044334400656, 4.023166567913165]], mean R²=0.013
    → |slope| ∝ η^0.95  C = exp(+7.06) = 1.161e+03
  kp2: slope(v2_zmax) [values = [0.21772580114553597, 0.350130632412916, 0.5908615555226111, 0.6294560939457468, 0.8961521629754241]], mean R²=0.008
    → |slope| ∝ η^0.46  C = exp(+2.72) = 1.517e+01
  kp3-5: slope(v2_zmax) [values = [0.23351817402086938, 0.4532644828912608, 0.20246721699695988, 0.6231128761348598, 2.1632907226900486]], mean R²=0.008
    → |slope| ∝ η^0.66  C = exp(+4.31) = 7.429e+01
  kp6+: slope(v2_zmax) [values = [0.11899833759833875, 0.22496728572161892, 0.3839675878627111, 0.8705027669737186, 0.9452439413379445]], mean R²=0.002
    → |slope| ∝ η^0.74  C = exp(+4.61) = 1.004e+02

## η 依存 (log-log fit of |slope|)  — form (v2_sgn)
  kp1: slope(v2_sgn) [values = [0.7870624255138969, 1.0239831812252767, 2.592612873745823, 5.044193539498063, 11.436454571234295]], mean R²=0.493
    → |slope| ∝ η^0.97  C = exp(+8.27) = 3.914e+03
  kp2: slope(v2_sgn) [values = [1.3814692372518524, 1.7187356123267834, 4.0810806524651895, 7.446417421868157, 17.926120292282505]], mean R²=0.534
    → |slope| ∝ η^0.92  C = exp(+8.40) = 4.446e+03
  kp3-5: slope(v2_sgn) [values = [2.418697015934289, 3.2666480282143913, 6.8749748121141065, 11.6133262424956, 28.215001942708657]], mean R²=0.544
    → |slope| ∝ η^0.86  C = exp(+8.47) = 4.749e+03
  kp6+: slope(v2_sgn) [values = [7.02285103758398, 9.988587004331213, 23.136935839373173, 33.961648486569736, 75.97926265585883]], mean R²=0.440
    → |slope| ∝ η^0.83  C = exp(+9.31) = 1.110e+04
