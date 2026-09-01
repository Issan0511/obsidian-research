# HANDOFF — `channel_2x2_0901`（チャネル遮断 2×2 の本走）

宛先: Codex / Claude Code ／ 発行: 2026-09-01・チャット `2x2_spec_0901`
**正本の spec は [[チャネル遮断2x2_spec_0901]]（vault）。** 本 HANDOFF は実行手順であり、判定基準の正本ではない。齟齬があれば spec が勝つ。

---

## 0. 一行

condA・深さ2 の系で、**$b$ チャネルの遮断（隠れ層 bias だけへの weight decay）× µ チャネルの遮断（層入力の EMA 中心化）の 2×2 要因計画**を、同一 spec・同一 seed ストリームで 1 本走らせる。既に別々の走として 4 セルは存在するが、seed 集合・bootstrap seed・交互作用・等価限界が揃っていないため要因計画として使えない。本走はそれを揃える。

---

## 1. 運用規律（違反すると結果が使えなくなる）

1. **spec は必ず単独で先に commit する。** 先例: `gate_dose_0830` は spec+config（`d66da2d`）→ 実装（`e15e081`）→ 結果（`c4fe8ed`）の 3 commit で順序が repo 履歴から示せる。`centered_freeze_0901` は 1 commit に畳まれて示せなかった。**本走は spec 単独 → config+実装 → 結果 の 3 commit を崩さない**
2. **結果 commit は push を確認して初めて「commit 済み出力」とみなす。** 各段で `git ls-remote origin refs/heads/main` を実行し、自分の commit hash がリモートに載っていることを確認して、その出力を報告に貼る
3. **数値は `results/*/verdict.csv` と `summary.md` からのみ引く。** それ以外から引く場合はファイル名と行の識別子（腕・ブロック・metric）まで書く
4. **窓（どの task 範囲か）を書かずに数値を書かない。** 過去に同じ事故が 3 回起きている
5. **spec は結果を見た後に書き換えない。** 追補は「事後」ラベル付きで別ファイル
6. **日付由来の値を流用しない。** 既用: `generator_offset` = `20260830` / `20260831`、bootstrap seed = `20260829` / `20260902` / `20260903` / `20260904`。**本走は `generator_offset = 20260905`、`bootstrap_seed = 20260906`**

---

## 2. 段階 A — spec を repo へ転記して単独 commit（**事前登録の成立点**）

1. vault の `可塑性喪失/spec/チャネル遮断2x2_spec_0901.md` を **`specs/spec_channel_2x2_0901.md` として本文をそのまま転記**する。冒頭に出自バナーを 1 行足すのは可（`出自: vault 可塑性喪失/spec/チャネル遮断2x2_spec_0901.md（commit 6693c4a）`）。**本文の数値・判定基準・§8 の事前予測を編集しない**
2. **このファイルだけを commit して push する。** config も実装もこの commit に含めない
3. `git ls-remote origin refs/heads/main` の出力を報告に貼る

これが完了するまで段階 B 以降に進まない。

---

## 3. 段階 B — config と実装

### 3.1 `configs/channel_2x2_0901.yaml`

