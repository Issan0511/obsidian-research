# 文字 GPT 沈降パイロット（1019）

格：**事後・未登録・seed 0 のみ・1 課題だけ**。クラウドセッションの CPU で実行（GPU なし）。使い道は [[文字GPTで継続学習_乱数マルコフ言語と窓の乱数ラベル_設計案_1019]] §1.2 の根拠と、本走の実装の起点。

## ファイル

- `tiny_gpt_sink.py`：実行したスクリプトそのもの（sha256 `8904ec0bea338277fc2796b90eecda68c08b1d7283aa5377b9d233b524b00ded`）。
- `pilot_trajectories_every100.csv`：5 走の推移を 100 反復ごとに間引いたもの（元の記録は 50 反復ごと。元の JSON はクラウドの一時領域にあり保存していない）。

## 再現

データは Tiny Shakespeare（`https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt`、1,115,394 byte、sha256 `86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed`）。環境は Python 3.13、torch 2.14.1+cpu。

```
python tiny_gpt_sink.py --data input.txt --out arm_A.json --arm A --threads 1
python tiny_gpt_sink.py --data input.txt --out arm_B.json --arm B --threads 1
python tiny_gpt_sink.py --data input.txt --out arm_C.json --arm C --threads 1
python tiny_gpt_sink.py --data input.txt --out arm_D.json --arm B --lr 1e-3 --threads 2
python tiny_gpt_sink.py --data input.txt --out arm_E.json --arm B --lr 1e-3 --act gelu --threads 2
```

既定値は 4 層・d 128・4 head・文脈 128・batch 32・1,200 反復・warmup 300・warmdown 350・測定 50 反復ごと・seed 0。スレッド数が違うと浮動小数の和の順が変わり、ビット一致はしない。1 反復は CPU 1 スレッドで約 0.85 秒、1 走 17 分ほど（D・E は 2 スレッドで 11 分ほど）。

## 腕

| 走   | `--arm`                    | 正規化と bias       | dropout | 活性化  | 最適化と lr                                                                                                      |
| --- | -------------------------- | --------------- | ------- | ---- | ------------------------------------------------------------------------------------------------------------ |
| A   | A                          | LN γ のみ・bias なし | 0       | ReLU | ブロック内の行列は Muon（lr 5e−4、運動量 0.95、Nesterov、Newton–Schulz 5 回）、ほかは AdamW（lr 5e−3、β 0.9/0.95、wd 0）。GPT-nano のレシピ |
| B   | B                          | LN γ・β・bias あり  | 0.1     | ReLU | Adam（lr 1e−4、β 0.9/0.999）                                                                                    |
| C   | C                          | LN γ のみ・bias なし | 0       | ReLU | AdamW（lr 1e−3、β 0.9/0.95、wd 0）                                                                               |
| D   | B ＋ `--lr 1e-3`            | LN γ・β・bias あり  | 0.1     | ReLU | Adam（lr 1e−3）                                                                                                |
| E   | B ＋ `--lr 1e-3 --act gelu` | LN γ・β・bias あり  | 0.1     | GELU | Adam（lr 1e−3）                                                                                                |

## CSV の列

測定は検証側（Tiny Shakespeare の末尾 10%）から生成器 seed 1234 で固定した 64×128 トークン、eval モード。z は各層の FFN の up 出力（活性化の直前）。

- `val_loss`：固定した検証バッチでの交差エントロピー（nat）。
- `neg_frac`：z < 0 の割合（全トークン・全 unit）。
- `units_mean_neg`：トークン平均 μᵢ が負の unit の割合。
- `med_mean_over_sd`：μᵢ/σᵢ の unit 中央値。
- `dead_units`：固定バッチの全トークンで z ≤ 0 の unit の割合。
- `bias_mean`：up の bias の平均（B・D・E のみ）。
- `frac_mean_from_bias`：Σᵢ|bᵢ| / Σᵢ|μᵢ|（unit ごとの比の中央値ではなく、和の比。B・D・E のみ）。
