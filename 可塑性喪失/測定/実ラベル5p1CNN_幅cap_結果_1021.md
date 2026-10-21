# 実ラベル5+1 CNN：幅capの登録結果（1021）

状態: **完走・独立集計一致。ReLU INCONCLUSIVE／ELU WORSENS。** / 更新: **2026-10-21**

実験ID `cnn_width_cap_1021`。同じ課題1末checkpointからnatural/capを各20slot（ReLU/ELU各10seed）で課題30末まで走らせた。各条件580行、欠損・除外・非有限更新0。登録主評価はlate hard 21/23/25/27/29の最初780更新のonline精度であり、全課題平均やtestへの差し替えはしない。

正本: [登録spec dffbbbf8](https://github.com/Issan0511/lop_analysis/blob/dffbbbf8/specs/spec_cnn_width_cap_1021.md) / [登録主判定](https://github.com/Issan0511/lop_analysis/blob/73fdc5d6/results/cnn_width_cap_1021/summary/primary.json) / [独立レポート](https://github.com/Issan0511/lop_analysis/blob/73fdc5d6/results/cnn_width_cap_1021/report/report.md)。部品3の証拠は [[V13機構の部品表_1021]]、本文配置は [[V13段落地図_機構を軸に_1019]]。

![登録主評価の全seed対応差とf2の幅・応答・死。全4隠れ層への介入で、f2は診断表示。](https://raw.githubusercontent.com/Issan0511/lop_analysis/73fdc5d6/results/cnn_width_cap_1021/report/figure.png)

図の[PDF](https://github.com/Issan0511/lop_analysis/blob/73fdc5d6/results/cnn_width_cap_1021/report/figure.pdf)。Aの点はseed、菱形は平均。B〜Dはseed平均。幅・応答はseed内unit中央値、死はunit割合。図の注釈配置を整形し目視確認済み。

## 読みと主張の範囲

- **ReLUの救済成立とは言わない。** 平均+11.639ポイントでも、正/負/同点は5/4/1、Holm p=1。seedごとに大きな改善と悪化があり、登録判定INCONCLUSIVEを保持する。
- **ELUは10/10で主精度が低下。** 83.657%→78.547%、-5.111ポイント、Holm p=.00390625。幅capは作動し局所応答も高く保ったが、学び直しの初期精度を改善しなかった。平均応答の高さだけで成績を説明する一般化を避ける。
- ELUのnaturalは今回、early hardからlate hardへ平均精度が下がっておらず、もともと新品以下の崩壊を救済する箱として登録していない。悪化を隠さず、幅を抑える操作の利益と不利益として扱う。
- 新しいnatural自身でも幅は増えた。固定probe/学習batch EMAとも、ReLU c1/c2/f1は10/10・f2は9/10、ELU全4層10/10。旧40slotの全4層10/10をそのまま新20slotへ転載しない。
- 上限はpost-Adam学習batch分散のEMA。固定probe幅や瞬間batch幅の厳密上限ではない。全4層でWとbiasを同率に縮小し、Adam状態は変えない。局所入力を固定した投影瞬間のrを保つが、全網の尺度だけの純粋な媒介効果ではない。
- 以下の課題30末の応答・死の表は診断。最初780更新の主成績と同一時刻の媒介測定ではない。ELUの課題末の高応答だけから、悪化の原因を片側化・実効学習率・表現力等のどれかに確定しない。

## 保存結果からの集計

ReLU / ELU（α=3.6）、各10seed、7,800更新/課題。両腕とも新しい20slotで課題1末から30末まで再生した。元40slotの古いnatural成績を対照に用いていない。主判定は登録済み集計と独立計算が一致した。

## 主評価と時間低下

late hard = 21,23,25,27,29。first780は最初780更新のpre-update online accuracy。各task平均→seed内5task平均→10seed平均。単位は%／対応差はポイント。

| 活性化 | natural | cap | cap−natural | 正/負/0 | Holm p | 判定 |
| --- | --- | --- | --- | --- | --- | --- |
| ReLU | 22.184 | 33.823 | 11.639 | 5/4/1 | 1.000000 | INCONCLUSIVE |
| ELU α=3.6 | 83.657 | 78.547 | -5.111 | 0/10/0 | 0.003906 | WORSENS |

### ReLU：全seed

| seed | natural late | cap late | 対応差 | natural early→late | cap early→late |
| --- | --- | --- | --- | --- | --- |
| 2000 | 51.442 | 19.543 | -31.898 | -6.524 | -49.172 |
| 2001 | 45.733 | 58.458 | 12.725 | -23.213 | -9.317 |
| 2002 | 29.277 | 61.579 | 32.302 | -32.169 | 5.045 |
| 2003 | 0.000 | 55.292 | 55.292 | -58.523 | -8.183 |
| 2004 | 0.000 | 62.431 | 62.431 | -63.758 | 0.530 |
| 2005 | 7.105 | 55.599 | 48.494 | -58.862 | -11.408 |
| 2006 | 27.084 | 15.194 | -11.890 | -42.144 | -53.433 |
| 2007 | 0.000 | 0.000 | 0.000 | -48.308 | -66.616 |
| 2008 | 10.862 | 0.000 | -10.862 | -54.379 | -66.682 |
| 2009 | 50.338 | 10.132 | -40.206 | -8.530 | -57.396 |

### ELU α=3.6：全seed

| seed | natural late | cap late | 対応差 | natural early→late | cap early→late |
| --- | --- | --- | --- | --- | --- |
| 2000 | 85.948 | 82.545 | -3.403 | 3.965 | 5.641 |
| 2001 | 81.242 | 76.079 | -5.163 | -3.152 | -5.287 |
| 2002 | 84.247 | 79.959 | -4.288 | 2.880 | 1.784 |
| 2003 | 83.329 | 76.615 | -6.715 | 0.091 | -2.262 |
| 2004 | 85.320 | 79.531 | -5.788 | 2.791 | 1.997 |
| 2005 | 81.805 | 78.689 | -3.116 | -2.758 | -2.493 |
| 2006 | 86.668 | 82.100 | -4.568 | 3.794 | -0.105 |
| 2007 | 83.924 | 78.945 | -4.979 | 0.790 | -0.721 |
| 2008 | 81.620 | 74.155 | -7.465 | -3.516 | -5.500 |
| 2009 | 82.470 | 76.847 | -5.623 | -1.032 | -2.354 |

early = hard 3,5,7,9。時間差はlate−earlyであり、cap−naturalとは別の量。

## 副評価

late hardのseed平均。副評価に追加の確認的有意差判定は付けない。

| 活性化 | 指標 | natural | cap | 対応差 |
| --- | --- | --- | --- | --- |
| ReLU | first100_online_acc (%) | 1.7488 | 8.8837 | 7.1350 |
| ReLU | online_acc (%) | 43.6309 | 54.9827 | 11.3518 |
| ReLU | test_acc (%) | 35.2080 | 46.7160 | 11.5080 |
| ReLU | ce_mean | 2.6734 | 2.2019 | -0.4715 |
| ReLU | ce_first780_mean | 4.8661 | 3.9895 | -0.8766 |
| ELU α=3.6 | first100_online_acc (%) | 53.2794 | 51.7687 | -1.5106 |
| ELU α=3.6 | online_acc (%) | 98.2953 | 97.4418 | -0.8535 |
| ELU α=3.6 | test_acc (%) | 75.3720 | 75.6160 | 0.2440 |
| ELU α=3.6 | ce_mean | 0.0719 | 0.0837 | 0.0118 |
| ELU α=3.6 | ce_first780_mean | 0.6594 | 0.6734 | 0.0140 |

online_accは全7,800更新。既存新品との比較はこの報告には混ぜていない。

## 新natural自体で幅は増大したか

まず今回再生したnaturalの始点・終点を直接比較する。各seedでunit中央値を取り、その10seed平均を示す。増加数はseed内unit中央値が厳密に増えたseed数。固定probeの画像集合は同じ。EMAはその時点の学習batch分布に依存し、課題1はhard、課題30はeasy。

### natural：課題1末→30末

| 活性化 | site | 幅の量 | 始点 | 終点 | 増加seed | 始点0幅unit |
| --- | --- | --- | --- | --- | --- | --- |
| ReLU | c1 | ema_post_adam_batch | 1.3334 | 2.9946 | 10/10 | 0 |
| ReLU | c1 | fixed_probe_pooled | 1.3376 | 3.1363 | 10/10 | 0 |
| ReLU | c2 | ema_post_adam_batch | 3.3667 | 21.4819 | 10/10 | 0 |
| ReLU | c2 | fixed_probe_pooled | 3.4264 | 22.6442 | 10/10 | 0 |
| ReLU | f1 | ema_post_adam_batch | 6.3282 | 60.9721 | 10/10 | 0 |
| ReLU | f1 | fixed_probe_images | 6.0731 | 68.0543 | 10/10 | 0 |
| ReLU | f2 | ema_post_adam_batch | 5.4146 | 55.3623 | 9/10 | 0 |
| ReLU | f2 | fixed_probe_images | 4.9194 | 61.0502 | 9/10 | 0 |
| ELU α=3.6 | c1 | ema_post_adam_batch | 0.5207 | 1.1369 | 10/10 | 0 |
| ELU α=3.6 | c1 | fixed_probe_pooled | 0.5302 | 1.1472 | 10/10 | 0 |
| ELU α=3.6 | c2 | ema_post_adam_batch | 0.8232 | 7.2887 | 10/10 | 0 |
| ELU α=3.6 | c2 | fixed_probe_pooled | 0.8301 | 7.3412 | 10/10 | 0 |
| ELU α=3.6 | f1 | ema_post_adam_batch | 1.3425 | 38.0576 | 10/10 | 0 |
| ELU α=3.6 | f1 | fixed_probe_images | 1.2756 | 43.6506 | 10/10 | 0 |
| ELU α=3.6 | f2 | ema_post_adam_batch | 1.7561 | 31.0142 | 10/10 | 0 |
| ELU α=3.6 | f2 | fixed_probe_images | 1.4986 | 33.9526 | 10/10 | 0 |

### cap：課題1末→30末

| 活性化 | site | 幅の量 | 始点 | 終点 | 増加seed | 始点0幅unit |
| --- | --- | --- | --- | --- | --- | --- |
| ReLU | c1 | ema_post_adam_batch | 1.3334 | 1.0540 | 0/10 | 0 |
| ReLU | c1 | fixed_probe_pooled | 1.3376 | 1.1292 | 0/10 | 0 |
| ReLU | c2 | ema_post_adam_batch | 3.3667 | 2.6707 | 0/10 | 0 |
| ReLU | c2 | fixed_probe_pooled | 3.4264 | 2.7729 | 0/10 | 0 |
| ReLU | f1 | ema_post_adam_batch | 6.3282 | 3.1195 | 0/10 | 0 |
| ReLU | f1 | fixed_probe_images | 6.0731 | 3.7901 | 0/10 | 0 |
| ReLU | f2 | ema_post_adam_batch | 5.4146 | 1.2678 | 0/10 | 0 |
| ReLU | f2 | fixed_probe_images | 4.9194 | 1.4066 | 0/10 | 0 |
| ELU α=3.6 | c1 | ema_post_adam_batch | 0.5207 | 0.4773 | 0/10 | 0 |
| ELU α=3.6 | c1 | fixed_probe_pooled | 0.5302 | 0.4855 | 2/10 | 0 |
| ELU α=3.6 | c2 | ema_post_adam_batch | 0.8232 | 0.7330 | 0/10 | 0 |
| ELU α=3.6 | c2 | fixed_probe_pooled | 0.8301 | 0.7700 | 3/10 | 0 |
| ELU α=3.6 | f1 | ema_post_adam_batch | 1.3425 | 1.2332 | 0/10 | 0 |
| ELU α=3.6 | f1 | fixed_probe_images | 1.2756 | 1.5142 | 9/10 | 0 |
| ELU α=3.6 | f2 | ema_post_adam_batch | 1.7561 | 0.9280 | 0/10 | 0 |
| ELU α=3.6 | f2 | fixed_probe_images | 1.4986 | 1.3859 | 3/10 | 0 |

全seedの始点・終点・差・倍率は `width_growth.csv`。EMAと固定probeを同じ幅として混ぜない。

## 課題30末の応答・位置とcapの幅効果

s,m,r,φ′平均/標準偏差,p+はunit中央値→seed平均。dead/low-responseはunit割合→seed平均。φ′は活性化関数の局所微分であり、網全体の勾配ではない。

| 活性化 | site | 腕 | 幅s | 位置r | φ′平均 | φ′sd | p+ | dead | low-response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ReLU | c1 | natural | 3.1363 | 0.0071 | 0.5145 | 0.4981 | 0.5145 | 0.0000 | 0.0000 |
| ReLU | c1 | cap | 1.1292 | 0.0095 | 0.5028 | 0.4988 | 0.5028 | 0.0000 | 0.0000 |
| ReLU | c2 | natural | 22.6442 | -0.9785 | 0.1513 | 0.2814 | 0.1513 | 0.0688 | 0.4813 |
| ReLU | c2 | cap | 2.7729 | -0.7697 | 0.2330 | 0.2915 | 0.2330 | 0.1750 | 0.3875 |
| ReLU | f1 | natural | 68.0543 | -2.7337 | 0.0014 | 0.0093 | 0.0014 | 0.6580 | 0.8540 |
| ReLU | f1 | cap | 3.7901 | -3.3925 | 0.0000 | 0.0000 | 0.0000 | 0.9160 | 0.9670 |
| ReLU | f2 | natural | 61.0502 | 未定義 | 0.0000 | 0.0000 | 0.0000 | 0.9560 | 0.9910 |
| ReLU | f2 | cap | 1.4066 | 未定義 | 0.0003 | 0.0000 | 0.0003 | 0.7620 | 0.8440 |
| ELU α=3.6 | c1 | natural | 1.1472 | -0.0284 | 1.3990 | 0.7837 | 0.4874 | 0.0000 | 0.0000 |
| ELU α=3.6 | c1 | cap | 0.4855 | -0.0170 | 1.7828 | 0.9201 | 0.4892 | 0.0000 | 0.0000 |
| ELU α=3.6 | c2 | natural | 7.3412 | -0.3321 | 0.5723 | 0.6284 | 0.3650 | 0.0000 | 0.0000 |
| ELU α=3.6 | c2 | cap | 0.7700 | -0.1701 | 1.5652 | 0.8349 | 0.4332 | 0.0000 | 0.0000 |
| ELU α=3.6 | f1 | natural | 43.6506 | -0.9265 | 0.2060 | 0.4148 | 0.1809 | 0.0000 | 0.2490 |
| ELU α=3.6 | f1 | cap | 1.5142 | -0.1614 | 0.9373 | 0.4560 | 0.4634 | 0.0000 | 0.0470 |
| ELU α=3.6 | f2 | natural | 33.9526 | -0.6880 | 0.2914 | 0.4522 | 0.2458 | 0.0000 | 0.1950 |
| ELU α=3.6 | f2 | cap | 1.3859 | 0.1136 | 0.9988 | 0.2387 | 0.5295 | 0.0000 | 0.1480 |

幅への対応差を性能の主判定と分けて示す。終点のunit中央値について、capで小さいseed数とcap−natural平均差：

| 活性化 | site | 幅の量 | cap−natural | capで小さいseed |
| --- | --- | --- | --- | --- |
| ReLU | c1 | ema_post_adam_batch | -1.9406 | 10/10 |
| ReLU | c1 | fixed_probe_pooled | -2.0071 | 10/10 |
| ReLU | c2 | ema_post_adam_batch | -18.8112 | 10/10 |
| ReLU | c2 | fixed_probe_pooled | -19.8713 | 10/10 |
| ReLU | f1 | ema_post_adam_batch | -57.8526 | 10/10 |
| ReLU | f1 | fixed_probe_images | -64.2643 | 10/10 |
| ReLU | f2 | ema_post_adam_batch | -54.0945 | 9/10 |
| ReLU | f2 | fixed_probe_images | -59.6436 | 9/10 |
| ELU α=3.6 | c1 | ema_post_adam_batch | -0.6596 | 10/10 |
| ELU α=3.6 | c1 | fixed_probe_pooled | -0.6617 | 10/10 |
| ELU α=3.6 | c2 | ema_post_adam_batch | -6.5556 | 10/10 |
| ELU α=3.6 | c2 | fixed_probe_pooled | -6.5711 | 10/10 |
| ELU α=3.6 | f1 | ema_post_adam_batch | -36.8244 | 10/10 |
| ELU α=3.6 | f1 | fixed_probe_images | -42.1364 | 10/10 |
| ELU α=3.6 | f2 | ema_post_adam_batch | -30.0863 | 10/10 |
| ELU α=3.6 | f2 | fixed_probe_images | -32.5667 | 10/10 |

固定probeでのseedごとのcap−natural差、convのwithin/between幅、m、rank、未定義r数は `endpoint_effects.csv` と `endpoint_units_summary.csv`。

## capの作動とEMA制御

同じ各7,800更新なので、unit×stepを分母に集計する。hardとeasyを分ける。参照は課題1hardのpost-Adam幅EMAで、現在batchや固定probeに厳密な上限を課した操作ではない。

| 活性化 | site | 課題型 | 発火率 | 平均倍率 | 最小倍率 | batch幅超過率 | EMA超過unit-step | 境界EMA超過unit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ReLU | c1 | hard | 0.1160 | 0.9999 | 0.9474 | 0.2480 | 0 | 0 |
| ReLU | c1 | easy | 0.0096 | 1.0000 | 0.9620 | 0.1297 | 0 | 0 |
| ReLU | c2 | hard | 0.0767 | 0.9999 | 0.9734 | 0.2484 | 0 | 0 |
| ReLU | c2 | easy | 0.0059 | 1.0000 | 0.9530 | 0.0983 | 0 | 0 |
| ReLU | f1 | hard | 0.0187 | 1.0000 | 0.8940 | 0.1446 | 0 | 0 |
| ReLU | f1 | easy | 0.0052 | 1.0000 | 0.8767 | 0.0648 | 0 | 0 |
| ReLU | f2 | hard | 0.0047 | 1.0000 | 0.9459 | 0.0527 | 0 | 0 |
| ReLU | f2 | easy | 0.0023 | 1.0000 | 0.9605 | 0.0253 | 0 | 0 |
| ELU α=3.6 | c1 | hard | 0.0854 | 0.9999 | 0.9573 | 0.3358 | 0 | 0 |
| ELU α=3.6 | c1 | easy | 0.0172 | 1.0000 | 0.9541 | 0.2697 | 0 | 0 |
| ELU α=3.6 | c2 | hard | 0.2368 | 0.9998 | 0.8863 | 0.5318 | 0 | 0 |
| ELU α=3.6 | c2 | easy | 0.0108 | 1.0000 | 0.9401 | 0.1806 | 0 | 0 |
| ELU α=3.6 | f1 | hard | 0.1014 | 0.9997 | 0.7549 | 0.4021 | 0 | 0 |
| ELU α=3.6 | f1 | easy | 0.0128 | 1.0000 | 0.8285 | 0.2825 | 0 | 0 |
| ELU α=3.6 | f2 | hard | 0.0320 | 1.0000 | 0.8411 | 0.2426 | 0 | 0 |
| ELU α=3.6 | f2 | easy | 0.0009 | 1.0000 | 0.8927 | 0.0173 | 0 | 0 |

参照幅0のunitは全20slot・全4siteで 0。 保存probeの非有限rの記録は 40 件（各boundary/siteを1件、unit数はJSON参照）。非有限の成績・更新を除外した走はない（存在すれば報告生成自体を拒否する）。

## 読みの限界

Wとbiasを同率に縮めるため、固定した局所入力で投影する瞬間のrは保つ。全4siteの介入では上流出力・入力分布・後続の学習が変わるので、全網の純粋な幅だけの媒介効果とは呼ばない。ELUは元から新品より高い場合があり、改善を自動的に『崩壊救済』としない。非有意・悪化・無効から『幅は原因ではない』とも結論しない。操作が幅を抑えたか、応答や性能を変えたか、同じ層・時期かを分けて読む。

## 保存と検算

学習runのcommit・コードhash・精度設定、全seed集合、P/Adam/activationの出発点、校正時の元40slot課題1末のbit一致、同20slot natural/shamの一致を照合した。登録集計と独立再計算は全seed差・検定・Holm・判定で一致する。

監視担当が報告したdata_sha256の型不整合（文字列対ファイル名→hashのsingleton dict）は、**学習後のレポートだけ**で恒久修正した。ファイル名と実ファイルSHAの検証を維持し、誤名・複数キー・不正digestの拒否を検査。監視担当のJSONと、スクリプトhash以外の全フィールドが一致した。図の整形もデータを変えない。新たな学習・forward・GPU計算は行っていない。

元driver sessionからnatural/cap/summary各工程のexit0記録を回収した。driver自身の終了コードは推定しない。[終了と修正の記録](https://github.com/Issan0511/lop_analysis/blob/73fdc5d6/analysis/cnn_width_cap_1021/postrun_report_fix_1021.md)。

生データ204ファイル・1,428,434,071 bytesを `/home/issan/Projects/obsidian-research-data/cnn_width_cap_1021/` へSHA256/bytes照合付きで退避した。[manifest](https://github.com/Issan0511/lop_analysis/blob/73fdc5d6/results/cnn_width_cap_1021/backup_manifest.json)。退避後の元コピーは検証してから除去し、元worktreeパスを保ったprovenanceからもレポートが参照を解決できるようにした。
