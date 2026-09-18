---
source_pdf: Archive_LoP_mech.pdf
converted: 2026-09-18
status: PDF転記
---

# 2025–2026 LoP mechanism 文献整理と Landing A–B の位置づけ

> 添付 PDF \`Archive_LoP_mech.pdf\` の Markdown 転記。文献情報・評価・新規性判断・投稿先レベルの見立てを含め、**PDF 内の記述をそのまま整理したもの**。この転記作業では各一次資料を Web で再検証していないため、文献の詳細・査読状況・評価は「PDF 作成時点の記述」として扱う。
>
> PDF 自身も末尾で、複数の一次資料について abstract レベルまでしか読めていないこと、2026 年の追加文献を見落としている可能性を明示している。

Kubo の要請に応じて、2025–2026 の LoP mechanism 文献を体系的に調査し、主要な mechanism 仮説と Kubo の Landing A–B の差別化を整理する。

---

## 1. 主要6 mechanism 仮説（2025–2026）

### 仮説1: Hessian spectral collapse — Prakash, He, Guo et al.

**論文**

“Spectral Collapse Drives Loss of Plasticity in Deep Continual Learning”

- arXiv:2509.22335
- v1: 2025-09-26
- v3: 2026-05-29
- PDF 記載では under review
- 著者: Arjun Prakash, Naicheng He, Kaicheng Guo* et al.
- Brown University・George Konidaris group と記載

**PDF 内の要約**

- LoP は Hessian eigenspectrum の collapse に先立たれる。
- curvature directions の消失で GD が非効率になる。
- linearized ReLU network で \(\epsilon\)-rank conditions を導出。
- loss-weighted Gram matrix と Generalized Gauss–Newton の spectral equivalence。
- \(\tau\)-trainability で既存の LoP 対策アルゴリズムを統一。
- 提案: KFAC 近似 + high effective feature rank + L2 penalty。
- 検証: Permuted MNIST・Continual ImageNet・Continual RL。
- MNIST では “raw kernel \(G(0)\) は pixel permutation 不変”であり、permutation 自体は spectral collapse を説明しない、と整理されている。PDF はこれを、task 切替による collapse が input 構造そのものではなく loss geometry から生じることを示唆すると読む。

### 仮説2: Dynamical systems entrapment — Joudaki et al.

**論文**

“Barriers for Learning in an Evolving World: Mathematical Understanding of Loss of Plasticity”

- arXiv:2510.00304
- ICLR 2026
- PDF では Kubo の memory に精読ノート
  - \`paper-joudaki-2026-cloning-manifold.md\`
  - \`audit-joudaki-2026-report.md\`
  があるとしている。

**PDF 内の要約**

LoP は parameter space の invariant sub-manifold への gradient trajectory の entrapment。

2 mechanism：

1. **Frozen-Unit Manifolds (\(M_F\))**: activation saturation で作られる。
2. **Cloned-Unit Manifolds (\(M_C\))**: representational redundancy で作られる。

さらに、

- Rank–Plasticity tension: 汎化を助ける low-rank compression が LoP manifold へ steer する。
- 標準的な gradient-based optimization は、いったん entrapped すると escape 不可能であることを証明。
- 検証: MLPs・ResNets・ViTs。
- Code: \`github.com/ajoudaki/loss-of-plasticity\`。

### 仮説3: Dual FTLE nature — Wang, Dai et al.

**論文**

“The Dual Nature of Plasticity Loss in Deep Continual Learning: Dissection and Mitigation”

- NeurIPS 2025
- 著者: Haoyu Wang, Wei Dai, Jiawei Zhang, Jialun Ma, Mingyi Huang, Yuguo Yu

**PDF 内の要約**

LoP を2種類に分ける：

- **Type-1 LoP**: highly negative FTLEs。representation collapse により学習不可。
- **Type-2 LoP**: excessively positive FTLEs。chaotic behavior により test accuracy が低下。

技術：

- neural collapse theory
- finite-time Lyapunov exponents（FTLE）

提案：

- Generalized Mixup で representation space を relax。

### 仮説4: Noise-curvature trainability — Baveja, Lewandowski, Schmidt

**論文**

“A Unified Noise-Curvature View of Loss of Trainability”

- arXiv:2509.19698
- NeurIPS 2025 OPT Workshop
- v3: 2025-12-10
- 著者: Baveja（UBC）・Lewandowski（Alberta）・Schmidt（UBC / CIFAR AI Chair）

**PDF 内の要約**

既存の個別診断：

- Hessian rank
- sharpness
- weight / gradient norms
- unit-sign entropy

は LoT の信頼できる predictor ではないと主張。

代わりに2つの相補的 indicators：

1. batch-size-aware gradient-noise bound
2. curvature volatility-controlled bound

提案：

- per-layer adaptive noise threshold on effective step-size。

### 仮説5: NTK rank + gradient decay — Wu, Tang et al.

**論文**

“The Rank and Gradient Lost in Non-Stationarity”

- ICLR 2026
- 著者: Zihao Wu, Hongyao Tang, Yi Ma, Jiashun Liu, Yan Zheng, Jianye Hao

**PDF 内の要約**

RL non-stationarity の2因子から2 mechanism：

1. NTK Gram matrix の rank collapse。
2. \(\Theta(1/k)\) の gradient magnitude decay。

提案：

- Sample Weight Decay。

### 仮説6: Activation function class — Lillo & Cheney

**論文**

“Activation Function Design Sustains Plasticity in Continual Learning”

- arXiv:2509.22562
- ICLR 2026
- peer が精読済み + 補完中と記載
- LC 補完 C1–C3 は 09-18 完了

**PDF 内の要約**

- activation の negative-branch shape と saturation behavior が primary lever。
- 提案: Smooth-Leaky と Randomized Smooth-Leaky。
- 既存文献の位置づけとして Lyle et al. 2024 の “Swiss cheese” view を引用。

---

## 2. 統合的 review 論文

### Wang, Srinivasa et al. 2026 — Predicting Plasticity

**論文**

“Predicting Plasticity in Deep Continual Learning: A Theoretical Perspective”

- arXiv:2605.09044
- 2026-05-09
- 著者: Jiuqi Wang（University of Virginia）, Jayanth Srinivasa（Cisco）, Claire Chen（Caltech）, Shuze Daniel Liu（Purdue）, Ali Payani（Cisco）, Shangtong Zhang（UVA）

**PDF 内の要約**

- representation rank・NTK rank など、広く採用されている diagnostics は反例によって future progress を予測できないとする。
- 新指標: **optimization readiness**
  - gradient strength
  - gradient reliability
  の組合せ。
- 重要な批判：
  > 既存 diagnostics は checkpoint の structural / geometric properties から動機づけられているが、future optimization progress の直接的 characterization ではない。

PDF は、Kubo の Landing A–B の per-event 駆動源5項式が担おうとしている役割を、この批判に対する直接的な応答として位置づける。

### Lyle et al. 2024 — Swiss cheese model

**論文**

“Disentangling the Causes of Plasticity Loss in Neural Networks”

- CoLLAs 2024
- arXiv:2402.18762
- 著者: Clare Lyle et al.（Google DeepMind）

**PDF 内の要約**

LoP は複数の独立した mechanism の重ね合わせ。

3 mechanism：

1. pre-activation distribution shift
2. regression target magnitude
3. parameter growth

対策：

- layer normalization + weight decay の組合せ。

---

## 3. Kubo の Landing A–B の位置づけ

### 既存仮説との対応

| Kubo の視点                  | 対応する既存仮説・最も近いもの                                 |
| ------------------------- | ----------------------------------------------- |
| spectrum / eigenvalue 構造  | He（Hessian）・Joudaki（invariant manifold）・Wu（NTK） |
| activation function class | Lillo & Cheney                                  |
| bias mode の SGD refit     | 最も近いのは He の loss-weighted Gram matrix           |
| per-event dynamics        | 最も近いのは Baveja の gradient-noise bound            |

### PDF が挙げる独自性 A–D

#### 独自性A: per-event per-unit の閉じた予言

- 駆動源5項式が per-event / per-unit で future optimization progress を \(R^2>0.9\) で予言する。
- PDF の整理では、既存論文は task-averaged または checkpoint / network-level の指標が中心。
- Wang 2026 の「checkpoint diagnostics は future progress の direct characterization ではない」という批判に対する direct answer と位置づける。

#### 独自性B: support 行列 \(K=XX^\top/32\) の spectrum

既存の spectrum：

- Hessian
- NTK
- Gram matrix

に対して、Kubo は **input support 行列そのもの**の spectrum を解剖する。

PDF に記載される構造：

- 1 bias mode
- 5 free-subspace modes
- bias mode \(\lambda_{\max}=9.29\) の完全 refit
- \(Y_i\) の cancellation

#### 独自性C: 5項式が実質4項式に整理される

PDF は、見かけ上の \(Y_i\) 項について

> \(Y_i\) は \(T_1\) operator response の0次近似の bias mode の cancellation

という統合的な読みを置く。

Lyle の Swiss cheese が複数 mechanism を並列に置くのに対し、PDF はこれを「連鎖型・還元型」の視点と位置づける。

#### 独自性D: peer V10 との4段階連鎖

\[
W\text{ 増大}
\rightarrow
\text{負側輸送}
\rightarrow
\text{到達後分岐}
\rightarrow
\text{機能的 LoP}
\]

という4段階の因果連鎖を組む。

Kubo の Landing A–B は、その **段階0 → 段階1 の微視的力学**を担う。

---

## 4. 「メカニズムを示した」主張の格 — PDF 内の再評価

PDF が整理する field の状態：

- 6つの独立した mechanism 仮説が並列に存在。
- Joudaki（ICLR 2026）と He（arXiv v3・under review）が最も理論的深度が高いと評価。
- 各仮説は architecture-agnostic な mitigation を提案：
  - Continual Backprop
  - Smooth-Leaky
  - KFAC + L2
  - Generalized Mixup
  - Sample Weight Decay
  - spectral regularization
  - InterpLayers
- Wang 2026 は既存 diagnostics を “checkpoint diagnostics” と批判。

### 前回 Q1 からの再評価

PDF 内の見立て：

- **単独 Landing A**: TMLR 級という以前の見立ては変わらず妥当。
- **Landing A + B + C + D + W（強化版）+ peer V10 の統合**:
  - ICLR / NeurIPS main track: 「確実」と評価。
  - ICML oral: 可能性あり。
  - Nature Communications 級: まだ open。

これは PDF 作成者による投稿先レベルの評価であり、一次資料の事実ではない。

### Nature Communications 級を「確実」にするため、と PDF が挙げるもの

1. Wang 2026 の optimization readiness と Kubo の駆動源5項式を直接比較し、優位を示す。
2. Joudaki 2026 の invariant manifold view との差別化（粒度・因果構造）。
3. He 2025 の Hessian spectral collapse と Kubo の support 行列 spectrum の関係を明示。

---

## 5. field 精査後の3つの差別化

### 1. 粒度差別化

PDF の主張：

> 既存 mechanism は task-averaged または checkpoint-level が中心だが、Kubo の駆動源5項式は per-event per-unit で future optimization progress を \(R^2>0.9\) で予言する。

これを Wang et al. 2026 の optimization readiness 批判への direct answer と位置づける。

### 2. spectrum の視点差別化

- He 2025: Hessian spectrum
- Joudaki 2026: parameter-space manifold
- Wu 2026: NTK rank
- Kubo: input support 行列の spectrum

PDF は、Kubo の視点を「data geometry から driven される」という新しい視点と評価する。

### 3. 因果連鎖差別化

- Lyle 2024: Swiss cheese = 並列的。
- Joudaki 2026: invariant manifold = topological。
- Kubo + peer:
  \[
  W\text{ 増大}
  \rightarrow
  \text{負側輸送}
  \rightarrow
  \text{到達後分岐}
  \rightarrow
  \text{機能的 LoP}
  \]
  + 駆動源力学。

PDF はこれを、微視的力学から巨視的機能低下までの因果連鎖と位置づける。

---

## 6. Nature Comm 条件の再定義

以前の整理：

> Landing A + B + C + D + W + Landing E（介入）で Nature Comm 級。

field 精査後の再定義：

> **Landing A + B + C + D + W + 既存6仮説との定量的排他性 + peer V10 の統合**  
> （介入実験は peer が既に大量に担う）で Nature Comm 級。

したがって PDF の判断では、

- **Kubo 側の新規 Landing E は不要**。
- 代わりに **【必須5】既存機構仮説との定量的排他性** が critical。

---

## 7. 【必須5】既存6仮説との定量的排他性

| 仮説                                 | 比較の焦点                                                        | PDF が期待する差別化                          |
| ---------------------------------- | ------------------------------------------------------------ | ------------------------------------- |
| 【1】He Hessian spectral collapse    | CondA の Hessian \(\epsilon\)-rank vs K spectrum・per-event 予言 | 我々の粒度が高い                              |
| 【2】Joudaki invariant manifold      | CondA で \(M_F,M_C\) の存在検証 vs 我々の4項式                          | 我々の予言力が定量的                            |
| 【3】Wang FTLE                       | CondA の FTLE vs per-event \(R^2\)                            | 粒度と \(R^2\)                           |
| 【4】Baveja noise-curvature          | 駆動源5項式と2 signal（noise-curvature）の比較                          | \(R^2\) 優位・step-size 制御なしで予言          |
| 【5】Wu NTK + gradient decay         | K spectrum vs NTK spectrum の関係                               | support spectrum が data geometry から自然 |
| 【6】Lillo & Cheney activation class | peer が補完中                                                    | peer 分担                               |

> 「期待する差別化」は PDF 内の仮説・見立てであり、比較実験を終えた結果ではない。

---

## 8. 現状 Vault に未追加とされた重要文献

PDF 作成時点で「Kubo の memory listing にない」とされたもの：

1. **Prakash / He et al. 2025 spectral collapse**  
   arXiv:2509.22335 — 最重要な直接比較対象。
2. **Wang, Dai et al. NeurIPS 2025 dual nature FTLE**
3. **Baveja et al. 2025 noise-curvature**  
   arXiv:2509.19698。
4. **Wang, Srinivasa et al. 2026 Predicting Plasticity**  
   arXiv:2605.09044 — 主張の位置づけに critical。
5. **Wu et al. ICLR 2026 rank + gradient**

memory listing にはあるが Vault 上で未確認とされたもの：

- \`paper-joudaki-2026-cloning-manifold.md\`
- \`paper-lyle-2023-understanding-plasticity.md\`
- \`paper-lyle-2024-disentangling.md\`

PDF は、Landing B の Related Work の下地としてこれらを Vault に取り込むべきとしている。

---

## 9. 提案する次のアクション

1. **【必要】新規 Related Work ノートを起票**  
   上記5論文の精読ノートを \`50_source/\` に \`paper-*\` 名で作る。

2. **【必要】【必須5】の具体的実施計画**  
   6仮説それぞれで数値比較する Landing の spec を作る。例：
   \`landing-b5-quantitative-exclusion-of-existing-mechanisms.md\`

3. **【推奨】Wang, Srinivasa et al. 2026 の optimization readiness を CondA で計算**  
   Kubo の per-event \(R^2\) と比較し、Landing A–B の独自性を direct evidence で示す。

4. **【推奨】He et al. 2025 の loss-weighted Gram matrix \(\epsilon\)-rank を CondA で計算**  
   K spectrum との関係を明示する。

5. **【推奨】peer との統合主張 spec**  
   field 精査で得た3つの差別化を peer と共有する。

---

## 10. 未読・未照合

PDF が明示する不確実性：

- 上記一次資料の重要な数式・実験は、PDF 作成者が abstract レベルでしか読んでいないものがある。
  - 特に He et al. 2025 の loss-weighted Gram matrix と linearized ReLU network の詳細。
  - Joudaki 2026 の \(M_F,M_C\) の具体的 proof。
  - Wang et al. 2026 の optimization readiness の定義。
- peer が精読した Joudaki 2026 ノートの内容は、memory listing にあることを知っているだけで未読。
- 2026 年の他の重要 LoP mechanism 論文を見落としている可能性がある。
- Prakash et al. 2025 v3（2026-05-29）の v1 との差分は未読。
- NeurIPS 2026 の LoP mechanism 論文は未確定（submission 段階の可能性）。
- Nature Communications への具体的戦略について、目標を「強化版セット」に置いたが、格上げ条件を Kubo と協議していない。

---

## 11. Kubo に求める判断

1. Vault に5新規論文の精読ノートを起票するか。
2. 【必須5】（定量的排他性）の具体 spec を優先して起票するか。
3. Wang, Srinivasa et al. 2026 の optimization readiness との direct 比較を先に実施するか。
4. He et al. 2025 の PDF 本文をさらに深く読み込むか。