```yaml
# proj_004: channel_2x2_0901 — b チャネル遮断 × µ チャネル遮断の 2×2 要因計画（本走）
#
# 仕様: specs/spec_channel_2x2_0901.md（単独 commit 済み）
# 前段: results/bias_wd_0901/（centered 側）、results/bias_wd_std_seediso_0901/（std 側）
#
# 日付の使い回し禁止（HANDOFF §1-6）:
#   20260830 / 20260831 = generator_offset で既用
#   20260829 / 20260902 / 20260903 / 20260904 = bootstrap seed で既用
# 本走は generator_offset=20260905、bootstrap_seed=20260906。

spec: specs/spec_channel_2x2_0901.md
baseline_dir: results/mlp2_phase1_0829

common:
  total_steps: 5000000          # = task 500
  seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  generator_offset: 20260905    # ★ 新規乱数系列（spec D1）。--seeds だけでは同一系列
  lr_main: 0.01
  device: cpu
  eval_batch: 2000
  lop_every: 10000
  loss_bin: 10000
  checkpoints: [0, 5000000]
  run_freeze: false
  dead_tol: 1.0e-7
  dead_tau: 0.95
  dup_tau: 0.95
  sat_ratio_tol: 1.0e-4
  sat_frac: 0.99
  sign_match_tau: 0.95

condA:
  m: 20
  f: 15
  target_hidden: 100
  beta: 0.7
  T_values: [10000]
  encodings: [std]              # 中心化は intervention 側の層内機構で入れる

intervention:
  name: A_layer_input_centering
  center_alpha: 0.01
  stop_gradient_on_running_mean: true
  consumes_rng: false

# 4 セル。深さは 4 腕すべて [100,100] に揃える（深さをまたぐ paired 比較は禁止・床も一本化）。
# 更新式は b -= lr*(gb + wd_b*b)（decoupled ではなく素の L2 勾配）。
# 掛けるのは両層の隠れ層 bias のみ。W・v・出力バイアス c には掛けない。
arms:
  - {name: none, hidden: [100, 100], centered_layers: [],     wd_b: 0.0}
  - {name: bwd,  hidden: [100, 100], centered_layers: [],     wd_b: 1.0e-3}
  - {name: cen,  hidden: [100, 100], centered_layers: [1, 2], wd_b: 0.0}
  - {name: both, hidden: [100, 100], centered_layers: [1, 2], wd_b: 1.0e-3}

pairing:
  # 4 腕とも同一 seed ストリーム。S-pair で init・教師・入力実現の bit 一致を検査する。
  paired_groups:
    - [none, bwd, cen, both]
  baseline: none

phase1:
  task_period: 10000
  exact_support: 32
  sigma_degenerate_tol: 1.0e-8

sanity:
  s1_identity_tol: 1.0e-10
  omp_num_threads: 1

channel_2x2:
  output_dir: results/channel_2x2_0901
  omp_num_threads: 1
  guard_every: 1000
  s0_replay_steps: 30000
  s0_reference_offset: 0        # S0 は generator_offset=0 に切り替えた別 replay
  s0_baseline_arm_std: L2_none
  s0_baseline_arm_cen: L2_Aall
  s2_probe_lambda: 1.0e-3

  seed_isolation:               # spec_bias_wd_std_seediso_0901 §2 を継承
    max_exclusions_per_arm: 2
    min_complete_seeds_per_arm: 8
    min_paired_seeds: 8
    quarantine: zero_training_state_and_set_lr_zero
    keep_rng_rows: 10
    exclude_entire_seed_trajectory: true
    stop_arm_on_limit_exceeded: true

  block_tasks: 50
  early_block_tasks: [51, 100]   # B02
  late_block_tasks: [451, 500]   # B10

  # ---- 事前登録のしきい（spec §6）
  equivalence_margin: 0.15       # Delta（spec D4）
  interaction_margin: 0.50       # Delta_int
  ceiling_flag_dex: 3.0          # B02 水準の 4 セル間最大差がこれを超えたら CEILING_CONTAMINATED
  eff_rank_keep_frac: 0.70

  # ---- 床（継承のみ・再較正しない）
  unfit_floor: 1.0e-23           # mlp2_phase1_0829 の S6 較正を継承（深さ2系）

  # ---- CI
  bootstrap_B: 20000
  bootstrap_seed: 20260906
  ci_method: percentile_paired
  degenerate_se_tol: 1.0e-15
  degenerate_frac_max: 0.01
  degenerate_width_ratio_max: 100.0

  numeric_divergence:
    status: NUMERIC_DIVERGENCE
    detection: nonfinite_training_state_at_probe
    action: quarantine_seed_and_continue
    exclude_entire_seed_trajectory: true
    rescue: none
```

