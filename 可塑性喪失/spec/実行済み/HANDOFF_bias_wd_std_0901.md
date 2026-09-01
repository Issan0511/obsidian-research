# HANDOFF — bias_wd_std_0901（std 腕に b-WD・反証テスト）

宛先: Codex / 委譲元: Issa / 作成: 2026-09-01
repo: `github.com/Issan0511/lop_analysis`（main = `da22465` 時点）
前件: `bias_wd_0901`（centered で `BIAS_WD_PROTECTS`）。本件はその**反証テスト**。

## 目的と予言（これを試しに行く）

centered の死と劣化は「b の自走」で、µ/Σ 駆動の本体 LoP とは別の病気だ、というのが現在の読み。ならば:

> **予言 P: std（無中心化）腕に同じ b-WD を入れても、本体の LoP はほぼ消えない。**
> 理由: std では $s = w\cdot\mu + b$ の **µ チャネルが生きている**ので、b を減衰させても壁には M 側から到達できる。さらに台帳（flip 15 座標と b が 1 自由度に縮退する構造）の逃げ道があり、実効バイアスは flip 側に記帳を移せる。

**この予言が外れたら（std でも LoP が消えたら）µ 駆動説のほうが危なくなる。** どちらに転んでも情報がある。

## 設計（`bias_wd_0901` の harness をそのまま流用）

- 問題・学習器・記録・統計・床（2層系 1e-23）・ブロック定義（B02 = task 51–100 / B10 = task 451–500）はすべて `bias_wd_0901` と同一。**encoding だけ std**（centering なし）
- 腕（各 10 seed・5M step）:

| 腕 | 構成 | wd_b |
|---|---|---|
| `S_none` | [100,100]・std | 0（= 既存 `L2_none` の複製） |
| `S_main` | [100,100]・std | 1e-3（centered の主 λ を流用） |
| `S_sub`  | [100,100]・std | 1e-1（最強水準） |

- λ の新パイロットは**やらない**。非効果の予言なのでグリッド精度は要らず、centered で効いた値をそのまま使うのが最も解釈しやすい

## 判定（spec で凍結すること）

主 endpoint: `mean(log10 unfit)` の **B10−B02**（劣化量）。参照: `S_none` は既存 `L2_none` と一致するはずで、その劣化はおよそ +9.7 dex。

- **`LOP_PERSISTS`**（予言どおり）: `S_main` の劣化が `S_none` の **50% 以上**（seed 対応の劣化比の percentile CI 下端 ≥ 0.5）
- **`LOP_REMOVED`**（予言の反証）: `S_main` の劣化が `S_none` の **10% 以下**（CI 上端 ≤ 0.1）
- 間は `INCONCLUSIVE_PARTIAL`（部分的緩和。効果量を記録して Issa に返す）

副（すべて REPORT_ONLY・判定に使わない）:
1. `strict_dead_frac`（終盤窓）— std では dead が µ 経由で残る予想
2. **台帳の移動**: per-unit の M チャネル（$w\cdot\mu$）と B チャネル（$b$）の alive 中央値の B02→B10 推移。予言: b を減衰させても **M 側の沈下は続く**
3. `S_sub` の同上（用量反応）
4. 静的水準 `mean(log10 unfit)`（B10）の腕間差

## サニティ（前件から流用・最小限）

- S0: `S_none` を committed `L2_none`（`mlp2_phase1_0829`）に対して 30k・1k 格子で replay、`unfit`・`eval_loss_exact` 一致
- S3: 壁恒等式・1/32 量子化・有限性（前件の実装をそのまま。β の一致尺度は**修正後**のスケール正規化版を使う）
- S4: 発散ガード（probe_every=1000。`L2_A2` の前例あり）
- 恒真ガードは今回は不要（std では高 λ でも dead=0 は強制されない — µ 経由で死ねる。むしろそれ自体が予言の一部）

## 規律（前件と同一）

1. spec 単独 commit → config+実装 → 結果、の 3 commit。各段で `git ls-remote origin refs/heads/main` により push を確認し、出力を報告に貼る
2. 数値は `verdict.csv` / `summary.md` からのみ。窓を必ず書く
3. bootstrap: seed 水準 paired percentile、B=20000、**bootstrap_seed=20260903**（20260830 / 20260901 / 20260902 は既用）
4. 事前登録から外れたら、外れた事実と理由を記録する（前件の逸脱記録の形式で）

## 引いてはいけない線

- `LOP_PERSISTS` が出ても「b-WD は無意味」と書かない（centered では効いた。regime が違うだけ）
- `LOP_REMOVED` が出ても µ 駆動説の棄却まで飛ばない（Issa の裁定に返す）
- 劣化比は分母（`S_none` の劣化）が seed ごとに大きいので安定だが、万一分母が小さい seed が出たら比でなく差でも併記する

## 完了報告

commit hash 3 つ＋push 確認、`verdict.csv` 全行、S0/S3/S4 の PASS/FAIL、台帳移動（M/B チャネル）の要約数値。
見積もり: 2 層 5M × 3 腕 ≈ 2 時間。
