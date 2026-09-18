---
aliases:
  - 駆動源 5 項式
  - 5 項式 per-event
  - kp0 branch 検証
  - T_0 T_1 T_4 T_5 Y_i
description: 駆動源 5 項式 (T_0 + T_1 + T_4 + T_5 + Y_i) の完全形と kp0 branch での per-event R² > 0.914 検証
---

# 駆動源 5 項式の per-event 検証

親: [[00_概要と5判定基準_0918]] / 状態: **決着** (kp0 branch は per-event R² > 0.914 で完結) / 更新: 2026-09-18

## 1. 主張

**per-task per-unit の $\Delta \bar z_i = T_0 + T_1 + T_4 + T_5 + Y_i$ の駆動源 5 項式は、kp0 branch (dead unit・$k_{\rm on,i} = 0$) では $Y_i = 0$ かつ $T_1 \approx 0$ で実質 3 項式 ($T_0 + T_4 + T_5$) に還元され、5 arm × per-unit で per-event R² > 0.914・slope 1.005 で予言する。**

これは [[06_Model_M4_v3i_joint_3判定_0918]] の kp0 branch の理論駆動化の直接的根拠。

## 2. 反証条件

以下のいずれかが観測されたら本主張は棄却される:

1. kp0 branch で他 seed の per-event R² が 0.5 未満に落ちる
2. kp0 branch の predicted vs actual の slope が 1 から相対 15% 以上乖離 (0.85 < slope < 1.15 を外れる)
3. Alive branch の $Y_i$ の閉形式が存在しない (詳細 [[08_Y_i閉形式_step_E_0918]] で反証条件別記)
4. $\kappa(\eta)$ と $c(\eta)$ の $\eta^{1}$ scaling が他 arm 系列で成立しない

## 3. 駆動源 5 項式の全体形

Per-task per-unit の集団平均前活性の変化:

$$\boxed{\Delta \bar z_i = T_0 + T_1 + T_4 + T_5 + Y_i}$$

各項の意味と数式:

### 3.1 $T_0$: 幾何 kick + offset

Task 切替 (1 bit flip) で:
- $fs$ が 1 bit 変わる
- $g = g(n_{\rm fixed})$ が再計算される
- 支持点行列 $X_c$ が更新される
- unit $i$ の $\bar z_i$ が **幾何的に** 変化する (SGD の前に)

**$T_0$ の数式**:

$$T_0 = \mathbb E_r[\text{new } z_i(x_r)] - \mathbb E_r[\text{old } z_i(x_r)] = w_i \cdot (\tilde\mu^{\rm new} - \tilde\mu^{\rm old})$$

ここで $\tilde\mu^{\rm new}, \tilde\mu^{\rm old}$ は新旧 task の support 平均。

Fixed bit の flip は $\tilde\mu$ に大きな変化を与える (例: bit 0 が 0 → 1 に flip すると $\tilde\mu_0$ が $-g \to 1-g$ で 1 変化)。

### 3.2 $T_1$: 一次 refit

Task 開始時の残差 $\delta'_r = \hat y(x_r) - y^{\rm new}(x_r)$ (SGD 開始前・32 支持点で計算) が SGD で refit される過程。unit $i$ が受ける contribution:

$$T_1 = -\eta v_i \sum_{t=1}^{T} \delta_t \varphi'(z_{i,t}) \cdot [\bar x^{\rm t\text{-avg}} - x_{r_t}]$$

より簡潔には、演算子応答 $\mathcal F(\mathcal K) \delta'$ を使う:

$$T_1 = -\eta v_i \cdot \bar\varphi'_i \cdot \tilde\mu \cdot \zeta$$

ここで $\zeta = [I - \mathcal F(\mathcal K)] \delta'$ は task 内で refit された残差量 ([[05_K_spectrumとF_K_decay_0918]] の演算子応答)。

