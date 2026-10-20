---
name: depth-silu-rlmnist-1020
description: 深さを変えた SiLU MLP（RL-MNIST、1・2・4 層、ReLU 1・4、扉 C）1020 — Issa「多層ほど沈みにくい」は外れ（NO_DEPTH_TREND）。2 層は細って水面か閉じて沈むかに割れ、4 層は中の層が第 1 層より深く沈み読み出しの隣が課題 4〜8 で閉じる。深い層を沈めるのは上流の項、担い手は常時点灯 unit
metadata:
  node_type: memory
  type: project
  originSessionId: d233b0e1-1bba-44a1-a7b6-6a5c50af6329
  modified: 2026-10-20T11:24:27.380Z
---

2026-10-20、V13 の Fable（親）経由で Issa「多層にしたらするほど沈みにくいのか」を Opus が登録走で測った。repo `depth_silu_rlmnist_1020`（spec 558425b4・engine c3993fa6・結果 d22a6539、main 統合）、vault `可塑性喪失/測定/深さを変えたSiLU_MLP_層ごとの沈みと担い手_結果_1020`（e19159c）、生データ `obsidian-research-data/depth_silu_rlmnist_1020/`。アニメーション `results/depth_silu_rlmnist_1020/depth_layers_anim_s{0,1}.gif`（Issa の依頼）。

**結果（課題 30、seed 0〜2、延長は 0〜9）**
- r_net（全隠れ unit の μ/s 中央値）1 層 −2.47・2 層 −1.07・4 層 −2.26 → `NO_DEPTH_TREND`。G30 は 0.386・0.364・0.494。4 層は 10/10 seed で 1 層より多く失う。
- 2 層: 第 1 層が沈み切ると担い手 ‖h̄₁‖ が 0.05 に消え、第 2 層は幅 0.46 で水面に残る（喪失は 1 層並み）。第 1 層に常時点灯 unit が残ると担い手が伸び、第 2 層が閉じて沈む。10 seed で 5:4:中間 1。
- 4 層: 第 2〜4 層は第 1 層より深い（−2.7〜−2.8 対 −1.55）。読み出しの隣の層が課題 4〜8 で全閉（p=0）、その課題で精度が床へ、開き直さない。第 1 層の切替の押しはその後 0。
- 切替の Δμ の 7〜9 割は上流（w·Δh̄）で、97〜100% の切替で沈める側。担い手は下の層の常時点灯 unit 1〜4 個が運び 100〜750 に伸びる（‖µ₂‖ 壁と同じ形）。
- 扉 C: 第 1 層は沈まない（−0.11）が第 4 層が課題 5 で閉じ、G50 は 1 層より悪い。ReLU 4 層は遅く死に深い層で死んだ unit が開き直すが 9/10 が床。
- 戻りは 4 層なら第 1 層でも起きる（深い戻り 23〜37/300）が、課題 2〜5 の過渡で 84〜100% は沈み直す。残るのは常時点灯への逃げ。素の戻り（p 1/2 を跨ぐ）は境の行き来で膨らむので深い戻り（p ≤ 0.1 から）で読む。
- 予測: Fable 6/12、Opus 11/18（戻りは両者外した）。

**Why:** V13 の機構の範囲（担い手が固定の 1 隠れ層）を深い網へ広げる問い。文字 GPT で SiLU が戻ったのは MLP の深さでは再現しない。
**How to apply:** 深い MLP の予測は「どの層が最後のゲート層か」と「担い手を運ぶ常時点灯 unit がいるか」で立てる（[[moving-carrier-deep-nets-1020]]）。動く担い手は戻りの源とは限らず、MLP では沈める側に働いた。torch.optim.Adam の CPU step は CUDA を初期化し 128 MiB の GPU を取る → CPU 走は `CUDA_VISIBLE_DEVICES=""`。関連: [[kappa-reload-1020]] [[three-layer-rlcifar-extension-1007]] [[issa-hypotheses-take-seriously]]
