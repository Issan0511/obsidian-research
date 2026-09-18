# Session 20 総まとめ — Claude Code 委譲実施結果

**実施者**: Claude Code (Opus 4.7)
**依頼元**: Chat Claude 第 19 回・Kubo（先生）
**実施日**: 2026-09-17
**spec**: [[claude-code-handoff-session20-spec-0917]]
**working directory**: `~/project/Nakatsuka`
**成果物ディレクトリ**: `~/project/Nakatsuka/claude/hole1_scripts/session20_out/`

---

## 0. 一行結論（chat が最初に読む）

1. **Step Q'** (κ SNR 向上): 450 chain × T=3×10⁴ で直測。CI 幅目標 3e-05 は **未達** (実測 CI 幅 2.8e-4〜4.6e-4・session19 と同レベル)。しかし **noise batch 別 κ** (3 batch) が per-η で一貫し、SNR は改善しているが chain resample が支配。**中心値**: η=0.000156 → +6.2e-5, η=0.0025 → +6.1e-4。特に **η=0.0025 で CI が [3.8e-4, 8.4e-4] と 0 を除外** ← session19 中心値 2.7e-4 より 2.3 倍大。
2. **Step R** (v 凍結で c 分離): sf_vfrozen で v_rel_diff_max = 0.0 完全凍結 ✓。しかし **v 凍結でも T_1 (一次 refit) が残る** (audit-v1b §3-10) ため、alive 群では c 分離できず (c_kon1 が正の符号 +6e-2 と異常)。**T_5 の isolate には v 凍結 GD の追加走行が必要**（要 chat 判断）。
3. **Step T** (T_0 joint): kon_pre=0 群で **T_0 mean が zbar 依存**。zbar_pre 深部 (-7.75) で +0.09、shallow (-1.75) で -0.20。これは v3f で per-unit fixed T_0 を使った失敗の直接原因を確定させる (T_0 は状態依存)。
4. **Step U** (500 タスク): 段 0 check 完全一致 (diff_kon=0, diff_zbar=0.00e+00) ✓。**W5 (441-500) で peak η が 0.0002 → 0.000156 に移動**。低 η (0.000156, 0.0002) で zbar_width が W1→W5 で +11%, +4% 増加 → **500 タスクでも中低 η は完全定常でない**。Spearman が W1〜W4 で +0.900 → W5 で +0.700 に低下。**§9-4 の着地点 A 判定基準は 260 タスクの過渡現象の可能性**。
5. **Step V** (T_1 理論式検証): ζ ≈ δ' の 0 次近似で kp1 群 corr = 0.42-0.46 (LRoff0 の 0.55-0.68 より低い)、slope = 0.60-0.69 (audit-v1b の 0.45 予想より高い)。**Y_i の残差平均 +0.18-0.21 と大きく、単純 T_1 式では kp1 の drift を説明できない**。実測 measured T_1+Y_i は正値 (+0.10-0.13) で **上向き** ← STEP_C_TABLE (負) と符号逆転。 T_5 の理論値 (0.107η) が過小で T_1+Y_i の isolation が不完全。
6. **Step W** (v3g simulation): peak η=0.0005 ✓、value 10.73 (実測 7.37 の 1.46× 過大)、Spearman +0.800。**着地点 A の 3 判定基準のうち 1 つ (peak position) のみ達成**。zbar_med が -6.9〜-7.2 で実測 -2.7〜-3.6 より 2 倍深い ← alive 群 Δz̄ を STEP_C_TABLE で加算した設計は不十分。

---

## 1. 各 Step の実施結果の要旨

### Step Q' — LRa0p03 arm の κ(η) SNR 向上直測

**手法**: `sf_sweep_plus.py`。checkpoint は seed 10 個しかないので、**3 noise batch × 10 seed × 15 flip = 450 chain** に増やし、T=10⁴ → 3×10⁴ に増加。段 0 check は `sf_s0.py` を再利用 (PASS)。

**主要結果 (κ 5 点)**:

