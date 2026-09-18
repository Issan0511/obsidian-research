---
aliases:
  - V-b 真の版
  - V-b 不動性
  - σ 中央値不動性
  - wnorm 不動性
description: V-b 判定基準の真の版検証。σ 中央値変化 5 arm 実測と proxy ‖w‖ との 6-7 倍差の解剖
---

# V-b 真の版・wnorm 不動性

親: [[00_概要と5判定基準_0918]] / 状態: **決着** / 更新: 2026-09-18

## 1. 主張

**σ 中央値変化 max 3.3% で V-b 判定 (± 5% 以内) 成立。proxy ‖w‖ 変化 max 0.55% との 6-7 倍差は $\Sigma_{XX}$ の free subspace 集中で説明される。**

これは Landing A の判定基準 3 ([[00_概要と5判定基準_0918]] 参照)。

## 2. 反証条件

以下のいずれかが観測されたら V-b 判定は棄却される:

1. 他 seed 群 (seed = 10-19 等) または他 arm で **σ 中央値変化が 10% を超える** arm が現れる
2. σ 中央値変化と proxy ‖w‖ 変化の **6-7 倍差が他 seed で再現しない** (比が [4, 10] の範囲を外れる)
3. Free subspace の敏感度 (σ の free subspace 集中) が他 seed で再現しない (σ_i = 0.5 · ‖w_i[15:20]‖ の相対誤差 > $10^{-6}$)

## 3. V-b 判定基準の定義

V-b は「500 tasks の SGD で σ_i の集団中央値がほぼ不動である」ことを要求する。具体的には:

$$\Delta_{\rm rel} \sigma = \frac{\mathrm{median}_i[\sigma_i^{\rm task=500}] - \mathrm{median}_i[\sigma_i^{\rm task=0}]}{\mathrm{median}_i[\sigma_i^{\rm task=0}]}$$

**target**: 全 arm で $|\Delta_{\rm rel} \sigma| \le 5\%$。

σ_i の per-unit 式 (詳細 [[02_V-a真の版_有界性_0918]] §4):

$$\sigma_i = 0.5 \cdot \|w_i[15:20]\|_2$$

したがって V-b は「free subspace への重みノルム分布の中央値が SGD で保存される」ことと等価。

## 4. 実測: σ 中央値変化 (5 arm × 10 seed)

Task 0 vs task 500 の集団中央値 (100 unit × 10 seed で median):

| arm    | $\eta$                | median σ (task=0) | median σ (task=500) | $\Delta_{\rm rel} \sigma$ | 判定  |
| ------ | --------------------- | ----------------- | ------------------- | ------------------------- | --- |
| lr0156 | $1.56 \times 10^{-4}$ | 0.3487            | 0.3540              | +1.52%                    | ✓   |
| lr02   | $2.0 \times 10^{-4}$  | 0.3492            | 0.3553              | +1.75%                    | ✓   |
| lr05   | $5.0 \times 10^{-4}$  | 0.3512            | 0.3586              | +2.11%                    | ✓   |
| lr10   | $1.0 \times 10^{-3}$  | 0.3506            | 0.3600              | +2.68%                    | ✓   |
| lr25   | $2.5 \times 10^{-3}$  | 0.3548            | 0.3667              | **+3.35%**                | ✓   |

- **max 変化**: lr25 で +3.35% ($\eta$ が最大の arm)
- **全 arm で $|\Delta_{\rm rel} \sigma| < 5\%$** — V-b 判定 ✓
- **単調増加**: $\eta$ が大きいほど σ 中央値が大きく成長 (SGD の Term II 積累によるドリフト・詳細は [[04_Term_I_II分解と3レジーム_0918]])

## 5. Proxy 版 ($\|w\|$ の中央値変化) との比較

同じ 500 tasks について、proxy 版として使われていた $\|w_i\|_2$ (20 dim 全体) の中央値変化:

| arm    | $\eta$                | median ‖w‖ (task=0) | median ‖w‖ (task=500) | $\Delta_{\rm rel} \|w\|$ | true 版比 |
| ------ | --------------------- | ------------------- | --------------------- | ------------------------ | ------- |
| lr0156 | $1.56 \times 10^{-4}$ | 0.7847              | 0.7828                | -0.24%                   | 6.33×   |
| lr02   | $2.0 \times 10^{-4}$  | 0.7853              | 0.7834                | -0.24%                   | 7.29×   |
| lr05   | $5.0 \times 10^{-4}$  | 0.7899              | 0.7874                | -0.32%                   | 6.60×   |
| lr10   | $1.0 \times 10^{-3}$  | 0.7887              | 0.7854                | -0.42%                   | 6.38×   |
| lr25   | $2.5 \times 10^{-3}$  | 0.7986              | 0.7942                | -0.55%                   | 6.09×   |

- **‖w‖ は僅かに減少** ($\Delta_{\rm rel} \|w\| \in [-0.55\%, -0.24\%]$)
- **σ は僅かに増加** ($\Delta_{\rm rel} \sigma \in [+1.52\%, +3.35\%]$)
- **比 6-7 倍**: σ の変化は ‖w‖ の変化の 6-7 倍 (符号も反対)

