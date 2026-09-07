# Random Label CIFAR × 適応 α Snake（WD が最も失敗する箱で差はさらに開くか・入力分布を替えて c=0.6 は保つか）

親: [[RandomLabelMNIST結果_0906]]（Q1 `ACTIVATION_MATTERS_UNDER_WD` +0.0233・Q2 `B_ABOVE_C` +0.0062）／[[PermutedMNIST_適応α結果_0905]] / 状態: **起草（v1・Claude）・予測 §6 記入済み（Claude のみ）・実装前** / 作成 2026-09-07 / 出典チャット: `活性化プロット_0904`
関連: [[論点/理論が説明すべき事実_0906|理論が説明すべき事実_0906]] §D／[[引用禁止]]

> **run id: `pmnist_rlcifar_0907`。** 宿主は `src/pmnist_rlmnist_0906.py`（プロトコル・介入・検査を継承）で、**データ層だけ差し替える**。新モジュール `src/pmnist_rlcifar_0907.py`。既存 `src/` は無改変。
> **本 spec は [[運用ルール]] §3 の自動起案ではない。** 2026-09-07 のチャットで Issa が「次に Snake をテストするのは CIFAR がいいか」「目安 8 時間」「seed 10 で中間結果が見られれば」と指示した。
> 順序: §6 予測 → 本 spec commit → 実装＋検査＋煙試験 → 本走。

---

## 0. 一行

**Kumar et al. の表で WD が最も失敗する列（Random Label CIFAR: L2 0.75 対 L2 Init 0.96・差 21 pt）で同じ 7 腕を回し、(Q1) `SNA+l2` − `R+l2` が MNIST の +0.0233 からさらに開くか、(Q2) 適応 α の c=0.6 が入力分布を替えても同じ帯（mob 0.55–0.85・2αW≈1.2）に落ちるか、を決める。**

## 1. なぜ回すか

| 材料 | 出所 | 格 |
|---|---|---|
| Permuted MNIST で `SNA+l2` − `R+l2` = **+0.0023**、Random Label MNIST で **+0.0233**（10 倍） | [[RandomLabelMNIST結果_0906]] | **登録済み** |
| Kumar Fig.2（Adam）の L2 対 L2 Init の差: Permuted 0.01・Random Label MNIST 0.15・**Random Label CIFAR 0.21**・5+1 CIFAR 0.12 | 原典 | 文献 |
| 適応 α は 2 箱（SGD/Adam・1ep/4ep）で mob 0.70・2αW 1.20 に落ちた。**ただし入力は常に MNIST だった** | [[PermutedMNIST_適応α結果_0905]] Q1 | 登録済み |
| WD 下で mobility と精度が単調（`R+l2` 0.233→0.941・`LR+l2` 0.393→0.950・`SNA+l2` 0.824→0.964） | 同 §5b-1 | 未登録 |

**動機**: 主張「**WD が失敗する箱ほど活性化が効く**」は 2 点（Permuted・Random Label MNIST）しか無い。Kumar の表が正しければ CIFAR は 3 点目で、しかも**最も開く点**である。加えて **`α_i = c/W_i` の c=0.6 が入力分布に依らないか**は今回が初めての検証（MNIST は画素 0–1・非負・スパース、CIFAR は自然画像で統計が違う）。

### 1.1 先に書いておく危険

1. **入力次元が 784 → 3072 で第 1 層の W が変わり、c=0.6 が外れる。** clip 率を必ず記録する。clip ≥ 5% なら Q2 は `ALPHA_NOT_SELF_SETTING`
2. **1200 枚の CIFAR を MLP で記憶できないかもしれない。** MNIST では 400 epoch で memo_acc 1.000 だった。**`memo_acc` < 0.9 の腕が出たら、その腕の online 精度は「記憶できない」と「学ぶのが遅い」の混合**になる。段 0 として 1 腕 2 タスクの煙試験で確認する
3. **8 時間で全 seed は終わらない見込み。** seed 逐次なので中間で読む。**6 seed で符号検定が p=0.031 に届く**ので、そこから暫定を出す
4. **Random Label CIFAR は「CIFAR の視覚構造」を全く使わない**（乱数ラベルの記憶）。外的妥当性は「入力分布が違う」ぶんだけで、CNN・自然画像タスクの証拠にはならない

