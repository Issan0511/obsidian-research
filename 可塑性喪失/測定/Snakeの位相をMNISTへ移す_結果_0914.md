# Snake の位相を MNIST へ移す：結果 0914

状態: **完了**（登録走・340/340 完走・main に統合済み） / 更新: 2026-09-14 09:5x JST / 起草: Claude（Issa 就寝中の「全自動」指示）
親: [[W増大メカニズム_0909]] §5.4 / spec: [[Snakeの位相をMNISTへ移す_spec_0914]]（repo `specs/spec_snake_phase_mnist_0914.md`・事前登録 `aa78461`・追補 1 `e6411cf`）
前段（CondA）: [[零点復元と重み収縮_新規学習結果_0913]]・[[セッション引き継ぎ_0914_零点復元と個体の伸縮]]

> 数値の出所は repo main の `results/snake_phase_mnist_0914/summary.md`・`verdict.csv`・`verdict.json`（結果 commit `388baba`、main 統合 `cbac3ee`）。単位は pt（test 精度 ×100）、窓は常に併記。**E1 だけが確認的な見出し**で、他は副次。EQUIVALENT は「単走のタスク標本の分解能より小さい」の意味で、「効果なし」ではない。

## 結論

1. **箱 B なら Snake の議論ができる。** N06（normal Snake α=0.6）は LIN より明確に劣化する: D_pair(N06−LIN) = +2.04 [+1.95, +2.13]（D = mean t16–30 − mean t101–120、n=20）。CondA（Snake が課題を解き切って劣化が無い）とは違う。
2. **固定 α の peak・valley は normal より劣化が小さいが、どの窓でも精度が低い。** C1 P06−N06 の D −0.41 [−0.50, −0.32]、C2 V06−N06 −0.24 [−0.32, −0.16]（ともに `LESS_DECLINE`）。一方 ΔA_base −0.98 / −1.01、ΔA_late −0.57 / −0.77（`LOWER`）、fresh の水準も −1.47 / −1.43 低い（`FRESH_LEVEL_CONFOUNDED`）。登録の総合クラスは `TEMPORAL_LOP_LESS` だが、中身は「**低く始まって少なく落ち、後期もまだ低い**」。絶対水準での可塑性の利点ではない。
3. **分解: peak は起点とオフセットが足し算にならず（`NON_ADDITIVE`）、オフセット側が主。valley は起点（死んだ初期関数）から来る（`ORIGIN`）。**
   - peak: 単純効果 C3 P06c−N06（オフセット K だけ）−0.46 `LESS`、C4 P06i−N06（初期関数だけ）−0.18 `LESS`、交互作用 I_P +0.23 [+0.10, +0.36]。主効果（REPORT）K −0.35 [−0.42, −0.27]、S −0.06 [−0.12, −0.01]。枝 B_P = P06c_k1−P06c −0.60 `LESS` → 根の幾何だけでなく**活性値の水準と符号**が効く。
   - valley: C6 V06i−N06 −0.26 `LESS`（ΔA_late・E3 も同じ向き）、C5 V06c−N06 +0.06 [−0.05, +0.17] `EQUIVALENT`。
4. **適応 α 族では逆に、peak の位相構造が劣化を増やす（`STRUCTURE`）。** 同じ初期関数どうしの C7s SNAP−SNAi_P で D +0.65 [+0.54, +0.76] `MORE_DECLINE`、ΔA_late −2.01、ΔGap +2.15（fresh の水準は +0.15 と同程度なので、差は逐次側の劣化）。M1 は層 1 の両窓で PHASE_ACTIVE。総効果 C7 SNAP−SNA も +0.48 `MORE`。SNAV は劣化こそ小さい（C8 −0.46）が、A_late が −2.39 と大きく低い。
5. **leaky に K_P（q=−2.14）を足すと、劣化が小さく、後期の精度も高い。** C9 LR_qKp−LR の D −1.13 [−1.21, −1.04]、ΔA_late **+0.48** [+0.41, +0.55]（`HIGHER`）。base は −0.65、fresh は −0.59 と低いのに、後期は上回る。今回の 17 腕で、時間劣化と後期の絶対水準の両方が基準より良かったのはこの腕だけ。符号を反転した C9n（q=+2.14）は劣化 −0.78 だが、後期 −2.28 と低い。
6. **CondA の「peak は育たない」は MNIST・Adam では再現しない。** CT1（層 1、ΔlogN、t101–120）: C1 +0.120（`GROWTH_ENHANCED`）、C2 +0.084（`GROWTH_ENHANCED_BELOW_CONDA_SCALE`）、C7 +0.183、C8 +0.215。P06 は N06 より幅が広いのに劣化は小さく、腕間で幅は劣化を並べない（既知の gate_shape_0911 A6 と同じ向き・W 病理の証拠にはしない）。
7. **CondA 型の個体の分岐（多数が初期値より縮む）は Adam 下で無い。** strict な縮小（‖W̃ᵢ(t120)‖² < ‖W̃ᵢ(0)‖²）は全 17 腕で 0%。層 1 の log 成長比のユニット間 SD は最大でも SNAV の 0.082（REPORT）。

