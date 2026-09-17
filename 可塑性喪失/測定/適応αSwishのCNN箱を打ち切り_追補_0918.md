# 適応αSwish の CNN 箱を打ち切り：追補 0918

親: [[適応αSwishをSnakeとバトルさせる_結果_0917]] / [[現在地]]
run id: `swish_battle_0917`（CNN 箱） / 状態: **打ち切り（2026-09-18 03:20）・main 統合済み・worktree 片付け済み**

## 1. 何が起きたか

CNN 箱を 70 本のうち 46 本まで回した時点で、Issa の指示（「もうまじでいらんからなー」「終了させて」）で打ち切った。
走行中だった 5 本（`SWA1`・`SW1`・`SWA3`・`SWA1u`・`SWA3u` の seed 6、各 1 時間半経過）は kill した。この runner に途中再開は無いので、その 5 本は残っていない。
GPU を空けて、同日起動の `rlcifar_mlp_battle_0918`（RL-CIFAR × MLP の活性化バトル）に回すのが目的。

## 2. 残ったもの

- `SNAc3`: seed 0–9（10 本・完走）→ 登録判定 `C_VALUE` は有効（[[適応αSwishをSnakeとバトルさせる_結果_0917]] §1）。
- `SW1`・`SW3`・`SWA1`・`SWA1u`・`SWA3`・`SWA3u`: seed 0–5（各 6 本・完走）。
- **Swish 腕の CNN の登録判定は未解決**。10 seed で登録したので、6 seed では検出力が足りない（符号検定は n=6 なら 6/6 で p=0.031、5/6 では p=0.219）。引くときは「seed 0–5・検出力不足」と明記する。
- MLP 箱（110 本）は完走していて判定は有効。

## 3. repo の状態

打ち切りと同時に [[運用ルール]] §4 の片付けを済ませた。ブランチ `claude/swish_battle_0917` は **`origin/main` に統合済み**（親ノートの「main に無い」という警告はこの時点で解消）。
git の外にあった生データ 318 MB（hist の npz・launcher のログ）は `obsidian-research-data/swish_battle_0917/` に退避し、`results/swish_battle_0917/backup_manifest.json`（source・backup・bytes・sha256）を commit した。worktree とブランチは削除した。