### 3.2 `src/channel_2x2_0901.py`

既存資産の合成でよい。**新規実装を書き起こさない。**

| 要素 | 流用元 |
|---|---|
| 腕の構築・学習・厳密記録 | `mlp2_phase1_0829` 経路（`setup_arm_p1` / `train_arm_p1` / `forward_centered` / `exact_layer_record_p1`） |
| `wd_b` の差し込み | `VecMLPL.set_weight_decay_b`（構築後に差し込む。乱数も状態も消費しない） |
| 腕ごとの `centered_layers` 切り替え | `src/bias_wd_0901.py` |
| seed 単位隔離 | `src/bias_wd_std_seediso_0901.py` |
| 共通ユーティリティ | `src/bias_wd_common.py` |

実装上の注意 2 点。

- **分岐を置かず常に `gb + wd_b*b` を計算する。** $\lambda=0$ の腕が WD コード経路を通したうえで無 WD 実装と bit 一致することを検査可能にするため（S1）
- **`freeze_bias=true` と `wd_b>0` の同時指定はエラー**にする

### 3.3 記録する列

`spec_bias_wd_0901` §3 の凍結セットをそのまま。層ごとに `strict_dead_frac` / `b_median_alive` / `B_median_alive` / `beta_median_alive` / `kappa_median_alive` / `sigma_median_alive` / `margin_median_alive` / `p_hat_median_alive` / `p_hat_thin_frac` / `p_hat_sat_frac` / `eff_rank` / `eff_rank_W` / `w_norm_median` / `wcos_mean`、および `unfit` / `eval_loss_exact` / `mean_log10_unfit` / `log10_mean_unfit` / `floor` / `floor_frac`。

**ロガー相乗り**: 台帳の $M_i = w_i\cdot\mu$、$B_i = b_i/\sigma_i$、分母 $\sigma_i$、`submerged_frac`、境界前後のスナップも既定で出す。**ただし主判定は spec §6.2 の 1 つだけ**で、相乗り列は事後ラベルでしか使わない。

config と実装をまとめて 1 commit・push 確認。

---

## 4. 段階 C — ゲート（`results/_gate_channel_2x2_0901/`）

**全 PASS でなければ本走を起動しない。** 各項目を JSON で保存する。

| ID | 内容 |
|---|---|
| **S-pair** ★ | **要因計画の前提。** 4 腕が seed ごとに init（$W$・$b$・$v$・$c$）・教師・入力実現で **bitwise 一致**すること。centering も `wd_b` も乱数を消費しないことを 30k step・1k 格子の replay で確認する |
| **S0** | `generator_offset=0` に切り替えて `none` / `cen` を既存 committed 腕（`L2_none` / `L2_Aall`）と 30k replay 比較し、`unfit`・`eval_loss_exact`・各層 `strict_dead_frac` が一致。**本走（offset 20260905）の腕とは一致しない。実装の同値性のみを示す** |
| **S1** | $\lambda=0$ が WD コード経路を通しても無 WD 実装と bit 一致 |
| **S2** | 同一状態から $\lambda=0$ と $\lambda>0$ で 1 step 進め、(i) $W$・$v$・$c$ が bitwise 一致、(ii) $b$ の差が厳密に $-\eta\lambda b_{\rm before}$、(iii) `wd_b` を参照する更新行が `self.bs[i]` の行だけ |
| **S3** | 壁恒等式 $\hat p=0 \iff \beta+\kappa\le0$、$\hat p$ の 1/32 量子化、第1層 $\kappa$ の閉形式一致、凍結済み `exact_layer_record_p1` との独立実装一致（許容 `1e-10`）。**$\beta\le-\sqrt5$ の十分条件は第1層限定で第2層に適用しない** |
| **S-iso** | seed 1 に人工的に非有限を注入し、隔離後 100 step で他 9 seed の全状態が対照 runner と bitwise 一致 |
| **S-cap** | 人工的に 3 seed を非有限化し、3 本目で `ARM_INVALID_EXCLUSION_LIMIT` になる |
| **S-count** | ブロック内 task 末点が 50 個ちょうど。`flip_state` の変化回数と境界個数が一致（教訓⑭） |

