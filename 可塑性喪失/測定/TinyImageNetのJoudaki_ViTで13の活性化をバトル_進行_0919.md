# Tiny ImageNet の Joudaki ViT で13活性化をバトル（進行記録）

親: [[RL-CIFARのMLPで13の活性化をバトル_kunekune_結果_0918]]
状態: **本走開始・結果未集計**（2026-09-19）。独立監査なし。
ユーザーはMLPのバトルをJoudaki ViTへ広げることを依頼。課題の違い・計算量を比較したうえでTiny ImageNetを選択し、高速化も依頼した。

## 設定

- 原典: [Joudaki et al., arXiv:2510.00304v3](https://arxiv.org/html/2510.00304v3)、公式コード `ajoudaki/loss-of-plasticity` commit `161217078ba52107c94a16602af958a321d62ce3`。
- Tiny ImageNet、重複なし5クラス×40タスク、各500更新（batch128、最後の68枚も使用、25epoch）。本物のカテゴリ分類であり乱数ラベルではない。
- ViTは原典の無改変モデル: patch8、埋め込み384、6層・6ヘッド、FFN1536、affine LayerNorm、dropout/attention dropout各0.1。
- Adam 1e-4、WDなし、float32。各タスク開始時に全200出力のheadをゼロへ、Adam momentは保持。
- 13腕: SNA / KKA / KKA23 / KKT1 / R / LK001 / LR / LK03 / SL / RSL / ELU / SILU / GELU。交換するのはFFNの活性化だけ。
- seed0–9、計130走。入力は原典のImageNet標準化と画像拡張。class順・batch順・拡張・dropoutをseed対応させる。
- SNA系のalphaは前回同様c=.6、beta=.01、clip[.005,3]。各層・各FFN channelのbatch×token分散を使う。EMA更新はbackward/Adamの後。

## 読み出しと原典との差

登録主指標は現タスク5クラス内のonline正解率のt21–40平均。早期t1–10と後期t31–40の差も取る。
原典コードは損失を5クラスへmaskする一方、正解率は全200出力argmaxで計算していた。この差を明記し、当方も `online_global_acc` などに全200出力版を併記する。
前回の符号検定ラベルを継承し、14種類の比較にHolm補正pも併記。非有意を同等性の証明とはしない。
本走が全件終わるまで順位を出さない。発散・欠測・条件の混在を黙って除かない。

## 高速化と検査（結果ではなく実装の検証）

- `torch.compile` + fused Adam。float32・TF32無効を維持。半精度化・学習量削減はしていない。
- 定常速度の実測: GELU 79.60→61.80 ms/更新、KKA 139.42→62.78 ms/更新（KKA約2.22倍）。出典 `results/joudaki_vit_battle_0919/speed_benchmark.json`。
- seed101・実画像500更新、初回コンパイル・評価・保存込み: GELU44.52秒、KKA46.84秒。出典 `real_data_timing.json`。学習だけの全走見込み約45時間で、実時間は保存等により長くなる。
- 適応EMAをcompiled forward内で変更した初期版は勾配検査に失敗した。EMAを学習更新後へ移して修正し、GELU/KKA/RSLの出力・勾配・EMAとAdam単独検査はPASS。失敗した検査はraw/preflightに保持。
- KKA/RSLは本番サイズ・実画像でタスク境界からの再開が、連続実行と重み・Adam・RNG・診断・前活性までbit一致。
- 初期化/勾配の13腕検査、乱数分離、mask/head reset、集計拒否検査もPASS。独立した外部監査ではない。

## 所在

- 実験repo: [lop_analysis の実験ブランチ](https://github.com/Issan0511/lop_analysis/tree/codex/joudaki_vit_battle_0919)。実装・検査 `efc4fc1`、最終速度 `677fc85`、push確認済み。main統合は完走後。
- 事前登録: `specs/spec_joudaki_vit_battle_0919.md`（初版 `6784fbf`、ユーザーの選択・高速化・検査修正は実行前追補として保存）。
- worktree: `/home/issan/Projects/claude/wt/joudaki_vit_battle_0919`。
- 生出力: `/home/issan/Projects/obsidian-research-data/joudaki_vit_battle_0919/`。共有データは別の `datasets/tiny-imagenet-200/`。symlinkによる移動はしない。
- 全重み・適応状態と固定16画像の前活性を各タスク保存。重み約230GB＋前活性は圧縮前約100GB＋checkpoint約17GB。空き容量を監視し25GiB未満なら停止する。
- systemd user service: `joudaki-vit-battle-0919.service`。1GPU逐次実行。raw rootの `STOP` でtask境界停止、同じlauncherで再開できる。
- 完走後、launcherが `summary.md` / `verdict.csv` / `verdict.json` / `paired_tests.csv` / `comparison.png` を自動生成する。Obsidianの結果転記・main統合・worktree片付けはその後に行う。

**ここには性能順位・可塑性についての結論はまだない。**


## 同一GPU並列の実測（2026-09-19）

ユーザーの質問を受け、本走をSNA seed0のtask22終了で一時停止して、KKA・seed100・batch128の合成入力を通常の独立CUDAプロセス1/2/4本で測定した。各10更新warmup後、各200更新の全体処理量は1本14.30更新/秒、2本13.16、4本13.92。4本まで実行可能だが、今回の学習部分では高速化なし。最終モデル・適応Vは全プロセスで1本実行とbit一致。

通常の複数プロセス化は採用せず、1本で本走をcheckpointから再開。実画像読込・保存を含む並列やMPSは未測定。本走精度・順位を判断に使用していない。追補7とbenchmarkをcommit/push（89fedb1）。凍結学習ソース変更なし。

結果: `/home/issan/Projects/claude/wt/joudaki_vit_battle_0919/results/joudaki_vit_battle_0919/parallel_benchmark.json`


## 停止・別マシン引き継ぎ（2026-09-19）

他作業への負荷を避けたいというユーザー依頼により元マシンを停止。KKA23 seed1 task31終了で保存・正常終了済み。18/130 run、751/5200 task完了。checkpointをCPUで読んでtask31と凍結source hash一致を確認した。STOPを残し、自動再開はしない。

コード・仕様・検査結果・小さな実行記録・環境・転送manifest・引き継ぎMDを実験ブランチ `codex/joudaki_vit_battle_0919` に保存。引き継ぎ: https://github.com/Issan0511/lop_analysis/blob/codex/joudaki_vit_battle_0919/specs/HANDOFF_joudaki_vit_battle_0919.md

raw約48.83GiB、Tiny ImageNet展開済み約481MiBとzip約237MiBはGit外に保持。別マシンへの転送は未実施。引き継ぎMDにrsync・ハッシュ検証・新環境検査・再開コマンドを記載した。次はKKA23 seed1 task32。別GPUをまたぐbit一致は保証せず、切替位置と環境を記録する。実験終了・main統合はまだ行わない。
