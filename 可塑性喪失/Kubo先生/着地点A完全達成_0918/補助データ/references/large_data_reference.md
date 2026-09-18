---
name: large_data_reference
description: 着地点 A 完全達成の裏付けとなる元 npz・checkpoint の manifest。Vault にはサイズ問題でコピーせず、Nakatsuka repo の元 path を明記。
sources: [chat]
aliases: [補助データ元参照, npz manifest, session 19/20/21 元データ]
---

# 元 npz・checkpoint の manifest

**目的**: [[00_概要と5判定基準_0918]] 以降 14 ノートの数値の元 (npz・checkpoint) の在り処を、
中塚君が Nakatsuka repo にアクセスできない状況でも指せるようにする。

**Vault にコピーしない理由**: 合計 619.58 MB。 Vault 容量と git 履歴を圧迫する。
代わりに 補助データ/scripts/ に script 全数と 補助データ/results/ に text 出力 (md/csv/json) をコピー済み。
npz を実際に開く必要が生じたら、Kubo に scp 依頼するか、`~/project/Nakatsuka` の git repo 全体を共有依頼する。

**現在時点の作業ディレクトリ**: `/home/kubo/project/Nakatsuka/claude/hole1_scripts/`
(中塚君は Filesystem MCP でこの path を直接見られない。以下は「Kubo 側から見える path」)。

---

## Session 19 出力 (198.10 MB・49 files)

### 主要 npz

| file                                                                  |                    サイズ | 内容                                                                                                                     |
| --------------------------------------------------------------------- | ---------------------: | ---------------------------------------------------------------------------------------------------------------------- |
| `session19_out/mt_U1_bareK1_v2_lr{0156,02,05,10,25}.npz`              | 各 9.23 MB (計 45.98 MB) | 260 タスク mtM_v2 5 arm 完全 record (kon, zbar, kick_i, offset_i, v_final, nband, v, etc.)                                  |
| `session19_out/mt_U1_bareK1_{nokahan,kahan}_lr{0156,02,05,10,25}.npz` | 各 13.5 MB (計 135.5 MB) | Step P Kahan 監査用 (Type A/B 決着に使用・Type B 確定)                                                                            |
| `session19_out/step_Q_sf_sweep_lr{0156,02,05,10,25}.npz`              | 各 3.28 MB (計 16.40 MB) | 150 chain × T=10⁴ の (zbar_pre, zbarT, kon_pre, kon0, kick, offset, v0, nband_t{100,1000,5000,10000}) — Step Q κ SNR 直測 |

### 主要 text (session 20 と共に補助データ/results/session19/ に個別コピーは未実施・参照のみ)

| file                                            |      サイズ | 内容                                                            |
| ----------------------------------------------- | -------: | ------------------------------------------------------------- |
| `session19_out/report.md`                       | 19.38 KB | Session 19 総まとめ                                               |
| `session19_out/step_Q_LRa0p03_coefficients.csv` |  3.24 KB | κ, c, T_0 の per-η 5 点値 (Step G/Step W で使用)                    |
| `session19_out/step_B_nband_fit_params.json`    |    781 B | n_band(z̄) = A · exp(-B · z̄²) の A=3.12, B=0.119 (Step W で使用) |
| `session19_out/step_C_crossing_stats.csv`       |  3.54 KB | Session 19 Step C の kp 群別 alive Δz̄ (STEP_C_TABLE の元)         |
| `session19_out/step_A_T0_eta_dependence.csv`    |  4.60 KB | T_0 の η 依存性 (Session 19 Step A)                               |
| `session19_out/step_P_kahan_vs_nokahan.csv`     |  1.59 KB | Type A/B 判定の元数値                                               |
| `session19_out/step_P_type_ab_judgment.md`      |  1.27 KB | Type B 確定の記録                                                  |

**特記**: session 19 は本着地点 A 記録の**初期条件**を与える (checkpoint 5M step からの初回 mtM 走行)。
Session 20 の 500-task 拡張と Session 21 の δ' 記録拡張は、Session 19 の走を延長・拡張したもの。

---

## Session 20 出力 (153.31 MB・55 files)

### 主要 npz

| file                                                              |                    サイズ | 内容                                                            |
| ----------------------------------------------------------------- | ---------------------: | ------------------------------------------------------------- |
| `session20_out/mt_U1_bareK1_500tasks_v2_lr{0156,02,05,10,25}.npz` | 各 17.5 MB (計 87.75 MB) | **500 タスク版 mtM_v2** (定常性判定に使用・W1〜W5 の 5 窓分析の元)                |
| `session20_out/step_Q_prime_sf_sweep_lr{0156,02,05,10,25}.npz`    | 各 9.81 MB (計 49.05 MB) | **450 chain × T=3×10⁴** の Step Q' 拡張 (SNR 向上直測・§9-4 の κ 再検討)  |
| `session20_out/step_R_sf_vfrozen_lr{0156,02,05,10,25}.npz`        | 各 3.28 MB (計 16.40 MB) | v 完全凍結 SGD で c(η) 分離の試み (Step R・v_rel_diff_max=0.0 確認済み)      |
| `session20_out/step_T_T0_joint_distribution.npz`                  |               21.65 KB | T_0 の (5 η × 22 zbar_bin × 5 kon 群) joint 分布 (Step W v3g で使用) |

