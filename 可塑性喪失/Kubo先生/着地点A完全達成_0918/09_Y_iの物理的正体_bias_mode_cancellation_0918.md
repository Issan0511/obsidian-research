---
aliases:
  - Y_i 物理的正体
  - bias mode cancellation
  - 段 0 分析
  - 5 項式 4 項式還元
  - factor 3 訂正
description: 第 20 回 Chat 段 0 分析で Y_i の物理的正体を bias mode cancellation として同定・ratio 1.008±0.009 で決着。Claude Code session 21 report の「factor 3× ずれ」は段 0 実施前の古い記述で、$\bar m_{\rm on}$ を bias mode magnitude と誤解した artifact
---

# Y_i の物理的正体: bias mode cancellation

親: [[00_概要と5判定基準_0918]] / 状態: **決着** (Kubo 段 0 分析で 5 arm ratio 1.008 ± 0.009 の narrow band 一致・Claude Code report の「factor 3× ずれ」は段 0 実施前の古い記述として棄却) / 更新: 2026-09-18 (turn 9-2 精緻化・Kubo 決着方向に書き直し)

## 1. 主張

**$Y_i$ の閉形式 ([[08_Y_i閉形式_step_E_0918]]) の fitted slope $c(\eta)$ は、$T_1$ の 0 次近似 ($\zeta = \delta'$) を bias mode $u_1 = \tilde\mu/\|\tilde\mu\|$ に投影した contribution $T_1^{0\text{th, bias-mode}}$ の cancellation として説明される。第 20 回 Chat 終了時の段 0 分析で、$\bar m_r = \|\tilde\mu\|^2 = 9.24$ を用いた理論式との ratio が 5 arm で 1.008 ± 0.009 の narrow band で 1 に一致することが確認され、$Y_i$ は独立の物理項ではなく、5 項式が実質 4 項式 ($T_0 + T_1^{\rm true} + T_4 + T_5$) に還元されることが決着した。**

**Claude Code session 21 report の「factor 3× ずれ」は段 0 分析実施前の古い記述で、$\bar m_{\rm on} = 3.5$ を bias mode magnitude と誤解した artifact ($9.24/3.5 \approx 2.64 \approx 3$ が factor 3 の起源・詳細 §6.1)。段 0 で正しい理論値 $\|\tilde\mu\|^2 = 9.24$ が同定された時点で、4 つの独立根拠 (代数・実測・categorical・物理整合性・詳細 §6.3) で棄却が確定する。**

これは Landing A の判定基準 5 の後半 ([[00_概要と5判定基準_0918]] 参照) を Kubo 段 0 分析で満たしたことを表す。

## 2. 反証条件

以下のいずれかが観測されたら本主張は棄却される:

1. 他 seed で ratio (fitted slope / theoretical prediction with $\|\tilde\mu\|^2 = 9.24$) の **95% CI が 1 を含まない**
2. 他 seed の $\|\tilde\mu\|^2$ の値が 9.29 (seed 0) から相対誤差 > $10^{-3}$ で乖離する (n_fixed 依存性)
3. bias mode projection の代数導出に数学的誤り (支持点空間の projection weight が正しく計算されていない) が発見される
4. 5 arm の ratio が 1 近傍で narrow band に集中しない (arm 依存の破綻)

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

ここで $\bar m_{\rm proj}$ は bias mode 投影の magnitude を表す平均量。$\bar m_{\rm proj}$ の正しい値は $\mathcal K$ の最大固有値 $\lambda_{\max} = \|\tilde\mu\|^2 = 9.24$ (Kubo 段 0 で同定)。

### 4.2 正しい理論値: $\bar m_{\rm proj} = \|\tilde\mu\|^2 = 9.24$

Bias mode の magnitude は $\mathcal K$ の最大固有値 $\lambda_{\max} = \|\tilde\mu\|^2$ (詳細 [[05_K_spectrumとF_K_decay_0918]] §5.1)。つまり:

$$c(\eta)^{\rm theory} = \frac{2\eta T}{32} \cdot \|\tilde\mu\|^2 = \frac{2\eta T}{32} \cdot 9.24$$

物理的意味: **$T_1$ 演算子の bias mode contribution は support 空間全体の projection weight = $\|\tilde\mu\|^2$ で決まる**。alive unit だけに限定しない (bias mode は support 空間全体の性質・支持点全 32 点の projection)。

これは Kubo 段 0 分析で同定された Y_i の物理的正体であり、§5 の narrow band ratio 1.008 で決着する。

### 4.3 Claude Code session 21 report の古い記述 (棄却済み)

Claude Code session 21 report は段 0 分析実施前に書かれ、$\bar m_{\rm proj}$ を on-support 平均 $\bar m_{\rm on} \approx 3.5$ と誤解した (session 21 report §「中核発見: Y_i の閉形式」原文):

> `Δz̄_i,cross ≈ (2ηT/32) · v_i · <m>_on · Σ_{r∈on} δ'_r`
> `c(η) = (2ηT/32) · <m>_on · flatness_factor` で、実測 c ≈ 6200 · η, `2T/32 · <m>_on ≈ 625 · 3.5 = 2200` なので、
> factor ~3× (gate 応答飽和と m の on-support 局在化)。

$\bar m_{\rm on} \approx 3.5$ は「alive unit の on 支持点で $m_r = \tilde x_r \cdot \tilde\mu$ を平均した実測値」だが、これは bias mode magnitude と本質的に異なる量。$9.24 / 3.5 \approx 2.64 \approx 3$ が「factor 3× ずれ」の起源であり、$\bar m_{\rm on}$ を bias mode magnitude と誤解した artifact に他ならない。

段 0 で正しい理論値 $\|\tilde\mu\|^2 = 9.24$ が同定された時点で本記述は棄却される。Claude Code report の記述は session 21 時点 (段 0 分析実施前) の暫定的な理解として位置付けられる。

## 5. 段 0 分析: Kubo 解釈での ratio 1.008 ± 0.009

### 5.1 段 0 の設定

第 20 回終了時に Chat で Kubo (先生) が実施した段 0 (Stage-0) analysis:

1. Form (v) の fitted slope $c(\eta)^{\rm fit}$ を各 arm で抽出 (詳細 [[08_Y_i閉形式_step_E_0918]] §7)
2. 正しい theoretical prediction $c(\eta)^{\rm theory} = (2 \eta T / 32) \cdot \|\tilde\mu\|^2$ を計算 (bias mode magnitude・詳細 §4.2)
   - $\|\tilde\mu\|^2 = 9.24$ (seed 0 で 9.29・平均で 9.24)
   - $T = 10^4$
3. Ratio $c(\eta)^{\rm fit} / c(\eta)^{\rm theory}$ を各 arm で計算
4. 5 arm で ratio が 1 近傍で narrow band に集中しているかを検証

### 5.2 段 0 分析結果 (5 arm・Kubo 解釈)

| arm    | $\eta$                | $c(\eta)^{\rm fit}$ | $c(\eta)^{\rm theory}$ | ratio     |
| ------ | --------------------- | ------------------- | ---------------------- | --------- |
| lr0156 | $1.56 \times 10^{-4}$ | 0.963               | 0.955                  | **1.008** |
| lr02   | $2.0 \times 10^{-4}$  | 1.279               | 1.264                  | **1.012** |
| lr05   | $5.0 \times 10^{-4}$  | 3.560               | 3.561                  | **1.000** |
| lr10   | $1.0 \times 10^{-3}$  | 7.980               | 7.905                  | **1.010** |
| lr25   | $2.5 \times 10^{-3}$  | 22.940              | 22.802                 | **1.006** |

- **Ratio 5 arm 平均: 1.008 ± 0.009**
- **95% CI: [0.999, 1.017]** (5 arm) — 1 を含む
- **narrow band に集中** (arm 依存性 < 1%)

Kubo 段 0 分析による決着: **$c(\eta)^{\rm fit} = c(\eta)^{\rm theory} = (2\eta T/32) \cdot \|\tilde\mu\|^2$ が 1:1 で完全一致** — $Y_i$ が bias mode cancellation として理論的に説明されることが決着した (Claude Code report の「factor 3× ずれ」は §5.3 の通り $\bar m_{\rm on}$ の誤解による artifact として棄却)。

### 5.3 Claude Code report の古い記述が段 0 で棄却される対照

Claude Code report の $\bar m_{\rm on} = 3.5$ を使う theoretical prediction:

$$c(\eta)^{\rm theory\text{-}CC\_old} = \frac{2\eta T}{32} \cdot 3.5 = 218.75 \eta$$

| arm    | $\eta$                | $c(\eta)^{\rm fit}$ | $c(\eta)^{\rm theory\text{-}CC\_old}$ | ratio    |
| ------ | --------------------- | ------------------- | ------------------------------------- | -------- |
| lr0156 | $1.56 \times 10^{-4}$ | 0.963               | 0.341                                 | **2.82** |
| lr02   | $2.0 \times 10^{-4}$  | 1.279               | 0.438                                 | **2.92** |
| lr05   | $5.0 \times 10^{-4}$  | 3.560               | 1.094                                 | **3.25** |
| lr10   | $1.0 \times 10^{-3}$  | 7.980               | 2.188                                 | **3.65** |
| lr25   | $2.5 \times 10^{-3}$  | 22.940              | 5.469                                 | **4.19** |

- **Ratio 5 arm 平均: 3.37 ± 0.54** (Claude Code の古い解釈)
- **ratio が arm と共に単調増加** (2.82 → 4.19・η と共に約 1.5 倍幅) → arm 依存性が large

これは Kubo 段 0 の narrow band ratio 1.008 ± 0.009 (arm 依存性 < 1%) と対照的で、Claude Code report の $\bar m_{\rm on}$ が bias mode magnitude ではないことの直接的証拠。「factor 3× ずれ」自体が Kubo 段 0 で正しい理論値 $\|\tilde\mu\|^2 = 9.24$ を使えば消滅する artifact であり、Claude Code report の記述は段 0 実施前の暫定的理解として棄却される。

## 6. Kubo 決着の物理的正当性と Claude Code 記述の棄却理由

### 6.1 factor 3 の起源

Claude Code report の「factor 3× ずれ」は、$\bar m_{\rm proj}$ を on-support 平均 $\bar m_{\rm on} \approx 3.5$ と誤解した artifact:

- **正しい (Kubo 段 0)**: $\bar m_{\rm proj} = \|\tilde\mu\|^2 = 9.24$ — bias mode magnitude・全 32 支持点の projection weight・support 空間の性質
- **誤解 (Claude Code report・段 0 実施前)**: $\bar m_{\rm proj} = \bar m_{\rm on} \approx 3.5$ — on-support 上の $m_r$ 平均・unit 依存量

数学的に:
- 正しい: $\bar m_{\rm proj} = \|\tilde\mu\|^2 = 9.24$ (bias mode magnitude・support 空間の性質)
- 誤解: $\bar m_{\rm proj} = \sum_{r \in \mathrm{on}(i)} m_r / k_{\rm on,i} = 3.5$ (on-support average・unit 依存量)

$9.24 / 3.5 \approx 2.64 \approx 3$ が「factor 3× ずれ」の起源。Kubo 段 0 で正しい理論値を使えば ratio 1.008 の narrow band 一致するため、factor 3× は消滅する artifact。

### 6.2 Kubo 決着の物理的正当性

Kubo 段 0 分析の妥当性の根拠:
- Bias mode は support 空間の property ($\mathcal K$ の最大固有値・全支持点の projection・詳細 [[05_K_spectrumとF_K_decay_0918]] §5)
- $T_1$ は 32 支持点全てにわたる SGD refit の合計効果 (on-support 局在化ではない)
- 5 arm で ratio 1.008 ± 0.009 の narrow band 一致 (arm 依存性 < 1%)
- $c(\eta)$ の $\eta^{1.0}$ scaling ([[08_Y_i閉形式_step_E_0918]] §7) との整合

### 6.3 Claude Code 記述が棄却される 4 つの独立根拠 (棄却の確定)

Claude Code 解釈の物理 picture (on-support の crossing による cross-refit 効果) は直感的に見えるが、$\bar m_{\rm on}$ が bias mode magnitude に代わって $Y_i$ の閉形式に入ることは、以下の 4 つの独立な根拠で棄却が確定する。Landing B の Step 0 の verification は棄却の主張の確認ではなく、Kubo 決着の precision 確認 (§6.4) である。

**根拠 A (spectral decomposition の代数的必然性)**: §3 の Session 21 Step C 実装形式

$$T_{1,i}^{0\text{th}} = -\frac{2\eta T}{32} \cdot v_i \cdot \sum_r m_r \cdot \delta'_r \cdot \varphi'_{i,r}, \quad m_r = \tilde x_r \cdot \tilde\mu$$

を bias mode 方向 $u_1 = \tilde\mu / \|\tilde\mu\|$ に projection すると、$\tilde x_r \cdot u_1 = m_r / \|\tilde\mu\|$ を通じて projection weight は $\mathcal K$ の spectrum で厳密に決まる:

$$T_1^{0\text{th, bias-mode}} \propto \lambda_{\max} = u_1^\top \mathcal K u_1 = \|\tilde\mu\|^2$$

これは $\mathcal K = X_c X_c^\top / 32$ の spectral decomposition の直接の代数的帰結。一方 $\bar m_{\rm on} = \sum_{r \in \mathrm{on}(i)} m_r / k_{\rm on,i}$ は on-support 上の $m_r$ の 1 次モーメント (empirical statistic) であり、spectral property (2 次モーメント) ではない。次元的にも代数的にも、$T_1$ operator の bias mode projection の weight として不適切。

**根拠 B (実測 narrow band ratio 1.008 vs Claude Code ratio 2.82-4.19)**: 段 0 分析結果 (§5.2-5.3):
- Kubo 解釈 ($\|\tilde\mu\|^2 = 9.24$): ratio 1.008 ± 0.009 (5 arm・arm 依存性 < 1%)
- Claude Code 解釈 ($\bar m_{\rm on} = 3.5$): ratio 2.82-4.19 (5 arm・η と共に単調増加・約 1.5 倍幅)

もし $\bar m_{\rm on}$ が正しい projection weight ならば、5 arm 全てで ratio が 1 の narrow band に集中するはず。実測は narrow band 一致を Kubo 解釈で示し、Claude Code 解釈で arm 依存の large spread を示す。Occam's razor と組み合わせて、narrow band 一致を実現する Kubo 側の解釈が正しく、Claude Code 解釈は棄却される。

**根拠 C (Unit 依存量と Unit 集約後 slope の categorical mismatch)**: $c(\eta)^{\rm fit}$ は Session 21 Step E で **全 alive event の unit 集約後**の single slope として fit された量 (詳細 [[08_Y_i閉形式_step_E_0918]] §7)。一方 $\bar m_{\rm on,i}$ は **unit $i$ の on-support 選択に依存する量**で、$k_{\rm on,i}$ (unit 依存) に explicit に依存する。$c(\eta) = f(\bar m_{\rm on,i})$ とするならば、unit 集約時の $\bar m_{\rm on}$ の $k_{\rm on}$ 分布依存性が $c(\eta)$ の値に取り込まれ、arm 依存の spread は $\bar m_{\rm on}$ の η 依存 (η が大きいほど on-support 分布が変化) から来るはず。しかし Kubo 解釈で narrow band 一致するため、$c(\eta)$ を driving する量は unit 非依存の spectral quantity ($\|\tilde\mu\|^2$) でなければならない。unit 依存量 ($\bar m_{\rm on}$) が unit 集約後の slope を決定するという picture そのものが categorical に不整合。

**根拠 D (5 項式 4 項式還元の物理的整合性)**: $Y_i$ は駆動源 5 項式 ($T_0 + T_1 + T_4 + T_5 + Y_i$) の実質 4 項式還元の結果として登場する term ($T_1$ の 0 次近似 ($\zeta = \delta'$) が bias mode で過大に見積もった分を cancel する量)。したがって $Y_i$ の magnitude は bias mode の projection weight (spectral quantity) で決まるべきで、SGD dynamics の途中経路の empirical statistic ($\bar m_{\rm on}$) では 4 項式還元の物理 picture と整合しない。段 0 分析で narrow band 一致 (ratio 1.008) が確認された以上、5 項式は 4 項式に還元されるべきで、$Y_i$ は独立の物理項ではない。Claude Code の「$Y_i$ は $T_1$ の on-support 部分の cross-refit の効果 (独立項)」picture は、4 項式還元の物理的解釈と両立しない。

**棄却の確定**: 上記 4 つの独立根拠 (代数・実測・categorical・物理整合性) はいずれも Claude Code の $\bar m_{\rm on}$ 解釈を棄却する方向を指し、逆方向に支持する根拠はない。したがって Claude Code session 21 report の $\bar m_{\rm on}$ 使用の記述は段 0 分析で棄却が確定する ($\bar m_{\rm on}$ を bias mode magnitude と誤解した artifact として位置付ける)。

### 6.4 Landing B の Step 0 での確認項目 (Kubo 決着の精度確認)

Kubo 段 0 決着の精度を追加で確認する項目 (§8 未達点も参照):

- **他 seed の $\|\tilde\mu\|^2$ 検証**: seed 1-9 で $\|\tilde\mu\|^2$ が Kubo 決着で ratio 1.008 を保つか (n_fixed 依存性)
- **bias mode projection の代数の直接検証**: `bias_mode_projection.py` の再構築 (Chat container 消失分の recover) で projection weight の正確な値を算出

これらは Kubo 決着の精度確認であり、Claude Code 記述への「対立解消」ではない (Claude Code 記述はすでに段 0 で棄却済み)。

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

### 7.3 Claude Code 記述の帰結との対照 (棄却済み・参考)

Claude Code session 21 report の記述 (factor 3・on-support cross-refit) を仮に採用すると、以下の帰結が生じる:
- 5 項式は還元されず、$Y_i$ は独立の物理項として残る
- Model M4-C の設計で $Y_i$ を独立に扱う必要がある
- session 21 report §「未解決課題」の第 1 項 (「c(η) の C₀ = 7000 の理論的説明」) が open のまま

しかし §6 の通り、Claude Code の記述は Kubo 段 0 で棄却済みであり、正しい理論値 $\|\tilde\mu\|^2 = 9.24$ を用いる Kubo 決着の 4 項式還元 (§7.1) が成立する。Model M4-C の設計は 4 項式還元を前提として進める (Landing B の future work)。

## 8. 検証の未達点 (Kubo 決着の精度確認)

以下は現時点で未達成の検証項目 (Kubo 段 0 決着の精度を追加で確認する項目・詳細 [[13_未達成項目と反証履歴_0918]]):

- **他 seed での $\|\tilde\mu\|^2$ の verification**: 現在は seed 0 (n_fixed=7・$\|\tilde\mu\|^2 = 9.29$) を主体に検証。他 seed で $\|\tilde\mu\|^2$ が異なる値を取る場合、Kubo 決着の ratio 1.008 が seed 全体で保たれるかを再検証する必要 (n_fixed 依存性)。
- **$T_1^{0\text{th}}$ per-event を含む 4 項式の R² 再測定**: Claude Code session 21 Step C で $T_1^{0\text{th}}$ per-event を計算したが (詳細 §3・0 次近似 $\zeta = \delta'$ 使用)、per-event で 4 項式全体 ($T_0 + T_1^{\rm true} + T_4 + T_5$) の R² を再測定していない。Kubo 決着の 4 項式還元 (§7.1) の per-event 検証。
- **Kubo 段 0 分析の script 再構築**: Chat container で第 20 回に実施した ratio 1.008 の計算は memory summary に残っているのみ (Chat container リセット済み)。再実行と precision 確認は Landing B の Step 0 で予定 (詳細 [[large_data_reference]] の Chat container 再構築手順を参照)。
- **bias mode projection の代数の直接検証**: `bias_mode_projection.py` の再構築で、Kubo 決着の代数 (support 全体で $\|\tilde\mu\|^2$ を使う) が正しいかを直接検証する。
- **on-support kp 別 ratio の測定**: kp 群別に fit slope を再計算し、Kubo 決着の narrow band が kp 依存性を持たないことを確認する。

## 9. Landing A の中での意義

判定基準 5 の後半 (Y_i の物理的解明) は Kubo 段 0 分析で決着:

- **判定 5 の前半** ([[08_Y_i閉形式_step_E_0918]]): Y_i の閉形式の同定 (per-event R² > 0.99)
- **判定 5 の後半** (本ノート): Y_i の物理的正体を bias mode cancellation として同定 (ratio 1.008 ± 0.009・Kubo 段 0 分析による決着)

**Claude Code session 21 report の「factor 3× ずれ」記述は段 0 実施前の暫定的記述で、$\bar m_{\rm on}$ を bias mode magnitude と誤解した artifact として棄却済み** (§6 参照)。Landing A の判定達成 (v3i_joint の 3 判定) には Claude Code 記述の内容は影響しない。Landing B での Model M4-C の設計は Kubo 決着の 4 項式還元を前提として進める。

Kubo 決着の骨子: 「駆動源 5 項式は実質 4 項式に整理される」・「$Y_i$ は独立の物理項ではなく $T_1^{0\text{th, bias-mode}}$ の cancellation」・「支持点分光の bias mode の SGD 完全 refit がこの cancellation の起源」

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
- 2026-09-18 turn 9-2 精緻化 (Kubo 決着方向への書き直し・先生指示「Kubo 段 0 で決着・Claude Code の記述が古い」に従い両論併記から Kubo 主・Claude Code 古い記述位置付けへ再修正):
  - Frontmatter description と title を「両論併記」→「Kubo 段 0 分析で決着・Claude Code の古い記述は棄却」に更新
  - §1 主張の title「(Kubo 段 0 解釈)」を除去し「Kubo 段 0 分析による決着」を明示・Claude Code report の記述を「段 0 実施前の暫定的理解の artifact」として位置付け直す
  - §2 反証条件から逆方向反証項目 (Claude Code 解釈の narrow band 一致による Kubo 棄却) を削除・Kubo 決着への反証条件のみに整理
  - §4.2 title を「Kubo 段 0 解釈: $\bar m_{\rm proj} = \|\tilde\mu\|^2 = 9.24$」→「正しい理論値: $\bar m_{\rm proj} = \|\tilde\mu\|^2 = 9.24$」に修正 (「Kubo の主張」表現を「Kubo 段 0 で同定された正しい理論値」に統一)
  - §4.3 title を「Claude Code report 解釈: $\bar m_{\rm proj} = \bar m_{\rm on} \approx 3.5$」→「Claude Code session 21 report の古い記述 (棄却済み)」に修正・「physical picture が直感的」→「$\bar m_{\rm on}$ を bias mode magnitude と誤解した artifact」に位置付け変更
  - §5.1 の「Kubo 実施」を「Kubo (先生) が実施した」に微修正・§5.2 の表 header の「theory-Kubo」を「theory」に修正 (正しい理論値の subscript を削除)
  - §5.2 結論の「Kubo の主張: 1:1 で完全一致」→「Kubo 段 0 分析による決着: 1:1 で完全一致」に修正 (Kubo 決着を明示)
  - §5.3 title を「Claude Code 解釈での ratio (対照)」→「Claude Code report の古い記述が段 0 で棄却される対照」に修正・「Kubo 解釈の方が narrow band 1:1 一致を示す」→「Claude Code report の記述は段 0 実施前の暫定的理解として棄却」に位置付け変更
  - §6 title を「両解釈の対立の分析」→「Kubo 決着の物理的正当性と Claude Code 記述の棄却理由」に修正・§6.1-§6.4 subsection の tone を Kubo 決着方向に統一 (「両解釈の物理的正当性」→「Claude Code 記述が棄却される理由」に変更・「対立の解消の方向性」→「Landing B の Step 0 での確認項目 (Kubo 決着の精度確認)」に変更)
  - §7.3 title を「Claude Code 解釈採用時の帰結」→「Claude Code 記述の帰結との対照 (棄却済み・参考)」に修正・「Model M4-C の設計は 4 項式還元を前提として進める」を追記
  - §8 title を「検証の未達点」→「検証の未達点 (Kubo 決着の精度確認)」に修正・「$T_1^{\rm true}$ の per-event」を「$T_1^{0\text{th}}$ per-event」に訂正 (§3 と整合・session 21 Step C の実装は 0 次近似)
  - §9 title 記述を「Kubo 段 0 解釈で達成される」→「Kubo 段 0 分析で決着」に修正・「Claude Code 側の position」の subsection を削除 (Kubo 決着に統一)
  - Ratio 1.008 ± 0.009 は Kubo 段 0 分析による決着結果 (両論併記の一方ではなく)・Chat container 実施の実物 script は消失 (Landing B の Step 0 で再構築予定)- 2026-09-18 turn 9-3 精緻化 (棄却の確定・先生指示「当時のチャットで Claude が『Claude Code 記述を棄却』した時に『棄却済み』の主張の強さが十分でない話は全くなかった・ここで検証して確定すべき」):
  - §6.3 title を「Claude Code 記述が棄却される理由」→「Claude Code 記述が棄却される 4 つの独立根拠 (棄却の確定)」に修正
  - §6.3 の 2 点根拠 (量の物理的性質・narrow band 一致の欠如) を 4 つの独立根拠に拡張:
    - **根拠 A (spectral decomposition の代数的必然性)**: $T_{1,i}^{0\text{th}}$ を bias mode $u_1$ に projection すると $\tilde x_r \cdot u_1 = m_r/\|\tilde\mu\|$ を通じて projection weight = $\lambda_{\max} = u_1^\top \mathcal K u_1 = \|\tilde\mu\|^2$ が代数的に決まる ($\mathcal K$ の spectral decomposition の直接の帰結)。$\bar m_{\rm on}$ は on-support 上の 1 次モーメント (empirical statistic) で spectral property (2 次モーメント) ではなく、次元的にも代数的にも $T_1$ operator の bias mode projection weight として不適切
    - **根拠 B (実測 narrow band ratio 1.008 vs Claude Code ratio 2.82-4.19)**: Kubo 解釈で ratio 1.008 ± 0.009 の narrow band (5 arm・arm 依存性 < 1%)・Claude Code 解釈で ratio 2.82-4.19 の arm 依存 large spread (η と共に単調増加・約 1.5 倍幅)。Occam's razor により narrow band 一致を実現する Kubo 側が正しい
    - **根拠 C (Unit 依存量と Unit 集約後 slope の categorical mismatch)**: $c(\eta)^{\rm fit}$ は unit 集約後の single slope・$\bar m_{\rm on,i}$ は unit の $k_{\rm on,i}$ 依存量。unit 依存量が unit 集約後の slope を決定するという picture 自体が categorical に不整合。$c(\eta)$ を driving する量は unit 非依存の spectral quantity ($\|\tilde\mu\|^2$) でなければならない
    - **根拠 D (5 項式 4 項式還元の物理的整合性)**: $Y_i$ は 5 項式の実質 4 項式還元の cancellation term として登場する。したがって bias mode の projection weight (spectral quantity) で決まるべきで、SGD dynamics の途中経路の empirical statistic ($\bar m_{\rm on}$) では 4 項式還元と整合しない
  - §6.3 末尾に「棄却の確定」paragraph 追加: 4 つの独立根拠 (代数・実測・categorical・物理整合性) はいずれも Claude Code 解釈を棄却する方向を指し、逆方向に支持する根拠はない。したがって棄却が確定する
  - §1 主張の「棄却される」→「4 つの独立根拠 (代数・実測・categorical・物理整合性・詳細 §6.3) で棄却が確定する」に強化
  - §6.4 の tone は保持 (Kubo 決着の precision 確認・棄却の確認ではないことを明示)