- **0 次近似** ($\zeta \approx \delta'$): 全 refit 完了と仮定 → **$T_1^{0\text{th}}$**
- **真の値** ($\zeta = [I - \exp(-\eta T \mathcal K / 16)] \delta'$): 有限 $\eta T$ での partial refit → **$T_1^{\rm true}$**

Kp0 branch ($k_{\rm on,i} = 0$) では $\bar\varphi'_i = a = 0.03$ で小さい → **$T_1 \approx 0$**。

### 3.3 $T_4$: 雑音の浮力

SGD の 2 次項 (Langevin) からの contribution。unit $i$ の $\bar z_i$ を「浮かす」方向:

$$T_4 = \kappa(\eta) \cdot (-\bar z_i^{\rm kick})$$

$\kappa(\eta)$ は $\eta$ に線形 (audit-v1b §3-4 で $\kappa(\eta) \propto \eta$)。

$\kappa$ の解析形:
$$\kappa(\eta) = \eta \cdot \frac{v_i^2 \bar\varphi'^2}{2} \cdot \text{something related to Σ}$$

Dead unit ($k_{\rm on,i} = 0$) では $\bar\varphi'^2 = a^2$ で $\kappa$ が小さい → $T_4$ も小さい ただし non-zero。

### 3.4 $T_5$: 雑音ゲート経由

Band unit (crossing frequency $n_{\rm band, i} > 0$) の場合の SGD 由来の shift:

$$T_5 = -c(\eta) \cdot v_i^2 \cdot n_{\rm band, i}$$

$c(\eta)$ は $\eta$ に線形。$n_{\rm band, i}$ は unit $i$ の crossing 数 (band unit のみ non-zero)。

Kp0 branch では $n_{\rm band, i}$ が非零の場合と 0 の場合の両方あり得る (band unit は $k_{\rm on} = 0$ でも band に residuosity を持つ)。

### 3.5 $Y_i$: 井戸・押し項

Alive unit で残る contribution:

$$Y_i = \eta \cdot v_i \cdot \sum_{r \in \mathrm{on}(i)} \delta'_r \cdot m_r$$

近似的に (詳細 [[08_Y_i閉形式_step_E_0918]] の閉形式):

$$Y_i \approx c(\eta) \cdot v_i \cdot \sum_{r \in \mathrm{on}(i)} \delta'_r$$

Kp0 branch では $\mathrm{on}(i) = \emptyset$ ($k_{\rm on,i} = 0$) なので:

$$\boxed{Y_i^{\rm kp0} = 0}$$

## 4. kp0 branch の 3 項式閉形式

Kp0 unit で $T_1 \approx 0$ (§3.2)・$Y_i = 0$ (§3.5) から:

$$\boxed{\Delta \bar z_i^{\rm kp0} \approx T_0 + T_4 + T_5 = T_0 + \kappa(\eta)(-\bar z_i^{\rm kick}) - c(\eta) v_i^2 n_{\rm band, i}}$$

## 5. $\kappa(\eta)$ と $c(\eta)$ の scaling (5 arm)

第 20 回で 5 arm × per-unit-5term-verification から fitted:

| arm    | $\eta$                | $\kappa(\eta)$        | $c(\eta)$             | $\kappa / \eta$ | $c / \eta$ |
| ------ | --------------------- | --------------------- | --------------------- | --------------- | ---------- |
| lr0156 | $1.56 \times 10^{-4}$ | $9.36 \times 10^{-5}$ | $8.10 \times 10^{-4}$ | 0.600           | 5.19       |
| lr02   | $2.0 \times 10^{-4}$  | $1.20 \times 10^{-4}$ | $1.02 \times 10^{-3}$ | 0.600           | 5.10       |
| lr05   | $5.0 \times 10^{-4}$  | $3.05 \times 10^{-4}$ | $2.62 \times 10^{-3}$ | 0.610           | 5.24       |
| lr10   | $1.0 \times 10^{-3}$  | $6.20 \times 10^{-4}$ | $5.35 \times 10^{-3}$ | 0.620           | 5.35       |
| lr25   | $2.5 \times 10^{-3}$  | $1.62 \times 10^{-3}$ | $1.42 \times 10^{-2}$ | 0.648           | 5.68       |

- **$\kappa / \eta \approx 0.6$** (5 arm で 0.600-0.648 の narrow band)
- **$c / \eta \approx 5.3$** (5 arm で 5.1-5.7 の narrow band)

両者とも **$\eta$ に対して線形 scaling** ($\eta^{1}$) が確認される (audit-v1b §3-4 の予測と一致)。

## 6. per-event R² の実測 (5 arm × 100 unit × 500 tasks)

第 19 回の per-unit-5term-verification で全 event に対して predicted $\Delta \bar z_i$ (3 項式) vs actual $\Delta \bar z_i$ を計算:

### 6.1 5 arm 集計

| arm    | $\eta$                | slope (all events) | R² (all events) | R² (kp0 only) |
| ------ | --------------------- | ------------------ | --------------- | ------------- |
| lr0156 | $1.56 \times 10^{-4}$ | 1.003              | 0.918           | **0.936**     |
| lr02   | $2.0 \times 10^{-4}$  | 1.005              | 0.921           | **0.941**     |
| lr05   | $5.0 \times 10^{-4}$  | 1.007              | 0.916           | **0.928**     |
| lr10   | $1.0 \times 10^{-3}$  | 1.004              | 0.914           | **0.919**     |
| lr25   | $2.5 \times 10^{-3}$  | 1.006              | 0.917           | **0.923**     |

**5 arm 全て R² > 0.914** (all events)、**kp0 only は R² > 0.919** — 反証条件 (R² > 0.5) を大幅にクリア。

**Slope は 5 arm で 1.003-1.007** — target 1 ± 0.15 を大幅にクリア。

### 6.2 kp2 branch の residual R negative

kp2 branch (unit $i$ で $k_{\rm on,i} = 2$) では:

$$R^{\rm kp2} = \Delta \bar z_i^{\rm actual} - (T_0 + T_4 + T_5)$$

が **systematic に負 (-0.05 to -0.15)** で、これは $Y_i$ の contribution ([[08_Y_i閉形式_step_E_0918]]) が正で $\Delta \bar z_i^{\rm actual}$ を大きくしていることを反映。

第 20 回の予備解析:
- kp2 R median: -0.08 (η=1e-3)
- kp2 R median: -0.13 (η=2.5e-3)
- **η が大きいほど負 residual が大きい** → $Y_i$ の η 依存 ([[08]] の $c(\eta) \propto \eta$) と整合

### 6.3 Y_i の $v_i^2$ model による fit 試行 (棄却)

第 20 回の Chat preliminary で Y_i を $v_i^2$ でモデル化してみた:

$$Y_i^{\rm try(v²)} = \alpha(\eta) \cdot v_i^2$$

結果: R² < 0.03 (5 arm) — **$v^2$ 単体は Y_i の閉形式として棄却**。

正しい閉形式は Claude Code session 21 Step E で発見された $Y_i = c(\eta) v_i \sum_{r \in \mathrm{on}(i)} \delta'_r$ (詳細 [[08_Y_i閉形式_step_E_0918]])。

## 7. Landing A の中での意義

判定 1 の Model M4 kp0 branch (詳細 [[06_Model_M4_v3i_joint_3判定_0918]]) は本ノートで確立された **kp0 の 3 項式閉形式** ($T_0 + T_4 + T_5$) を直接使う。したがって:

- **kp0 branch は本ノートで理論駆動化された** (per-event R² > 0.914)
- **alive branch は本ノートでは未解決** ($Y_i \ne 0$ で 5 項式全体が要る) → [[08_Y_i閉形式_step_E_0918]] で扱う
- **完全理論駆動化 (Model M4-B)** は Claude Code session 21 で試みたが発散 → [[11_Model_M4-B発散の3大欠陥_0918]]

## 8. Provenance

- **source-result**: 
  - `~/project/Nakatsuka/claude/hole1_scripts/session20_out/per_unit_5term_verification_lr*.npz` (5 arm × 100 unit × 500 tasks の 5 項式 decomposition)
  - `~/project/Nakatsuka/claude/hole1_scripts/session20_out/kappa_c_scaling.csv` ($\kappa(\eta), c(\eta)$ の 5 arm fit)
- **source-commit**: 本ノート起票時の teacher branch head
- **verified-on**: 2026-09-18
- **script**: [[12_再現用scripts_data_0918]] の `補助データ/scripts/session20_scripts/` の以下:
  - `per_unit_5term_verification.py` — 5 arm × per-unit で $\Delta \bar z_i$ decomposition
  - `kappa_c_scaling_fit.py` — $\kappa(\eta), c(\eta)$ の η scaling fit
  - `alive_branch_decomp.py` — kp1, kp2 branch の R decomposition

## 9. Log

- 2026-09-18 起票 (第 19 回の per-unit-5term-verification と第 20 回の kp2 residual 解析)
- 5 項式の理論形 (T_0, T_1, T_4, T_5, Y_i) は audit-v1b (Kubo 内部文書) で確立
- kp0 branch の 3 項式還元は第 19 回で per-event R² > 0.914 確認
- $Y_i$ の $v^2$ モデルは第 20 回で R² < 0.03 で棄却・正しい閉形式は Claude Code session 21 Step E で発見 (詳細 [[08_Y_i閉形式_step_E_0918]])
- kp2 branch の R systematic negative は Y_i の η 依存と整合 ([[08]] の $c(\eta) \propto \eta$)
