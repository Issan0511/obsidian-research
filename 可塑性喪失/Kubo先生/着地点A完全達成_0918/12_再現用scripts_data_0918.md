---
aliases:
  - 再現用 scripts
  - data manifest
  - session 20 scripts
  - session 21 scripts
  - Chat 分析 scripts
description: Landing A 完全達成の記録に使われた scripts と data の manifest、実際の Nakatsuka repo の script name、Chat container 側の再構築必要性を明示
---

# 再現用 scripts と data

親: [[00_概要と5判定基準_0918]] / 状態: **決着** (資料ノート・turn 8-a 訂正) / 更新: 2026-09-18

## 1. 目的

本ノートは Landing A 完全達成 ([[00_概要と5判定基準_0918]]) の記録に使われた scripts と data の manifest。実際の Nakatsuka repo (`/home/kubo/project/Nakatsuka/claude/hole1_scripts/`) の構造と、Chat container 側の再構築必要性を明示する。

**大きい `.npz` ファイル (合計 ~ 350 MB) は Obsidian vault にコピーせず、元の場所を reference のみで示す** (Kubo の指示による)。

## 2. 補助データフォルダの構造

```
可塑性喪失/Kubo先生/着地点A完全達成_0918/補助データ/
├── scripts/
│   ├── session21_scripts/     # Claude Code session 21 の全 scripts (実物コピー)
│   │   ├── mtM_v3.py                          # Step A: δ' 保存版シミュレータ
│   │   ├── mtM_v3_variants.py                 # Step B: 4 変種分解 (SKIP)
│   │   ├── run_step_A_all.sh                  # Step A shell
│   │   ├── run_step_B_variants.sh             # Step B shell (SKIP)
│   │   ├── step_C_t1_theory.py                # Step C: T_1 theory per-event
│   │   ├── step_D_yi_extract.py               # Step D: Y_i per-event 抽出
│   │   ├── step_E_yi_fit.py                   # Step E: 6 関数形 fit
│   │   ├── step_F_markov.py                   # Step F: Markov 遷移確率
│   │   └── step_G_model_m4_theory_driven.py   # Step G: Model M4-A / M4-B
│   ├── session20_scripts/     # Chat 第 20 回で使用した Claude Code scripts (実物コピー)
│   │   ├── mtM_500task.py                     # Step U: 500 tasks trajectory
│   │   ├── sf_analyze_plus.py                 # Step Q': κ analyze
│   │   ├── sf_sweep_plus.py                   # Step Q': κ sweep (450 chain × T=3e4)
│   │   ├── sf_vfrozen.py                      # Step R: v 凍結 SGD
│   │   ├── sf_vfrozen_analyze.py              # Step R: c analyze
│   │   ├── step_T_T0_joint.py                 # Step T: T_0 joint 分布
│   │   ├── step_U_stationarity.py             # Step U: 500 tasks 定常性判定
│   │   ├── step_V_T1_theory.py                # Step V: T_1 理論式検証
│   │   └── v3g_full_theoretical.py            # Step W: v3g 完全理論駆動 sim
│   └── chat_scripts_reconstruction/  # Chat container で第 20 回に実行した分析 (実物なし・再構築必要)
│       └── README_reconstruction.md  # 再構築の手順と Chat 第 20 回の分析内容
├── results/                   # session21_out/ と session20_out/ の md/csv/json (実物コピー)
│   ├── session21/
│   │   ├── report.md                          # Session 21 総まとめ
│   │   ├── step_E_yi_functional_form.md       # Step E report
│   │   ├── step_E_yi_fits.json                # Step E fit 結果 (5 arm × 6 form)
│   │   ├── step_F_markov_transitions.csv      # Step F 遷移確率
│   │   ├── step_F_report.md                   # Step F report
│   │   ├── step_G_alive_branch_theory_driven.md  # Step G report (M4-A/B)
│   │   └── logs/                              # 実行ログ (mtM_v3_*.log, step_C_log.txt, etc.)
│   └── session20/
│       ├── report.md                          # Session 20 総まとめ
│       ├── step_Q_prime_kappa_5point.csv      # Step Q' κ 5 点
│       ├── step_Q_prime_report.md             # Step Q' report
│       ├── step_R_c_vfrozen_5point.csv        # Step R c 5 点 (v 凍結)
│       ├── step_R_report.md                   # Step R report
│       ├── step_T_report.md                   # Step T T_0 joint report
│       ├── step_U_5window_stats.csv           # Step U 5 窓 zbar_width
│       ├── step_U_report.md                   # Step U 500 tasks 定常性 report
│       ├── step_V_T1_verification.csv         # Step V T_1 検証
│       ├── step_V_T1_verification.md          # Step V T_1 report
│       ├── step_W_v3g_prediction.csv          # Step W v3g 5 arm 予測
│       └── step_W_v3g_report.md               # Step W v3g report
└── references/               # 大きい npz は reference のみ
    └── large_data_reference.md   # 元の場所と data 構造の明記
```