本走中の項目:

| ID | 内容 |
|---|---|
| **S4** | 非有限ガード `probe_every=1000`。seed 単位で隔離（config の `seed_isolation`）。**前段で `bwd` 相当の腕が seed 7・step 3,381,000 で発散した実績があるので、起きる前提で扱う** |
| **S-floor** ★ | 4 腕・B02/B10 とも `floor_frac = 0` を確認。床に触れた点があれば **E-drift は無効**とし E-level のみで報告する |
| **S-ceiling** ★ | B02 水準の 4 セル間最大差を記録。**3 dex 超で `CEILING_CONTAMINATED`** を立て、`summary.md` に「E-drift 単独では読まない」と明記 |

---

## 5. 段階 D — 本走と判定

### 5.1 走

4 腕 × 深さ2 × 5M × 10 seed。前段実績で 1 腕約 38 分、**逐次で約 2.5 時間**。腕ごとの独立プロセス並列は可（軌道不変・`OMP_NUM_THREADS=1` を全プロセス共通に固定）。

### 5.2 集計

- 実験単位は seed。ブロック内 50 個の task 末を seed 内で平均して一値にする
- **B02 = task 51–100、B10 = task 451–500**
- 主 endpoint は **`mean(log10 unfit)`**（seed ごとにブロック内 50 点の $\log_{10}$ を平均）。`log10(mean unfit)` も出すが**判定に使わない**
- 床 `1e-23` を各点に当てる。**再較正しない**
- **主比較は 4 腕の完走 seed の共通集合のみ。** 8 本未満なら `CONTRAST_INVALID_TOO_FEW_PAIRED` として主判定を出さない
- CI は seed 水準 paired percentile bootstrap、`B=20000`、`bootstrap_seed=20260906`。studentized も併算し退化ガードの結果を `ci_degenerate` 列に出す。**percentile が主**
- 二値割合は Clopper–Pearson

### 5.3 共主 endpoint

| ID | 定義 |
|---|---|
| E-drift | `mean(log10 unfit)` の B10 − B02 |
| E-level | `mean(log10 unfit)` の B10 |

**主判定は E-drift。E-level を必ず併記する。** 両者で結論の向きが食い違ったら `LADDER_INVERTS` を立て、**どちらも単独で引かない**。

### 5.4 主判定（$\Delta = 0.15$ dex）

| 条件 | 内容 | しきい |
|---|---|---|
| (a) | `both` の E-drift の 95% CI | $[-\Delta, +\Delta]$ に収まる |
| (b) | `bwd − none` の対応差の CI 上端 | $< -\Delta$ |
| (c) | (i) `bwd` の E-drift の CI 下端 $> +\Delta$ かつ (ii) `both − bwd` の対応差の CI 上端 $< -\Delta$ | 両方 |

**決定木（この順で評価する）**

1. (a) 偽・`both` の CI 下端 $> +\Delta$ → `RESIDUAL_UNEXPLAINED`
2. (a) 偽・`both` の CI 上端 $< -\Delta$ → `OVERSHOOT_IMPROVES`
3. (a) 偽・CI が $\pm\Delta$ をまたぐ → `INCONCLUSIVE_WIDE`
4. (a) 真・(b) 偽 → `MU_CHANNEL_ONLY`
5. (a) 真・(b) 真・(c) 偽 → `B_CHANNEL_ONLY`
6. 3 条件すべて真 → `TWO_CHANNELS_BOTH_NECESSARY`

### 5.5 副判定（すべて主判定に入れない）