### 主要 text (補助データ/results/session20/ に個別コピー済み)

| file                                          |      サイズ | vault コピー                                                      |
| --------------------------------------------- | -------: | -------------------------------------------------------------- |
| `session20_out/report.md`                     | 22.41 KB | ✓ [[report]] (session20)                                       |
| `session20_out/step_T_report.md`              |  6.70 KB | ✓ [[step_T_report]]                                            |
| `session20_out/step_U_report.md`              |  1.52 KB | ✓ [[step_U_report]]                                            |
| `session20_out/step_U_5window_stats.csv`      |  3.54 KB | ✓ [[step_U_5window_stats]]                                     |
| `session20_out/step_V_T1_verification.md`     |  1.34 KB | ✓ [[step_V_T1_verification]]                                   |
| `session20_out/step_V_T1_verification.csv`    |  1.64 KB | ✓ [[step_V_T1_verification]]                                   |
| `session20_out/step_W_v3g_report.md`          |  1.36 KB | ✓ [[step_W_v3g_report]]                                        |
| `session20_out/step_W_v3g_prediction.csv`     |    810 B | ✓ [[step_W_v3g_prediction]]                                    |
| `session20_out/step_Q_prime_kappa_5point.csv` |  3.08 KB | (未コピー・Session 20 の κ 5 点値・[[05_K_spectrumとF_K_decay_0918]] の元) |
| `session20_out/step_Q_prime_report.md`        |  2.78 KB | (未コピー・κ SNR 向上直測 report)                                       |
| `session20_out/step_R_c_vfrozen_5point.csv`   |  2.58 KB | (未コピー・c(η) v 凍結の 5 点値)                                         |
| `session20_out/step_R_report.md`              |  2.17 KB | (未コピー・v 凍結 SGD の report)                                       |

**特記**: Session 20 は Chat Claude 第 19 回から Claude Code へ委譲された作業。作業者は Claude Code (Opus 4.7)、
実施日 2026-09-17。CI 幅目標 3e-5 は未達 (実測 2.8e-4〜4.6e-4)・Landing A の 3 判定基準は 1/3 (peak position) のみ達成。

---

## Session 21 出力 (268.17 MB・22 files)

### 主要 npz

