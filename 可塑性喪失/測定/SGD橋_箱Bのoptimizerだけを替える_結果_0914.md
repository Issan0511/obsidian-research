# SGD 橋：箱 B の optimizer だけを替える：結果 0914

状態: **完了**（登録走・50/50 完走・main に統合済み） / 更新: 2026-09-14 10:3x JST / 起草: Claude
親: [[Snakeの位相をMNISTへ移す_結果_0914]] / spec: [[SGD橋_箱Bのoptimizerだけを替える_spec_0914]]（repo 事前登録 `a3d5f3a`・実装 `81ddc84`・結果 `f15cea6`・退避 `1993e94`）
発端: Issa「peak は重みを縮めましたか？」→（MNIST・Adam では縮まず育った）→「SGD 橋いりそうですね」→ 範囲「α=0.6 の 5 腕」

> 数値の出所は repo main の `results/sgd_bridge_mnist_0914/summary.md`・`verdict.csv`。ΔlogN は log（t101–120 の中心化ノルムの二乗平均平方根）、精度は pt。n = 10 seed（0914 の seed 0–9 と同じ初期 W・タスク列）。

## 結論

1. **SGD にすると、peak の「余分な成長」は小さくなり、層 2 では CondA と同じ向き（normal より育たない）に反転する。**
   - 見出し X（ΔlogN の SGD − Adam、seed 対）:
     - 層 1: −0.083 [−0.089, −0.077]、`X_NEGATIVE`。peak−normal は Adam の +0.118 から SGD の +0.035（`GROWTH_ENHANCED_BELOW_CONDA_SCALE`）へ縮む。
     - 層 2: −0.240 [−0.254, −0.226]、`X_NEGATIVE`＋`SIGN_REVERSED`。SGD の peak−normal は −0.204 [−0.212, −0.196]（`GROWTH_SUPPRESSED`）で、CondA の log 差 −0.099 の約 2 倍。
   - spec §4.2 の書き方の規則により、「optimizer が peak の成長の向きを決める」と書けるのは**層 2 だけ**。層 1 は「SGD では peak の余分な成長が小さくなる」まで。
2. **それでも、初期値より縮むユニットは SGD でも出ない。** strict な縮小の割合は N06・P06・LIN・LR の層 1・層 2 すべてで 0%（`FORK_ABSENT`）。伸びの最小値も層 1 で N06 3.66 倍・P06 4.07 倍、層 2 で 1.33 倍（P06）。CondA の「多数が縮み少数が育つ」分岐は、optimizer では説明できない（損失・入力・深さの側の差として残る）。
3. **valley は SGD では死んだ起点から抜け出せない。** V06 は 10 seed すべてで t1 から正答率 11.35%（最多クラスの水準）に張り付いた。抜け出したのは 4 seed で t102–t117、残る 6 seed は t120 まで抜けなかった。BROKEN 7/10 で C2 は `INCOMPLETE`。Adam では同じ初期値から task 1 で学習できていたので、**Adam の座標正規化が valley の消えかけた勾配を救っていた**（0914 の事後値: 初期の |g_W1| 中央値は 1.3–1.6e−7）。
4. **時間劣化の向きも optimizer で逆になる。** SGD の C1 P06−N06: D +0.19 [+0.05, +0.33]（`MORE_DECLINE`）、ΔA_late −0.96、ΔGap +0.22（`GAP_LARGER`）、ΔA_fresh −0.74（`FRESH_LEVEL_CONFOUNDED`）→ `TEMPORAL_LOP_MORE`。Adam では同じ対比が LESS_DECLINE（−0.41）だった。
5. SGD 箱の水準: N06 の A_late は 93.3（Adam 89.5）、劣化 D は 0.93（Adam 2.27）。TESTABLE_FIXED（N06−LIN）は +0.75 [+0.66, +0.85] で成立。

## 表

### X と G

