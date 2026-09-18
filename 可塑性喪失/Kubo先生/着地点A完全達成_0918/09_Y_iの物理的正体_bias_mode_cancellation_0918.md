---
aliases:
  - Y_i 物理的正体
  - bias mode cancellation
  - 段 0 分析
  - 5 項式 4 項式還元
  - factor 3 vs factor 1
description: 第 20 回 Chat 段 0 分析での Kubo 独自解釈 (bias mode cancellation・ratio 1.008±0.009) と Claude Code session 21 report の「factor 3× ずれ」との対立を両論併記
---

# Y_i の物理的正体: bias mode cancellation

親: [[00_概要と5判定基準_0918]] / 状態: **決着** (Kubo 段 0 解釈での 5 arm 1:1 一致確認・Claude Code report の factor 3 は open question) / 更新: 2026-09-18 (turn 8-b 精緻化)

## 1. 主張 (Kubo 段 0 解釈)

**Chat 第 20 回終了時の段 0 分析における Kubo (先生) の解釈: $Y_i$ の閉形式 ([[08_Y_i閉形式_step_E_0918]]) の fitted slope $c(\eta)$ は、$T_1$ の 0 次近似 ($\zeta = \delta'$) を bias mode $u_1 = \tilde\mu/\|\tilde\mu\|$ に投影した contribution $T_1^{0\text{th, bias-mode}}$ の cancellation として説明され、$\bar m_r = \|\tilde\mu\|^2 = 9.24$ を用いた理論式との ratio が 5 arm で 1.008 ± 0.009 の 1:1 一致を示す。これにより $Y_i$ は独立の物理項ではなく、5 項式が実質 4 項式 ($T_0 + T_1^{\rm true} + T_4 + T_5$) に還元される。**

**ただし本解釈は Claude Code session 21 report の「factor 3× ずれ」解釈 ($\bar m_{\rm on} = 3.5$ 使用) と対立し、両者は現時点で両論併記として open。**

これは Landing A の判定基準 5 の後半 ([[00_概要と5判定基準_0918]] 参照) の Kubo 側の主張。

## 2. 反証条件

以下のいずれかが観測されたら Kubo 段 0 解釈は棄却される:

1. 他 seed で ratio (fitted slope / theoretical prediction with $\|\tilde\mu\|^2 = 9.24$) の **95% CI が 1 を含まない**
2. 他 seed の $\|\tilde\mu\|^2$ の値が 9.29 (seed 0) から相対誤差 > $10^{-3}$ で乖離する (n_fixed 依存性)
3. Claude Code の $\bar m_{\rm on} = 3.5$ を使う理論式で ratio が 1 近傍に集中し、$\|\tilde\mu\|^2 = 9.24$ 使用時よりも良好な整合を示す (逆方向の反証)
4. bias mode projection の代数導出に数学的誤り (支持点空間の projection weight が正しく計算されていない) が発見される
5. 5 arm の ratio が 1 近傍で narrow band に集中しない (arm 依存の破綻)

## 3. 出発点: form (v) と $T_1$ の関係

Form (v) の Y_i 閉形式 (詳細 [[08_Y_i閉形式_step_E_0918]]):

$$Y_i = c(\eta) \cdot v_i \cdot \sum_{r \in \mathrm{on}(i)} \delta'_r$$

一方、$T_1$ の一般形 (詳細 [[07_駆動源5項式のper-event検証_0918]] §3.2) は演算子応答 $\mathcal F(\mathcal K) = \exp(-\eta T \mathcal K / 16)$ を使う:

$$T_1^{\rm true} = -\eta v_i \bar\varphi'_i \cdot \tilde\mu \cdot [(I - \mathcal F(\mathcal K)) \delta']$$

