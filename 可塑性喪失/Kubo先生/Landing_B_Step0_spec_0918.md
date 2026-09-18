---
aliases:
  - Landing B Step 0
  - Landing B の Step 0 spec
  - Chat container recover
  - Kubo 決着の precision 確認
description: Landing A 記録 (turn 9 完成度 2 版) の未達点集約。Chat container リセット分の recover・Kubo 決着の precision 確認・1000 tasks 定常性検証
---

# Landing B の Step 0 spec: Chat container recover と Kubo 決着の precision 確認

親: [[00_概要と5判定基準_0918]] / 状態: **未着手** (Landing A 記録 close 後の次段階) / 更新: 2026-09-18 (起票・改善余地 2 の実装)

## 1. 主旨

Landing A 記録 (turn 9 完成度 2 版・[[00_概要と5判定基準_0918]]) は 5 判定基準を全て達成し、Kubo 段 0 分析で Y_i の bias mode cancellation を決着させた。しかし以下 3 系統で未達点が残る:

1. **Chat container 生成物の失われた script/data**: 第 20 回の段 0 分析・K spectrum 対角化・Term I/II 分解等の実装 script は Chat container リセットで失われている。再構築が必要 ([[README_reconstruction]] の 6 項目)
2. **Kubo 決着の precision 確認**: seed 0 での確認のみで、他 seed の $\|\tilde\mu\|^2$ verification 等が未実施
3. **Landing A 判定 1 の定常性**: 260 tasks 判定で、W5 (441-500) で peak η 移動・Spearman 低下 ([[13_未達成項目と反証履歴_0918]] §5 参照)

本 spec は Landing B の Step 0 として、これらを systematic に解消するための作業リスト。

## 2. 未達点の集約 (Landing A 記録から)

### 2.1 Chat container 消失 script の recover (6 項目)

[[README_reconstruction]] に再構築手順あり:

1. **K spectrum 対角化** — $\mathcal K = X_c X_c^\top / 32$ の対角化・非零固有値抽出 (詳細 [[05_K_spectrumとF_K_decay_0918]])
2. **段 0 分析 (Kubo 決着)** — Y_i の閉形式 $c(\eta)^{\rm fit}$ と正しい理論値 $(2\eta T/32) \cdot \|\tilde\mu\|^2$ の ratio 1.008 の narrow band 一致 (詳細 [[09_Y_iの物理的正体_bias_mode_cancellation_0918]] §5)
3. **V-a 真の版** — $\Sigma_{XX}$ 解析形の数値検算 ([[02_V-a真の版_有界性_0918]] §3.7)
4. **V-b 真の版** — σ 中央値変化の 5 arm 実測 ([[03_V-b真の版_wnorm不動性_0918]] §4-5)
5. **Term I / Term II 分解** — leaky ReLU 恒等式による decomposition ([[04_Term_I_II分解と3レジーム_0918]] §5)
6. **v3i_joint Model M4 統合** — joint 分布条件付けで Spearman +0.900 ([[06_Model_M4_v3i_joint_3判定_0918]] §6)

### 2.2 Kubo 決着の precision 確認 (4 項目)

1. **他 seed の $\|\tilde\mu\|^2$ verification (n_fixed 依存性)**: seed 1-9 で $\|\tilde\mu\|^2$ を測定・Kubo 決着の ratio 1.008 が seed 全体で保たれるか (詳細 [[09_Y_iの物理的正体_bias_mode_cancellation_0918]] §8)
2. **bias mode projection の代数の直接検証**: `bias_mode_projection.py` の再構築で $\lambda_{\max} = u_1^\top \mathcal K u_1 = \|\tilde\mu\|^2$ を数値的に verify (詳細 [[09_Y_iの物理的正体_bias_mode_cancellation_0918]] §6.4)
3. **09 §5.2 numerical consistency の解消 (P10)**: 09 §5.2 表の $c^{\rm theory}$ (lr0156: 0.955) を単純に $(2\eta T/32) \cdot 9.24 = 5775\eta$ で計算すると 0.9009 で 0.05 ずれる。$\mathcal F(\mathcal K)$ の高次補正を含む正確な式を明示化 (turn 9-3 で指摘)
4. **05/09 の $\|\tilde\mu\|^2$ 値の不整合の解消 (P9)**: 05 §5.4 「seed 0 実測 9.29・手計算 9.25」と 09 §5.1 「seed 0 で 9.29・平均で 9.24」の「平均」の意味 (seed 平均 or 5 arm 平均) を明示化 (turn 9-3 で指摘)

### 2.3 04 §5.4 の Term II 閉形式の精度確認 (P8)

