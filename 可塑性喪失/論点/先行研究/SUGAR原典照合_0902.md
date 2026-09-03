# SUGAR 原典照合（forward ReLU / backward 代替勾配の先行）

親: [[逆伝播漏れ2x2_spec_0902]] §9 #6 / 状態: **精読済み（2026-09-02）** / 格: **外部・一次資料**（PDF 本文から直接引用）
関連: [[論点マップ]]／[[運用ルール]] §2

> **原典**: Horuz, Kasenbacher, Higuchi, Kairat, Stoltz, Pesl, Moser, Linse, Martinetz, Otte, *The Resurrection of the ReLU*, arXiv:2505.22074v1, 2025-05-28。
> spec 起草時は「alphaxiv 要約・原典未精読・数値は引かない」の格だった。**本ノートで一次資料に上げる。** 以下の数値は PDF 本文からの直接引用。

---

## 1. 機構は当方の `BL` と同じ

SUGAR は **forward を標準 ReLU に固定したまま、backward だけ代替関数 $f$ の導関数に差し替える**。原典 §4.1 の言い方では、代替 $f$ について「$f$ を forward に使い真の勾配を backward に使う（非 SUGAR）」対「ReLU を forward に使い $f$ の勾配を backward に使う（SUGAR）」を比べている。**これは [[逆伝播漏れ2x2_spec_0902]] の `BL`（順 ReLU／逆 leaky）と同一の構成である。**

さらに近い先行が原典 §2.1 に挙がっている: **ProxyGrad**（Linse, Barth, Martinetz [22]）は「backward に LeakyReLU、forward に ReLU」をそのまま使っており、活性化最大化（AM）が悪い局所解から抜けられるようになったと報告している。**当方の `BL` の構成そのもの**だが、目的は特徴可視化であって学習の汎化でも可塑性でもない。著者群が SUGAR と重なっている。

## 2. LeakyReLU 代替は弱かった — その設定

評価された代替関数は **LeakyReLU・SELU・ELU・GELU・SiLU (Swish)・Mish・B-SiLU・NeLU** の 8 種。

> 原典 §4.1: LeakyReLU と NeLU は「negligible or negative gains」。ResNet-18 / CIFAR-100 で **43.67 % → 43.41 %**（テスト精度・SUGAR 適用で下がっている）。最良は B-SiLU で、ResNet-18 / CIFAR-100 が **48.99 % → 56.51 %**、VGG-16 が **48.73 % → 64.47 %**。CIFAR-10 では ResNet-18 が 76.76 % → 86.42 %、VGG-16 が 78.50 % → 88.35 %。

新規提案の 2 つ:

- **B-SiLU**（Bounded Sigmoid Linear Unit）: $\mathrm{B\text{-}SiLU}(x) = (x+\alpha)\sigma(x) - \tfrac{\alpha}{2}$、$\alpha = 1.67$
- **NeLU**（Negative slope Linear Unit）: 導関数が $x>0$ で 1、それ以外で $\dfrac{2\alpha x}{(1+x^2)^2}$。**深い負側で 0 に戻る帯型**

原典の結論は「simple linear leakage fails to harness the benefits of SUGAR **under this setup**」。

## 3. その setup が当方と違うところ（§9 #6 の一行）

| | SUGAR | 当方 `bwd_leak_0902` |
| --- | --- | --- |
| データ分布 | **定常 i.i.d. 単一タスク**（CIFAR-10 / CIFAR-100 を 50 / 100 epoch。continual・non-stationary・task switching の語は本文に 1 度も出ない） | **非定常**。condA・$T=10^4$ ステップごとに flip が替わる 500 タスク |
| endpoint | **テスト精度**（と検証損失） | **未フィット率 $U_k$ が閾値 0.05 を超えるか**（発症数）。精度ではない |
| 規模・最適化 | VGG-16 / ResNet-18（＋Conv2NeXt・Swin）、batch 128、SGD lr 0.001、data augmentation なし、5 seed | 隠れ 1 層 w100、batch 1、素の SGD lr 0.01、10 seed |
| 死んだユニット | 「dying ReLU」「dead neurons を蘇らせる」を明示的に扱い、SUGAR が dead activation の確率を大きく下げると報告 | 同じ現象を扱うが、**可塑性喪失（LoP）の発症**として測る |
| 可塑性喪失 | **言及なし**（plasticity / continual / non-stationary いずれも本文に無し） | これが主題 |

**一行**: SUGAR で LeakyReLU 代替が弱かったのは**定常 i.i.d. の CIFAR 分類をテスト精度で測った設定**であって、当方が測るのは**非定常タスク列で可塑性喪失が起きるか否か**という別の endpoint・別の regime なので、あちらの「線形な漏れは効かない」は当方の予言にならない。

## 4. 引用上の注意

- 本ノートの数値は **PDF 本文からの直接引用**であり、当方の走の結果ではない。[[逆伝播漏れ2x2_spec_0902]] の verdict と同じ表に並べない
- SUGAR は**当方の `BL` の機構的先行**である。「先行がある」で済ませず、上の設定差を添えて引く
- **ProxyGrad の方が `BL` に近い**（順 ReLU／逆 LeakyReLU そのもの）。ただし AM 用途。原典 [22] は未精読
- SUGAR は $a$ を掃いていない側の情報も持つ: NeLU は $\alpha \in \{0.01, 0.05, 0.1\}$ で 43.2 / 42.4 / 41.9 %（大きいほど悪い）。**帯型代替勾配は [[逆伝播漏れ2x2_spec_0902]] §2 が「本走が答えないこと」に挙げた項目**なので、当方の未走部分に対応する外部証拠として残す