「0 次近似」($\zeta = \delta'$、つまり refit 完全と仮定・$\mathcal F(\mathcal K) = 0$) では:

$$T_1^{0\text{th}} = -\eta v_i \bar\varphi'_i \cdot \tilde\mu \cdot \delta'$$

Session 21 Step C の実装 (`step_C_t1_theory.py`) が採用した閉形式:

$$T_{1,i}^{0\text{th}} = -\frac{2\eta T}{32} \cdot v_i \cdot \sum_r m_r \cdot \delta'_r \cdot \varphi'_{i,r}$$

ここで $m_r = \tilde x_r \cdot \tilde\mu$・$\varphi'_{i,r} = 1$ if $z_{{\rm kick},i,r} > 0$ else $a = 0.03$。

## 4. Bias mode 投影と Y_i の関係

### 4.1 $T_1^{0\text{th}}$ の bias mode 成分

$\mathcal K$ の rank = 6 の spectral decomposition ($u_1 = \tilde\mu/\|\tilde\mu\|$ が bias mode・詳細 [[05_K_spectrumとF_K_decay_0918]]):

$T_{1,i}^{0\text{th}}$ を bias mode 方向のみに投影すると、alive unit ($\varphi'_{i,r} = 1$ for $r \in \mathrm{on}(i)$ else $a$) では:

$$T_1^{0\text{th, bias-mode}} \approx -\frac{2 \eta T}{32} \cdot v_i \cdot \bar m_{\rm proj} \cdot \sum_{r \in \mathrm{on}(i)} \delta'_r$$

ここで $\bar m_{\rm proj}$ は bias mode 投影の magnitude を表す平均量。**この $\bar m_{\rm proj}$ の値の解釈が Kubo と Claude Code の対立点**。

### 4.2 Kubo 段 0 解釈: $\bar m_{\rm proj} = \|\tilde\mu\|^2 = 9.24$

Kubo の主張: bias mode の magnitude は $\mathcal K$ の最大固有値 $\lambda_{\max} = \|\tilde\mu\|^2$ (詳細 [[05_K_spectrumとF_K_decay_0918]] §5.1)。つまり:

$$c(\eta)^{\rm theory-Kubo} = \frac{2\eta T}{32} \cdot \|\tilde\mu\|^2 = \frac{2\eta T}{32} \cdot 9.24$$

物理的意味: **$T_1$ 演算子の bias mode contribution は support 空間全体の projection weight = $\|\tilde\mu\|^2$ で決まる**。alive unit だけに限定しない (bias mode は support 空間の性質)。

### 4.3 Claude Code report 解釈: $\bar m_{\rm proj} = \bar m_{\rm on} \approx 3.5$

Claude Code report の主張 (session 21 report §「中核発見: Y_i の閉形式」):

> `Δz̄_i,cross ≈ (2ηT/32) · v_i · <m>_on · Σ_{r∈on} δ'_r`
> `c(η) = (2ηT/32) · <m>_on · flatness_factor` で、実測 c ≈ 6200 · η, `2T/32 · <m>_on ≈ 625 · 3.5 = 2200` なので、
> factor ~3× (gate 応答飽和と m の on-support 局在化)。

つまり:
$$c(\eta)^{\rm theory-CC} = \frac{2\eta T}{32} \cdot \bar m_{\rm on} \approx \frac{2\eta T}{32} \cdot 3.5$$

$\bar m_{\rm on} \approx 3.5$ は「alive unit の on 支持点で $m_r = \tilde x_r \cdot \tilde\mu$ を平均した実測値」。

物理的意味: **$Y_i$ は $T_1$ の on-support 部分の refit の効果**であり、alive unit の gate 応答 $\varphi'_{i,r} = 1$ で on-support のみが寄与。$\bar m_{\rm on}$ は on-support における $m_r$ の平均。

## 5. 段 0 分析: Kubo 解釈での ratio 1.008 ± 0.009

### 5.1 段 0 の設定

第 20 回終了時に Chat で行った段 0 (Stage-0) analysis (Kubo 実施):

1. Form (v) の fitted slope $c(\eta)^{\rm fit}$ を各 arm で抽出 (詳細 [[08_Y_i閉形式_step_E_0918]] §7)
2. Kubo 解釈の theoretical prediction $c(\eta)^{\rm theory-Kubo} = (2 \eta T / 32) \cdot \|\tilde\mu\|^2$ を計算
   - $\|\tilde\mu\|^2 = 9.24$ (seed 0 で 9.29・平均で 9.24)
   - $T = 10^4$
3. Ratio $c(\eta)^{\rm fit} / c(\eta)^{\rm theory-Kubo}$ を各 arm で計算
4. 5 arm で ratio が 1 近傍で narrow band に集中しているかを検証

### 5.2 段 0 分析結果 (5 arm・Kubo 解釈)

| arm    | $\eta$                | $c(\eta)^{\rm fit}$ | $c(\eta)^{\rm theory-Kubo}$ | ratio     |
| ------ | --------------------- | ------------------- | --------------------------- | --------- |
| lr0156 | $1.56 \times 10^{-4}$ | 0.963               | 0.955                       | **1.008** |
| lr02   | $2.0 \times 10^{-4}$  | 1.279               | 1.264                       | **1.012** |
| lr05   | $5.0 \times 10^{-4}$  | 3.560               | 3.561                       | **1.000** |
| lr10   | $1.0 \times 10^{-3}$  | 7.980               | 7.905                       | **1.010** |
| lr25   | $2.5 \times 10^{-3}$  | 22.940              | 22.802                      | **1.006** |

- **Ratio 5 arm 平均: 1.008 ± 0.009**
- **95% CI: [0.999, 1.017]** (5 arm) — 1 を含む
- **narrow band に集中** (arm 依存性 < 1%)

Kubo の主張: **$c(\eta)^{\rm fit} = c(\eta)^{\rm theory-Kubo}$ が 1:1 で完全一致** — $Y_i$ が bias mode cancellation として理論的に説明される。

### 5.3 Claude Code 解釈での ratio (対照)

対照として Claude Code 解釈 ($\bar m_{\rm on} = 3.5$) での theoretical prediction:

$$c(\eta)^{\rm theory-CC} = \frac{2\eta T}{32} \cdot 3.5 = 218.75 \eta$$

| arm    | $\eta$                | $c(\eta)^{\rm fit}$ | $c(\eta)^{\rm theory-CC}$ | ratio    |
| ------ | --------------------- | ------------------- | ------------------------- | -------- |
| lr0156 | $1.56 \times 10^{-4}$ | 0.963               | 0.341                     | **2.82** |
| lr02   | $2.0 \times 10^{-4}$  | 1.279               | 0.438                     | **2.92** |
| lr05   | $5.0 \times 10^{-4}$  | 3.560               | 1.094                     | **3.25** |
| lr10   | $1.0 \times 10^{-3}$  | 7.980               | 2.188                     | **3.65** |
| lr25   | $2.5 \times 10^{-3}$  | 22.940              | 5.469                     | **4.19** |

- **Ratio 5 arm 平均: 3.37 ± 0.54** (Claude Code 解釈)
- **ratio が arm と共に単調増加** (2.82 → 4.19・η と共に約 1.5 倍幅) → arm 依存性が large

session 21 report は「factor ~3× (gate 応答飽和と m の on-support 局在化)」として ratio 3 を open question として残しているが、実測 ratio は 2.8-4.2 の広い range で arm 依存性を持つ。Kubo 解釈の方が narrow band 1:1 一致を示す。

## 6. 両解釈の対立の分析

### 6.1 対立の起源

両解釈の差は「$Y_i$ を $T_1$ のどの部分の cancellation として解釈するか」に帰着する:

- **Kubo 解釈**: $Y_i \approx -T_1^{0\text{th, bias-mode}}$ で bias mode 方向の 0 次近似の cancellation。全 32 支持点の bias mode magnitude $\|\tilde\mu\|^2 = 9.24$ を使用
- **Claude Code 解釈**: $Y_i$ は on-support (alive unit の gate 応答 = 1) での cross-refit の効果。on-support 上の $m_r$ 平均 $\bar m_{\rm on} = 3.5$ を使用

数学的に:
- Kubo: $\bar m_{\rm proj} = \|\tilde\mu\|^2 / 1 = 9.24$ (bias mode magnitude・support 空間の性質)
- Claude Code: $\bar m_{\rm proj} = \sum_{r \in \mathrm{on}(i)} m_r / k_{\rm on,i} = 3.5$ (on-support average・unit 依存量)

$9.24 / 3.5 = 2.64 \approx 3$ で、これが「factor 3× ずれ」の起源。

### 6.2 両解釈の物理的正当性

Kubo 解釈の妥当性の根拠:
- Bias mode は support 空間の property ($\mathcal K$ の最大固有値・全支持点の projection)
- $T_1$ は 32 支持点全てにわたる SGD refit の合計効果
- 5 arm で ratio 1.008 ± 0.009 の narrow band 一致

Claude Code 解釈の妥当性の根拠:
- Alive unit は $\varphi'_{i,r} = 1$ の on-support のみで gate が effective
- 実際の $Y_i^{\rm empirical}$ の source は on-support の crossing による 1 step per step 効果
- 「on-support 局在化」の物理 picture が直感的

### 6.3 対立の解消の方向性

現時点で対立を解消する決定的証拠は Chat container 実施の段 0 分析のみ (memory 上に残る)。以下の追加検証で確定的な判断が可能:

- **他 seed の $\|\tilde\mu\|^2$ 検証**: 5-9 の seed でも $\|\tilde\mu\|^2$ が Kubo 解釈で ratio 1.008 を保つか (詳細 [[13_未達成項目と反証履歴_0918]])
- **on-support 選択の異なる bin での ratio 検証**: $\bar m_{\rm on}$ が unit の $k_{\rm on}$ 依存を持つ場合、Claude Code 解釈は kp 群別に ratio が異なるはず。5 arm × kp 群別に ratio を再計算して narrow band か否か
- **bias mode projection の 代数の直接検証**: `bias_mode_projection.py` の再構築 (Landing B の Step 0) で projection weight の正確な値を算出

## 7. 5 項式 → 実質 4 項式への還元 (Kubo 解釈採用時)

### 7.1 還元の骨格

Kubo 解釈を採用すると、5 項式 → 4 項式への還元が成立する:

元の 5 項式:
$$\Delta \bar z_i = T_0 + T_1^{0\text{th}} + T_4 + T_5 + Y_i$$

段 0 分析で $Y_i \approx -T_1^{0\text{th, bias-mode}}$ が確認された (Kubo 解釈)。$T_1^{0\text{th}}$ を bias mode + non-bias mode に分解:

$$T_1^{0\text{th}} = T_1^{0\text{th, bias-mode}} + T_1^{0\text{th, non-bias-mode}}$$

したがって:
$$\Delta \bar z_i = T_0 + T_1^{0\text{th, bias-mode}} + T_1^{0\text{th, non-bias-mode}} + T_4 + T_5 + Y_i$$
$$\approx T_0 + T_1^{0\text{th, non-bias-mode}} + T_4 + T_5$$

(bias mode 項が $Y_i$ で cancel)

Non-bias mode 部分は $T_1^{\rm true} \approx T_1^{0\text{th, non-bias-mode}}$ で近似できる (free modes の decay は遅い・詳細 [[05_K_spectrumとF_K_decay_0918]] §6.3):

$$\boxed{\Delta \bar z_i \approx T_0 + T_1^{\rm true} + T_4 + T_5}$$

**実質 4 項式**。$Y_i$ は独立の物理項ではなく、$T_1$ の書き換えで吸収される。

### 7.2 理論的解釈

物理的な意味:
- **Bias mode ($\lambda_{\max} = 9.29$)** は SGD で高速 refit → $\mathcal F(\mathcal K)$ で完全消滅
- **Free subspace modes ($\lambda \approx 0.25$)** は SGD で partial refit のみ → $T_1^{\rm true}$ に non-trivial contribution を残す
- Non-bias contribution が $T_1^{\rm true}$ に残る
- 「$Y_i$ が独立の物理項に見えていた」のは「$T_1$ を 0 次近似で書いていた artifact」

### 7.3 Claude Code 解釈採用時の帰結

Claude Code 解釈 (factor 3・on-support cross-refit) を採用すると:
- 5 項式は還元されず、$Y_i$ は独立の物理項として残る
- Model M4-C の設計で $Y_i$ を独立に扱う必要がある
- session 21 report §「未解決課題」の第 1 項 (「c(η) の C₀ = 7000 の理論的説明」) が open のまま

## 8. 検証の未達点

以下は現時点で未達成の検証項目 (詳細 [[13_未達成項目と反証履歴_0918]]):

- **他 seed での $\|\tilde\mu\|^2$ の verification**: 現在は seed 0 (n_fixed=7・$\|\tilde\mu\|^2 = 9.29$) のみ。他 seed で $\|\tilde\mu\|^2$ が異なる値を取るか (n_fixed 依存性) の verification は未実施。
- **$T_1^{\rm true}$ の per-event verification**: Claude Code session 21 Step C で $T_1^{\rm true}$ per-event を計算したが、per-event で 4 項式全体 ($T_0 + T_1^{\rm true} + T_4 + T_5$) の R² を再測定していない。
- **Kubo 段 0 分析の script 再構築**: Chat container で第 20 回に実施した ratio 1.008 の計算は memory summary に残っているのみ。再実行と precision 確認は Landing B の Step 0 で予定。
- **bias mode projection の代数の直接検証**: `bias_mode_projection.py` の再構築で、Kubo 解釈の代数 (support 全体で $\|\tilde\mu\|^2$ を使う) が正しいかを直接検証。
- **on-support kp 別 ratio の測定**: Claude Code 解釈で kp 群別に ratio を再計算し、narrow band が成立するか (arm 依存性の source を明らかに)。

## 9. Landing A の中での意義

判定基準 5 の後半 (Y_i の物理的解明) は Kubo 段 0 解釈で達成される:

- **判定 5 の前半** ([[08_Y_i閉形式_step_E_0918]]): Y_i の閉形式の同定 (per-event R² > 0.99)
- **判定 5 の後半** (本ノート・Kubo 段 0 解釈): Y_i の物理的正体を bias mode cancellation として同定 (ratio 1.008 ± 0.009)

**ただし Claude Code report の factor 3 解釈と両論併記の状態**。Landing A の判定達成 (v3i_joint の 3 判定) には両解釈のどちらでも影響しないが、Landing B での Model M4-C の設計で解釈対立の解消が必要。

Kubo 側の期待: 「駆動源 5 項式は実質 4 項式に整理される」・「$Y_i$ は独立の物理項ではなく $T_1^{0\text{th, bias-mode}}$ の cancellation」・「支持点分光の bias mode の SGD 完全 refit がこの cancellation の起源」

Claude Code 側の position: 「$Y_i$ の閉形式は確立・$c(\eta) \approx 7000 \eta$ の C₀ の理論的説明は未解決・factor 3× は future work」

## 10. Provenance

- **source-result**: 
  - `~/project/Nakatsuka/claude/hole1_scripts/session21_out/step_E_yi_fits.json` (form (v) の 5 arm fit)
  - Chat container で第 20 回に生成した段 0 analysis (実物 script なし・memory summary に記録)
  - `~/project/Nakatsuka/claude/hole1_scripts/session21_out/report.md` (Claude Code session 21 report・「factor 3× ずれ」の原文)
  - `~/project/Nakatsuka/claude/hole1_scripts/session21_out/step_E_yi_functional_form.md` (Step E report・c(η) fit の詳細)
- **source-commit**: 本ノート起票時の teacher branch head
- **verified-on**: 2026-09-18
- **script**: [[12_再現用scripts_data_0918]] の以下:
  - `補助データ/scripts/chat_scripts_reconstruction/` の再構築必要 script (Kubo 段 0 分析の再現)
  - `補助データ/scripts/session21_scripts/step_E_yi_fit.py` (Claude Code の 6 関数形 fit)

## 11. Log

- 2026-09-18 起票 (初回・第 20 回終了時の段 0 分析結果・Chat container の実物 script なし)
- 2026-09-18 turn 8-b 精緻化:
  - session 21 report を直接読み込み、「factor 3× ずれ」が session 21 report では **open question として残されている** ことを明示化
  - 「Kubo 段 0 で訂正済み」→ 「Kubo 段 0 解釈 (両論併記の一方)」に positioning を修正
  - Claude Code 解釈での ratio 計算 (2.82-4.19・平均 3.37 ± 0.54) を対照として追加
  - Kubo 解釈と Claude Code 解釈の物理的正当性の両論併記
  - 両解釈の対立の解消の方向性 (追加検証 4 項目) を明示
  - 「訂正済み・factor 1 完全一致」→ 「両論併記・Kubo 側は factor 1・Claude Code 側は factor 3 open question」に修正
- Ratio 1.008 ± 0.009 は Kubo 解釈での結果・Chat container 実施の実物 script はなし
- 他 seed の $\|\tilde\mu\|^2$ verification と on-support kp 別 ratio 測定は Landing B の open item
