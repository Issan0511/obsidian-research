# Step W — v3g 完全理論駆動 simulation

Monte Carlo: N_UNITS=1000 × N_TASKS=260 × N_SEEDS=10
モデル要素:
- κ(η): Step Q' 直測 (n_band=0 stayer, 450 chain, T=3×10⁴)
- c(η): audit-v1b 理論 0.107η (Step R は T_1 汚染で使えず要再検討)
- T_0(k_on, z̄): Step T joint 分布サンプル (Gaussian per cell, 5 未満は fallback)
- T_1+Y_i: session19 Step C 経験表 (kp1/kp2/kp3-5/kp6+)
- n_band(z̄): 3.12 × exp(-0.119 × z̄²)
- k_on 遷移: session19 mt_v2 の task 100-260 の Markov chain

## v3g 5 点予言 vs 実測

|        η | v3g width |   ± σ | v3g zbar_med | v3g N_alive | v3g near_frac | §9-4 width |  α_ref |
| -------: | --------: | ----: | -----------: | ----------: | ------------: | ---------: | -----: |
| 0.000156 |     8.697 | 0.472 |       -6.111 |       184.0 |         0.015 |       6.93 | +0.389 |
|   0.0002 |     9.893 | 0.508 |       -6.244 |       176.8 |         0.027 |       7.37 | +0.607 |
|   0.0005 |    10.728 | 0.637 |       -6.356 |       150.1 |         0.043 |       7.37 | +0.540 |
|    0.001 |     9.759 | 0.661 |       -6.528 |       105.9 |         0.019 |       6.15 | +0.186 |
|   0.0025 |     8.723 | 0.822 |       -6.531 |        67.0 |         0.012 |       5.13 | -1.540 |

## 着地点 A 判定基準
1. Peak position η ∈ [0.0002, 0.0005]
2. Peak value zbar_width ≈ 7.37
3. Spearman(pred, α_ref) ∈ [+0.9, +1.0]

v3g peak: η=0.0005, width=10.728
Spearman(v3g_width, α_ref) = 0.600 (p=0.285)

### 判定結果
- Peak position: η=0.0005 → **OK**
- Peak value: 10.73 vs 7.37 → **×**
- Spearman: 0.600 → **×**
