# centered bias凍結 結果（9/1）

親: [[中心主張v5計画_0831]] §5 P-1・[[現象2_b経由の死_0831]] / run id: `centered_freeze_0901`

状態: **決着（実行前固定介入・10 seed・5M）** / 更新: 2026-09-01 / repo commit: `f402f80`

> **格の自己申告。** repo の spec は5M本走前に作成し、判定閾値を固定して S0 replay と frozen smoke を通してから本走した。ただし **spec 単独の事前 commit はしていない**。したがって「committed 事前登録」とは呼ばず、**チャットログで時系列を追える実行前固定**として運ぶ。実装・spec・結果は本走後に repo commit `f402f80` で一括 commit した。

## 一行

**condA・centered の終盤 `strict_dead` は $b\equiv0$ で 0 になり、b 経路の必要性は P1 `BIAS_ROUTE_DECISIVE`。しかし厳密 `unfit` は 0.00397 → 0.22811 と逆に悪化し、bias 凍結は治療ではない。Dead と機能は逆向きに解離した。**

## 設計

- condA・1隠れ層・幅100・ReLU・$T=10^4$・batch=1・plain SGD・lr=0.01
- 学習器入力だけ EMA centered（`center_alpha=0.01`）、教師は生入力
- seed 0–9、5M step。新規走は `freeze_bias=true` の1腕
- free 対照は既存 `mlp2_phase1_0829/L1w100_A1`。30k・1k格子の free replay で `p_hat` 配列一致、`eval_loss_exact` / `unfit` 一致を確認
- 32パターン全支持を task-end で厳密列挙。主窓は task 451–500

## 判定

| endpoint | 判定 | 主な数値 |
|---|---|---|
| P1（終盤50 task・主判定） | **`BIAS_ROUTE_DECISIVE`** | `strict_dead_frac`: free **0.463940** → frozen **0.000000**。減少率 **1.000**。paired差 frozen−free **−0.463940 [−0.514620, −0.410039]** |
| P1-final（5M・補助） | `REPORT_ONLY` | free **0.469000** → frozen **0.000000**。paired差 **−0.469000 [−0.515000, −0.420000]** |
| P2（終盤50 task・厳密 `unfit`） | **`FROZEN_WORSE`** | free **0.0039701** → frozen **0.228112**。paired差 **+0.224142 [+0.205488, +0.245500]** |

P1 の実行前固定条件は frozen $\le0.05$、減少率 $\ge0.80$、paired CI 上端 $<0$。3条件をすべて満たした。最終5Mは **10/10 seedすべて `strict_dead=0`**。さらに step 10k 以降の全500 task-end × 10 seed（5,000 seed-step）で `strict_dead=0` だった。

## 読み

1. **現象2の Dead 側は決着。** EMA centered で µ 経路を弱めた condA の終盤死には、学習可能な $b$ が必要だった。std の `condA_freeze_0815` がヌルだったことと合わせると、µ 経路支配の std と b 経路支配の centered が介入で分かれた。
2. **LoP の治療とは逆。** b を止めると dead は完全に消えるが `unfit` は約57倍に悪化した。bias 凍結は閾値表現力も奪うので、この差から dead の機能コストは同定できない。
3. **Dead → LoP を一本で結ばない。** free は dead 約46%でも `unfit` 約0.004、frozen は dead 0でも `unfit` 約0.228。少なくとも本介入では、`strict_dead` の水準と機能劣化は逆向きである。
4. **言える範囲は輸送チャネルの必要性。** 「b の更新が centered 死に必要」は言えるが、「b を凍結すれば学習が改善する」「centered の LoP は b だけが原因」は言えない。

## Sanity

- S0: free 30k replay、10 seed × 31記録点で既存 `L1w100_A1` と一致
- S2: frozen 全501記録点 × 10 seedで `max|b|=0`
- S3: 32点支持の壁恒等式、`p_hat` の1/32量子化、全主指標の有限性 PASS
- checkpoint: step 0 / 5M。学習時間 **1655.9秒**

## スコープと禁止

- condA・1層幅100・EMA `center_alpha=0.01`・$T=10^4$・batch=1・lr=0.01・5M限定
- condB、std、多層、他幅、他 optimizer へ外挿しない
- **`BIAS_ROUTE_DECISIVE` を `LOP_CURED` と読み替えない。機能は有意に悪化した**
- frozen は「同じネットから dead だけを除いた反実仮想」ではない。bias 表現力を欠く別の仮説クラス

## 成果物

- repo: `results/centered_freeze_0901/`
- spec: `specs/spec_centered_freeze_0901.md`
- 主出力: `summary.md` / `verdict.csv` / `paired_endpoints.csv` / `task_end_metrics.csv` / `fig_centered_freeze.png` / `provenance.json`
- 実装・spec・結果の repo commit: `f402f80`