Term II 閉形式の理論値 (2.31 × 10⁻⁴ per task・500 tasks で 0.116) と実測 (0.223) の 2 倍差。「±factor 2 は通常のずれ」と正当化されているが、パラメータ $\overline{\delta^2}$・$\overline{\varphi'^2}$・$\overline{\|x\|^2}$ の精度を上げれば 2 倍差が解消する可能性 (turn 9-4 で指摘)。

### 2.4 元 Nakatsuka repo の実物 file 確認

turn 9-4 で保留した項目。元 Nakatsuka repo の `session20_out/` と `session21_out/` の実物 file list を厳密に取得し、Landing A ノートの Provenance の記述と照合する。特に:

- session20_out/ の Chat container 生成物 (all5arm_sigma_d.npz・per_task_d_true.npz・term_decomposition.npz・model_m4_v3i_joint_*.npz・per_unit_5term_verification_lr*.npz・kappa_c_scaling.csv) と Session 20 実物 (mt_U1_bareK1_500tasks_v2_lr*.npz 等) の区別
- session21_out/ の実物 file (turn 8-h で copy した session21/results と一致するか)

### 2.5 Landing A 判定 1 の 1000 tasks 定常性検証

Session 20 Step U で W5 (441-500) 窓の peak η 移動 (0.0002 → 0.000156)・Spearman +0.700 低下が判明 ([[13_未達成項目と反証履歴_0918]] §5)。Landing A の 260 tasks 判定が過渡現象の可能性がある。1000 tasks 拡張検証で W6-W10 の窓での peak η の定常性を確認。

## 3. 作業計画 (優先度順)

### 優先度 1: Kubo 決着の precision 確認 (§2.2)

**理由**: Landing A の判定 5 (Y_i の物理的解明) の中核・Kubo 決着の権威性を確定する

**作業**:
1. Nakatsuka repo の `session21_scripts/mtM_v3.py` を基点に、5M ckpt から K spectrum を対角化する script (`bias_mode_projection.py`) を作成
2. seed 1-9 で $\|\tilde\mu\|^2$ を測定・n_fixed 依存性を確認
3. 09 §5.2 の theoretical value の formula を明示化 ($\mathcal F(\mathcal K)$ の高次補正を含む正確な式)
4. 05/09 の $\|\tilde\mu\|^2$ 値の統一 (「平均」の意味の明示)

### 優先度 2: 元 Nakatsuka repo の実物 file 確認 (§2.4)

**理由**: Landing A ノートの Provenance の精度確定・Chat container 生成物と実物の区別

**作業**:
1. `ls session20_out/` と `ls session21_out/` で file list を取得
2. Landing A ノート 02-07 の Provenance の「元 Nakatsuka repo で実在」の記述との照合
3. Chat container 生成物の判別 (turn 9-4 の私の判断の verify)

### 優先度 3: Chat container 消失分の recover (§2.1)

**理由**: 再現性の確保・Landing A の科学的正当性の担保

**作業**:
1. [[README_reconstruction]] の 6 項目の再構築を実施
2. 各項目の numerical value を Landing A ノートの記述と照合

### 優先度 4: Landing A 判定 1 の 1000 tasks 定常性検証 (§2.5)

**理由**: Landing A の 260 tasks 判定の限定条件の解消

**作業**:
1. Session 20 Step U を 1000 tasks に拡張実行
2. W6-W10 の窓での peak η・Spearman を測定
3. Landing A 判定 1 が定常性を持つか (500-1000 tasks で peak η が [0.0002, 0.0005] に stable か) を確認

### 優先度 5: Term II 閉形式の 2 倍差の precision 確認 (§2.3)

**理由**: 04 §5.4 の判定 4 の precision 向上

**作業**:
1. パラメータ $\overline{\delta^2}$・$\overline{\varphi'^2}$・$\overline{\|x\|^2}$ の精度を上げる (実測値の再確認)
2. Term II の theoretical value を再計算し、実測との factor 2 差が解消するかを確認

## 4. 反証条件

以下のいずれかが観測されたら Landing A 記録 (完成度 2 版) は再修正が必要:

1. **Kubo 決着の破綻**: seed 1-9 で $\|\tilde\mu\|^2$ の値が seed 0 (9.29) から相対誤差 > $10^{-3}$ で乖離する・かつ ratio が 1 から乖離する
2. **Provenance 判断の誤り**: 元 Nakatsuka repo で 06 §11 の 3 script (model_m4_v3i_joint.py 等) の実物 file が存在した場合 (Chat container 生成物の私の判断が誤り・turn 9-4 の弱点)
3. **判定 1 の 260 tasks 限定確定**: W6-W10 で peak η が [0.0002, 0.0005] から系統的にずれる (Landing A 判定 1 が 260 tasks 限定であることが確定)
4. **代数的破綻**: bias mode projection の代数計算で $\lambda_{\max} \ne \|\tilde\mu\|^2$

## 5. Landing A 記録との整合性

本 spec は Landing A 記録 ([[00_概要と5判定基準_0918]]) と integrated な関係:

- **Landing A の中核 (5 判定達成)** は本 spec の作業で棄却されない予想 (優先度 1-2 の結果は精度確認・Landing A の主張と整合)
- **Landing A の限定条件** (260 tasks 判定・Kubo 決着の seed 0 中心) は本 spec の作業で解消される予定
- **Landing A の Provenance の精度** は本 spec の作業で確定される

本 spec の作業が完了した後、Landing A 記録の完成度 3 版として再 close するか、Landing B の別 spec に統合するかは Kubo が判断。

## 6. Provenance

- **source-note**: [[00_概要と5判定基準_0918]] (Landing A 完全達成の主張) の未達点集約
- **source-commit**: 本 spec 起票時の teacher branch head
- **verified-on**: 2026-09-18
- **参照**:
  - [[02_V-a真の版_有界性_0918]] - [[13_未達成項目と反証履歴_0918]] (Landing A 14 ノート)
  - [[README_reconstruction]] (Chat container 消失分の再構築手順)
  - [[large_data_reference]] (元 Nakatsuka repo の実物 file 位置)

## 7. Log

- 2026-09-18 起票 (Landing A 記録 (turn 9 完成度 2 版) の未達点を集約した Landing B の Step 0 spec・改善余地 2 の実装)
- Landing A 記録の close 宣言 ([[00_概要と5判定基準_0918]] 冒頭 turn 9-5 追記) と対応
- 優先度 1-5 の作業は Landing B の実施タイミングで Kubo が判断