## 2. 設計

### 2.1 箱（Kumar et al. §4.2「Random Label CIFAR は Random Label MNIST と同一の設定で、データが CIFAR-10 から来る」）

- **データ**: CIFAR-10 訓練 50,000 から **1200 枚を seed ごとに 1 度だけ**無作為抽出（層化なし）。全タスクで同じ 1200 枚
- **前処理**: 32×32×3 = **3072 次元にフラット化**し `/255` で [0,1] に（MNIST 側と同じ流儀。チャネル正規化はしない — 正規化は §2.4 の対象外）
- **タスク**: 各画像に一様乱数ラベル ∈ {0..9} を独立に割り当て直す。**50 タスク**
- **訓練**: **400 epoch/タスク**・batch 16（75 step/epoch → 30,000 step/タスク）・epoch ごとに順序を引き直す・cross-entropy
- **最適化**: Adam(0.9, 0.999, 1e−8)・lr **0.001**・moment はタスク跨ぎで保持・重みもリセットしない
- **ネット**: **3072–100–100–10** MLP（隠れ層は MNIST 版と同一）・init は U(±1/√fan_in)
- **seed 0–9**。乱数 role: `rlc_subset` / `rlc_labels` / `rlc_batch` / `init`

### 2.2 腕（7 本・MNIST 版と同一）

`R` / `LR` / `SNA`(c=0.6, β=0.01) / `R+l2` / `LR+l2` / `SNA+l2` / `R+l2init`、λ=1e−3。

### 2.3 測る量

MNIST 版と同一（`online_acc`＝更新前バッチ精度の平均・`memo_acc`・層別 mobility/zbar/zsd/dead_frac/w_norm/eff_rank・`SNA` の α 統計と clip 率）。

### 2.4 本走が答えないこと

CNN・自然画像の分類タスク・5+1 CIFAR・入力正規化・λ の走査・c の走査・深さの変更。

## 3. 登録判定

評価窓 = **タスク 31–50** の `online_acc` 平均。seed 対応・符号検定（両側）＋平均±SE。**n < 10 のときは「反対 seed が 1 本以下かつ p<0.05」を有意とする**（n=10 なら 9/10 と厳密に同じ・[[RandomLabelMNIST結果_0906]] で採った読み）。

### 3.1 主判定 Q1 — 差は MNIST より開くか

`SNA+l2` − `R+l2`:

| 条件 | ラベル |
|---|---|
| 有意 **かつ 平均差 ≥ +0.0233**（Random Label MNIST の値） | **`GAP_WIDENS`** |
| 有意だが +0.02 以上 +0.0233 未満 | `GAP_HOLDS` |
| 有意だが +0.02 未満 | `GAP_NARROWS` |
| 有意でない／負 | `GAP_CLOSES` |

**ガード**: `R+l2` の窓平均が **< 0.30**（チャンス 0.10 の 3 倍未満）なら「WD が救えていない」ので `INCONCLUSIVE_WD_TOO_WEAK`。`SNA` の `memo_acc` が **< 0.90** なら「MLP が記憶しきれない」ので全 Q を `INCONCLUSIVE_CAPACITY`。

### 3.2 Q2 — c は入力分布に依らないか

`SNA` と `SNA+l2` の mobility L1（窓 31–50・中央値）と clip 率:

| 条件 | ラベル |
|---|---|
| 両腕とも mob ∈ [0.50, 0.85] **かつ** clip < 5% | **`C_TRANSPORTS`** |
| 片方のみ | `C_PARTIAL` |
| どちらも外／clip ≥ 5% | `C_DOES_NOT_TRANSPORT`（c は箱ごとに要調整＝「チューニング不要」の主張が崩れる） |