|        η | κ mean (all 450 chain) |        95% CI [lo, hi] |   CI 幅 | κ_batch0 | κ_batch1 | κ_batch2 |
| -------: | ---------------------: | ---------------------: | -----: | -------: | -------: | -------: |
| 0.000156 |              +6.21e-05 |     [-6.9e-5, +2.1e-4] | 2.8e-4 |  +5.4e-5 |  +6.1e-5 |  +6.4e-5 |
|   0.0002 |              +4.82e-05 |     [-9.3e-5, +2.0e-4] | 2.9e-4 |  +5.0e-5 |  +3.6e-5 |  +5.1e-5 |
|   0.0005 |              -1.67e-05 |     [-1.7e-4, +1.5e-4] | 3.2e-4 |  -4.1e-5 |  -6.9e-6 |  -1.1e-5 |
|    0.001 |              +2.42e-05 |     [-1.2e-4, +1.8e-4] | 3.1e-4 |  +3.4e-5 |  -3.1e-5 |  +6.2e-5 |
|   0.0025 |          **+6.09e-04** | **[+3.8e-4, +8.4e-4]** | 4.6e-4 |  +5.6e-4 |  +6.4e-4 |  +6.2e-4 |

**a² × η^{1.352} scaling 予想との比較 (κ_LRa0p03 = 0.09 × κ_LRoff0)**:

|          η | LRoff0 予想 |     ×0.09 予想 |    LRa0p03 実測 | ratio 実測/予想 |
| ---------: | --------: | -----------: | ------------: | ----------: |
|   0.000156 |  ~4.5e-05 |     ~4.0e-06 |     +6.21e-05 |        ~15× |
|     0.0002 |  ~6.4e-05 |     ~5.8e-06 |     +4.82e-05 |         ~8× |
|     0.0005 |  ~2.2e-04 |     ~2.0e-05 |     -1.67e-05 |   ~0 (符号異常) |
|      0.001 |  ~5.6e-04 |     ~5.0e-05 |     +2.42e-05 |        ~0.5 |
| **0.0025** |  ~1.9e-03 | **~1.7e-04** | **+6.09e-04** |   **~3.6×** |

- session19 で「η=0.001 で ratio 1.03 の見事な一致」を報告したが、今回の再走 (chain 3 倍・T 3 倍) では η=0.001 中心値が 2.4e-5 に低下し ratio 0.5 → **session19 の 1.03 は偶然一致だった可能性**。
- η=0.0025 で **中心値 6.1e-4 が session19 の 2.7e-4 と 2.3 倍差** ← T=3×10⁴ 長時間で n_band=0 stayer 条件が破れやすく、pure T_4 unit の選択が変わる可能性 (chat 検証 必要)。
- **noise batch 別 κ** が per-η で一貫 → 真の SNR は 10^-5 レベル。bootstrap CI が広いのは **init seed × kp の 150 unique chain のばらつき** が主で、chain 数 3 倍にしても CI 幅は 0.9 倍程度しか改善しない。

**判定条件**:
- CI 幅目標 3e-05 → **未達** (2.8e-4〜4.6e-4 で 10 倍過大)
- Spearman(κ, η): 中心値で +0.100 (p=0.873) → 単調性弱

### Step R — v 凍結で c(η) 分離

**手法**: `sf_vfrozen.py` で SGD 内側の `v -= η × 2d × φ` を削除。v_rel_diff_max=0.0 で v 完全凍結を検算 ✓。150 chain × T=10⁴。

**主要結果 (v 凍結時の c 5 点値・T_4 減算後)**:

|        η | κ_vfrozen (参考) |  c_stayer |    c_kon0 |        c_kon1 |    c_kon2 |  c_kon3_5 |   c_kon6p |
| -------: | -------------: | --------: | --------: | ------------: | --------: | --------: | --------: |
| 0.000156 |      +1.10e-04 | -9.63e-03 | -2.12e-04 | **+5.73e-02** | -2.50e-03 | +2.43e-02 | +4.20e-02 |
|   0.0002 |      +1.04e-04 | -1.11e-02 | -1.96e-03 |     +6.26e-02 | -6.29e-04 | +2.56e-02 | +4.13e-02 |
|   0.0005 |      +4.73e-05 | -1.56e-02 | -9.80e-03 |     +6.08e-02 | +8.70e-04 | +1.87e-03 | +7.07e-02 |
|    0.001 |      -1.23e-04 | -2.00e-02 | -1.69e-02 |     +5.96e-02 | -2.86e-02 | -2.00e-02 | +8.74e-02 |
|   0.0025 |      -2.81e-04 | -2.38e-02 | -2.44e-02 |     +2.74e-02 | -4.43e-02 | +7.62e-04 | +1.09e-01 |

- **重要発見**: **v 凍結でも c_kon1, c_kon6p が正の符号 (+5.7e-2 から +1.1e-1)**。audit-v1b §3-10「full-batch でも v 凍結でも η/8 でも分岐は残る——決定論的な一次の効果」から、**v 凍結 SGD には T_1 (一次 refit) が残る**。→ SGD - GD の差でないと T_5 は isolate できない (audit-v1b §3-12 の定義通り)。
- c_stayer (pure T_4 減算後) の log-log 傾き = 0.33 → 理論 η^1 と大きく異なる。これは stayer 群にも T_1 が残る（跨いだ後 T=10⁴ の間に kon が変わる unit）ため。
- **Step R 単独では c(η) 直測できず**。v 凍結 GD の追加走行が必要 (要 chat 判断)。

**Step Q' の c_kon1_ratio との比較 (v 生存 vs v 凍結)**:

|        η | Q' c_kon1_ratio | R c_kon1 (v 凍結) |    比 |
| -------: | --------------: | --------------: | ---: |
| 0.000156 |         +0.1336 |       +5.73e-02 | 0.43 |
|   0.0025 |         +0.1195 |       +2.74e-02 | 0.23 |

v 凍結で c_kon1 が減る (T_1/Y_i 部分が isolate されている) が、まだ有意な T_1 が残る。

### Step T — T_0 の (k_on, z̄) joint 分布

**手法**: `step_T_T0_joint.py`。session19 の `mt_U1_bareK1_v2_lr*.npz` から末尾窓 (task 200-260) で per-task per-unit の kick_i + offset_i を 5 η × 22 zbar_bin × 5 kon 群で集計。走ゼロ。

**主要所見**:

**kon_pre=0 群の T_0 mean by zbar_bin** (η=0.000156 例、全 η で類似):
| zbar_center |         T_0 mean |
| :---------: | ---------------: |
|    -7.75    |           +0.092 |
|    -6.25    |           +0.020 |
|    -5.25    |           -0.009 |
|    -3.25    |           -0.059 |
|    -1.75    | -0.095 to -0.210 |

- **kon_pre=0 T_0 mean が zbar 深部で +0.09、shallow で -0.20** — 系統的に zbar 依存 (以前 §9-4 で仮定していた +0.019 は全 zbar 統合平均だった)。
- kon_pre≥1 群では T_0 mean が全体的に負 (-0.02〜-0.17) — crosser で kick が下向き。
- v3f の失敗 (per-unit fixed T_0) の根本原因を確定: **T_0 は zbar_pre と kon_pre の両方に依存する状態変数**。

**crosser 群の kon 別 T_0 mean**:

| kon 群  | η=0.000156 | η=0.0025 | 変化   |
| ------ | ---------- | -------- | ---- |
| kon0   | +0.002     | -0.005   | ほぼ 0 |
| kon1   | -0.101     | -0.152   | 増加   |
| kon2   | -0.095     | -0.166   | 増加   |
| kon3_5 | -0.074     | -0.080   | ほぼ一定 |
| kon6p  | -0.024     | -0.155   | 増加   |

出力: `step_T_T0_joint_distribution.npz` (T0_mean/std/count/skew/kurt の 5 η × 22 zbar_bin × 5 kon_group), `step_T_report.md`。