| ID | 内容 | ラベル |
|---|---|---|
| I | `(bwd − none) − (both − cen)` の対応差（E-drift・E-level それぞれ） | CI が $\pm 0.50$ 内 → `ADDITIVE` ／ 下端 $> +0.50$ → `SUBADDITIVE` ／ 上端 $< -0.50$ → `SUPERADDITIVE` |
| L | 4 セルの E-level 順位、B02 水準の最大差 | REPORT_ONLY ＋ S-ceiling のフラグ |
| D | 各セル L1/L2 `strict_dead_frac` の B02→B10 | **REPORT_ONLY。判定に使わない** |
| R | 第1層活性 `eff_rank` の B10。`cen − both` の対応差 CI 下端 $>0$ | `SATURATION_PREVENTED` / `NOT_PREVENTED` |
| 台帳 | $M$ と $B$ の alive 中央値・B02→B10 | REPORT_ONLY |

**I が `SUBADDITIVE` に出ても機構の証拠として書かない。** centered 系のセルは B02 水準が低く、落ちる余地がないことだけでも劣加法は生じる。本走はこの 2 つを分離しない。この旨を `summary.md` に明記する（spec §8.1）。

---

## 6. 事前予測（Issa 記入済み・結果を見る前に凍結）

1. 主判定 → `TWO_CHANNELS_BOTH_NECESSARY`
2. `both` の E-drift は $\pm\Delta$ に収まる → yes
3. 交互作用 → `SUBADDITIVE`
4. E-level の最良 → `bwd`（2 位以下は未指定）
5. 外れたときの書き直し先 → わからない

**`summary.md` に予測と結果の対応表を必ず出す。** 外れた項目は「外れた」と明記する。3 は spec §8.1 の格の限定 3 点を添える。

---

## 7. 引いてはいけない線（spec §9 の要約。全文は spec を見る）

1. **本走の 2×2 を、v4.2 の「積の構造」の 2×2（µ/Σ × 片道ゲート）や [[論点マップ]] §20 の 2×2（µ ダイヤル × 可識別性ダイヤル）と混同しない**
2. **「µ チャネル遮断」は µ の除去ではない。** EMA 中心化は µ とタスク可識別性を同時に消す。**「µ を消した」と書かず「µ チャネルを EMA 中心化で遮断した」と書く**
3. **`strict_dead` を判定に使わない**
4. **本走は新規乱数系列なので前段と bit 一致しない。** S0 は実装の同値性のみを示す
5. **「$b$ だけの weight decay で LoP が治る」と一般に書かない。** スコープは condA・幅100・hidden `[100,100]`・$T=10^4$・batch=1・`lr=0.01`・plain SGD・5M・$\lambda=$1e-3
6. **「2/3 : 1/3」の比を主張に載せない**
7. **$\lambda$ を結果を見て選び直さない**（前段パイロットで凍結済み）

---

## 8. 成果物

```
specs/spec_channel_2x2_0901.md      ← 段階 A で単独 commit
configs/channel_2x2_0901.yaml       ← 段階 B
src/channel_2x2_0901.py             ← 段階 B
results/_gate_channel_2x2_0901/     ← 段階 C（S-pair / S0 / S1 / S2 / S3 / S-iso / S-cap / S-count）
results/channel_2x2_0901/           ← 段階 D
    verdict.csv  summary.md  paired_endpoints.csv  exclusions.csv
    task_end_metrics.csv  block_levels.csv  run_sanity.json  provenance.json
    fig_channel_2x2.png
```

3 commit（spec 単独 → config+実装 → 結果）。**各段で `git ls-remote origin refs/heads/main` の出力を報告に貼る。**

---

> **帰趨（2026-09-01）:** 全段階完了。repo は spec `31f3792` → 実装 `a072f09` → 結果 `bb5fd09`。主判定と監査は [[チャネル遮断2x2結果_0901]]。
