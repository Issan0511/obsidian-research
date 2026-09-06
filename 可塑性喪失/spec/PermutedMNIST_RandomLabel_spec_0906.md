# Random Label MNIST × 適応 α Snake（WD が失敗すると報告されている箱で、正則化の下でも活性化は効くか）

親: [[PermutedMNIST_適応α結果_0905]]（Q4 `B_BELOW_C`・WD 3 腕で `SNA+l2` − `R+l2` = +0.0023）／[[PermutedMNIST_追加診断_0905]] §11–§14 / 状態: **起草（v1・Claude）・予測 §6 記入済み（Issa 指示により Claude のみ）・実装前** / 作成 2026-09-06 / 出典チャット: `活性化プロット_0904`
関連: [[PermutedMNIST_適応α_spec_0905]]／[[PermutedMNIST結果_0905]]／[[引用禁止]]

> **run id: `pmnist_rlmnist_0906`。** 宿主は `src/pmnist_0905.py`（init・Adam・l2/l2init フック・`AdaptiveSnake`・`evaluate` を import）。**新モジュール `src/pmnist_rlmnist_0906.py`** に置き、宿主の登録経路は 1 ビットも変えない。実装は Opus subagent（Issa 指示）。
> **本 spec は [[運用ルール]] §3 の自動起案ではない。** 2026-09-06 のチャットで Issa が「Random Label MNIST 実装してください」と指示した。
> 順序: §6 予測 → 本 spec commit → 実装＋検査＋煙試験 → 本走。

---

## 0. 一行

**Permuted MNIST では WD が活性化の差を吸収した（`SNA+l2` − `R+l2` = +0.23 pt）。原典の表で WD が失敗する唯一の MNIST 箱 — Random Label（概念シフト・記憶が要る）— で同じ 7 腕を並べ、その吸収が箱固有か一般かを決める。**

## 1. なぜ回すか

| 材料 | 出所 | 格 |
|---|---|---|
| Permuted MNIST・箱 A で `SNA+l2` − `R+l2` = +0.0023・10/10。ノルム制御がほぼ全部 | [[PermutedMNIST_追加診断_0905]] §11 | 未登録 |
| Kumar et al. Fig. 2（Adam）: Random Label MNIST で **L2 0.71・L2 Init 0.86・CBP 0.92・Baseline 0.16** | 原典 | 文献 |
| Lillo & Cheney 表 2（Adam・WD なし）: Random Label MNIST で **ReLU 20.03%・Leaky 91.53%・Deep Fourier 92.61%** | 原典 | 文献 |
| 適応 α は箱を替えても mob 0.70・2αW 1.20 に落ちる | [[PermutedMNIST_適応α結果_0905]] Q1 | 登録済み |

**動機**: Issa「活性化頑張らなくても l2 だけで十分に可塑性防げるの悲しい」「負け惜しみするならタスクが簡単すぎる？」。原典の表は、その負け惜しみが**表の別の列に既に書いてある**ことを示している（WD は概念シフトで 15 pt 負ける）。生きたゲートが正則化の下で価値を持つ場所があるなら、ここである。

### 1.1 先に書いておく危険

1. **λ=1e−3 が弱すぎて `R+l2` が素の `R` と同じく崩落する。** その場合 `SNA+l2` − `R+l2` は巨大になるが「WD が仕事をしていない」せいで、活性化の主張には使えない → `R+l2` − `R` を必ず併記し、`R+l2` が崩落（online 精度 < 0.5）なら **λ=1e−2 で再走**（Kumar の最良値）を段 2 として登録しておく
2. **1200 枚を 400 epoch は過学習が目的**なので test 精度は無意味。指標は online 精度（更新前バッチ）と記憶完了率（タスク末尾の 1200 枚精度）
3. **30,000 step/タスクで Snake の ‖w‖ が大きく育つ**（記憶はノルムを押し上げる）。適応 α は W に追随するが、W が 3 を超えると α_i が下限 0.05 に当たる可能性 → clip 率を記録
4. **費用**: 1.5M step/run。Permuted の 12 倍。7 腕 × 10 seed = 70 run ≈ 4 並列で 5 時間（S-cost で確定）

## 2. 設計

### 2.1 箱（Kumar et al. §4.2・Lyle et al. 2023 変種・登録）

