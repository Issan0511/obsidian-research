---
source_pdf: W_Problem.pdf
converted: 2026-09-18
status: PDF転記
---

# W 増加問題を解明する道筋

> 添付 PDF \`W_Problem.pdf\` の Markdown 転記。文意・数値・「未読・未照合」などの留保を原文に沿って保持し、数式と表だけ Markdown / LaTeX として整形した。外部資料との再照合はしていない。
>
> PDF 内で埋め込みフォント由来と思われる記号欠落がある数式は、推測で補わず \`[PDFで記号欠落]\` とした。

前回提示した骨格を起点に、第20回の中核発見（K spectrum の bias mode + Term I / Term II 分解 + \(Y_i\) の物理的正体）と統合して、W 増加問題を解明する道筋を段階的に示す。

## 1. 前回の骨格の詳細化

### 行1: \(\langle W,\Delta W\rangle=-\eta\cdot\text{マージン}+\text{バイアス補正}\)

peer §11 の恒等式：

\[
\sum_j a_j e_j
=
\sum_j b_j\phi'(z_j)e_j,
\]

ここで

\[
a_j=\phi(z_j),\qquad e_j=v_j\delta
\]

であり、\(e_j\) は unit \(j\) のマージン寄与。

SGD の1 step の内積は

\[
\langle W,\Delta W\rangle_{\rm step}
=
-\eta e_i\phi'(z_i)\langle w_i,x_r\rangle
=
-\eta e_i\phi'(z_i)[z_i-b_i].
\]

leaky ReLU では

\[
\phi'(z_i)z_i=\phi(z_i)=a_i
\]

なので、

\[
\langle W,\Delta W\rangle_{\rm step}
=
-\eta\left[a_ie_i-b_i\phi'(z_i)e_i\right].
\]

1タスク合計では

\[
\sum_t\langle W,\Delta W\rangle_t
=
-\eta
\left[
\underbrace{\sum_t a_i e_i}_{\text{マージン}}
-
\underbrace{b_i\sum_t\phi'(z_i)e_i}_{\text{バイアス補正}}
\right].
\]

### 行2: マージン打ち消し \(\rightarrow\) 整列項 \(\simeq0\)

「タスク前半（\(\delta>0\) の押し下げ）と後半（\(\delta<0\) の押し上げ）の対称性」で

\[
\sum_t a_i e_i\simeq0
\]

が成立する。バイアス補正も同様に

\[
\sum_t\phi'(z_i)e_i\simeq0.
\]

### 行3: Adam の新規項 \(\|\Delta W\|^2\simeq\eta^2nc\)

Adam の座標正規化：

\[
\Delta W_{\rm Adam}
=
-\eta P_{\rm ctr}
\left(
\frac{m_t}{\sqrt{v_t}+\epsilon}
\right).
\]

各座標で

\[
\left|\frac{m}{\sqrt v}\right|\simeq O(1)
\]

であり、勾配の大きさに鈍い。したがって

\[
\|\Delta W\|^2
=
\eta^2\sum r^2
\simeq
\eta^2nc,
\]

ここで \(n\) は座標数、\(c=O(1)\)。

### 行4: 独立増分の累積で \(\|W\|\sim\eta\sqrt{nt}\)

FRESH では各タスクの \(\Delta W\) が互いに直交する（peer A1）ので、

\[
\|W_t\|^2
=
\sum_{s=1}^t\|\Delta W_s\|^2
=
t\,\eta^2 n.
\]

よって

\[
\|W_t\|=\eta\sqrt{nt}.
\]

---

## 2. 第20回の中核発見を組み込んだ精密化

前回の骨格には3つの弱点があった。第20回発見でこれらを精密化する。

### 弱点1: 「マージン打ち消し \(\rightarrow 0\)」の粒度

前回は「タスク全期でマージン打ち消し \(\rightarrow\) 整列項 \(\simeq0\)」と書いていた。

Kubo の Term I / Term II 分解（§8-7・第20回）では3レジームが得られた：

- **低 \(\eta\)**（\(\eta\le2\times10^{-4}\)）: マージン打ち消し不完全・Term I の縮小方向が大きい。
- **中 \(\eta\)**（\(\eta\sim10^{-3}\)）: マージン打ち消しが最良・Term I \(\simeq0\)。前回骨格が想定した regime。
- **高 \(\eta\)**（\(\eta=2.5\times10^{-3}\)）: マージン打ち消しが再び不完全。

\[
c(\eta):=-\cos(W,\Delta W)=C_0(\eta)+O(\eta^p).
\]

中 \(\eta\) では \(C_0(\eta)\simeq0\)、低 \(\eta\)・高 \(\eta\) では \(C_0(\eta)>0\)（縮小方向・侵食項の起源）。

peer の実測 \(c\simeq0.045\text{--}0.05\)（3腕普遍・Adam・RL-MNIST）は、peer が観測した特定の \(\eta/T/n\) の組合せで得られる値である。\(c\) 自体は \(\eta,n,T\)、活性化、入力分布に依存し、3腕で近い値になったのは peer の実験条件が共通の regime に入っているため、と読む。

### 弱点2: Adam の \(\eta^2n\) の粒度

Kubo の Term II（§8-7）は SGD の \(\|\Delta w_i\|^2\) の閉形式：

\[
{\rm Term~II}
=
\eta^2T v_i^2\,
\overline{\delta^2}\,
\overline{\phi_i'^2}\,
\overline{\|x\|^2}.
\]

各因子は

- \(\overline{\|x\|^2}\): 入力の二乗ノルム平均（CondA では 10.5）。
- \(\overline{\phi_i'^2}\): 活性化と unit 状態に依存。
- \(v_i^2,\overline{\delta^2}\): 読み出しと残差。

Adam では概念的に

\[
\|\Delta W\|^2_{\rm Adam}
\approx
\eta^2
\sum_j
\frac{g_j^2}{v_j+\epsilon}
\]

と書ける。Adam の座標正規化は \(|m_j/\sqrt{v_j}|\) を \(O(1)\) にするため、\(\overline{\|x\|^2}\) の入力依存は弱まる一方、\(\overline{\phi_i'^2}\) の活性化依存は残る。

活性化ごとの例：

- leaky（\(a=0.03\)）: dead unit で
  \[
  \overline{\phi'^2}=a^2=9\times10^{-4},
  \]
  alive unit では \(\overline{\phi'^2}\simeq k_{\rm on}/32\)。
- ELU: 負側で
  \[
  \phi'(z)=e^z
  \]
  が滑らかに0へ近づくので、\(\overline{\phi'^2}\) は leaky と異なる。
- Snake: 位相依存（非単調）。

peer の実測では、t2–20 の注入が LR で 1.005、SNA で 0.465 と、活性化で2倍以上違った。これは \(\overline{\phi'^2}\) の活性化依存が Adam の \(\|\Delta W\|^2\) に残る証拠と位置づける。

### 弱点3: 「独立増分の累積」の粒度

タスク \(t\) の更新を

\[
\Delta W_{\rm task}
=
-\eta\sum_t
v_i\delta_t\phi'(z_{i,t})x_{r_t}
\]

とし、K の固有基底で

\[
\Delta W_{\rm task}
=
\sum_k\alpha_k({\rm task})u_k
\]

と展開する。

Kubo の K spectrum：

\[
K=\frac{XX^\top}{32}.
\]

非零固有値は、

- \(\lambda_{\max}=9.29\): bias mode
  \[
  u_1\simeq\widetilde\mu/\|\widetilde\mu\|,
  \]
- 5個の free-subspace modes: \(\lambda\simeq0.25\)。

\[
F(K)=\exp(-\eta TK/16)
\]

の decay により、bias mode は高 \(\eta\) で完全に消滅する。

タスク間の更新内積は

\[
\langle\Delta W_{{\rm task}=s},
\Delta W_{{\rm task}=t}\rangle
=
\sum_k\alpha_k(s)\alpha_k(t).
\]

FRESH regime では新しい置換ごとに \(\alpha_k\) がほぼ独立にサンプルされ、相関が弱くなるため、更新が直交しやすい。

CondA のような「固定入力空間 + 新しい teacher output の bit-flip」でも、

- 各タスクで \(\alpha_1\) は生じるが、SGD 内 refit で
  \[
  \exp(-\eta T\lambda_{\max}/16)\to0
  \]
  と消滅する。
- タスク境界の \(\alpha_1({\rm task})\) は、新タスク残差 \(\delta'\) の bias 方向 projection。
- free-subspace の5モードは fully refit されずに残る。
- 新タスクごとに新しい残差方向を持つため、
  \[
  \mathbb E[\alpha_k(s)\alpha_k(t)]\simeq0
  \]
  が期待される。

この読みでは、peer の穴 D-1「なぜ直交するか」に対して、**支配的な bias mode が SGD で refit され、残る free-subspace 成分がタスク間で弱相関になるから**と答える。

また、peer の条件で観測された \(\cos(W,\Delta W)\) の3腕の近さについては、bias mode の refit が活性化に依らない SGD 側の構造であることが一つの説明候補になる。

---

## 3. W 増加問題を解明する5段階

### 段階1: FRESH \(\sqrt t\) 蓄積の閉じた導出 — Landing B の一部

**目標**

\[
\|W_t\|=\eta\sqrt{n t}
\]

を、更新則から閉じた形で導く。

**既存の構成要素**

- peer §11 の恒等式（証明済み・180点で \(3.3\times10^{-9}\)）。
- Kubo の Term I / II 分解（§8-7・第20回・数値検証済み）。
- Adam の座標正規化（peer A6・観察）。
- K spectrum の bias mode 消滅（Kubo 第20回・数値検証済み）。

**新規に書くべきもの**

1. peer §11 恒等式 \(\rightarrow\) Kubo Term I 分解 \(\rightarrow\) 3 regime を、一つの \(\eta\) 依存式にする。
2. Adam の \(\|\Delta W\|^2\) を Term II の Adam 版として書く。
3. K spectrum の bias mode 消滅から、任意 activation でのタスク間直交性を位置づける。

**予想される到達点**

\[
\boxed{
\|W_t\|
=
\eta
\sqrt{n_e({\rm activation})\,t}
}
\]

で、\(n_e\) は \(\overline{\phi'^2}\) から決まる。

### 段階2: 活性化依存の指数差の導出 — Landing B の一部

**目標**

peer の実測

- leaky: 0.47
- ELU: 0.43
- SNA: 0.38

の指数差を、活性化から導く。

**構成要素**

- peer の指数順序: LR \(>\) ELU03 \(>\) ELU1 \(>\) SNA。
- peer §D-0c: 侵食項の正体は「誤答標本へのヘッジ」。
- peer §G: ③a「何が \(\beta\) を決めるか（負側ゲート）」、③b「何が \(c\) を決めるか」。
- Kubo Term II の \(\overline{\phi'^2}\) 活性化依存。

**新規に書くべきもの**

1. Term II の Adam 版で \(\overline{\phi'^2}\) を閉じた形にする。
2. 活性化ごとの \(\overline{\phi'^2}\) の順序を評価する。
3. \(\beta\) と \(c\) を分けて、
   - \(\beta\): \(\overline{\phi'^2}\)（Adam の \(\|\Delta W\|^2\)）
   - \(c\): Term I / Term II 比（整流残差 / 直交堆積）
   と位置づける。

**予想される到達点**

指数差の \(o(\eta)\) 補正が活性化ごとに異なることの理論表現。

### 段階3: 長時間則の判別 — Landing C の一部

**目標**

peer の現象論モデル

\[
[\text{PDFで記号欠落}]^2/t
=
[\text{PDFで記号欠落}]^2
-
2c[\text{PDFで記号欠落}]
\]

が持つ固定点

\[
[\text{PDFで記号欠落}]
=
\frac{[\text{PDFで記号欠落}]}{2c}
\]

が実在するのか、それとも別の則へ切り替わるのかを判別する。

**構成要素**

- peer A4: t120 で 8.05、固定点予測 12.5、67%。
- Kubo Term I / II 分解の \(\eta\) 依存（3 regime）。
- K spectrum の5 modes の refit 完了時間。

**新規に書くべきもの**

1. \(c\) の \(N\) 依存性：peer の \([PDFで記号欠落]^{0.2}\)（持続因子 40）と \(c\simeq{\rm const}\) の同時観測を整理。
2. \(c\) の依存の非自明性：Adam の座標正規化が \(N\) に対して非線形。
3. 現象論モデルの \(c\) に Kubo の Term I / Term II 比を代入。

**予想される到達点**

\[
\text{短時間: }\sqrt t
\quad\rightarrow\quad
\text{中時間: }t^{0.4}\text{--}t^{0.5}
\quad\rightarrow\quad
\text{長時間: 飽和}
\]

という3 regime 構造。中時間の指数ずれは Adam の \(N\) 依存、長時間の飽和は侵食が注入に追いつくことに対応する。

### 段階4: Adam ハイパー依存 — Landing C の一部

**目標**

peer の穴 D-3（Adam 帰属）に答える。

**構成要素**

- Kubo の SGD regime での Term I / II 分解。
- Adam の座標正規化 \(m_t/\sqrt{v_t}\)。
- Kubo の3 regime（\(\eta\)）。

**新規に書くべきもの**

1. Adam の Term II 版：
   \[
   \eta^2\sum_j
   \left(\frac{m_j}{\sqrt{v_j}}\right)^2.
   \]
2. SGD \(\rightarrow\) Adam の座標正規化補正。
3. Kubo の CondA / SGD / 中 \(\eta\) と peer の CondA / Adam の対応。
4. \(\beta_1,\beta_2,\epsilon\) 依存を含む精密化。

**予想される到達点**

Adam の座標正規化は \(\|\Delta W\|^2\) の \(\overline{\|x\|^2}\) 因子を弱める一方、\(\overline{\phi'^2}\) 因子は残す。

### 段階5: \(W\rightarrow\sigma\rightarrow\) 折れ目密度 \(\rightarrow\) LoP — Landing D の一部

**目標**

W 増加が LoP を引き起こす因果を3段で接続する。

**既存の構成要素**

- \(W\rightarrow\sigma\): peer §D-0b で
  \[
  \sigma^2=0.065\|W\|^2
  \]
  の普遍定数を報告。
- \(\sigma\rightarrow\) 折れ目近くの密度: peer F6（幅が伸びれば、正負の押しの非対称が釣り合う点を沈める）+ Kubo の
  \[
  \Sigma_{XX}=0.25\,{\rm diag}(0_{\{15\}},1_5).
  \]
- 折れ目近くの密度 \(\rightarrow\) LoP: peer の resp_ee（\`RESPONSE_BOTH_WAYS\`）+ Kubo の \(S_b\)（\(\bar z_{\rm width}\) と \(\alpha\) の \(\rho=+1.000\)）。

**新規に書くべきもの**

1. \(W\rightarrow\sigma\) を CondA でも確認し、peer の RL-MNIST 版と対応づける。
2. \(\sigma\rightarrow\) 折れ目密度を Kubo の「駆動源5項式」の中に位置づける。
3. peer「長い地平線で沈下と幅を分ける_結果_0910」の「82–91% が消える」を因果的に解釈する。

**予想される到達点**

\[
\boxed{
W\text{ 増加}
\rightarrow
\sigma\text{ 増加}
\rightarrow
{\rm sinking}
\rightarrow
{\rm LoP}
}
\]

---

## 4. 各段階の実施可能性

| 段階                          | Chat で可能? | 走が要る?         | 位置づけ        | 時間見積り |
| --------------------------- | --------- | ------------- | ----------- | ----- |
| 1. FRESH \(\sqrt t\) の閉じた導出 | ✓         | 不要            | Landing B   | 1–2週間 |
| 2. 活性化依存の指数差                | ✓・部分的     | Landing C で必要 | Landing B/C | 2–3週間 |
| 3. 長時間則の判別                  | 骨格まで      | 必要            | Landing C   | 2–4週間 |
| 4. Adam ハイパー依存              | 骨格まで      | 必要            | Landing C   | 2–3週間 |
| 5. 3段構造の接続                  | 骨格まで      | Landing D で必要 | Landing D   | 3–4週間 |

**合計: 10–16週間**。PDF では、以前 Q1 で見積もった「強化版セット 5–7か月」の下限に相当するとしている。

---

## 5. 段階1の具体的な着手案

Kubo と peer で共有する Vault ノートとして、次を起票する案：

\`50_source/w-growth-sqrt-t-derivation-with-k-spectrum-0918.md\`

### 内容の骨組み

1. **前提**
   - peer §11 の恒等式
   - Kubo の Term I / II 分解
   - Kubo の K spectrum
   - Adam の座標正規化
2. **中核導出**
   - 1タスクの \(\langle W,\Delta W\rangle\) = マージン + バイアス補正
   - タスク全期でマージン打ち消し（Kubo の3 regime・中 \(\eta\) で最良）
   - Adam の
     \[
     \|\Delta W\|^2\simeq\eta^2 n_e({\rm activation})
     \]
   - タスク間の直交性 = K spectrum の bias mode 消滅から
   - 独立増分の累積で
     \[
     \|W\|\sim\eta\sqrt{n_e\,t}
     \]
3. **予測**
   - CondA / SGD / 中 \(\eta\) で \(\sqrt t\) 成長が観測される。
   - peer の RL-MNIST / Adam の実測との数値対応。
4. **未達**
   - 活性化依存の指数差（段階2）。
   - 長時間則の飽和（段階3）。

---

## 6. 未読・未照合

PDF 内で明示されている留保：

- peer の [[駆動源問題_0909]] 全文は精読していない。peer の「なぜ正味の \(i(t)\) が負になるか」の Q1 が W 増加問題と密接に関連。
- peer の \`第1層の成長の中身_事後_0910.md\`: \(\widetilde W\) の「タスク内 coherent + タスク間直交」、持続因子 12–23 step。
- peer の \`なぜ下がるか_活性化誤差の分解_事後_0910.md\`: 侵食項の正体を「誤答標本へのヘッジ」と同定。
- peer の \`ゲートなし線形網の幅成長_結果_0910.md\`: LIN での成立検証。
- peer の \`長い地平線で沈下と幅を分ける_結果_0910.md\`: 3段構造の「82–91% が消える」の登録実験。
- Kubo の以前の U4 勾配式は詳細未読。
- Kubo の \(S_b\) の詳細：\(\bar z_{\rm width}\) と \(\alpha\) の \(\rho=+1.000\) を Tier D へ上げる証拠・数値。
- Adam 座標正規化の精密な閉形式には \(\beta_1,\beta_2,\epsilon\) 依存が必要。
- CondA / SGD の500タスク実験では middle 領域は見えているが、真の \(\sqrt t\) 検証には数千タスクの走が必要。

---

## 7. Kubo への提案

PDF の推奨は **(1) + (2) を先に**。

1. 段階1（FRESH \(\sqrt t\) の閉じた導出）の Vault ノートを起票する。
2. peer の [[駆動源問題_0909]] を精読する。
3. CondA / SGD の長期実験（数千タスク）を Claude Code に委譲するか判断する。
4. Adam の座標正規化の精密化を Chat で先に理論作業するか判断する。