## 箱と走

- 箱 B = gate_shape_0911 と同一（784–100–100–10・CE・batch 16・625 更新/タスク・Adam 1e−3・moment 持ち越し・t1–120・CPU float32）。17 腕 × seed 0–19 = 340 走、全走 COMPLETE、BROKEN・DIVERGED 0。
- **G1**: N06/LR/LIN/SNA の s0–2 が gate_shape_0911 の per-unit 16 配列 × 120 タスクと全一致（`ANCHORED`）。段階 0 の S1–S9・S14・S15 は all_pass、変異はすべて検出（実装 `ee00d4a`）。
- 分解能マージン（基準対 N06−LIN・LR−LIN のみから）: h_D 0.201、h_Alate 0.124、h_Abase 0.158、h_Gap 0.154。
- 可検定性: TESTABLE_FIXED +2.04 [+1.95, +2.13]、TESTABLE_LEAKY（LR−LIN）+1.78 [+1.71, +1.86]、ともに成立。

## E1・E2・E3（全対比）

| 族 | 対比 | E1 D（t16–30 − t101–120） | E1 | ΔA_late（t101–120） | ΔA_base（t16–30） | ΔGap（fresh−seq, t101–120） | ΔA_fresh（t101–120） | §6.4 |
|---|---|---:|---|---:|---:|---:|---:|---|
| F1 | C1 P06−N06 | −0.41 [−0.50,−0.32] | LESS_DECLINE | −0.57 | −0.98 | −0.90 | −1.47 | TEMPORAL_LOP_LESS |
| F1 | C2 V06−N06 | −0.24 [−0.32,−0.16] | LESS_DECLINE | −0.77 | −1.01 | −0.66 | −1.43 | TEMPORAL_LOP_LESS |
| F1 | C3 P06c−N06 | −0.46 [−0.55,−0.37] | LESS_DECLINE | −0.62 | −1.08 | −0.20 | −0.82 | TEMPORAL_LOP_LESS |
| F1 | C4 P06i−N06 | −0.18 [−0.27,−0.08] | LESS_DECLINE | −0.16 | −0.34 | −1.12 | −1.27 | TEMPORAL_LOP_LESS |
| F1 | C5 V06c−N06 | +0.06 [−0.05,+0.17] | EQUIVALENT | −0.28 | −0.22 | +0.05 | −0.23 | LEVEL_ONLY |
| F1 | C6 V06i−N06 | −0.26 [−0.33,−0.18] | LESS_DECLINE | −0.55 | −0.81 | −0.60 | −1.16 | TEMPORAL_LOP_LESS |
| F1x | I_P | +0.23 [+0.10,+0.36] | NON_ADDITIVE | | | | | |
| F1x | I_V | −0.04 [−0.18,+0.10] | ADDITIVE | | | | | |
| F1x | B_P P06c_k1−P06c | −0.60 [−0.71,−0.49] | LESS_DECLINE | −0.80 | −1.40 | −0.87 | −1.67 | |
| F2 | C7 SNAP−SNA | +0.48 [+0.35,+0.62] | MORE_DECLINE | −1.97 | −1.49 | +0.83 | −1.14 | TEMPORAL_LOP_MORE |
| F2 | C8 SNAV−SNA | −0.46 [−0.67,−0.25] | LESS_DECLINE | −2.39 | −2.85 | −0.03 | −2.42 | INCONCLUSIVE |
| F2 | C7s SNAP−SNAi_P | +0.65 [+0.54,+0.76] | MORE_DECLINE | −2.01 | −1.36 | +2.15 | +0.15 | TEMPORAL_LOP_MORE |
| F2 | C8s SNAV−SNAi_V | −0.10 [−0.28,+0.08] | INCONCLUSIVE | −2.06 | −2.16 | +1.85 | −0.21 | LEVEL_DIFF_DECLINE_INCONCLUSIVE |
| F3 | C9 LR_qKp−LR | −1.13 [−1.21,−1.04] | LESS_DECLINE | **+0.48** | −0.65 | −1.07 | −0.59 | TEMPORAL_LOP_LESS |
| F3 | C9n LR_qKpn−LR | −0.78 [−0.90,−0.66] | LESS_DECLINE | −2.28 | −3.06 | −0.13 | −2.40 | INCONCLUSIVE |