- **データ**: MNIST 訓練 60,000 から **1200 枚を seed ごとに 1 度だけ**無作為抽出（層化しない・原典に従う）。全タスクで同じ 1200 枚
- **タスク**: 各画像に **一様乱数のラベル ∈ {0..9}** を独立に割り当て直す。タスクごとに新しいラベル。**50 タスク**
- **訓練**: **400 epoch/タスク**・batch 16（1200/16 = 75 step/epoch → 30,000 step/タスク）・epoch ごとに順序を引き直す・cross-entropy
- **最適化**: Adam(0.9, 0.999, 1e−8)・lr 0.001・moment はタスク跨ぎで保持・重みもリセットしない
- **ネット**: 784–100–100–10（Lillo & Cheney と同一・本走と地続き）・init は宿主と同じ U(±1/√fan_in)
- **seed 0–9**。seed は 1200 枚の抽出・ラベル列・batch 順・init を決める。乱数は role 別 stream（`rl_subset` / `rl_labels` / `rl_batch`・init は宿主の `init`）

### 2.2 腕（7 本・階級は [[PermutedMNIST_適応α_spec_0905]] §2.1）

| 腕 | 階級 | 役割 |
|---|---|---|
| `R` | A | 崩落の確認（参照 20%） |
| `LR` | A | 非ゼロ床の対照（参照 91.5%） |
| **`SNA`**（c=0.6・β=0.01） | B | 主対象・素 |
| `R+l2`（λ=1e−3） | C | **主判定の相手**。参照 Kumar 0.71 |
| **`SNA+l2`**（λ=1e−3） | B+C | **主判定** |
| `R+l2init`（λ=1e−3） | C | 最強の既存手法。参照 0.86 |
| `SNA+l2init`（λ=1e−3） | B+C | アンカーの差 |

### 2.3 測る量（タスクごと）

- **`online_acc`**: 30,000 バッチの**更新前**バッチ精度の平均（Kumar の average online task accuracy）
- **`memo_acc`**: タスク末尾で 1200 枚に対する精度（記憶完了率）
- 宿主 `evaluate()` の全量を **1200 枚上で**（test 集合が無い箱なので入力集合で測る）: `mobility`・`zbar`・`zsd`・`dead_frac`・`w_norm`・`eff_rank`・`SNA` の α 統計（`alpha_med`・clip 率・`2αW`）

### 2.4 本走が答えないこと

Random Label CIFAR・5+1 CIFAR・λ の走査（段 2 の 1e−2 のみ）・c の感度・CBP/SnP・学習可能 α・500 タスク。

## 3. 登録判定

評価窓 = **タスク 31–50** の `online_acc` 平均。seed 対応・符号検定（n=10・両側）＋対応差の平均±SE。

### 3.1 主判定 Q1 — 正則化の下で活性化は効くか

`SNA+l2` − `R+l2`:

| 条件 | ラベル |
|---|---|
| 9/10 以上・p<0.05・**かつ対応差の平均 ≥ +0.02** | **`ACTIVATION_MATTERS_UNDER_WD`**（Permuted の +0.0023 から桁で開いた） |
| 有意だが平均 < +0.02、または有意でない | `WD_ABSORBS`（Permuted と同じ結末が一般化） |
| `SNA+l2` < `R+l2` が有意 | `SNAKE_WORSE_UNDER_WD` |

**ガード**: `R+l2` の窓平均が **< 0.50** なら「WD が仕事をしていない」ので Q1 は `INCONCLUSIVE_WD_TOO_WEAK` とし、段 2（λ=1e−2）へ。

### 3.2 Q2 — 既存最強に対して

`SNA+l2` − `R+l2init`: 9/10 で上 → `B_ABOVE_C`／有意差なし → `B_WITHIN_C`／9/10 で下 → `B_BELOW_C`。

### 3.3 Q3 — 素の活性化として

`SNA` − `R`（崩落するか）と `SNA` − `LR`（非ゼロ床との差）。REPORT。

### 3.4 REPORT_ONLY

`memo_acc`・‖w‖ 比・mobility・α 統計・`R+l2` − `R`（WD の効き）・アンカー差 `SNA+l2` − `SNA+l2init`・崩落の時点（`R` の online 精度が 0.5 を割るタスク）。