### 3.3 Q3 — Snake 固有か（REPORT・MNIST で +0.0149 だった）

`SNA+l2` − `LR+l2`。

### 3.4 REPORT_ONLY

`R` の崩落タスク・`memo_acc`・‖w‖ 比・層比 L2/L1（[[RandomLabelMNIST結果_0906]] §5b-4 の項目 16）・素の `SNA` の位置・`SNA+l2` − `R+l2init`。

## 4. 検査

- **S-data**: CIFAR-10 の sha256。1200 枚が全タスク・全腕で同一（bit）、重複なし
- **S-labels**: 一様（χ² p>0.01）・タスク間独立（一致率 0.10±0.02）・腕を跨いで bit 一致
- **S-init**: 3072–100–100–10 の初期重みが腕を跨いで bit 一致
- **S-online**: `online_acc` が更新前の予測であること（1 バッチ手計算）
- **S-capacity**（新規・§1.1-2）: `SNA` seed 0 を 2 タスクだけ回し `memo_acc` ≥ 0.90 を確認。**下回れば本走を止めて設計変更**
- **S-repro**: 1 腕 seed 0・2 タスク（epoch 2）を 2 回で CSV byte 一致
- **S-div** / **S-cost**（1 腕 2 タスクの壁時計 → 70 run の見積もり）

## 5. 出力

`results/pmnist_rlcifar_0907/<arm>/per_task.csv`・`provenance.json`（CIFAR sha256・1200 枚 index の sha256・λ・c・β・git hash）・`verdict.csv`・`summary.md`。

## 6. 予測（Claude・2026-09-07・実装前）

1. **Q1 = `GAP_WIDENS`。** `SNA+l2` − `R+l2` ≥ +0.03。Kumar の表で L2 と L2 Init の差が MNIST 0.15 → CIFAR 0.21 と 1.4 倍なので、当方の +0.0233 も同程度に伸びる。確信 **中**
2. **Q2 = `C_TRANSPORTS`。** 適応 α は W を測って追随するので入力分布が変わっても帯に落ちる。確信 **中〜高**。外れるなら clip 下限 0.05 に当たる側（CIFAR の W が MNIST より大きい）
3. **`R` は MNIST（task 3）より**早く**崩落する。** 入力次元が 4 倍で第 1 層の z の分散が大きく、沈下が速い。確信 中
4. **`memo_acc` は全腕 ≥ 0.95**（1200 枚・30,000 step は 3072 次元でも足りる）。確信 中。**これが外れると S-capacity で本走が止まる**
5. **素の `SNA` がまた全腕最高。** 記憶課題では正則化が容量税（MNIST と同じ）。確信 中
6. **Q3 は MNIST（+0.0149）と同程度以上。** 確信 低〜中
7. **層比 L2/L1 は Snake だけ > 1**（項目 16 が入力分布に依らない）。確信 中
8. **外れたときに第一に疑うもの**: 前処理（`/255` のみでチャネル正規化なし）。CIFAR は MNIST と違って画素が全チャネルで広く分布するので、第 1 層の W が大きく出て c=0.6 が合わない可能性

**起草側（Claude）の予測であり独立の予言ではない。**

## 7. 実行

seed 逐次で走らせ、**6 seed 完了時点（符号検定が p=0.031 に届く）で中間判定**を出す。8 時間で 6–7 seed の見込み。残りは走らせ切る。

## 引用制限

- **Random Label CIFAR を「CIFAR での検証」と書かない。** 乱数ラベルの記憶であり視覚構造を使わない。CNN・自然画像タスクの証拠にはならない（§1.1-4）
- **Kumar の表の値と当方の値を直接比べない**（彼らは別ネット・別 λ・online 精度の定義も要確認）
- **`GAP_WIDENS` が出ても「活性化 > 正則化」と書かない。** 階級 B+C 対 C の比較（[[PermutedMNIST_適応α_spec_0905]] §2.1）
- **c=0.6 が transport しても「チューニング不要」を一般化しない。** MNIST 系 2 種＋CIFAR 1 種の 3 点