E1 の角括弧は 95% 反転 CI（符号反転検定）。E2・E3 の CI とラベルは `summary.md`。F1–F3 の E1 はすべて Holm 後、表のラベルどおり。**すべての対比に `FRESH_LEVEL_CONFOUNDED`**（fresh の水準差が有意）が付く。spec の規則どおり、fresh gap の差は初期関数を揃えた角（C3・C5・C7s・C8s）で読む。

§6.6 の答え: peak `NON_ADDITIVE`、valley `ORIGIN`、structure_C7s `STRUCTURE`、structure_C8s `STRUCTURE_INCONCLUSIVE`。

M1（Φ = 2|sin(Δθ/2)|·medianᵢ Aᵢ − IQRᵢ ḡᵢ^ref）: 6 対 × 2 層 × 2 窓の 24 組すべてが PHASE_ACTIVE。固定 α の後期（層 1 t101–120）でも C1 +0.118 [+0.115, +0.120]、C2 +0.158。位相の振幅そのものは後期に小さくなるが、基準腕のユニット間のゲートの散らばりはさらに小さい。

## 腕ごと（REPORT・seed 平均）

| 腕 | D | A_late（t101–120） | Gap | logN1 late | logN2 late |
|---|---:|---:|---:|---:|---:|
| LIN | 0.23 | 88.71 | 0.72 | 1.930 | −0.105 |
| LR | 2.01 | 89.97 | 1.12 | 2.092 | 0.906 |
| LR_qKp | 0.88 | 90.44 | 0.05 | 2.097 | 0.780 |
| LR_qKpn | 1.23 | 87.69 | 0.99 | 2.354 | 1.051 |
| N06 | 2.27 | 89.49 | 2.26 | 1.749 | 0.087 |
| P06 | 1.86 | 88.92 | 1.36 | 1.869 | 0.126 |
| P06c | 1.81 | 88.87 | 2.06 | 1.883 | 0.148 |
| P06c_k1 | 1.21 | 88.07 | 1.19 | 1.968 | 0.252 |
| P06i | 2.09 | 89.33 | 1.14 | 1.786 | 0.091 |
| V06 | 2.03 | 88.72 | 1.59 | 1.833 | 0.277 |
| V06c | 2.33 | 89.21 | 2.31 | 1.780 | 0.140 |
| V06i | 2.01 | 88.94 | 1.65 | 1.812 | 0.210 |
| SNA | 0.73 | 91.50 | 0.20 | 1.789 | 0.292 |
| SNAP | 1.21 | 89.53 | 1.03 | 1.972 | 0.431 |
| SNAV | 0.27 | 89.11 | 0.17 | 2.004 | 0.604 |
| SNAi_P | 0.56 | 91.54 | −1.12 | 1.819 | 0.318 |
| SNAi_V | 0.37 | 91.17 | −1.68 | 1.824 | 0.275 |

登録互換の L（中央値 t16–20 − 中央値 t101–120）は N06 2.41、SNA 0.71、LR 2.10、LIN 0.35（seed 中央値）。gate_shape_0911 の 3 seed（SN06 2.74・SNA 0.71・LR 2.28・LIN 0.63）と同じ並び。

## 事前予測の採点（Claude、spec §12）

| # | 予測 | 結果 |
|---|---|---|
| P1 | 恒等式・変異 | ○ |
| P2 | G1 錨 | ○（ANCHORED） |
| P3 | TESTABLE 両方成立 | ○ |
| P4 | N06 の D 平均 ∈ [1.955, 2.599] | ○（2.271） |
| P5 | 固定 α 後期 PHASE_WASHED／適応族後期 ACTIVE | △（固定 α は ACTIVE で外れ、適応族は当たり） |
| P6 | C1・C2 の CI が ±0.8 以内 | ○ |
| P7 | 両位相で \|K\| > \|S\|、C4・C6 は有意にならない | ×（valley は S が主、C4・C6 とも LESS） |
| P9 | B_P は EQUIVALENT でない | ○ |
| P10 | C9 と C3 が同符号／C9n は逆符号 | △（同符号は当たり、C9n も同符号で外れ） |
| P11 | C7/C8 のどちらかが MORE、STRUCTURE（.35） | ○ |
| P13 | CONFLICT なし | ○ |
| P14 | log 成長比 SD < 0.13 | ○（最大 0.082） |
| P18 | CT1 C1 層 1 は SUPPRESSED でない | ○（ENHANCED） |
| P19 | logN2 が \|K\| の順に小さい | ×（逆順に大きい: P06c_k1 0.252 > P06c 0.148 > V06c 0.140 > N06 0.087） |
| P22 | C2 LOWER／V06 FRESH_LEVEL_CONFOUNDED／C1 はどちらでもない | △（前 2 つ当たり、C1 も LOWER で外れ） |
| P23 | V06・P06 の BROKEN/DIVERGED 0 | ○ |

