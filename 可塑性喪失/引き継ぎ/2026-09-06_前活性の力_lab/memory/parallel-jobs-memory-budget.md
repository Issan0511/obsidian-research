---
name: parallel-jobs-memory-budget
description: ローカル並列実行はコア数でなくメモリ実測で本数を決める(2026-08-20 に OOM で Wayland を落とした)
metadata:
  type: feedback
---

**ローカルで重いジョブを並列起動する前に、必ず `free -h` と `swapon --show` を見て、1 プロセスの peak RSS を短時間走行で実測してから本数を決めること。** 並列数はコア数ではなく `min(コア数/スレッド数, 空きメモリ / 実測peakRSS)` で決める。swap が既に埋まっている場合は並列度を下げるか逐次にする。

**Why**: 2026-08-20、proj_004 の teachw_0820 で 28 コアあることだけを見て 6 並列(`OMP_NUM_THREADS=1` × 6 プロセス)を起動した。1 プロセス約 2.3 GiB × 6 = 約 13.4 GiB を消費し、もともと約 90% 埋まっていた swap が 100% に達して **OOM が発動、巻き添えで Claude Desktop → GNOME Wayland ごと落ちた**。ユーザーのデスクトップセッションを実際に破壊している。マシンは 30 GiB RAM / 8 GiB swap。CPU 並列の知見([[proj-004-drift-experiment]] の「w100=4スレ×6並列」)は**スレッド数の話であって RAM の話ではない**のに、そのままプロセス数として流用したのが誤り。

**How to apply**: 並列起動の直前に (1) `free -h; swapon --show` (2) 短縮走行 (例 300 イテレーション) で `/proc/self/status` の VmRSS と `ru_maxrss` を測る (3) 本数を決める、の 3 ステップを踏む。長時間ジョブは走行中も RSS を監視する。実験フレームワークの peak RSS は**走行長に依存して伸びることがある**ので、短縮走行の値をそのまま使わず伸び率から本走の値へ外挿すること。
