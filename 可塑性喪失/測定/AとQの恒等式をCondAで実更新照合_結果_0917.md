# AとQの恒等式をCondAで実更新照合 — 結果 0917

状態: 完了（着手 2026-09-17、数値診断・保存完了 2026-09-18）
依頼: Issa「一旦この式を疑いたい。CondAかPMで各項が本当に合ってるか検証して」
親: [[駆動源問題_0909]] §11.1 / [[W増大メカニズム_0909]]
run: aq_identity_0917 / 担当: Codex_AQ検証0917

## 結論

**通常SGDの A・Q の展開式と、実更新によるノルム変化は一致した。**
float64で、中心化ノルムの一更新収支の最大絶対誤差は 1.86114891e-14。正負の増減の判定不一致は0。

ただし、**登録した総合判定は FAIL のまま保存**した。float32で演算順を変えた独立順伝播との比較に100個のスカラー許容差超過が出たため。
結果を見た後に別の診断追補を固定して調べると、100個すべてが再現し、順伝播を実装と同じ演算順に揃えた自動微分では許容差超過が0となった。診断は FORWARD_ROUNDING_ORDER。元の許容差を緩めたりFAILをPASSに書き換えたりしていない。
数式・実更新の収支と、float32の異なる計算順の一致は分けて判定する。

## 式と独立な照合経路

一標本、損失 $\ell=(f-y)^2$、$u_i=2(f-y)v_i$、$h_i=u_i\phi'(z_i)$。
行平均を除いた重みを $\widetilde w_i$、入力の座標平均を除いたものを $\widetilde x$ とする。

$$
\widetilde z_i=\widetilde w_i^\top\widetilde x,\qquad
A_i=h_i\widetilde z_i,\qquad
Q_i=h_i^2\|\widetilde x\|^2,
$$
$$
\Delta\|\widetilde w_i\|^2=-2\eta A_i+\eta^2Q_i.
$$

1. 更新前の残差・v・活性化の微分・入力から各項を展開。
2. 別記述の順伝播とPyTorch自動微分から勾配を取り、内積と二乗ノルムを直接計算。
3. 本番実装の手書き勾配とSGD更新を実行し、更新前後の重みからノルム差を直接計算。
4. S+H-B-C、実変位の平行・直交分解、256更新の累積収支、32標本のバッチ勾配の交差項も照合。

更新則・勾配・今回のleaky活性化の分岐は元の学習commit 0ba13e8 とAST一致。更新前の値だけで予測し、W・bias・v・出力biasは同時更新する。

## 対象と格

CondAの保存済み学習状態。20入力（うち5自由bit）・隠れ100unit・スカラー出力・MSE・通常SGD。

- 4条件: leak 0.1 / 0.3 / 0.7、leak 0.3に出力offset +0.5。
- 保存点: 更新0 / 200000 / 1000000 / 5000000、各10 seed。
- 各時点の全32支持点、固定状態からの学習率 0.0001 / 0.001 / 0.005。
- float64とネイティブfloat32を別々に検査。
- 更新200000の状態から、各条件・精度で256更新の短い継続も検査。保存時のタスク・入力offsetを固定し、登録した新しい入力列を使う。元の乱数列の再生や1タスク全体ではない。

**格は、手順を先に登録した既存checkpointの数式・実装監査。長期の学習率依存やLoP機構の新たな実証ではない。**
CondAで従来「自由重み」と呼ぶ末尾5座標と、行平均除去による中心化重みは別。全W・中心化W・自由5座標を別々に検算した。

## 数値結果

数値正本: results/aq_identity_0917/summary.md、verdict.csv、diagnostic_verdict.csv。

| 検査（float64・中心化重み） |         最大絶対誤差 |
| ----------------- | -------------: |
| A：展開式と自動微分        | 1.51878510e-13 |
| Q：展開式と自動微分        | 2.84217094e-13 |
| AとS+H-B-C         | 5.32907052e-15 |
| 一更新のノルム収支         | 1.86114891e-14 |
| 256更新の累積収支        | 2.39261735e-14 |

固定状態の一更新プローブは各精度1,536,000 unit-update件。float64は全件が登録した丸め誤差幅より大きく、収縮773,973件・成長762,027件、符号不一致0。これはcheckpoint・入力・個体・学習率を束ねた検算件数で、独立な学習実験の本数ではない。

float32の一更新収支の最大絶対誤差は2.83980464e-6で、全件が登録した丸め誤差幅内。固定状態プローブのうち符号を判定できたのは447,382件で、不一致0。残り1,088,618件は精度上未判定であり、「符号一致」と数えていない。

float32の別演算順で起きた100個の不一致は、順伝播出力の最大差3.09944153e-6から来ていた。活性化ゲートの符号違いは0。演算順を合わせた自動微分との比較では不一致0。これらの事後診断は診断追補と別CSVに保存。

## 誤った式を検出できるか

次の意図的な誤りをすべて検出した。

- MSEの係数2を落とす。
- 中心化応答 $\widetilde z$ を全前活性 $z$ に置き換える。
- Qで入力の中心化を落とす。
- offset活性化で非斉次補正Hを落とす。
- バッチのQを「平均勾配の二乗」ではなく「標本勾配の二乗の平均」に置き換える。

## 会話の解釈への制約

**式が合っていることと、「正側なら縮む・負側なら伸びる」が正しいことは別。**
固定状態のfloat64プローブでは正側・負側のどちらにも収縮と成長があった。正側z>0だけでは中心化応答の符号もAの符号も決まらない。正負の長期差や学習率が大きい側での縮小を説明するには、残差との整列・AとQの時間収支を調べる必要がある。

## 出所・再現

- [登録spec](https://github.com/Issan0511/lop_analysis/blob/c7df571/specs/spec_aq_identity_0917.md)
- [結果summary](https://github.com/Issan0511/lop_analysis/blob/745707b/results/aq_identity_0917/summary.md)
- [全照合結果](https://github.com/Issan0511/lop_analysis/blob/745707b/results/aq_identity_0917/checks.csv)
- [診断追補](https://github.com/Issan0511/lop_analysis/blob/a78115c/specs/addendum_aq_identity_0917.md)
- [float32診断判定](https://github.com/Issan0511/lop_analysis/blob/745707b/results/aq_identity_0917/diagnostic_verdict.csv)
- [検証図](https://github.com/Issan0511/lop_analysis/blob/745707b/results/aq_identity_0917/identity_check.png)
- 元データ: ~/Projects/obsidian-research-data/zero_attraction_0913/training/ckpts/
- 本検証の全配列・ログ: ~/Projects/obsidian-research-data/aq_identity_0917/。42ファイルのSHA256をbackup_manifest.jsonで検証済み。
- 実行コード・checkpoint hash・実装hashはprovenance.json。追加の長期学習は行っていない。
