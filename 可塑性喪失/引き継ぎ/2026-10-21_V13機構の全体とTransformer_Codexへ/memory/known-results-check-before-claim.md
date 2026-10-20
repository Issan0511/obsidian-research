---
name: known-results-check-before-claim
description: 新しい走の問いと読みを書く前に、vault で同じ構図の既知（µ 経路／b 経路など）を探して引く。既知の言い直しを発見として書いた（1010、Issa 指摘）
metadata:
  type: feedback
---

cnn_center_1010 で「中心化すると入力層の沈降は bias 経路で続く＝駆動は入力の幾何に依らない」を新しい読みとして書き、予測でも「止まる」を本命にした。Issa「中心化でバイアス経由になるのは既知ですね」。vault の [[centered_bias凍結結果_0901]]（µ 経路支配の std と b 経路支配の centered）と 帯別帳簿_0922 の恒等式（平均方向の重み勾配 = bias 勾配 × ‖µ‖²）で確定済みだった。

**Why:** 既知を引かないと、予測の本命を外し、結果ノートで既知を発見として書き、Issa の時間を訂正に使わせる。この研究は 9 月から大量の測定があり、同じ構図が別の名前（µ 経路・DC 経路・平均パッチ方向・u₀）で何度も出てくる。

**How to apply:** spec の「既知」の節を書く前に、問いのキーワードの同義語（µ・平均方向・DC・中心化・bias・b 経路・u₀ など）で vault の 測定/ と 論点/ を grep し、該当があれば既知として引いて、新しく問えるのは量か別の箱での成立かに絞る。結果ノートの「読み」も、既知と新規を分けて書く。関連: [[theory-question-answer-theory-grade]] [[derived-mechanism-over-narrative]]