## 4. 検査

- **S-subset**: 1200 枚が全タスクで同一（bit）・全腕で同一・重複なし
- **S-labels**: ラベルが各タスクで一様（χ² p>0.01）・タスク間で独立（相関 ≈ 0）・全腕で bit 一致
- **S-init**: 初期重みが宿主 `init_params` と bit 一致（腕を跨いで同一）
- **S-online**: `online_acc` が**更新前**の予測で計算されていること（1 バッチで手計算と一致）
- **S-act / S-detach / S-clip**: 宿主の `checks_adapt.py` を継承（`SNA` のみ）
- **S-repro**: 1 腕 seed 0・2 タスク（epoch 2）を 2 回走らせ CSV が byte 一致
- **S-div**: 非有限で腕を落とす
- **S-cost**: 1 腕 1 seed 2 タスク（400 epoch）の壁時計 → 70 run の見積もりを §8 に

## 5. 出力

`results/pmnist_rlmnist_0906/<arm>/per_task.csv`・`provenance.json`（データ sha256・1200 枚の index の sha256・λ・c・β・git hash）・`verdict.csv`・`summary.md`。

## 6. 予測（Claude・2026-09-06・実装前。Issa 指示により Issa 欄は設けない）

1. **素の `R` は崩落する** — online 精度が 10〜20 タスクで 0.3 を割り、窓では ≈ 0.2（Lillo & Cheney 20.03% と同桁）。確信 高
2. **素の `SNA` は崩落しない** — 窓で ≥ 0.85（leaky 91.5%・Deep Fourier 92.6% と同じ側）。確信 高。`SNA` − `R` は +0.6 以上・10/10
3. **`SNA` 対 `LR`: ±2 pt・符号不定。** 非ゼロ床であれば足りる箱で、周期性の追加価値は小さい。確信 低〜中
4. **主判定 Q1 = `ACTIVATION_MATTERS_UNDER_WD`。** `SNA+l2` − `R+l2` ≥ +0.05・10/10。Kumar の L2 0.71 対 L2 Init 0.86 の 15 pt は「ユニットを生かす」から来ており、`SNA` は生かし方が違っても同じ側。確信 中。**外れ方**: λ=1e−3 で `R+l2` が崩落（危険 1）→ `INCONCLUSIVE_WD_TOO_WEAK`。これが最もありそうな外れ方で、その場合は段 2
5. **Q2 = `B_BELOW_C`** — `R+l2init` が `SNA+l2` を 0〜5 pt 上回る（Kumar でも l2init が L2 系最強）。確信 低〜中。**ここで `B_WITHIN_C` 以上なら Snake の居場所が初めて数字になる**
6. **`SNA+l2` の ‖w‖ 比は 3〜6 倍**（記憶がノルムを押し上げる）、`R+l2init` は ≤ 1.5 倍。確信 中
7. **適応 α は 2αW = 1.20 に落ちる**が、α_med は箱 A（0.30）より小さい（W が大きい）。clip 率 < 5%。確信 中
8. **`memo_acc`（記憶完了率）は online より 5〜10 pt 高く、崩落した `R` だけ 0.3 未満。** 確信 中
9. **外れたときに第一に疑うもの**: λ（Kumar は 1e−2 が最良）。次に、1200 枚上で測る mobility が Permuted の test 集合上の値と比較不能であること

**起草側（Claude）の予測であり独立の予言ではない。** 今夜の全結果と原典 2 本の表を見たあとに立てている。

## 7. 段 2（条件付き・登録）

Q1 が `INCONCLUSIVE_WD_TOO_WEAK` のときのみ: `R+l2`・`SNA+l2`・`R+l2init`・`SNA+l2init` を **λ=1e−2** で再走（4 腕 × 10 seed）。判定は §3 と同一。

## 引用制限

- **`SNA+l2` が `R+l2` に勝っても「活性化だけで」と書かない**（階級 B+C）
- **`R+l2` の崩落を「WD は効かない」と書かない**（λ が弱いだけの可能性・段 2 まで保留）
- **1200 枚上の mobility を Permuted の test 上の値と直接比べない**
- **online 精度と `memo_acc` を混ぜない**（Kumar と比べるのは online）
- **Permuted の結論（WD が吸収）をこの箱の結果で上書きしない。両方書く**