### Step U — 500 タスク拡張 & 定常性判定

**手法**: `mtM_500task.py` で session19 mtM_v2.py を base に ntask=500 で 5 η 再走。各 η ~ 235 秒 × 5 (4 並列) → 実 walltime 7 分。段 0 check: session19 mt_v2 の task 0-260 と一致 (diff_kon=0, diff_zbar=0.00e+00) ✓。

**5 窓 zbar_width の時系列**:

|        η | W1 (200-260) | W2 (261-320) | W3 (321-380) | W4 (381-440) | W5 (441-500) | ΔW/W1 |
| -------: | -----------: | -----------: | -----------: | -----------: | -----------: | ----: |
| 0.000156 |        6.735 |        6.944 |        7.421 |        7.460 |    **7.471** |  +11% |
|   0.0002 |        7.152 |        7.051 |        7.461 |        7.610 |        7.453 |   +4% |
|   0.0005 |        6.719 |        6.695 |        6.986 |        7.010 |        7.023 |   +5% |
|    0.001 |        6.365 |        6.319 |        6.308 |        5.693 |        6.221 |   -2% |
|   0.0025 |        4.773 |        5.475 |        5.630 |        4.896 |        4.597 |   -4% |

**Peak η per window**:
- W1: 0.0002 (7.15) — §9-4 と一致
- W2〜W4: 0.0002 (7.05→7.46→7.61)
- **W5: 0.000156 (7.47)** — peak が下 η 側に移動！

**Spearman(zbar_width, α_ref) の窓別変化**:
| Window | Spearman ρ |         p |
| ------ | ---------: | --------: |
| W1     |     +0.900 |     0.037 |
| W2     |     +0.900 |     0.037 |
| W3     |     +0.900 |     0.037 |
| W4     |     +0.900 |     0.037 |
| **W5** | **+0.700** | **0.188** |

**判定 (相対変動 (max-min)/min)**:
- η=0.000156: 0.110 (軽度過渡)
- η=0.0002: 0.079 (定常)
- η=0.0005: 0.049 (定常)
- η=0.001: 0.118 (軽度過渡)
- η=0.0025: 0.225 (軽度過渡)

**総合判定: 中低 η (0.000156) で軽度過渡・500 タスクでも peak がまだ育っている**。§9-4 の着地点 A 判定基準 (peak η=0.0002・width 7.37) は W1 では OK だが、**W5 で peak が η=0.000156 に移動・Spearman +0.700 に低下**。これは:

- 260 タスクでの peak η=0.0002 は **過渡的な現象**
- 定常状態では peak が更に低 η 側 (or 消失) に向かう可能性
- **着地点 A 判定基準そのものが 260 タスクの limit に依存**

**N_alive**:
- η=0.000156: 17.3 → 15.9 (減少 8%)
- η=0.0025: 5.7 → 4.6 (減少 20%)
→ N_alive は η と共に減少・時間と共にゆるやかに減少。h(u) も η と共に上昇 (0.14→0.34)、時間発展はほぼ一定 (定常)。

### Step V — T_1 飽和形理論式の検証

**手法**: `step_V_T1_theory.py`。session19 `step_Q_sf_sweep_lr*.npz` の kp1 unit (kon_pre=0 & kon0=1) に対して、audit-v1b §3-10 の `T_1 = -0.45 · v_i · <ζ, m⊙φ'_i>` を計算。走ゼロ。

**近似**: ζ ≈ δ' (時間発展を無視した 0 次近似)。m_r = row-mean of K/32 matrix (K = Xc Xc^T)。 φ'_{i,r} = 1 for z_post > 0, α=0.03 else。sat = 0.45。

**主要結果**:

|        η | kp1 n |   corr |  slope |     R² | mean_theo | mean_meas | Y_residual | kp2 n |   corr |  slope |
| -------: | ----: | -----: | -----: | -----: | --------: | --------: | ---------: | ----: | -----: | -----: |
| 0.000156 |  1101 | +0.535 | +0.687 | +0.287 |   -0.0727 |   +0.0855 |    +0.1582 |    57 | +0.610 | +0.827 |
|   0.0002 |  1101 | +0.517 | +0.664 | +0.267 |   -0.0727 |   +0.0885 |    +0.1613 |    57 | +0.590 | +0.799 |
|   0.0005 |  1101 | +0.462 | +0.601 | +0.213 |   -0.0727 |   +0.1047 |    +0.1774 |    57 | +0.485 | +0.680 |
|    0.001 |  1101 | +0.440 | +0.641 | +0.194 |   -0.0727 |   +0.1273 |    +0.2001 |    57 | +0.436 | +0.684 |
|   0.0025 |  1101 | +0.421 | +0.688 | +0.177 |   -0.0727 |   +0.1271 |    +0.1998 |    57 | +0.402 | +0.719 |

- **corr = 0.42-0.54** (LRoff0 の 0.55-0.68 より低い・LRa0p03 の a=0.03 で phi' の飽和が起こる可能性)
- **slope = 0.60-0.69** (audit-v1b の LRoff0 実測 0.42-0.48 の飽和 factor より **30-50% 高い**)
- **mean_measured が +0.09-0.13 と正 (上向き)** に対し、mean_theory は -0.07 (下向き)。→ **Y_i の残差平均 +0.16-0.20 と非常に大きい**。
- **T_5 減算過小の疑い**: T_5 の理論値 c=0.107η を使ったが、実測 T_5/(v²n_band) ratio (session19 Step Q kon1=0.13) より小さい。真の T_5 が大きければ measured から引かれて theory (負) に近づく。
- kp2 群で corr がやや高い (0.40-0.61)。跨ぎ点数が増えると T_1 の signal も増える。

**判定条件**:
- corr > 0.5 → η=0.000156, 0.0002 のみ達成
- slope 0.45 近傍 → slope 0.6-0.7 で **30-50% 過大** (LRoff0 と異なる飽和)
- Y_i 残差 < 0.02 → 0.16-0.20 で **10 倍過大**

→ **単純化した T_1 = -0.45 v_i <δ', m⊙φ'_i> 式では LRa0p03 の kp1 群を十分に説明できない**。真の T_1 の伝播 (ζ = F(K)δ' の F の具体化) と T_5 の正確な減算が必要。

### Step W — v3g 完全理論駆動 simulation

**手法**: `v3g_full_theoretical.py`。N_UNITS=1000 × N_TASKS=260 × N_SEEDS=10。

**モデル要素**:
- κ(η): Step Q' 直測
- c(η): audit-v1b 理論 0.107η (Step R は T_1 汚染で使えず)
- T_0(kon, zbar): Step T の joint 分布サンプル (Gaussian per cell, 5 未満は kon 群 fallback)
- alive 群 (kon≥1): STEP_C_TABLE (session19 Step C の kp 群別 Δz̄ 全体) を直接加算
- dead 群 (kon=0): T_0(kon=0, zbar) + T_4 + T_5 の 3 項式駆動
- kon 遷移: session19 mt_v2 (task 100-260) の Markov chain
- dead→alive kick: +0.52 (session19 Step C dead2alive_kick 実測)

**主要結果 (末尾窓 task 201-260)**:

|          η |  v3g width |   ± σ | v3g zbar_med | v3g N_alive | §9-4 width |  α_ref |
| ---------: | ---------: | ----: | -----------: | ----------: | ---------: | -----: |
|   0.000156 |      8.850 | 0.491 |       -6.111 |       184.0 |       6.93 | +0.389 |
|     0.0002 |      9.893 | 0.508 |       -6.244 |       176.8 |       7.37 | +0.607 |
| **0.0005** | **10.728** | 0.680 |       -6.356 |       150.1 |       7.37 | +0.540 |
|      0.001 |     10.001 | 0.667 |       -6.528 |       105.9 |       6.15 | +0.186 |
|     0.0025 |      9.023 | 0.822 |       -6.531 |        67.0 |       5.13 | -1.540 |

**着地点 A 判定基準**:
1. Peak position η=0.0005 → **OK** (実測 range [0.0002, 0.0005] 内)
2. Peak value 10.73 vs 7.37 → **× 46% 過大**
3. Spearman(v3g_width, α_ref) = +0.800 → **× (0.9 未達)**

**未達の主因**:
- v3g zbar_med -6.1〜-6.5 で **実測 -2.7〜-3.6 より 2 倍深い** → alive 群の Δz̄ を STEP_C_TABLE で毎タスク加算する設計が **深く沈み続ける**
- STEP_C_TABLE は「alive 群の task 単位 Δz̄ 平均」であり、これを alive 群の全 unit に加算するのは物理的に不正確 (task 単位 pool は unit の生死交代を含む)
- κ(η) の Step Q' 中心値が SNR 不足で真値と乖離 (η=0.001 で 2.4e-5 vs LRoff0 予想 5e-5)
- T_1+Y_i の Step V 残差が示唆する Y_i の追加寄与が未モデル化

---

## 2. 数値の妥当性のセルフチェック

### Q1: Step Q' の κ(η=0.0025) の桁

- session19: 2.71e-4 CI [-7e-5, +6.0e-4]
- Step Q': **6.09e-4 CI [3.8e-4, 8.4e-4]** — CI が 0 を除外
- session19 の中心値 2.7e-4 は 今回の CI 下限に近い → session19 の中心値は 「T=10⁴ で n_band=0 stayer 継続の unit」に依存し、T 増加で pure T_4 unit が変わる可能性
- **T 依存性の chat 側検証を推奨**

### Q2: Step V の Y_i 残差 +0.16-0.20 の起源

- 実測 T_1+Y_i mean = +0.10-0.13 (**正・上向き**)
- session19 Step C の kp1 alive 群 Δz̄ mean は -0.11-0.31 (**負・下向き**)
- 矛盾: 同じ kp1 unit 群でも kick 直後 (Step V) と task 単位 (Step C) で符号が逆
- 説明候補:
  - Step V は kon_pre=0 & kon0=1 の unit (flip 直後 alive) で、SGD 前の状態変化を見ている
  - Step C は tasks 201-260 の alive 群 (継続 alive)、SGD 中の全 drift を含む
  - → 2 つは別の unit プールを見ている

### Q3: Step T T_0 mean の zbar 依存

- zbar 深部 (-7.75) で T_0 mean = +0.09 → kick の "浮力"
- zbar 浅部 (-1.75) で T_0 mean = -0.10〜-0.21 → kick の "沈下"
- これは §9-4 で仮定していた「T_0 は η 独立の geometric quantity ≈ +0.019」の平均値であり、**per-unit で見ると zbar 状態依存**
- **v3g/v3f で T_0 = fixed geometric mean にする limit は破綻**

---

## 3. 3 判定基準の到達度と Type A/B

**Type**: 不明 (Step P で B と確定・session20 では Kahan 監査していない・base 前提 f64 no-Kahan)

**Landing A 判定**:
|          基準           |          目標          |  実測 (v3g)  |    判定    |
| :-------------------: | :------------------: | :--------: | :------: |
|     Peak position     | η ∈ [0.0002, 0.0005] | η = 0.0005 |  **OK**  |
|      Peak value       |  zbar_width ≈ 7.37   |   10.73    | × 46% 過大 |
| Spearman(pred, α_ref) |      +0.9〜+1.0       |   +0.800   |   × 未達   |

→ **着地点 A は 3 判定基準のうち 1 つのみ達成**。session19 v3e (Peak η=0.0002, width=7.40, Spearman +0.900) を超えていない。

**§9-4 実測との Spearman**:
- W1 (200-260, session19 の default): +0.900
- **W5 (441-500): +0.700** ← 500 タスクで基準が緩む

---

## 4. Chat に確認したい点（重要順）

### A. Step Q' の T 依存 κ の再現性
- **η=0.0025 で 中心値が session19 の 2.7e-4 → Step Q' の 6.1e-4 に 2.3 倍増加**
- T=10⁴ → 3×10⁴ で n_band=0 stayer 継続条件が破れやすい可能性
- → chat 側で T=10⁴, 3×10⁴, 10⁵ の 3 点比較を推奨

### B. Step V の Y_i 残差 +0.16-0.20 の理論的解釈
- Step V mean_measured (+0.10-0.13) は session19 Step C mean (-0.11-0.31) と符号逆
- kp1 群を kon_pre=0 & kon0=1 で見るか、kon_pre=0 & 継続 alive で見るかで別のプール
- audit-v1b §3-4 の Y_i (井戸・押し) 実装式 (m_bar/2 [...] の降下) を LRa0p03 で数値化する必要

### C. v 凍結でも残る T_1 の isolate 手法
- Step R では v 凍結 SGD で c_kon1 = +5.7e-2 (正の符号) の異常
- 真の T_5 isolate には v 凍結 GD (full-batch) - v 凍結 SGD の差を取る必要
- → v 凍結 GD の追加走行の必要性を chat で判断

### D. Step T の T_0 zbar 依存を v3g に組み込む方法
- 現状の v3g は Step T の joint 分布から Gaussian サンプル
- しかし zbar 分布が実測より深く伸びる → T_0 sampling で "shallow 側の bin" の pull-back が不足
- alive/dead 遷移の zbar shift (+0.52, -0.35 対称) が不正確な可能性 (session19 で -0.35 未実測)

### E. Step U で W5 に peak が η=0.000156 へ移動した意味
- 260 タスクでの peak η=0.0002 が過渡的
- 定常では peak が下 η 側にシフト → **§9-4 の judgment 基準 (peak η=0.0002, width=7.37) の解釈を再検討**
- 中低 η で更に長い T (1000 タスク?) 走らせて peak 移動を確認するべきか

### F. Step W v3g の zbar_med が実測より 2 倍深い問題
- alive 群 Δz̄ を STEP_C_TABLE で加算する設計は「task 単位 pool」を「unit 単位 drift」と混同
- 正しくは T_0(kon, zbar) + T_1(kon, zbar) + T_4 + T_5 の per-unit 加算
- Step T の T_0 と Step V の T_1 を組み合わせて v3h を chat 側で構築

---

## 5. 全 output ファイル一覧

`session20_out/` 直下:

**Step Q' 関連**:
- `sf_sweep_plus.py` (script: session20_scripts/)
- `step_Q_prime_sf_sweep_lr{0156,02,05,10,25}.npz` (5 files, 各 ~10 MB, 450 chain × T=3e4)
- `step_Q_prime_kappa_5point.csv`
- `step_Q_prime_report.md`
- `step_Q_prime_analyze.log`, `step_Q_prime_sf_sweep_*.log`

**Step R 関連**:
- `sf_vfrozen.py`, `sf_vfrozen_analyze.py` (scripts)
- `step_R_sf_vfrozen_lr{0156,02,05,10,25}.npz` (5 files, 各 ~3.4 MB)
- `step_R_c_vfrozen_5point.csv`
- `step_R_report.md`
- `step_R_analyze.log`, `step_R_sf_vfrozen_*.log`

**Step T 関連**:
- `step_T_T0_joint.py` (script)
- `step_T_T0_joint_distribution.npz`
- `step_T_report.md`
- `step_T_T0_joint.log`

**Step U 関連**:
- `mtM_500task.py`, `step_U_stationarity.py` (scripts)
- `mt_U1_bareK1_500tasks_v2_lr{0156,02,05,10,25}.npz` (5 files, 各 ~18 MB, 500 タスク)
- `step_U_5window_stats.csv`
- `step_U_report.md`
- `step_U_analyze.log`, `mtM_500task_*.log`

**Step V 関連**:
- `step_V_T1_theory.py` (script)
- `step_V_T1_verification.csv`
- `step_V_T1_verification.md`
- `step_V_analyze.log`

**Step W 関連**:
- `v3g_full_theoretical.py` (script)
- `step_W_v3g_prediction.csv`
- `step_W_v3g_report.md`
- `step_W_analyze.log`

**Meta**:
- `report.md` (本ファイル・chat が最初に読む)

---

## 6. 作業タイムラインと計算コスト

|    Step    | 実施                                                                     |      所要時間 |
| :--------: | ---------------------------------------------------------------------- | --------: |
|  環境確認・段 0  | sf_s0.py で LRa0p03 検算                                                  |        数秒 |
|     Q'     | sf_sweep_plus 5 η × 450 chain × T=3e4 (並列)                             |      ~2 分 |
| Q' analyze | sf_analyze_plus.py                                                     |      10 秒 |
|     R      | sf_vfrozen 5 η × 150 chain × T=1e4 (並列)                                |      ~5 秒 |
| R analyze  | sf_vfrozen_analyze.py                                                  |        数秒 |
|     T      | step_T_T0_joint (走ゼロ)                                                  |      10 秒 |
|     U      | mtM_500task 5 η × 500 タスク × T=1e4 (並列)                                 |      ~5 分 |
| U analyze  | step_U_stationarity                                                    |        数秒 |
|     V      | step_V_T1_theory (走ゼロ)                                                 |       5 秒 |
|     W      | v3g_full_theoretical (Monte Carlo・N_units=1000×N_tasks=260×N_seeds=10) |       5 秒 |
|     合計     |                                                                        | **~10 分** |

CPU: single-thread numpy einsum。想定 (3-4 時間) より大幅に短縮 (5 η を並列で走らせた効果)。

---

## 7. 制約遵守

- ✓ peer main ブランチ・teacher ブランチ・obsidian-research・teacher_out に触っていない
- ✓ 30_conjecture ノート本文を更新していない（達成判定は chat）
- ✓ Research Vault (`~/project/Research_Vault/`) は read only で使用
- ✓ GitHub からの取得 (lop_update 等) はしていない
- ✓ `session20_scripts/` の新規 script のみ作成・既存 (session19_*) は上書きしていない
- ✓ 予期しない結果 (Step Q' CI 幅未達・Step R T_1 汚染・Step W zbar_med 深すぎ・Step U W5 peak 移動) は §4 で明示
- ✓ arm mismatch guard: sf_sweep_plus.py と sf_vfrozen.py で act='leaky_relu' かつ alpha=0.03 を assert
- ✓ 段 0 check: sf_s0 (LRa0p03 検算 PASS)、Step U の 500 タスク版が session19 mt_v2 の task 0-260 と完全一致 (diff=0)
- ✓ Kahan は不要 (session19 Step P で Type B 確定)

---

## 8. 次 chat session への引き継ぎ

1. まず本 `session20_out/report.md` を読む
2. 数値の妥当性を検証:
   - Step Q' 中心値 (κ_batch3) の一貫性 vs bootstrap CI 幅の乖離
   - Step U W1 vs W5 の peak shift (η=0.0002 → η=0.000156)
   - Step V の Y_i 残差 +0.16-0.20 の物理起源
   - Step W の zbar_med -6.1〜-6.5 の深すぎ問題
3. **v3g の改良方針 (v3h)**:
   - alive 群 Δz̄ = T_0(kon, zbar) + T_1(kp 群別) + T_4 + T_5 の per-unit 完全 4 項式
   - T_1 は Step V の corr 実測を使って kp 群別に scaled version
   - alive→dead 遷移で zbar shift を session19 mt_v2 から実測
4. **v 凍結 GD 追加走行の要否 (Step R 続き)** を判断:
   - もし必要なら 5 η × 150 chain × T=1e4・full-batch で 30 分程度
5. **§9-4 判定基準の再解釈**: peak η が過渡か定常かは 500 タスクだけでは決着できず
6. handoff v21 の起票（着地点 A 未達・v3g の 3 問題を継続課題として明記）
