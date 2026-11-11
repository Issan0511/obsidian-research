# 読み出し成長の害を方向・尺度・伝達・記憶に分ける

2026-11-11。依頼「ViTとELUの読み出し成長による害をちゃんと分離して」への追加実験。**280本の学習軌道と2520件の局所比較を完了**。ELUはtask-end10の10 seeds、最終affine LNありのViT SLはtask-end100の5 seeds。両者の状態・課題・期間は異なるため、アーキテクチャ一般やLNの有無だけの因果比較ではない。

**P後にも縮小で除ける学習費用がELUでは大きく残った。ViTではP自体が改善をもたらし、P後の追加縮小利益は確認できなかった。ただし「ELUは大きさだけ、ViTは整列だけ」という分離は支持されない。**

## 何を操作したか

- S：元の読み出し。
- P：読み出し行列の各列でクラス要素を独立に並べ替える。重みを縮めず、列内の値とノルムを保存する。ただしクラス対応・列間Gram・出力確率を変えるので、純粋な整列除去ではない。
- O：全1方向を固定するクラス空間の直交変換。WᵀW・特異値・列平均・列ノルムを保存する。
- 0.1倍：クラス平均を除いた読み出し成分を縮小し、biasでfork時の全訓練集合の各クラス平均logitを保存する。ゼロhead介入とは異なる。
- body Adam保持／消去、forwardの弱化／body勾配gain、ELU／最終LNの逆伝播変更を別条件にした。全新条件でhead Adamは消去済み。

同じsource内ではbody・次課題ラベル・batch系列を共通にした。ELUは4000更新、ViTは1500更新。主指標Uは学習期間平均の訓練accuracy不足。

## 主要結果

下表はbaseline−interventionのU差をpp表示。正なら期間平均accuracy改善。95%区間は対応付きseed bootstrap 10000回、記述的・多重比較調整なし。body Adam保持。

| 操作             |        ELU 改善pp [95% CI] |      ViT 改善pp [95% CI] |
| -------------- | -----------------------: | ---------------------: |
| Sを0.1倍へ縮小      |     +19.46 [18.63,20.65] |     +6.80 [2.15,11.47] |
| 大きさを保ちS→P      |       −0.76 [−1.78,0.20] |     +9.18 [5.29,14.44] |
| **P後に0.1倍へ縮小** | **+19.48 [18.35,20.79]** | **−1.42 [−3.75,1.02]** |
| S→O            |       −0.12 [−1.09,1.06] |     −0.03 [−6.56,3.75] |
| O後に0.1倍へ縮小     |     +19.80 [18.99,20.59] |     +7.28 [0.46,14.14] |

ViTのP自体の改善は5/5 seedsで同方向。P後縮小の区間がゼロを跨ぐのは「残余費用がゼロ」という同等性の証明ではない。OはPの改善を再現せず、O後の縮小利益は残る。ただしSとOも同等と証明されていない。Pの効果をGramだけに帰属することもできない。

![[可塑性喪失/測定/補助データ/readout_separation_1111/physical_curves.png]]

出典：contrasts.csv の metric=U、kind=scale/direction。縮小効果に対するPの交互作用 scale_by_P_keep はELU −0.018 [−1.033,0.962] pp、ViT +8.222 [2.707,14.460] pp。

## 局所の機序と、後の学習を分ける

**ELUでは残差と読み出しの組合せが重要。** 同じ確率ベクトルのままbackwardだけS→Pへ変えると、virtual Adamによる全1200入力の平均preactivation変位は−0.00652から+0.00131へ反転した。しかしforwardもP自身の確率にすると−0.00832となる。固定状態のP/Pにも下向き作用が現れるため、P後に残る作用を「整列を除いた純粋なノルムの害」とは呼べない。

**ViTでは方向と本体への伝達が重要。** Sの確率を固定してbackwardをS/P/Oへ変えると、head入力勾配normは1.735/1.754/1.703なのに、trunk parameter gradient normは59.83/13.80/71.41。Pでhead入力やpre-LNのnormは減っていないのに、trunkで減る。最終LNによる単純なnorm減衰だけでは説明が足りない。特定の層・Gram成分が長期効果を媒介した割合までは未識別。

![[可塑性喪失/測定/補助データ/readout_separation_1111/frozen_crossed_maps.png]]

行はforward、列はbackward。同じ行では確率全体が一致。左はELUの平均位置のAdam変位、右はViTのtrunk勾配norm。局所の測定対象が違うため左右の数値を直接比較しない。