**大きい `.npz` ファイル (Obsidian vault にコピーせず・元の場所を reference)**:
- `session21_out/mt_U1_bareK1_dprime_v3_lr*.npz` (5 files × ~ 36 MB = 180 MB)
- `session21_out/step_C_t1_theory_per_event.npz` (~ 41 MB)
- `session21_out/step_D_y_per_event.npz` (~ 46 MB)
- `session20_out/mt_U1_bareK1_500tasks_v2_lr*.npz` (5 files × ~ 18 MB = 87 MB)
- `session20_out/step_Q_prime_sf_sweep_lr*.npz` (5 files × ~ 10 MB = 49 MB)
- `session20_out/step_R_sf_vfrozen_lr*.npz` (5 files × ~ 3.3 MB = 16 MB)
- `session20_out/step_T_T0_joint_distribution.npz` (~ 22 KB・small のためコピー可)

**合計** (Obsidian vault にコピーする分):
- scripts: ~ 130 KB
- results (md/csv/json/log): ~ 200 KB
- **総計 ~ 330 KB** (Obsidian vault へ)

**元の場所に残す分** (reference のみ): ~ 420 MB

## 3. Claude Code session 21 scripts の役割

### 3.1 `mtM_v3.py` (Step A)

- **目的**: δ' per-event を保存する v3 版シミュレータ (session19 mtM_v2 継承 + δ' + z_kick_full + n_active + kp_hist)
- **入力**: 5M ckpt (seed 0-9)・$\eta$・$T_{\rm task} = 10^4$・$N_{\rm task} = 250$
- **出力**: `mt_U1_bareK1_dprime_v3_lr*.npz` (5 arm × 10 seed × 250 tasks × 100 unit × 32 支持点の δ', z, kon)
- **段 0 check**: v3 の全 field が session 20 v2 500-tasks npz と bit-exact 一致 (max|diff|=0.0 for zbar, kon, kon_kick, loss, wnorm, zmax, nband, zbar_kick)
- **実行時間**: 1 arm あたり 30-60 分 (10 seed × 250 tasks × 10⁴ step・~ 470s total)

### 3.2 `mtM_v3_variants.py` (Step B・SKIP)

- **目的**: 4 変種分解 (GD full-batch と GD_vfrozen の 2 variant)
- **状態**: 時間不足で走行 SKIP・script は作成完了
- **代替**: Step D の T_5_theory は audit-v1b §3-12 の閉形式から直接計算

### 3.3 `step_C_t1_theory.py` (Step C)

- **目的**: $T_1^{\rm true}$ を演算子応答 $\mathcal F(\mathcal K) \delta'$ から per-event で計算
- **閉形式**: $T_{1,i}(t) = -(2\eta T / 32) \cdot v_i \cdot \sum_r m_r \cdot \delta'_r \cdot \varphi'_{i,r}$
  - $\zeta = \mathcal F(\mathcal K) \delta'$ の 0 次近似 ($A^t \approx I$): scale = $2\eta T / 32$
  - $m_r = \tilde x_r \cdot \tilde\mu$
  - $\varphi'_{i,r} = 1$ if $z_{\rm kick, i, r} > 0$ else $a = 0.03$
- **入力**: `mt_U1_bareK1_dprime_v3_lr*.npz`
- **出力**: `step_C_t1_theory_per_event.npz` (per-event $T_1^{\rm true}$)

### 3.4 `step_D_yi_extract.py` (Step D)

- **目的**: $Y_i^{\rm empirical} = \Delta \bar z_i^{\rm actual} - (\text{kick}_i + \text{offset}_i + T_{4,\rm theory} + T_{5,\rm theory}) - T_{1,\rm theory}$
- **入力**: `mt_U1_bareK1_dprime_v3_lr*.npz`, `step_C_t1_theory_per_event.npz`
- **出力**: `step_D_y_per_event.npz` (per-event $Y_i, R, T_{4/5, \rm theory}$)

### 3.5 `step_E_yi_fit.py` (Step E) ★ 中核

- **目的**: 6 関数形 (i)-(vi) の per-arm per-kp 群 R² 比較 (詳細 [[08_Y_i閉形式_step_E_0918]])
- **入力**: `step_D_y_per_event.npz`
- **出力**: `step_E_yi_fits.json` (5 arm × 6 form × 5 kp の fit 結果), `step_E_yi_functional_form.md`
- **発見**: **form (v) $Y_i = c(\eta) \cdot v_i \cdot \sum_{r \in \mathrm{on}} \delta'_r$ の圧勝** (kp6+ で R² = 0.994-0.998)

### 3.6 `step_F_markov.py` (Step F)

- **目的**: Markov 遷移確率 $p(k^{\rm next} \mid k^{\rm kick}, \eta)$ の抽出
- **入力**: `mt_U1_bareK1_500tasks_v2_lr*.npz` (session 20 v2 の 500 tasks trajectory)
- **出力**: `step_F_markov_transitions.csv`, `step_F_report.md`

### 3.7 `step_G_model_m4_theory_driven.py` (Step G)

- **目的**: Model M4-A (empirical R bootstrap + Markov) と M4-B (closed form Y_i + IID Gaussian δ') の 260 tasks シミュレーション (詳細 [[11_Model_M4-B発散の3大欠陥_0918]])
- **入力**: 5M ckpt state, Step Q' の κ, Step R の c, Step T の T_0, Step F の Markov 遷移
- **出力**: `step_G_alive_branch_theory_driven.md`

## 4. Claude Code session 20 scripts の役割 (Chat 第 20 回で使用)

Session 20 は Landing A の判定達成の前段階 (Chat 第 19 回で session 19 の v3e で判定達成後・第 20 回で session 20 で 500 tasks 定常性検証と v3g 完全理論駆動化を試行)。

### 4.1 `mtM_500task.py` (Step U)

- **目的**: mtM_v2 を base に $N_{\rm task} = 500$ で 5 arm 再走 (session 19 の 260 tasks 版を拡張)
- **入力**: 5M ckpt (seed 0-9)
- **出力**: `mt_U1_bareK1_500tasks_v2_lr*.npz` (~ 18 MB × 5)
- **段 0 check**: session 19 mt_v2 の task 0-260 と bit-exact 一致 (diff_kon=0, diff_zbar=0.00e+00) ✓
- **実行時間**: 各 η ~ 235 秒 × 5 (4 並列) → 実 walltime 7 分

### 4.2 `sf_sweep_plus.py`, `sf_analyze_plus.py` (Step Q')

- **目的**: LRa0p03 arm の $\kappa(\eta)$ SNR 向上直測
- **手法**: 3 noise batch × 10 seed × 15 flip = 450 chain・$T = 3 \times 10^4$
- **結果**: CI 幅目標 3e-5 は未達 (2.8e-4 - 4.6e-4)・η=0.0025 で中心値 6.09e-4・[3.8e-4, 8.4e-4] で 0 除外
- **出力**: `step_Q_prime_sf_sweep_lr*.npz`, `step_Q_prime_kappa_5point.csv`

### 4.3 `sf_vfrozen.py`, `sf_vfrozen_analyze.py` (Step R)

- **目的**: v 凍結 SGD で $c(\eta)$ 分離を試行
- **重要発見**: **v 凍結でも $T_1$ が残る** (audit-v1b §3-10) ため、alive 群では c 分離できず (c_kon1 が正の符号 +6e-2 と異常)
- **T_5 の isolate には v 凍結 GD (full-batch) 追加走行が必要** (要 chat 判断)
- **出力**: `step_R_sf_vfrozen_lr*.npz`, `step_R_c_vfrozen_5point.csv`

### 4.4 `step_T_T0_joint.py` (Step T)

- **目的**: $T_0$ の $(k_{\rm on}, \bar z)$ joint 分布抽出
- **重要発見**: **$k_{\rm on, pre} = 0$ 群で $T_0$ mean が $\bar z$ 依存**。$\bar z$ 深部 (-7.75) で +0.09、shallow (-1.75) で -0.20
- **意味**: v3f の失敗 (per-unit fixed $T_0$) の直接原因を確定 (**$T_0$ は状態依存**)
- **出力**: `step_T_T0_joint_distribution.npz`

### 4.5 `step_U_stationarity.py` (Step U analyze)

- **目的**: 5 窓 $\bar z_{\rm width}$ 時系列と Spearman の窓別変化
- **重要発見**: **W5 (441-500) で peak η が 0.0002 → 0.000156 に移動・Spearman +0.900 → +0.700 に低下**
- **意味**: **§9-4 の Landing A 判定基準は 260 tasks の過渡現象の可能性**
- **出力**: `step_U_5window_stats.csv`, `step_U_report.md`

### 4.6 `step_V_T1_theory.py` (Step V)

- **目的**: audit-v1b §3-10 の $T_1 = -0.45 \cdot v_i \cdot \langle \zeta, m \odot \varphi'_i \rangle$ (0 次近似 $\zeta \approx \delta'$) の検証
- **結果**: corr = 0.42-0.54 (LRoff0 の 0.55-0.68 より低い)・slope = 0.60-0.69・**$Y_i$ 残差平均 +0.16-0.20 と非常に大きい**
- **T_5 減算の過小疑い** (theory 0.107η が過小・真の T_5 が大きければ Y_i 残差が減る)
- **出力**: `step_V_T1_verification.csv`, `step_V_T1_verification.md`

### 4.7 `v3g_full_theoretical.py` (Step W)

- **目的**: $N_{\rm units} = 1000 \times N_{\rm tasks} = 260 \times N_{\rm seeds} = 10$ で v3g Monte Carlo 完全理論駆動シミュレーション
- **モデル要素**: κ (Step Q')・c (audit-v1b 0.107η)・T_0 (Step T joint)・STEP_C_TABLE (session 19 Step C の kp 群別 Δz̄・alive 群加算)・T_4・T_5・Markov (session 19 mt_v2 task 100-260)
- **結果**: peak η=0.0005 (OK・target [0.0002, 0.0005])・peak value 10.73 (target 7.37 の 46% 過大・NG)・Spearman +0.800 (target ≥ +0.9 未達・NG)
- **判定**: **着地点 A 3 判定基準のうち 1 つ (peak position) のみ達成**
- **未達の主因**: v3g の $\bar z_{\rm med} = -6.1 \sim -6.5$ で **実測 $-2.7 \sim -3.6$ より 2 倍深い** — alive 群 Δ$\bar z$ を STEP_C_TABLE で加算する設計は「task 単位 pool」を「unit 単位 drift」と混同
- **出力**: `step_W_v3g_prediction.csv`, `step_W_v3g_report.md`

## 5. Chat container で第 20 回に実行した分析 (実物なし)

Chat container はセッションごとにリセットされるため、第 20 回 (2026-09-18) に Chat container 内で生成された scripts (`/home/claude/*.py`) の **実物は残っていない**。

### 5.1 memory summary からの再構築必要性

Chat 第 20 回で以下の分析が実施された (memory summary より):

- **K spectrum 対角化**: $\mathcal K = X_c X_c^\top / 32$ の rank = 6・非零固有値 (bias mode $\lambda_{\max} = 9.29 = \|\tilde\mu\|^2$・free modes 0.25 × 4・混合 mode 0.208)
- **段 0 分析**: $Y_i$ の fitted slope $c(\eta)^{\rm fit}$ vs 理論 $(2\eta T / 32) \cdot \|\tilde\mu\|^2$ の 5 arm ratio (1.008 ± 0.009)
- **V-a 真の版**: $\Sigma_{XX} = 0.25 \cdot \mathrm{diag}(0_{15}, 1_5)$ の解析導出と数値検算
- **V-b 真の版**: σ 中央値変化の 5 arm 実測 (max +3.35%)
- **Term I / Term II 分解**: SGD の $\Delta \|w\|^2$ の Term I/II 分解・3 レジーム発見
- **v3i_joint 実装と 3 判定達成**: v3i の joint 分布 ($k_{\rm on\_kick}, \bar z_{\rm kick}$) 条件付けで Spearman +0.900 達成

### 5.2 再構築の手順

`chat_scripts_reconstruction/README_reconstruction.md` に、各分析の再構築手順を記述する (実装は Landing B の Step 0 で予定):

1. Nakatsuka repo の `session21_scripts/mtM_v3.py` を基点とする
2. 5M ckpt の初期状態から $\mathcal K$ を対角化する短い script を作成
3. Step E の $c(\eta)^{\rm fit}$ を使い、$\|\tilde\mu\|^2$ から ratio を計算
4. Term I/II 分解は session 21 の Step C/D の per-event 分解を elaborate

これらの分析結果は本ノート群 ([[02_V-a真の版_有界性_0918]] - [[10_Markov遷移確率_a二乗scaling_0918]]) に記録されているので、再構築は Landing B の作業として実施可能。

## 6. 実行環境要件

### 6.1 Python

- Python 3.10+
- NumPy 1.24+
- SciPy 1.11+ (spearmanr 用)
- pandas 2.0+ (CSV I/O)
- (optional) matplotlib 3.7+ (可視化)

### 6.2 データ

`/home/kubo/project/Nakatsuka/claude/hole1_scripts/` に既存 の以下ファイル:

- **5M ckpt**: `/home/kubo/project/Nakatsuka/data/act_sweep_hole1_0910_local/ckpts/LRa0p03_1216_step5000000.pt`
  (10 seed 分・net['W'], net['b'], net['v']・fs, rm, act, alpha)
- **v2 500 tasks trajectory**: `session20_out/mt_U1_bareK1_500tasks_v2_lr*.npz` (5 arm × ~18 MB)
  (500 tasks × 10 seed × 100 unit の zbar, kon, kick_i, offset_i, nband, v_final)
- **v3 250 tasks δ' 付き**: `session21_out/mt_U1_bareK1_dprime_v3_lr*.npz` (5 arm × ~ 36 MB)
  (250 tasks × 10 seed × 100 unit × 32 支持点の δ', z_kick_full)

### 6.3 メモリ

- $\mathcal K$ 対角化: 数百 KB
- 500 tasks trajectory の集計: 数百 MB (in-memory)
- Full analysis: 数 GB (5 arm 全体)

## 7. 実行手順 (Landing A の全結果再現)

### 7.1 手順の順序

1. **Step U (session 20)**: `mtM_500task.py` で 500 tasks trajectory 生成 (5 arm × 10 seed) → `mt_U1_bareK1_500tasks_v2_lr*.npz`
2. **Step Q' / Step R (session 20)**: `sf_sweep_plus.py`, `sf_vfrozen.py` で κ, c 5 点直測
3. **Step T (session 20)**: `step_T_T0_joint.py` で $T_0$ joint 分布抽出
4. **Step U analyze (session 20)**: `step_U_stationarity.py` で 5 窓 stationarity 判定
5. **Step V (session 20)**: `step_V_T1_theory.py` で $T_1$ 理論式検証
6. **Step W (session 20)**: `v3g_full_theoretical.py` で v3g Monte Carlo (完全理論駆動化・部分達成)
7. **Step A (session 21)**: `mtM_v3.py` で δ' 保存版 250 tasks 走行 → `mt_U1_bareK1_dprime_v3_lr*.npz`
8. **Step C (session 21)**: `step_C_t1_theory.py` で $T_1^{\rm true}$ per-event
9. **Step D (session 21)**: `step_D_yi_extract.py` で $Y_i^{\rm empirical}$ per-event
10. **Step E (session 21)**: `step_E_yi_fit.py` で 6 関数形 fit → form (v) 圧勝
11. **Step F (session 21)**: `step_F_markov.py` で Markov 遷移確率
12. **Step G (session 21)**: `step_G_model_m4_theory_driven.py` で M4-A/B 実装 (未達確認)
13. **Chat 分析 (第 20 回・container で実施)**: K spectrum 対角化・段 0 分析・V-a/V-b・Term I/II・v3i_joint (実物なし・Landing B で再構築)

### 7.2 実行時間の見積り

| Step                 | 実行時間                      |
| -------------------- | ------------------------- |
| Step Q'              | ~ 2 分                     |
| Step R               | ~ 5 秒                     |
| Step T               | 10 秒 (走行なし)               |
| Step U (mtM_500task) | ~ 5 分                     |
| Step U analyze       | 数秒                        |
| Step V               | 5 秒 (走行なし)                |
| Step W (v3g)         | 5 秒 (Monte Carlo)         |
| Step A (mtM_v3)      | 30-60 分 × 5 arm × 10 seed |
| Step B               | (SKIP)                    |
| Step C-F             | 各 5-30 分                  |
| Step G               | ~ 30 秒                    |
| **合計 (session 20)**  | ~ 10 分                    |
| **合計 (session 21)**  | ~ 10-20 時間                |

### 7.3 CPU

Single-thread NumPy einsum。session 20 は 5 arm 並列で walltime 短縮。

## 8. 大きい data の reference (Obsidian vault 外)

`references/large_data_reference.md` に以下の情報を記述する:

- 元の場所 (`/home/kubo/project/Nakatsuka/claude/hole1_scripts/session2*_out/*.npz`)
- 各 npz の shape と field 名 (zbar, kon, kick_i, δ' 等)
- 5M ckpt の場所と network 構造

これにより Obsidian vault にはコピーせず、必要時に元の場所から load 可能。

## 9. Provenance

- **source-result**: (本ノート自体が全 scripts と data の manifest)
- **source-commit**: 本ノート起票時の teacher branch head
- **verified-on**: 2026-09-18

## 10. Log

- 2026-09-18 起票 (初回・memory summary ベース・session 20 の script name が誤り)
- 2026-09-18 turn 8-a 訂正:
  - session 20 の scripts を実際の `/home/kubo/project/Nakatsuka/claude/hole1_scripts/session20_scripts/` の 9 files (mtM_500task.py, sf_analyze_plus.py, sf_sweep_plus.py, sf_vfrozen.py, sf_vfrozen_analyze.py, step_T_T0_joint.py, step_U_stationarity.py, step_V_T1_theory.py, v3g_full_theoretical.py) に修正
  - session 21 の scripts を実際の 9 files に修正 (元記述はほぼ正しかった)
  - Chat container の scripts は「実物なし・Landing B での再構築」と明示
  - 大きい npz (合計 ~ 420 MB) は Obsidian vault にコピーしない (元の場所を reference のみ)
  - Session 20 の Landing A 到達度 (v3g は 3 判定の 1 つのみ達成) を明示
  - Session 21 の Landing A 到達度 (Y_i 閉形式は確立・Model M4-A/B は未達) を明示