## 6. 6-7 倍差の解剖 ($\Sigma_{XX}$ の集中)

なぜ σ は ‖w‖ の 6-7 倍の変化を示すか。$\sigma_i$ と $\|w_i\|$ の関係を分解する。

### 6.1 $\sigma_i^2 / \|w_i\|^2$ の期待値

Isotropic $w_i$ (一様分布) の下では:

$$\frac{\sigma_i^2}{\|w_i\|^2} = \frac{0.25 \cdot \|w_i[15:20]\|^2}{\|w_i\|^2} = 0.25 \cdot \frac{\|w_i[15:20]\|^2}{\|w_i\|^2}$$

Isotropic 期待値: $\mathbb E[\|w_i[15:20]\|^2 / \|w_i\|^2] = 5/20 = 0.25$、したがって $\mathbb E[\sigma^2/\|w\|^2] = 0.25 \times 0.25 = 0.0625$、$\mathbb E[\sigma/\|w\|] \approx 0.5 \times \sqrt{0.25} = 0.25$。

### 6.2 実測の cos 集中

しかし 5M ckpt (task 0 開始時) では:

| arm    | median cos(w, free-subspace) | median $\sigma/\|w\|$ |
| ------ | ---------------------------- | --------------------- |
| lr0156 | 0.888                        | 0.4442                |
| lr02   | 0.888                        | 0.4438                |
| lr05   | 0.899                        | 0.4497                |
| lr10   | 0.897                        | 0.4483                |
| lr25   | 0.901                        | 0.4507                |

- cos ≈ 0.90 (isotropic の $\sqrt{0.25} = 0.5$ より遥かに集中)
- σ/‖w‖ ≈ 0.44-0.45 ≈ 0.5 · 0.9 = 0.45 (整合)

**5M pretrain で w_i の重みは free subspace に強く集中**している。cos(w, free) ≈ 0.9 の状態。

### 6.3 集中による感度増幅

Task 500 で ‖w‖ が僅かに減少するとき、その減少が **free subspace の重み** $w_i[15:20]$ に集中すると σ の変化が拡大される:

$$\Delta \sigma \approx \frac{\partial \sigma}{\partial \|w[15:20]\|} \cdot \Delta \|w[15:20]\| = 0.5 \cdot \Delta \|w[15:20]\|$$

$$\Delta \|w\|^2 \approx 2 \|w[15:20]\| \Delta \|w[15:20]\| + (\text{fixed subspace 分})$$

Fixed subspace 分が **相殺** (task 0 の学習で fixed に必要な重みが安定) すれば、‖w‖ 全体は小さく変化するが、free subspace への変化は残る → σ の変化が ‖w‖ の変化を大きく上回る。

Kubo の実測 6-7 倍は、fixed subspace の重みが SGD 中に僅かに縮小 ($ \|w[0:15]\|$ 減少・全体 ‖w‖ を下げる) しつつ、free subspace の重みは僅かに成長 ($\|w[15:20]\|$ 増加・σ を上げる) という **subspace 分別的な運動** を示している。

## 7. 意味 (V-b が保つもの・保たないもの)

**V-b は保つ**:
- σ の集団中央値の不動性 (< 5%)
- ‖w‖ 集団中央値の不動性 (< 1%)
- 統計的な集団構造の安定性

**V-b は保たない**:
- 個別 unit の σ (per-unit の $|d_{\rm true}|$ は最大 7.4 に達する・[[02_V-a真の版_有界性_0918]])
- 個別 unit の w (per-unit は task 内で refit で大きく動く)
- Fixed subspace vs free subspace の分別的な運動 (これは V-b の主張範囲外)

V-a と V-b の関係:
- V-a は「個別 event の $|d|$ 有界性」→ 分布の p99 が有界
- V-b は「集団の中央値不動性」→ 分布の中央が安定
- 両者が成立すれば「集団も個別も (extremal を除いて) 有界」となり、$\bar z_{\rm width}$ が長期でも意味を持つ量として残ることが保証される

## 8. Provenance

- **source-result**: 
  - `~/project/Nakatsuka/claude/hole1_scripts/session20_out/mt_U1_bareK1_500tasks_v2_lr*.npz`
  - `~/project/Nakatsuka/claude/hole1_scripts/session20_out/all5arm_sigma_d.npz`
  - `~/project/Nakatsuka/claude/hole1_scripts/session20_out/verify_and_t500.npz` (Chat container で第 20 回に生成)
- **source-commit**: 本ノート起票時の teacher branch head
- **verified-on**: 2026-09-18
- **script**: [[12_再現用scripts_data_0918]] の `補助データ/scripts/chat_scripts/` の以下:
  - `verify_and_t500.py` — task 0 vs task 500 の σ, ‖w‖ 中央値比較 (5 arm)
  - `all5arm_sigma_d.py` — 5 arm 集計 (σ の CV, cos 統計)

## 9. Log

- 2026-09-18 起票 (第 20 回・V-b 真の版検証結果)
- σ 中央値変化の 5 arm 実測は第 20 回で Chat container で生成
- 6-7 倍差の解剖は Σ_XX の解析形 ([[02_V-a真の版_有界性_0918]] §3) と w の free subspace 集中 (cos ≈ 0.9) から導出