**勾配制限を外せば改善するわけではなかった。** 最初の200更新だけ、forwardをその時点のnativeと同じに保ち、ELU derivativeを1へ変えると全Uが+11.30 [10.83,11.83] pp悪化。ViTの最終LN radial subtractionを外すと+10.85 [8.83,12.88] pp悪化した。固定初期状態でELUの下向き平均変位が消えても、そのJacobian方策の学習成績は改善しない。LNなしモデルの実験ではなく、forward正規化とgamma/beta、他のLNは残る。

## Adam・head再学習・時間帯を分ける

**Adam履歴の効果は尺度で反転した。** S1でbody Adamを消去するとELU −4.36、ViT −5.99 pp悪化。S0.1ではELU +6.16、ViT +2.56 pp改善し、各95%区間は同符号。勾配を0.1倍にしても、clear Adamの局所更新normは約0.975/0.997倍に留まり、保存Adamでは約0.456/0.293倍だった。勾配の大きさと実際の更新量を混同しない。

**forwardの弱化とbody gainは足し算できない。** 最初の200更新のSに対するforward単独操作Tの全U改善はELU +10.12、ViT +1.54 pp（後者は区間ゼロ跨ぎ）。body gain単独Gは+2.37/+7.98 pp。大きな交互作用があり、ViTのP後Tは−21.00 ppと悪化する。Tは固定したクラス別平均logitを基準に縮小するので、argmaxも変わり得る。純粋なconfidence/temperature操作ではない。

**物理縮小とTGでもheadの学び直しが異なる。** 初期p・body/head勾配を揃えても、同じ最初のhead座標更新がlogitへ反映される係数は物理縮小で1、TGで0.1。解除前200更新でも物理縮小が有利だった（physical−TGのUacute：ELU S −1.97、ViT S −4.55 pp、各区間負側）。ただしその後はhead/body/pが連成して分岐し、TGだけ200更新で解除されるため、全U差をhead再学習の倍率だけに帰属しない。

**初期と全期間も違う。** ELUの縮小はbody Adam保持だと初期200では小さく悪化（S −0.56 pp、P −0.35 pp、O −0.64 pp、各区間負側）するが、その後の改善により全期間では約+19〜20 ppになる。Uacuteは解除前200、Ulateは解除後200を使用する。

ViTではW→0.1W、gamma/beta→10倍によりlogitsと上流VJPを保存できることを全5 sourcesで確認した。raw W normだけでは機能的な読み出し強度が決まらない。ただしAdam軌道まで同じではない。

## 今回言えること

ELUでは、固定状態の残差/readout/activation derivativeの組合せが平均位置を動かし、P後にも縮小で除ける学習費用が残る。ViTではPによる読み出しの対応・幾何の変更が大きく効き、その後の縮小利益は未確認。両者にAdamとhead再学習、伝達規則が作用するので、同じ「大きな読み出しの害」と一括できない。

局所の平均位置変化がELUの長期費用の唯一の原因とは認定していない。以前の [[P後に残る読み出し依存費用とViT装填費用の直接比較_p_residual_loading_結果_1111]] のゼロheadと今回の平均logit保存0.1倍は別操作で、差を原因割合やdose効果に換算しない。

## 出典と再現

- [統合報告](/home/issan/Projects/claude/proj_004_drift/results/readout_separation_1111/synthesis.md)
- [全学習比較](/home/issan/Projects/claude/proj_004_drift/results/readout_separation_1111/summary.md)
- [局所比較の式・CI・出典キー](/home/issan/Projects/claude/proj_004_drift/results/readout_separation_1111/frozen_interpretation.md)
- [独立解釈](/home/issan/Projects/claude/proj_004_drift/results/readout_separation_1111/independent_interpretation.md)
- [科学レビュー](/home/issan/Projects/claude/proj_004_drift/results/readout_separation_1111/scientific_review.md)
- [事前登録](/home/issan/Projects/claude/proj_004_drift/specs/spec_readout_separation_1111.md)

実行commit a079256e9dc153cc029e3f8c01863efeddb4824f、分析コード固定411f2804246d9015db90496f8b24d694f0e4c912。全280曲線・2520局所記録の完全性検査PASS、旧KC対照30本は全保存点で完全一致。停止した最初の試行も保全し、主解析から除外した。実行時の数値検証修正はimplementation_notes.md、全資源・完了検査はcompletion.json。

生データとログは /home/issan/Projects/obsidian-research-data/readout_separation_1111/ に742ファイル、913628851 bytes、SHA256照合済み。結果ディレクトリのbackup_manifest.jsonで元パスと退避先を対応付けている。
