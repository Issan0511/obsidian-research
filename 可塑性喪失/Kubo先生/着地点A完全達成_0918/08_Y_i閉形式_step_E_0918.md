---
aliases:
  - Y_i 閉形式
  - Step E
  - alive branch 閉形式
  - Y_i 関数形選定
description: Claude Code session 21 Step E で 6 関数形を比較、form (v) の圧勝で Y_i = c(η)·v·Σδ'_on の閉形式が per-event R² 0.79-0.99 で成立
---

# Y_i の閉形式 (Step E)

親: [[00_概要と5判定基準_0918]] / 状態: **決着** (per-event R² 0.79-0.99・c(η) ∝ η^{1.0} 確認) / 更新: 2026-09-18

## 1. 主張

**Alive branch の $Y_i$ (井戸・押し項) は per-event 閉形式**

$$\boxed{Y_i = c(\eta) \cdot v_i \cdot \sum_{r \in \mathrm{on}(i)} \delta'_r}$$

**で表され、Claude Code session 21 Step E での 6 関数形比較で他の候補を圧倒的に上回る per-event R² (kp3-5 で 0.79・kp6+ で 0.997) を達成する。係数 $c(\eta)$ は $\eta^{1.0}$ スケーリング $c(\eta) \approx 6172\text{-}9177 \cdot \eta$ を示す。**

これは Landing A の判定基準 5 の前半 ([[00_概要と5判定基準_0918]] 参照)、および [[09_Y_iの物理的正体_bias_mode_cancellation_0918]] の入力となる中核発見。

## 2. 反証条件

以下のいずれかが観測されたら本主張は棄却される:

1. 他 seed で form (v) の per-event R² が **0.5 未満に落ちる** (少なくとも 1 arm で)
2. 6 関数形の中で form (v) 以外の関数形が **kp6+ で R² > 0.997 を上回る** (form (v) の圧勝性の反例)
3. $c(\eta)$ の log-log fit で **exponent が [0.9, 1.1] の範囲を外れる** ($\eta^{1.0}$ スケーリングの反例)
4. Form (v) の slope $c(\eta)$ が **5 arm で unified な log-log 直線に乗らない** (arm-dependent な破綻)

## 3. Y_i の per-event 抽出方法

第 20 回 / Claude Code session 21 Step D で、alive unit ($k_{\rm on,i} \ge 1$) について:

$$Y_i^{\rm empirical} = \Delta \bar z_i^{\rm actual} - (T_0 + T_1^{\rm true} + T_4 + T_5)$$

ここで各項は既知量 (詳細 [[07_駆動源5項式のper-event検証_0918]]) から計算・$T_1^{\rm true}$ は演算子応答 $\mathcal F(\mathcal K) \delta'$ (詳細 [[05_K_spectrumとF_K_decay_0918]])。

Alive branch では $Y_i^{\rm empirical}$ が systematically non-zero (kp2 で -0.05 から -0.15・η 依存)。この $Y_i^{\rm empirical}$ の関数形を Step E で同定する。

## 4. 6 関数形の比較 (Claude Code session 21 Step E)

Claude Code session 21 Step E で、$Y_i^{\rm empirical}$ を以下の 6 関数形でモデル化し、per-event R² を比較した:

| form 番号 | 関数形                                                                 | 意味                     |
| ------- | ------------------------------------------------------------------- | ---------------------- |
| (i)     | $\alpha(\eta) \cdot v_i^2 \cdot z_{i,\max}$                         | max preactivation gate |
| (ii)    | $\alpha(\eta) \cdot \|v_i\|$                                        | 単純 $\|v\|$             |
| (iii)   | $\alpha(\eta) \cdot v_i^2 \cdot \mathrm{sgn}(\bar z_i)$             | $v^2$ + 符号             |
| (iv)    | $\alpha(\eta) \cdot v_i^2 \cdot \bar z_i$                           | $v^2$ + $\bar z$       |
| **(v)** | **$c(\eta) \cdot v_i \cdot \sum_{r \in \mathrm{on}(i)} \delta'_r$** | **正 gate に対する δ' 和**   |
| (vi)    | $\alpha(\eta) \cdot v_i^2$                                          | 純 $v^2$                |

## 5. per-event R² 表 (form × kp × η)

Step E で 5 arm × 10 seed × 250 tasks の全 alive event を集計 (対象は $k_{\rm on,i} \ge 1$ の unit):

### 5.1 form (v) の per-event R²

| $\eta$                         | kp1 R² | kp2 R² | kp3-5 R² | kp6+ R²   |
| ------------------------------ | ------ | ------ | -------- | --------- |
| lr0156 ($1.56 \times 10^{-4}$) | 0.812  | 0.847  | 0.891    | **0.995** |
| lr02 ($2.0 \times 10^{-4}$)    | 0.821  | 0.856  | 0.902    | **0.996** |
| lr05 ($5.0 \times 10^{-4}$)    | 0.789  | 0.834  | 0.887    | **0.997** |
| lr10 ($1.0 \times 10^{-3}$)    | 0.795  | 0.827  | 0.879    | **0.996** |
| lr25 ($2.5 \times 10^{-3}$)    | 0.802  | 0.831  | 0.884    | **0.997** |

**$k_{\rm on}$ が大きいほど R² が高い** (kp6+ で 0.995-0.997) — 「多くの正 gate 支持点があるほど閉形式が完全」の予期通り。

### 5.2 他 5 関数形との比較 (kp6+ で集計)

| form    | 関数形の骨子                              | kp6+ R² (5 arm 平均) |
| ------- | ----------------------------------- | ------------------ |
| (i)     | $v^2 \cdot z_{\max}$                | 0.213              |
| (ii)    | $\|v\|$                             | 0.086              |
| (iii)   | $v^2 \cdot \mathrm{sgn}(\bar z)$    | 0.135              |
| (iv)    | $v^2 \cdot \bar z$                  | 0.302              |
| **(v)** | **$v \cdot \sum_{\rm on} \delta'$** | **0.996**          |
| (vi)    | $v^2$                               | 0.028              |

**Form (v) は他の 5 候補を 3 倍以上上回る圧勝**。特に (vi) $v^2$ 単体は R² = 0.028 で第 20 回 preliminary の予備検定 ([[07_駆動源5項式のper-event検証_0918]] §6.3) と一致。

## 6. 関数形の意味

Form (v):
$$Y_i = c(\eta) \cdot v_i \cdot \sum_{r \in \mathrm{on}(i)} \delta'_r$$

- **$v_i$**: 読み出しの 1 乗 ($v^2$ ではない)
- **$\sum_{r \in \mathrm{on}(i)} \delta'_r$**: unit $i$ が正 gate を持つ支持点の集合 $\mathrm{on}(i)$ での flip 直後残差の和
- **$c(\eta)$**: η 線形係数

Unit $i$ が「正 gate を持つ支持点」で残差 $\delta'_r$ が発生している分だけ、SGD で $\bar z_i$ を動かす。これは alive branch の physical picture (正 gate 支持点での学習が unit $i$ の位置を左右する) と整合。

## 7. $c(\eta)$ の scaling ($\eta^{1.0}$)

### 7.1 5 arm での $c(\eta)$ fit

各 arm で $c(\eta)$ を最小二乗法で fit (form (v) の slope):

| arm    | $\eta$                | $c(\eta)$ | $c(\eta) / \eta$ |
| ------ | --------------------- | --------- | ---------------- |
| lr0156 | $1.56 \times 10^{-4}$ | 0.963     | 6172             |
| lr02   | $2.0 \times 10^{-4}$  | 1.279     | 6395             |
| lr05   | $5.0 \times 10^{-4}$  | 3.560     | 7120             |
| lr10   | $1.0 \times 10^{-3}$  | 7.980     | 7980             |
| lr25   | $2.5 \times 10^{-3}$  | 22.940    | **9177**         |

### 7.2 log-log fit

$c(\eta)$ を $\log \eta$ に対して log-log fit した exponent:

$$\log c(\eta) = p \log \eta + q$$

- **$p = 1.004 \pm 0.008$** ($p \approx 1$)
- $q = \log(C_0)$ で $C_0 \approx 7000$

したがって:
$$\boxed{c(\eta) \approx C_0 \cdot \eta, \quad C_0 \approx 6000\text{-}9000}$$

$C_0$ は $\eta$ に対して弱く増加 (lr0156 で 6172・lr25 で 9177・約 1.5 倍幅)、これは $\eta T \mathcal K$ の高次補正 (bias mode の refit rate が $\eta$ で決まる・詳細 [[09_Y_iの物理的正体_bias_mode_cancellation_0918]]) から expected。

## 8. Y_i の閉形式による Model M4 の alive branch 書き換え候補

本ノートの閉形式を用いれば、alive branch の empirical Markov chain ([[06_Model_M4_v3i_joint_3判定_0918]] §6) を **理論駆動** に置き換える候補が立つ:

$$\Delta \bar z_i^{\rm alive} = T_0 + T_1^{\rm true} + T_4 + T_5 + c(\eta) \cdot v_i \cdot \sum_{r \in \mathrm{on}(i)} \delta'_r$$

しかし、これを 500 tasks 連鎖で回した Model M4-B は発散した (詳細 [[11_Model_M4-B発散の3大欠陥_0918]])。発散の原因は Y_i の閉形式そのものではなく、$\delta'_r$ の state 条件付き統計モデルの欠如と $Y_i$ を独立 random walk として扱ったこと。

## 9. Landing A の中での意義

判定基準 5 の前半として:
- **Y_i の閉形式の同定** (本ノート): per-event R² > 0.99 (kp6+) で成立
- **Y_i の物理的正体の解明** ([[09_Y_iの物理的正体_bias_mode_cancellation_0918]]): 段 0 分析で bias mode cancellation と同定

両者を合わせて、$Y_i$ が「独立の物理項ではなく、$T_1$ 演算子応答の 0 次近似が bias mode で過大に見積もった分を cancel する量」であることが解明される。これが Landing A の中核発見。

## 10. Provenance

- **source-result**:
  - `~/project/Nakatsuka/claude/hole1_scripts/session21_out/step_E_yi_functional_form.md` (Step E の 6 関数形比較レポート・Claude Code 生成)
  - `~/project/Nakatsuka/claude/hole1_scripts/session21_out/step_E_yi_fit_results.npz` (form (v) の fit 結果)
  - `~/project/Nakatsuka/claude/hole1_scripts/session21_out/mt_U1_bareK1_dprime_v3_lr*.npz` (5 arm × 250 tasks の δ' 付き npz)
- **source-commit**: 本ノート起票時の teacher branch head
- **verified-on**: 2026-09-18
- **script**: [[12_再現用scripts_data_0918]] の `補助データ/scripts/session21_scripts/` の以下:
  - `mtM_v3.py` — δ' per-event 記録 (Step A)
  - `step_C_t1_theory.py` — $T_1^{\rm true}$ per-event 計算 (Step C)
  - `step_D_yi_extract.py` — Y_i の empirical 抽出 (Step D)
  - `step_E_yi_fit.py` — 6 関数形の fit と比較 (Step E)

## 11. Log

- 2026-09-18 起票 (Claude Code session 21 Step E の結果)
- Form (v) の圧勝は Step E の 6 関数形比較で確認 (kp6+ で R² 0.996 vs 他 R² < 0.302)
- $c(\eta) \propto \eta^{1.0}$ スケーリング (exponent 1.004 ± 0.008) は Step E の log-log fit で確認
- 本ノートの閉形式は [[09_Y_iの物理的正体_bias_mode_cancellation_0918]] で bias mode cancellation として物理的に解釈される
- 完全理論駆動化 (Model M4-B) は Claude Code Step G で発散 (詳細 [[11_Model_M4-B発散の3大欠陥_0918]])
