---
name: harness-silent-failure-pitfalls
description: 2026-09-05 に踏んだ無言失敗 3 種 — nohup のログ名に / が入ると起動せず pid だけ出る、CUDA のスカラー除算は逆数乗算に畳まれるので bit 一致検査は * a.reciprocal() で揃える、str.replace は必ず assert
metadata:
  type: feedback
---

1. **`nohup cmd > $S/name_$x.log &` で `$x` に `/` が入ると**、ディレクトリが無くてリダイレクトが失敗し、**python は起動しないのに pid は表示される**。GPU 0% で気づいた。ログ名は `${name//\//_}` で平坦化し、launch 直後に `ps -C python3 | grep <stage>` で本数を数える。
2. **PyTorch CUDA の `tensor / python_float` は逆数乗算に畳まれる**ので、同じ式を `tensor / tensor` で書くと 1 ulp ずれ、数千 step で 1e-6 まで育つ（精度は一致したまま）。「機構を切ると既存腕と bit 一致」型の検査（S-ema-off）は、参照側と**演算順序まで**揃える: `sin(a*z)**2 * a.reciprocal()`。1 回の forward で 3 通り比べれば 1 分で切り分けられる。
3. **`s.replace(old, new)` は見つからなくても黙って通る。** 署名の置換 1 か所だけ失敗して `TypeError: unexpected keyword` で 3 本の走が起動時に落ちた。多段パッチは全部 `assert old in s`。

4. **shard ディレクトリの glob `s*` は `sna_l2` / `sna_l2init` も拾う。** 2026-09-06 に `SNA` の α・‖w‖ を WD 腕と混ぜて 7.45 → 3.68 と誤報し、誤った説明を結果ノートに一度書いた（次 commit で訂正）。腕別ディレクトリが混在する `results/<run>/<box>/` では **shard 名を明示列挙**するか、`per_task.csv` を読む段で `--iv` 相当のラベルを付け直す（`verdict_adapt.py` の relabel 方式）。「同じ量が 2 通りの値で出たら glob を疑う」。

5. **マシンのサスペンド中はプロセスもタイマーも止まり、復帰後にターンが実行される。** 2026-09-06 に「05:0x に launch」と報告したが実際は 13:12。`date` を launch 出力に必ず含め、見積もりは監視ログの最初の行から数える。launch-bound の走は N 並列で N 倍近く遅くなる（7 並列で 3.5 倍）ので、S-cost（1 プロセス）を並列数で割らない。

**Why:** どれも「走らせたつもり」「一致したつもり」で数十分〜数時間を失う種類。pmnist_adapt_0905 の launch で 1 と 3、検査で 2 を同日に踏んだ。

**How to apply:** launch スクリプトは書いたら `bash -n` → 実行 → `ps` で本数確認、の 3 手を必ず。bit 一致検査が「精度は一致・統計だけ 1e-7 ずれ」なら演算順序を疑う。関連: [[pmnist-0905-lessons]] [[parallel-jobs-memory-budget]]