| 対比・層 | Adam の ΔlogN（seed 0–9） | SGD の ΔlogN | SGD の G ラベル | X（SGD − Adam） | X ラベル |
|---|---:|---:|---|---:|---|
| C1 P06−N06 層 1 | +0.118 | +0.035 [+0.031, +0.039] | GROWTH_ENHANCED_BELOW_CONDA_SCALE | −0.083 [−0.089, −0.077] | X_NEGATIVE |
| C1 P06−N06 層 2 | +0.035 | −0.204 [−0.212, −0.196] | GROWTH_SUPPRESSED | −0.240 [−0.254, −0.226] | X_NEGATIVE・SIGN_REVERSED |
| C2 V06−N06 層 1・2 | +0.084 / +0.187 | — | INCOMPLETE（n=3） | — | INCOMPLETE |

### 腕ごと（REPORT）

| 腕 | 層 1 成長倍率 | 層 2 成長倍率 | logN1 の SGD−Adam | logN2 の SGD−Adam | 最小倍率 層 1 / 層 2 | D | A_late |
|---|---:|---:|---:|---:|---|---:|---:|
| N06 | 4.87 | 2.36 | −0.72 | +0.21 | 3.66 / 1.41 | 0.93 | 93.30 |
| P06 | 5.04 | 1.92 | −0.80 | −0.03 | 4.07 / 1.33 | 1.12 | 92.35 |
| LIN | 4.27 | 1.40 | −1.03 | −0.12 | 3.65 / 1.04 | 0.17 | 90.19 |
| LR | 5.29 | 3.21 | −0.98 | −0.30 | 1.50 / 1.15 | 1.40 | 92.40 |
| V06（n=3） | 1.69 | 1.30 | −1.86 | −0.56 | 0.99 / 0.96 | — | — |

SGD では層 1 の成長は Adam の約半分（N06 で 10 倍 → 4.9 倍）、層 2 は腕によって Adam より大きい（N06 +0.21）。M1: C1 は層 1・2 の両窓で PHASE_ACTIVE。

## 事前予測の採点（Claude）

| # | 予測 | 結果 |
|---|---|---|
| Q1 | S16 の橋が完全一致 | ○ |
| Q2 | lr 0.02 で発散しない | ○（パイロット GO。ただし V06 は発散ではなく学習不能） |
| Q3 | TESTABLE_FIXED 成立 | ○（+0.75） |
| Q4 | X C1 層 1 が X_NEGATIVE | ○ |
| Q5 | SGD の C1 層 1 が GROWTH_SUPPRESSED | ×（層 1 は ENHANCED のまま。反転したのは層 2） |
| Q6 | 5 腕とも層 1 で FORK_ABSENT | △（4 腕 ABSENT、V06 は n=3 で INCONCLUSIVE。反証条件の FORK_PRESENT は無し） |
| Q7 | 層 2 で少なくとも 1 腕が PRESENT か INCONCLUSIVE | △（V06 の INCONCLUSIVE は n=3 によるもので、分岐の証拠ではない） |
| Q8 | C1 の E1 が Adam と同じ LESS_DECLINE | ×（MORE_DECLINE） |

## 読み方の限定

- X は「optimizer と更新数（625 → 2,500/タスク）を合わせて替えた効果」。どちらが効いたかは分けていない。
- CondA との残りの違い（MSE 対 CE、5 自由入力 対 784 入力、1 層 対 2 層、α=1 対 0.6）は分けない。**分岐が出ない理由は optimizer 以外**、までが言える。
- V06 の欠測は判定規則（BROKEN）どおりで、C2 は答えられない。valley を SGD で比べるなら、死んだ起点を避けた初期関数の角（V06i 型）か、学習を始められる lr が要る。
- n = 10。腕間の幅の差は W 病理の証拠ではない。
- BROKEN の修飾は summary.md の表に出ていない（判定コードの出力漏れ）。V06 の BROKEN 7/10（seed 0・3・4・5・6・7・9）は rows.csv の ce0/ce20 から数えた値で、`verdict.json` の n と一致する。

## 所在

repo main: `specs/spec_sgd_bridge_mnist_0914.md`・`configs/sgd_bridge_mnist_0914.yaml`・`src/sgd_bridge_mnist_0914.py`（0914 のループの Adam 関数だけをプロセス内で SGD に差し替え）・`analysis/sgd_bridge_mnist_0914/`・`results/sgd_bridge_mnist_0914/`（summary・verdict・adam_reference.json・全 50 走の rows と provenance）。生データは `~/Projects/obsidian-research-data/sgd_bridge_mnist_0914/`（280 ファイル・0.26 GiB、manifest あり）。
