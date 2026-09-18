---
source_pdf: Peer_V10.pdf
converted: 2026-09-18
status: PDF転記
---

# Peer V10 の担当範囲と共同研究の残作業

> 添付 PDF \`Peer_V10.pdf\` の Markdown 転記。文意・数値・評価・「未読・未照合」の留保を原文に沿って保持し、表記だけ Markdown 化した。外部資料との再照合はしていない。
>
> PDF 記載時点の peer head は \`9332115\`。本文には「101 未マージ commits」「第20回開始時から6新 commits」とある。

## 1. peer V10 の骨格（Issa 採用済み）

中心文：

> **負側飽和を介した可塑性喪失は、重みの増大に伴って前活性が負側へ運ばれる過程と、到達後の応答が活性化の形によって分岐する過程からなる。**

4段階構成：

1. **段階0**: \(W\) が増大する。
2. **段階1**: 負側へ運ばれる。
3. **段階2**: 到達後に分岐する。
4. **段階3**: 機能的 LoP。

PDF 記載の到達点：

- 09-17 夜、崩壊する箱（RL・ELU→ELU）で「1箱の4本の矢印」が全部つながった。
- 09-18、H7（担い手直接介入）が独立検算 + main 統合まで済んだ。

---

## 2. Q1 の各方法への peer V10 のカバー範囲

### 方法1: 介入実験（causal intervention）

PDF の評価では、peer が大量に担当し、完了に近い。

実施済み介入：

- **cap12**（第1層 + 第2層の重み上限）: ELU→ELU で \`RESCUED\` 10/10 seed。
- **\(\mu_2\) 壁への LayerNorm 介入**: \`RESCUED\`。
- **層別キメラ**（第1層・第2層の活性化を分けて置換）: \`FLOOR_IN_DEEP_LAYER\`。
- **応答の場の移植**（resp_ee）: \`RESPONSE_BOTH_WAYS\` 10/10。
- **cap12 + 場の入れ替え**（swap_ee）: \`BOTH_WAYS\` 0.96・1.06。
- **成長を止めた場での担い手保持**（escape・escneff）: \`REMAINDER_REDUCED_BY_HOLD\`、\(r=+0.92\)。
- **担い手の直接介入**（neffdir_ee_0918・H7）:
  - \`ADD_H_MOVES_E\`
  - \`SUPRAPROPORTIONAL\`
  - \`COMPENSATES\`
  - \`FELU_SAME\`
- **\(\epsilon\) の再判定**（eps_rejudge）: 訓練の微分の厳密な0が凍結を作り、\(\epsilon\) は停止機構ではない。
- **max-pool → avg-pool 切替**（CNN）: 谷越えは max-pool が起こすが、劣化主因ではない。
- **蹴りのダイヤル**: RL ラベルのまま画素を部分置換。

PDF の評価：

> 既存の LoP 文献にほとんどないレベルの介入実験の充実。以前「Landing E として追加」とした介入実験の大半は、peer が既に実施している。

### 方法2: 条件 ablation

peer が試した条件マトリクス：

- **箱**: RL-MNIST・PermutedMNIST（PM）・CIFAR-CNN・condA。
- **活性化**: ReLU・leaky-ReLU・ELU・GELU・SiLU・Swish・Snake・adaptive-\(\alpha\) Swish/Snake・linear。
- **optimizer**: Adam・SGD（SGD 橋）。
- **教師**: RL（random label）・PM（permutation）・幅ダイヤル。
- **深さ・幅**: 幅クランプ・cap12・重みノルム制御。

登録判定として挙げられているもの：

- RL の GELU・SiLU は150タスクで死ぬ（t150 で8割以上の学習能力を失う・09-17 訂正で第1層から）。
- ELU→leaky で崩壊しない条件を分ける。
- Snake の位相で構造依存が出る。
- 層別キメラで「殺しているのは第2層の \(\phi'\) の床がないこと」。

### 方法3: novel prediction

peer が部分的に担当。

- cap12 の \`RESCUED\` 予測: Claude・Issa とも的中。
- swap_ee の \`BOTH_WAYS\` 予測: 両者的中。
- cap_perp の予測（mucap_el）: 両者外れ。実測は \`BOTH_HELD\`。予測外れとして記録。
- H7 の neffdir_ee 予測: 独立検算済み。

### 方法4: 反証性の議論

peer の「主張しないこと・読み違えやすい点」で明示：

- **沈下（位置）そのものを LoP と呼ばない**。
- **\(W\) 増大を正側侵食の必要条件に置かない**。
- **低応答は自動的に LoP ではない**。

PDF は、これを反証可能な主張構造として clean に整理されていると評価している。

### 方法5: 定量的排他性

peer は Lillo & Cheney との照合を担当。

参照ノート：

\`飽和からLoPへ_LilloCheneyとの照合と補完_0917.md\`

PDF 内の整理：

- Lillo & Cheney の「飽和 → LoP」は相関と未支持の仮説で、V10 の介入と定理が補う。
- LC 補完 C1–C3 は 09-18 完了。
- 「押しの持続と判定の混同」を補完。
- C2 は衝撃有害・時点依存。
- C3 は E36 のみ生存。

PDF の評価では、peer は既存文献との定量的排他性を、当初の想定より深く進めている。

### 方法6: multi-scale validation

peer が段階0–3の連鎖として担当。

- **microscale**: unit 個別の応答。
- **mesoscale**: 集団の \(n_{\rm eff}\)。
- **macroscale**: task loss。

RL・PM・CNN の3主要箱で類似の崩壊構造を確認している、と整理されている。

---

## 3. Q2 の原因論的メカニズムへの分担

### (a) なぜ支持点分光がこの構造か

peer が10+箱で確認。

ただし、**「1箱の限定を外す」H5** が残る穴。

### (b) なぜ SGD が支配モードを最速 refit するか

これは Kubo の Landing A–B 担当。

PDF では、peer はここを扱っておらず、**Kubo の駆動源5項式が peer の穴 H1（上流の駆動源）を埋める中核**と位置づける。

### (c) なぜ leaky ReLU の非対称性が LoP の峰を決めるか

peer が活性化クラス命題として担当。

V10 の第三文（PDF 記載時点では Issa の採用待ち）：

> **到達後に応答を失うのは、負側の微分が消える固定尺度の活性化のクラスである。**

関連：

\`固定尺度のReLU型活性化の飽和不可避性_仮説_0916.md\`

### (d) なぜタスク切替の頻度・大きさが LoP を決めるか

peer が「蹴りのダイヤル」で部分的に担当。

関連：

\`蹴りのダイヤル_RLラベルのまま画素を部分置換_結果_0915\`

---

## 4. 全体の分担構図

### peer（V10・中塚くん）が担当している範囲

- 段階0（W 増大）→ 段階1（負側輸送）→ 段階2（到達後分岐）→ 段階3（機能的 LoP）の4段階を、1箱の中で4本の矢印がつながる形で実現。
- microscale → mesoscale → macroscale。
- RL・PM・CNN の3主要箱で類似の崩壊構造。
- Landing C–D の一部。
- 方法1（介入）・方法2（ablation）・方法5（排他性）の大半。
- 方法6（multi-scale）の全体構造。
- 原因論 (a)(c)(d) の主要部分。

### Kubo（Landing A–B）が担当している範囲

- 方法3（novel prediction）の駆動源側：per-event \(R^2>0.9\) の予言。
- 原因論 (b)：駆動源5項式（peer の穴 H1）。
- 微視的な力の分解と K spectrum。

---

## 5. 共同研究として「メカニズムを示した」と言えるか

PDF の判断：

> **Yes・既にほぼ揃っている。**

統合文として、PDF は次を挙げる：

> \(W\) 増大が微視的な力の分解（Kubo の駆動源5項式・per-event \(R^2>0.9\)）で予言でき、その結果として前活性が負側に運ばれ（peer の \(\mu_2\) 壁・cap12・BOTH_HELD）、到達後の応答が活性化のクラスで分岐し（peer の層別キメラ・resp_ee・第三文）、機能的 LoP に至る（peer の \(n_{\rm eff}\)・swap・escneff）。

PDF は、この粒度と論理構造を「Nature Communications 級の統合主張として立てられる」と評価している。

### 「介入実験が要る」の再評価

以前の「Nature Comm を目指すなら Landing E（介入実験）が事実上必須」という判断は、peer branch を精読していない状態での判断で、部分的に誤りだったと訂正している。

- 介入実験は peer が既に大量に実施済み。
- Kubo（Chat 側）が Landing E を追加する必要はない。
- 統合主張として「メカニズムを示した」と書ける段階に近い。

---

## 6. 残る主要な作業

共同研究として残る主要作業：

1. **Kubo の Landing A–B の完成**  
   Model M4-C の完全理論駆動化（第20回で骨格まで到達）。

2. **peer の穴 H5 の解消**  
   1箱の限定を外す。例：PM GELU の移植。

3. **peer の穴 H1 と Kubo の統合**  
   V10 §11–§12 の十分条件を Kubo の駆動源5項式で埋める。PDF はこれを「本質的な統合作業」とする。

4. **peer の穴 A3 の閉じ方**  
   登録した第2層帳簿と、cap12 下でも沈む \(b_2\)。

5. **V10 第三文の Issa 採用の確定**。

---

## 7. 未読・未照合

PDF 内で判断に影響すると明示されている未読・未照合：

- \`飽和からLoPへ_LilloCheneyとの照合と補完_0917.md\` の全文。
- Lillo & Cheney（ICLR 2026）の原論文。PDF 作成者は内容を memory 内で知らないとしている。
- peer の101未マージ commits の全体。特に第20回開始時から6新 commits：
  - LC 補完 C1–C3
  - avg-pool CNN
  - neffdir_ee_0918 の main 統合
  - 現在地更新
- V10 §11–§12 の「駆動源の十分条件」の具体形と、Kubo の駆動源5項式との接続方法。
- peer の H7（担い手直接介入）neffdir_ee_0918 の設計・較正・判定の詳細。
- V10 第三文の採用状況。
- peer worktree に残る未コミット変更2件の意味：
  - \`オラクル中心化_spec_0831_追補2.md\` の削除
  - 失効フォルダへの \`??\`

---

## 8. Kubo への提案

1. peer branch の V10 第三文採用と、穴 H5・H1・A3 の完成計画を次回 peer との調整で確認する。
2. **Kubo の Landing B（Model M4-C）が peer の穴 H1（上流の駆動源）を埋める形で、共同研究の統合主張の正式な spec を起票する。**
   - 「駆動源5項式が V10 段階0–1の因果を担う」を明示的に位置づける。
3. Lillo & Cheney（ICLR 2026）原論文を Kubo が精読し、V10 統合主張の位置づけを確定する。
4. collaboration_ack を PDF 記載時点の最新 peer head \`9332115\` で打ち、H7 と LC 補完 C1–C3 を精読するタイミングを設定する。

PDF は特に **(2) の統合主張 spec の起票**を、主張の輪郭を先に固定する重要な作業としている。
