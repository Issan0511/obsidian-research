---
name: proj-004-operating-latitude-0902
description: 2026-09-02 以降 Issa は Claude に実験・spec・事前予測の自発起案を許可した (Obsidian 運用ルールは特例で無視可)。ただし PC を落とさないことが条件。
metadata:
  type: feedback
---

Issa の指示 (2026-09-02, 現象3 の再開時): 「だいたいあなたの好きなようにしてください。Obsidian の運用ルールは特例で無視していい。勝手に実験・spec・事前予測をしていいが、プロセスとメモリを見て PC をクラッシュさせないように」。

**Why:** 主張V6 (硬いゲート不在なら LoP なし) が gate_dial_0902 で否定され、主張V5 現象3 (非ReLU での LoP) の探索が再開された。探索段階なので運用ルール §3 (追跡実験を自動起案しない) より速度を優先したい。

**How to apply:** 追跡実験は自発的に起案してよいが、(1) 走らせる前に `free -g` と実行中 python を確認し、並列数はメモリで決める ([[parallel-jobs-memory-budget]])、(2) 事前予測は今まで通り走らせる前に書き残す、(3) 力場分解は根拠に使わない ([[force-field-self-rest-decomposition-caution]])。関連: [[proj-004-drift-experiment]]