○ 11・△ 3・× 2。

## 読み方の限定

- **E1 の LESS_DECLINE は、多くの対比で「水準が低い」と同時に出ている。** 劣化の量は、落ちる前の水準に依存しうる（床に近いほど落ちる余地が小さい）。この走は水準を揃えた比較をしていない。固定 α の位相腕を「可塑性を守る」と書かない。後期の絶対精度も上がったのは LR_qKp だけ。
- `FRESH_LEVEL_CONFOUNDED` が全対比に付く。活性化やオフセットを変えると、初期状態から 625 更新で学べる水準自体が変わる。
- 位相腕は隠れ層 2 層ともに活性化を変える。層を限定したオフセットは未検定。
- 箱 B（Permuted MNIST・Adam・625 更新・t1–120・幅 100）限定。Random Label・SGD・長い地平線へ外挿しない。
- CT1 は腕間の比較で、W 病理の証拠ではない。CondA の自由重み u（5 bit への入射）に当たる量は MNIST に無く、CT1 は ‖W̃ᵢ‖ についての答え。
- M1 のラベル（書き方の規則と STRUCTURE）は層 1 で判定した（実装時に固定した解釈、`verdict.py` 冒頭）。24 組すべて ACTIVE なので、層 2 で判定しても結論は変わらない。

## 運用の記録

- **追補 1（運用のみ）**: 起動規則の「SwapFree < RSS_peak なら起動しない」が、07:35–08:38 の約 1 時間、起動を完全に止めた（MemAvailable は 16–20 GiB、swap は他アプリの古いページで 7 GiB 超使用）。swap 条件を「MemAvailable < 2·RSS_peak + ΔM_desk のときだけ」に限定し、launcher を入れ替えた。判定規則・腕・seed は不変。
- 見張りの動作（`launch_log.txt`）: 入れ替え前の launcher で SIGSTOP 18 回（07:0x–07:3x、wcap の 10 プロセスと重なった時間帯）、入れ替え後に SIGSTOP 3 回・SIGCONT 3 回（MemAvailable の最低 5.9 GiB）、SIGTERM は全期間 0 回・OOM なし。
- 入れ替え後、最後の 20 並列で swap の空きが 0 まで下がった（09:32、`free` で確認）。追補 1 の緩和は swap の満杯を防がない。**次の走では並列の上限を物理コアより低く抑えるか、swap が満杯に近いときは MemAvailable の境界を上げる**。
- 経過: 登録 03:40 → 実装・検査 06:37–06:55 → 本走 06:57 → 追補 1 08:49 → 完走 09:35。

## 次の候補（未起票・自動では走らせない）

1. LR_qKp（leaky + 負のオフセット）の後期の優位は、層 1 だけ・層 2 だけのオフセット、|q| の用量、fresh の水準を揃えた比較のどれで残るか。
2. 適応族の peak（SNAP）が劣化を増やす機構: ω（lr/‖W̃ᵢ‖）とゲートの位置の分離（`STRUCTURE` の媒介）。
3. 水準を揃えた比較（初期の精度を合わせる lr や更新数の調整）で、固定 α の LESS_DECLINE が残るか。
4. 後段に回した群除去（CT2）・根への着座（CT3）・群の将来学習は、保存済みの snapshot t20/t60/t120 から行える（本結果を見た後の登録になることを明記する）。

## 後続

- SGD 橋（optimizer だけを SGD に替えた 5 腕）→ [[SGD橋_箱Bのoptimizerだけを替える_結果_0914]]

## 所在

- repo main: `specs/spec_snake_phase_mnist_0914.md`・`specs/addendum_1_snake_phase_mnist_0914.md`・`src/snake_phase_{acts_,}mnist_0914.py`・`analysis/snake_phase_mnist_0914/`（checks・verdict・launch・resources）・`results/snake_phase_mnist_0914/`（verdict.csv/json・summary.md・全 340 走の rows.csv と provenance.json・錨 12 走の units.npz・launch_log・g1_full.json）。ブランチ `claude/snake_phase_mnist_0914` は main 統合後に削除。
- 生データ（git 外）: `~/Projects/obsidian-research-data/snake_phase_mnist_0914/`（units.npz・snapshot t20/t60/t120・煙走、1428 ファイル・1.75 GiB）。`results/snake_phase_mnist_0914/backup_manifest.json` に source・backup・bytes・sha256。
