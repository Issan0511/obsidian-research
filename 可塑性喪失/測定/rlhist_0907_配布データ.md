# rlhist_0907 — Random Label MNIST 前活性分布データ（配布用）

親: [[RandomLabelMNIST結果_0906]] §5b-4 / 状態: **配布中（2026-12-16 まで）** / 作成 2026-09-07
関連: [[PermutedMNIST_RandomLabel_spec_0906]]（事前登録）／[[論点/理論が説明すべき事実_0906|理論が説明すべき事実_0906]] 項目 16

**ダウンロード**: https://76.gigafile.nu/1216-d919e4b708fff6e4696213ad7624c2adf
**ファイル**: `rlhist_0907_npz.tar.gz`（398 KB・README.md ＋ npz 7 本）
**期限**: 2026-12-16（100 日）／削除キー `ff1d`
**アップロード**: 2026-09-07

```
tar xzf rlhist_0907_npz.tar.gz
python -c "import numpy as np; d=np.load('SNA.npz'); print(d.files, d['h1'].shape)"
```

読み込み例（アニメーションの再生）:

```python
import numpy as np, matplotlib.pyplot as plt
d = np.load("SNA.npz")
E = d["edges"]; ctr = (E[:-1] + E[1:]) / 2
t = 49                                  # タスク 50
plt.plot(ctr, d["h1"][t] / d["h1"][t].max())          # プール分布（第 1 層）
plt.hist(d["m1"][t], bins=E, density=True)            # 100 ユニットの平均前活性
plt.twinx().plot(ctr, 1 + np.sin(2 * 0.6 * ctr))      # φ'(z)（α=c=0.6 は初期値・実際は α_i）
```

---

# rlhist_0907 — Random Label MNIST の前活性分布（タスク別キャプチャ）

7 腕 × 50 タスク・seed 0。`preact_rl.gif` の元データ。**未登録の診断（REPORT_ONLY）。**

## npz の中身（1 腕 1 ファイル）

| key | shape | 意味 |
|---|---|---|
| `edges` | (241,) | ヒストグラムのビン境界。`-16.0 .. 8.0` を 240 等分 |
| `h1` | (50, 240) int64 | 第 1 層のプール前活性 z のヒストグラム。1200 画像 × 100 ユニット = 120,000 値をタスクごとに |
| `h2` | (50, 240) int64 | 第 2 層の同じもの |
| `m1` | (50, 100) float32 | 第 1 層の**ユニットごとの平均前活性** z̄ᵢ（1200 画像にわたる平均） |
| `m2` | (50, 100) float32 | 第 2 層の同じもの |
| `acc` | (50,) float64 | タスク末尾の 1200 画像に対する精度（= 記憶完了率 `memo_acc`） |

行 index はタスク 1..50。前活性はそのタスクのラベルで訓練し終えた**タスク末尾の状態**で、そのタスクの 1200 画像に対して測っている。

ファイル: `R.npz` `LR.npz` `SNA.npz` `R_l2.npz` `LR_l2.npz` `SNA_l2.npz` `R_l2init.npz`

## 実験設定

**箱: Random Label MNIST**（Kumar, Marklund, Van Roy 2024 §4.2 / Lyle et al. 2023 の変種）

- MNIST 訓練 60,000 から **1200 枚を seed ごとに 1 度だけ**無作為抽出（層化なし）。全タスクで同じ 1200 枚
- 各タスクで 1200 枚に **一様乱数のラベル ∈ {0..9}** を独立に割り当て直す。**50 タスク**
- **400 epoch/タスク**・batch 16（1200/16 = 75 step/epoch → **30,000 step/タスク**）・epoch ごとに順序を引き直す
- 損失 cross-entropy。**タスク間で重みも Adam の moment もリセットしない**

**ネット**: 784–100–100–10 MLP・bias あり・出力は線形。init は PyTorch `nn.Linear` 既定 U(±1/√fan_in)（活性化非依存）
**最適化**: Adam(β1=0.9, β2=0.999, eps=1e−8)・lr **0.001**
**seed**: 0（本走は 0–9。本キャプチャは seed 0 のみ）

**腕**

| ファイル | 活性化 | 介入 |
|---|---|---|
| `R` | ReLU | なし |
| `LR` | leaky ReLU (a=0.1) | なし |
| `SNA` | **適応 α Snake**: φ(z) = z + sin²(α_i z)/α_i、**α_i = clip(c/W_i, 0.05, 3.0)**、W_i = sqrt(EMA_β[var_batch(z_i)])、**c=0.6・β=0.01**、V_i の初期値 1、**ユニットごと・層ごと**、α は detach（BatchNorm の running statistics と同じ扱い） | なし |
| `R_l2` | ReLU | L2（原点へ）λ=1e−3・勾配に `2λp` を加算 |
| `LR_l2` | leaky | 同上 |
| `SNA_l2` | 適応 α Snake | 同上 |
| `R_l2init` | ReLU | L2-Init（初期値 θ₀ へ）λ=1e−3・勾配に `2λ(p−p₀)` を加算 |

**乱数**: role ごとに sha256 から独立の系列（`rl_subset` / `rl_labels` / `rl_batch` / `init`）。同 seed なら腕を跨いで 1200 枚・ラベル列・初期重みが bit 一致

## 本走との対応

本走 `pmnist_rlmnist_0906`（7 腕 × **10 seed**）の窓 31–50 の online 精度（更新前バッチ精度の平均・10 seed 中央値）:

| 腕 | online 31–50 | mobility L1 | ‖w‖ L1 比 |
|---|---|---|---|
| `R` | **0.1138**（task 3 で崩落） | 0.0000 | 1.35 |
| `LR` | 0.8076 | 0.114 | **16.92** |
| **`SNA`** | **0.9859**（全腕最高） | 0.558 | 5.31 |
| `R+l2` | 0.9412 | 0.233 | 0.92 |
| `LR+l2` | 0.9497 | 0.393 | 0.99 |
| `SNA+l2` | 0.9644 | 0.824 | 1.08 |
| `R+l2init` | 0.9579 | 0.289 | 1.00 |

本キャプチャは本走と別プロセスだが、**タスク 1 の `memo_acc` が 7 腕すべてで本走と一致**（`R_l2init` の 0.9992 まで）。同じ乱数系列・同じ軌跡。

## 出所

- 実装: `src/pmnist_rlhist_0907.py`（宿主 `src/pmnist_0905.py`・走モジュール `src/pmnist_rlmnist_0906.py` を import）
- 本走 git hash `ff3befe218b050850d6e0c783e80d66b36778e0b`
- MNIST sha256（train images）`440fcabf73cc546fa21475e81ea370265605f56be210a4024d2ca8f203523609`
- seed 0 の 1200 枚 index の sha256（昇順）`11411ac14aee613b8d2b24352b50a1953bb733225e3a50886432fb7aa0b259ff`
- 事前登録 spec: `可塑性喪失/spec/PermutedMNIST_RandomLabel_spec_0906.md`、結果: `可塑性喪失/測定/RandomLabelMNIST結果_0906.md`

## 読むときの注意

- **seed 1 本**。本走の判定（10 seed）とは別
- `h1`/`h2` はプール分布で、**ユニット内の広がり W とユニット間の散らばりの和**。ゲートの平均化に効く W とは別量（W は `m1` の分散をプール分散から引いて出す）
- `acc` は 1200 枚に対する記憶完了率であって test 精度ではない（この箱に test 集合は無い）