| file                                                            |                    サイズ | 内容                                                                                           |
| --------------------------------------------------------------- | ---------------------: | -------------------------------------------------------------------------------------------- |
| `session21_out/mt_U1_bareK1_dprime_v3_lr{0156,02,05,10,25}.npz` | 各 36.3 MB (計 181.5 MB) | **250 タスク版 mtM_v3** (δ' + z_kick_full + n_active + kp_hist を追加保存・Step E の閉形式 fit の元)         |
| `session21_out/step_C_t1_theory_per_event.npz`                  |               40.61 MB | Step C: T_1 theory per-event 計算結果 (5 arm × 250 タスク × 10 seed × 100 unit の T_1_theory scalar) |
| `session21_out/step_D_y_per_event.npz`                          |               45.76 MB | Step D: Y_i per-event 抽出 (Y_i, R, T_4_th, T_5_th の 4 field)                                  |

### 主要 text (補助データ/results/session21/ に個別コピー済み)

| file                                                 |      サイズ | vault コピー                                                                                                           |
| ---------------------------------------------------- | -------: | ------------------------------------------------------------------------------------------------------------------- |
| `session21_out/report.md`                            |  8.65 KB | ✓ [[report]] (session21)                                                                                            |
| `session21_out/step_E_yi_functional_form.md`         | 17.16 KB | ✓ [[step_E_yi_functional_form]]                                                                                     |
| `session21_out/step_E_yi_fits.json`                  | 67.75 KB | 未コピー (代わりに 3 抽出 csv: [[step_E_form_v_slope_by_arm_kp]] [[step_E_form_v_r2_by_arm_kp]] [[step_E_form_v_loglog_fit]]) |
| `session21_out/step_F_markov_transitions.csv`        |  6.89 KB | ✓ [[step_F_markov_transitions]]                                                                                     |
| `session21_out/step_F_report.md`                     |  3.37 KB | ✓ [[step_F_report]]                                                                                                 |
| `session21_out/step_G_alive_branch_theory_driven.md` |  4.90 KB | ✓ [[step_G_alive_branch_theory_driven]]                                                                             |

**特記**: Session 21 も Claude Code 実施。日付 2026-09-18。**中核発見**:
Y_i = c(η) · v · Σ_{r∈on} δ'_r (R²=0.79-0.998・c(η) ∝ η^{1.0}, C ≈ 6172-9177)。
Step E で form (v) を選定・Step F で Markov 遷移・Step G で Model M4 統合 (部分達成)。

---

## Checkpoint (元モデル)

| file                                                                                             |       サイズ | 内容                                                                                                |
| ------------------------------------------------------------------------------------------------ | --------: | ------------------------------------------------------------------------------------------------- |
| `/home/kubo/project/Nakatsuka/data/act_sweep_hole1_0910_local/ckpts/LRa0p03_1216_step5000000.pt` | 189.23 KB | LRa0p03 arm の 5 M step 学習済 checkpoint (act='leaky_relu', alpha=0.03, seed 1216, W b v c fs Tt rm) |

**arm 確認**: `sim_act.load_ck()` で `act=='leaky_relu'` かつ `alpha≈0.03` を assert (全 script で)。

---

## Session 19 script 群 (`session19_scripts/`・全 script は 補助データ/scripts/ に未コピー)

参照だけ:
- `mtM_v2.py` (8.09 KB): mtM_v3 の基底クラス (session 21 mtM_v3.py が継承)
- `sf_sweep.py` (Step Q・150 chain × T=10⁴)
- `step_A_T0.py`, `step_B_nband_fit.py`, `step_C_crossing.py`, `step_D_prediction.py`
- `step_Q_analyze.py`, `step_Q_arm_comparison.py`
- `step_P_driver.py`, `step_P_compare.py`, `step_P_type_ab_judgment.py`

Session 20 では、これらのうち `mtM_v2.py` を `mtM_500task.py` (500-task wrapper) と `session21_scripts/mtM_v3.py` (継承拡張) が使用。

---

## npz field 型と shape の目安

**mtM_v2 500-task 版** (`mt_U1_bareK1_500tasks_v2_lr*.npz`):
- `zbar`: shape (501, 10, 100), dtype float32, description: per-task per-seed per-unit の 32-support 平均 z̄
- `kon`: shape (501, 10, 100), dtype int8, description: per-task の kon (on-support 数)
- `kon_kick`: shape (500, 10, 100), dtype int8, description: flip 直後の kon (SGD 前)
- `kick_i`: shape (500, 10, 100), dtype float32, description: SGD 前の flip による Δz̄
- `offset_i`: shape (500, 10, 100), dtype float32, description: g offset の Δz̄ 寄与
- `v_final`: shape (10, 100), dtype float32, description: 全 task 終了後の v (500 tasks 後・SGD で更新済み)
- `zbar_kick`: shape (500, 10, 100), dtype float32, description: SGD 前 (kick 直後) の z̄
- `nband`: shape (501, 10, 100), dtype float32, description: on-band n_band 実測

**mtM_v3 250-task 版** (`mt_U1_bareK1_dprime_v3_lr*.npz`):
- 上記フィールド + `dprime`: shape (250, 10, 100, 32), dtype float32, description: per-task per-seed per-unit per-support の δ' (跨いだ後の残差)
- + `z_kick_full`: shape (250, 10, 100, 32), dtype float32, description: SGD 前の per-support z
- + `n_active`: shape (250, 10, 100), dtype int8, description: SGD 前の |{r: z>0}|
- + `kp_hist`: shape (250, 10, 100), dtype int8, description: kon の history

**Step Q'** (`step_Q_prime_sf_sweep_lr*.npz`):
- `zbar_pre`, `zbarT`: shape (450, 100), dtype float32, description: pre/T=30000 の z̄ per chain per unit
- `kon_pre`, `kon0`: shape (450, 100), dtype int8, description: pre/kick 直後の kon
- `kick`, `offset`, `v0`: shape (450, 100), dtype float32
- `nband_t{100,1000,5000,10000,30000}`: shape (450, 100), dtype float32
- `chain_seed`, `chain_kp`: shape (450,), dtype int32

---

## 未コピー items の内容(参考)

以下は Vault にコピーせず、Nakatsuka repo に残す:

- **全 npz** (合計 619.58 MB) — サイズ問題
- **全 log ファイル** (小・stdout captures) — 情報として非必須
- **session19 の Step Q/R/T 中間 csv/md** (合計 ~ 30 KB) — Session 20 report で参照済み
- **session20 の Step Q'/R report/csv** (合計 ~ 10 KB) — [[00_概要と5判定基準_0918]] と [[05_K_spectrumとF_K_decay_0918]] で参照済み
- **step_E_yi_fits.json** (67 KB) — 3 抽出 csv で代替

---

## 参照時の注意

1. 中塚君が npz を直接開く必要があるとき: Kubo に `scp` 依頼、または git repo 全体 (`~/project/Nakatsuka`) の共有依頼。
2. npz を開くコード例: `numpy.load('...npz')` で dict-like object。field 名は `d.files` で一覧、`d[field_name]` で ndarray 取得。
3. hash / 検証: 各 file の sha256 は未取得。必要なら Kubo が再取得可能。
4. 元 script (session20_scripts/, session21_scripts/) は補助データ/scripts/ にコピー済み・md/csv の元数値を再現できる。
