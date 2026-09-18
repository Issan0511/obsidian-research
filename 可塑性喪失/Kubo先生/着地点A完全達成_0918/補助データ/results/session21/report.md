# Session 21 report — Landing A alive branch 理論的閉形式化

- 起票: 2026-09-18 (Chat 第 20 回)
- 作業者: Claude Code
- 作業 dir: `/home/kubo/project/Nakatsuka/claude/hole1_scripts/session21_*/`

## 総合判定

| Step | Status        | 発見                                                                      |
| ---- | ------------- | ----------------------------------------------------------------------- |
| A    | **SUCCESS**   | mtM_v3.py 完成・5 arm × 250 tasks 走行完了・段 0 check bit-exact PASS            |
| B    | **SKIPPED**   | 時間不足で GD 変種未走行 (詳細は下記)                                                  |
| C    | **SUCCESS**   | T_1 theory per-event 計算 (0-th order operator scale ζ ≈ (2ηT/32)·δ')     |
| D    | **SUCCESS**   | Y_i per-event 抽出完了                                                      |
| E    | **SUCCESS** ★ | **Y_i = c(η) · v · Σ_{r∈on} δ'_r の閉形式発見**  (R² = 0.79-0.99・c ∝ η^{1.0}) |
| F    | **SUCCESS**   | Markov 遷移確率 5 arm 完了・§3-11 の LRoff0 テーブル LRa0p03 版取得                    |
| G    | **PARTIAL**   | Model M4 で closed form + Markov を統合するも state-conditional R が要件          |

## 中核発見: **Y_i の閉形式**

**Y_i = c(η) · v_i · Σ_{r∈on(i)} δ'_r**

- **c(η) ≈ (6172 – 9177) · η**  (log-log 指数 1.01-1.05・ほぼ **η^{1.0}**)
- R² per (kp_group, η):
  - kp1: R² = 0.79 – 0.89
  - kp2: R² = 0.90 – 0.96
  - kp3-5: R² = 0.95 – 0.99
  - kp6+: **R² = 0.994 – 0.998**

**物理解釈**: 跨いだユニット i の on-supports (φ' = 1) では、SGD が per-step で
`Δz_i,r ≈ -2η · v_i · d_r · (x_r · x_r_t)` で更新される。r_t が on-supports を hit する確率
は n_on/32・T=10000 hit で平均。これを合計すると:

`Δz̄_i,cross ≈ (2ηT/32) · v_i · <m>_on · Σ_{r∈on} δ'_r`

`c(η) = (2ηT/32) · <m>_on · flatness_factor` で、実測 c ≈ 6200 · η, `2T/32 · <m>_on ≈ 625 · 3.5 = 2200` なので、
factor ~3× (gate 応答飽和と m の on-support 局在化)。

**audit-v1b §3-10 との整合**: audit の 70% predictor `sign(v · Σ_{r∈on} δ'_r)` は本形式の
sign 部分に相当。本発見は **magnitude と R² を桁で改善** (form iv sign-only は R² ≈ 0.5、
form v magnitude を含めて R² ≈ 0.99)。

## Step ごとの詳細

### Step A: mtM_v3.py と 5 arm 走行

- `session21_scripts/mtM_v3.py` を作成 (mtM_v2 継承 + δ' + z_kick_full + n_active + kp_hist)
- 5 arm × 250 tasks 走行完了 (総 walltime ~470s)
- 各 arm の npz サイズ ~ 38MB (z_kick_full が主)

**段 0 check (lr0156)**: v3 の全 field が session20 v2 500-task npz と bit-exact 一致
(max|diff|=0.0 for zbar, kon, kon_kick, loss, wnorm, zmax, nband, zbar_kick)。
seed_rng の順序不変性を検証。

### Step B: 4 変種分解 — SKIPPED (時間不足)

script `mtM_v3_variants.py` 作成完了。GD (full-batch) は SGD の 10-20× コストのため、
5 arm × 250 tasks × 2 variants (GD, GD_vfrozen) は数時間を要する見積り。

**代替情報源**: Step D で使う T_5_theory は audit-v1b §3-12 の閉形式 (per-unit-5term §1-1)
から直接計算。Step B の変種分解による直接検証は future work。

### Step C: T_1 theory per-event 計算

閉形式: `T_1_i(t) = -(2ηT/32) · v_i · Σ_r m_r · δ'_r · φ'_{i,r}`
- ζ = ℱ(𝒦)δ' の 0-th order (A^t ≈ I): scale = 2ηT/32
- m_r = tilde_x_r · tilde_μ = n(1-2g) + 15g² + (0.5-g)(f_r - 5g)  (f_r = FREE[r].sum())
- φ'_{i,r} = 1 if z_kick_i,r > 0 else a = 0.03 (LRa0p03 leaky slope)

**T_1 magnitude 問題**: 0-th order scale (2ηT/32) は η と共に線形増加 (0.098 → 1.56)。
実測 |Δz̄| ≈ 0.3 だが T_1_theory は η=0.0025 で median|·| = 9.4 と過大。
→ T_1_theory と Y_i が near-cancellation で R (真の残差) は小さい。

### Step D: Y_i per-event 抽出

R = Δz̄_meas - kick_i - offset_i - T_4_theory - T_5_theory  (per-event)
Y_i = R - T_1_theory

per-arm per-kp 集計:
- kp0: **Y_i ≈ 0**  (mean ± 0.001-0.09、大幅に有意でない — audit-v1b §3-4 の予言通り) ✓
- kp1: Y_i = +0.14 (lr0156) → +5.71 (lr25) — η と共に急増
- kp2: Y_i = +0.15 → +10.30 — 同じ

Y_i が T_1 と ほぼ逆符号で cancellation する構造。閉形式 fit の主目的。

### Step E: Y_i 関数形 fitting (中核)

6 関数形を per-arm per-kp で fit:

| Form                       | 説明                      | R² (kp6+ 代表) |
| -------------------------- | ----------------------- | ------------ |
| (i)   `v²`                 | 純 v²                    | 0.001        |
| (ii)  `\|v\|`              | 純 \|v\|                 | 0.001        |
| (iii) `v²·z_max_kick`      | v² · 着地点                | 0.002        |
| (iv)  `v²·sgn(v·Σδ'_on)`   | 符号予測子 (audit-v1b §3-10) | 0.44         |
| **(v)  `v·Σ_{r∈on} δ'_r`** | **本発見**                 | **0.998**    |
| (vi)  `v²·z̄_kick`         | v² · flip 直後 zbar       | 0.0005       |

**η 依存性** — form (v) のみ log-log で clean:

| kp    | slope@lr0156 | slope@lr02 | slope@lr05 | slope@lr10 | slope@lr25 | log-log 指数 | C = e^(intercept) |
| ----- | ------------ | ---------- | ---------- | ---------- | ---------- | ---------- | ----------------- |
| kp1   | 0.94         | 1.24       | 3.32       | 6.80       | 17.05      | **1.05**   | 9177              |
| kp2   | 0.94         | 1.21       | 3.25       | 6.63       | 16.46      | **1.04**   | 8427              |
| kp3-5 | 0.92         | 1.19       | 3.09       | 6.24       | 15.52      | **1.02**   | 7038              |
| kp6+  | 0.90         | 1.15       | 2.92       | 5.85       | 14.73      | **1.01**   | 6172              |

- c(η) = C · η with C ≈ 6000-9000
- 指数はほぼ 1.0 (0.99 - 1.05)
- kp6+ は最も clean (log-log R²=0.997)

### Step F: Markov 遷移確率

session20 500-task v2 npz から (kon_kick → kon_next) 遷移を per-η 集計。

**kp1 → 次 task 分布**:

| η        | → kp0 | → kp1 | → kp2 | → kp3+ |
| -------- | ----- | ----- | ----- | ------ |
| 0.000156 | 22.3% | 70.3% | 5.8%  | 1.7%   |
| 0.0002   | 26.2% | 65.0% | 6.5%  | 2.2%   |
| 0.0005   | 34.2% | 55.1% | 6.6%  | 4.0%   |
| 0.001    | 40.7% | 50.1% | 5.4%  | 3.8%   |
| 0.0025   | 49.2% | 42.8% | 4.4%  | 3.6%   |

**audit-v1b §3-11 LRoff0 reference** (η=0.01): kp1 → kp0 が 37%, → kp≥3 が 13%。
LRa0p03 では η=0.001 の kp1→kp0 = 40.7% と LRoff0 の 37% がほぼ一致
(LRa0p03 の等価 η = a·η_LRa0p03·(a_LRoff0/a_LRa0p03)² スケール比較で ~ LRoff0 の 3-8 倍相当)。

**η 依存**: kp1 → kp0 は η の増加と共に単調に増加 (22.3% → 49.2%)。
高 η で "上がったユニットが戻される" 確率が増える → alive branch の維持は難しくなる。

### Step G: Model M4 alive branch 理論駆動化

**2 バリアント**を試行:

1. **M4-A (empirical R bootstrap + Markov)**: kp_kick を Step F の marginal から、R を empirical
   distribution per (η, kp_kick) からブートストラップ。
2. **M4-B (closed form: Y_i = c(η)·v·N(0, σ√n_on))**: 閉形式を素朴に IID sample した δ'_on で駆動。

**結果**:

| η        | 実測 (v2 npz) | v3i_joint (Chat) | M4-A | M4-B   | §9-4 目標  |
| -------- | ----------- | ---------------- | ---- | ------ | -------- |
| 0.000156 | 6.08        | 7.30             | 5.16 | 12.67  | 6.93     |
| 0.0002   | 6.09        | **7.40** ✓       | 4.00 | 21.58  | **7.37** |
| 0.0005   | 5.67        | 5.75             | 4.95 | 66.38  | 7.37     |
| 0.001    | 4.68        | 5.29             | 5.83 | 90.65  | 6.15     |
| 0.0025   | 3.48        | 2.81             | 6.06 | 170.10 | 5.13     |

**3 判定基準**:

- M4-A: Peak position NG (0.0025), Peak value OK (6.06), Spearman -1.0 → **部分達成**
- M4-B: 全て NG (発散) → **失敗**

**Landing A 判定**: **部分達成**。
- Y_i の closed form (**中核発見**) は確立
- ただし closed form の Model M4 統合には δ' の**状態依存**モデル(feedback loop)が必要
- v3i_joint (Chat) が Landing A を達成しているのは、R を state-conditional (v²・z̄・kon の bin) で
  サンプリングするため。Step G の unconditional bootstrap は state feedback が抜けている。

## 反証条件と次段階

### 判明した閉形式

**Y_i = c(η) · v_i · Σ_{r∈on(i)} δ'_r  with c(η) ≈ 7000 · η, R² = 0.79-0.99**

### 未解決課題

1. **c(η) の C₀ = 7000 の理論的説明** — (2T/32)·<m>_on = 2200 との factor 3× ずれ。gate 応答飽和項?
2. **δ'_r の tail 統計モデル** — Step F は kon 遷移だけ、δ' の magnitude 分布は未モデル化
3. **T_1 magnitude discrepancy** — 0-th order (2ηT/32) が高 η で過大。真の operator response
   ℱ(𝒦) の η-scaling を得る必要 (audit-v1b §3-9 の M(t) 漸化式で計算可)
4. **Landing A 完全達成のための Model M4 改良** — state-conditional R sampling を実装
   (v3e Chat 版と同等)

## 成果物一覧

- `session21_out/report.md`  ← 本ファイル
- `session21_out/mt_U1_bareK1_dprime_v3_lr{0156,02,05,10,25}.npz` — 5 arm × 250 tasks の
  δ'・z_kick・kick_i・offset_i 等 (~38 MB × 5)
- `session21_out/step_C_t1_theory_per_event.npz` — T_1 theory per-event (両 scale)
- `session21_out/step_D_y_per_event.npz` — Y_i, R, T_4/5_th per-event
- `session21_out/step_E_yi_functional_form.md` + `.json` — 関数形 fit 結果
- `session21_out/step_F_markov_transitions.csv` + `step_F_report.md` — Markov 遷移
- `session21_out/step_G_alive_branch_theory_driven.md` — Model M4 統合結果

## Log

- 2026-09-18 起票 (Chat 第 20 回)
- 2026-09-18 Step A-F 完了・Step G 部分完了。閉形式 Y_i 発見を報告。
