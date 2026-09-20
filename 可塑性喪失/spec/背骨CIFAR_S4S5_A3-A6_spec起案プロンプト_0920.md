# 背骨を RL-CIFAR × MLP に置くための 6 本 — S4・S5・A3・A4・A5・A6 の spec 起案プロンプト

親: [[中心主張v11作業リスト_0920]] §2 / 前身: [[初版必須走S1-S3_spec起案プロンプト_0919]]（共通の前置きはそちらの §「共通の前置き」をそのまま先頭に付ける） / 状態: **起案プロンプト（spec はまだ無い）。Issa「背骨を CIFAR にします」（0920）を受けて作成** / 作成: 2026-09-20 / 起草: Claude

## 位置づけ

背骨の箱を RL-CIFAR × MLP（3072-100-100-10・1200 枚固定・毎タスク乱数ラベル・50 タスク × 30,000 更新・Adam 1e−3・WD なし・正規化層なし・float32）に決めたので、MNIST の ELU→ELU にしか無かった環（応答 → LoP の移植、W 増大の上限介入）をこの箱で作り直す（S4・S5）。二つの売りの対照（A3・A4）、μ の大きさの予言（A5）、走なしの帳簿（A6）を足す。活性化と LoP の環は **std** で閉じ、raw は μ のダイヤルとして使う（作業リスト §1。Issa 未裁定なら spec の分岐点に出す）。

## 共通の前置きへの追加（0919 の前置きの末尾に足す）

```
追加 1（背骨）: 背骨の箱は RL-CIFAR × MLP。エンジンは src/rlcifar_mlp_battle_0918.py（13 腕・R=20 束ね・CUDA グラフ・各タスク末に snap/<arm>_<cond>_seed<s>/t<XX>.npz へ W1,b1,W2,b2,W3,b3 を保存）と、その派生 src/relu_doors_0919.py（扉 C/H/B/CS/LN・--conds raw|std・R=10 束ね）。両方とも φ と φ′ を手書きしている（Act クラスの phi/dphi）。
追加 2（再利用の規則・S2 の教訓）: 同じエンジンでも束ねる走の数 R が違うと bit 一致しない（relu_doors_h_0919: R=10 と R=20 で 460 項目中 193 不一致）。登録済みの結果を再利用するときは同じ R で S-reuse（2 タスク再走の bit 一致）を通す。通らなければ ref を同じ束ねで新規に走らせる（relu_doors_h_ref_0920 の型）。
追加 3（並走）: wt/resp_pm_gg_0919（S1・Codex）、wt/relu_doors_h_ref_0920（S2・本走中）、wt/ch_chb_200_0919（S3・GPU 待ち）に触らない。GPU は 1 枚・直列。本走の起動は S2・S3 の終了後。
追加 4（読み）: vault 主張/中心主張v11草案_0920.md と 主張/中心主張v11作業リスト_0920.md を、0919 の読む順の後に読む。この spec が埋める穴の番号（S4/S5/A3–A6）はそこにある。
追加 5（branch）: worktree は wt/<run>_0920、branch は <claude|codex>/<run>_0920、origin/main から切る。
```

## A6 — 走なし・最初に

```
# A6: CIFAR の帳簿 — どの層が崩れ、誰が運んだか（走なし・解析 spec）

穴: 作業リスト A6。CIFAR で「第 2 層が µ₂ の壁で沈む」は登録列（per_task.csv の zbar/zsd/dead_frac）の読みだけで、MNIST の l2_wall のような帳簿（自己・上流・交差・bias）が無い。S4 の移植する層と S5 の上限を置く層は、この帳簿で決める。

材料（新しい学習なし）: ~/Projects/obsidian-research-data/rlcifar_mlp_battle_0918/results/rlcifar_mlp_battle_0918/<arm>/snap/<arm>_<cond>_seed<s>/t<XX>.npz（t00 = 初期化、t01–t50 = 各タスク末の W1,b1,W2,b2,W3,b3、float32）と hist/<arm>_<cond>_seed<s>.npz（m1/m2 = ユニット別の z̄、alpha、θ ヒストグラム）。seed の 1200 枚はエンジンのローダで再現し、エンジンの単一スロット評価（rlcifar_mlp_battle_0918.py の「One slot on its own (R=1)」の関数）で z1・z2・a1 を 1200 枚について再計算する。S-snap: 再計算した z̄ が hist の m1/m2 と 2·eps·max|値| の中で一致。

対象: ELU・GELU・SILU・R（固定尺度 4 種）と KKT1・LR（生存の対照）× raw/std × seed 0–9。主対象は t00–t10（固定尺度 4 種は std で t3–t5、raw では t1–t4 に崩れる）。t50 まで取るが判定は崩壊までの区間で。

量（タスク末ごと・層ごと）: z̄_ℓ,i、sd_ℓ,i、µ_ℓ（層入力の平均。µ₁ = x̄、µ₂ = mean_x a₁(x)）、‖µ₂‖、‖w_{2,i}‖、cos(w_{2,i}, µ̂₂)、b_{2,i}、(ユニット, 画像) で φ′ < 1e−6 の割合と厳密 0 の割合。帳簿は l2_wall §4 と同じ: 連続するタスク末の間で
  Δz̄₂ = (ΔW₂) µ₂ + W₂ Δµ₂ + ΔW₂ Δµ₂ + Δb₂（自己・上流・交差・bias。旧状態で評価）、上流項は ‖µ₂‖ の伸びと µ̂₂ の回転に対称差分で割る。閉包検査: 4 項の和が Δz̄₂ に float の丸めの中で一致（変異対照: µ₂ を別 seed のものに差し替えると閉じない）。

登録する読みの規則（計算する前に固定）:
- R1 崩壊層: (ユニット, 画像) の φ′ < 1e−6 の割合が初めて 0.5 を越えた層。どちらも越えないまま online が 0.5 を割ったら、その時点で |z̄/sd| の大きい層。腕 × 条件ごとに 10 seed の多数で決め、割れたら SPLIT と書く。
- R2 運び手: 崩壊タスクまでの Σ Δz̄₂ に占める上流項の割合 ≥ 0.5 → UPSTREAM_CARRIES、自己項 ≥ 0.5 → SELF_CARRIES、他は MIXED。交差と bias の割合は併記。
- R3 上流の中身: 上流項のうち ‖µ₂‖ の伸びの割合を報告（MNIST は伸びが大半・回転は小さく逆向き）。
- KKT1・LR は同じ帳簿を報告のみ（判定しない）。

出力: analysis/cifar_ledger_0920/ と results/cifar_ledger_0920/summary.md（腕 × 条件 × 層の表と seed 別 csv）。学習走なし。費用は CPU/GPU で腕あたり数分、全体で半日。

Issa の判断が要る分岐: 判定区間を t00–t10 に固定するか崩壊時刻で切るか、ユニットの集約を中央値にするか平均にするか。

起案セッションの Claude の予測: std の固定尺度 4 種は崩壊層が第 2 層 0.9、raw の GELU/SiLU/R は第 1 層 0.9、raw の ELU は第 1 層が先に越える 0.6。ELU std の R2 は UPSTREAM_CARRIES 0.7、GELU std 0.6。bias の割合 < 5% 0.85。
```

## S4 — 応答 → LoP を背骨の箱で

```
# S4: CIFAR std の ELU に第 2 層の応答の場を移植する（作業リスト S4・V10 H5 の背骨版）

穴: 応答 → 再学習能力の介入証拠（resp_ee `BOTH_WAYS`・respdyn `PARTIAL`・swap）は MNIST ELU→ELU にしか無い。背骨の箱で同じ移植を 1 本。

箱: rlcifar_mlp_battle_0918.py の ELU・std・seed 0–9。既知の自然軌道（登録列・読みは事後）: online t1 0.983 / t2 0.920 / t3 0.435 / t4 0.179 / t5 0.133 / t10 0.102。第 2 層の φ′ < 1e−6 の割合 t1 0.000 / t2 0.010 / t3 0.14 / t4 0.41 / t5 0.665 / t10 0.955、z̄₂/sd₂ −0.5 → −1.95。第 1 層は z̄₁/sd₁ −0.1・死亡 0 のまま。移植する層は A6 の R1 が第 2 層なら第 2 層（予測 0.9）。
この箱の ELU は手書きの e^z で expm1 の床（−16.64）が無く、厳密 0 は float32 の underflow（z < −87 付近）でしか出ない。つまり resp_ee の「厳密 0」でなく respdyn の「0 でない微分でも学べない」の側の箱である。これを §1 に開示し、resp_ee §5.4 の「ε の段」は使わない。

接頭部と分岐点: 自然軌道を seed 0–9・std で t10 まで再走し（R=10。バトルは R=20 なので per_task の行は一致しない。一致しないことを S-prefix で確認して開示し、再走の行を正とする）、t1 末（健康・次タスクを 0.92 で学ぶ）と t10 末（崩壊・次タスクを 0.10）で P・Adam の m/v/t・乱数状態を保存する。分岐点の candidates: 健康側を t1 末にするか t2 末にするかは分岐点一覧に出す（t2 末は既に 0.92 で少し落ちている）。

移植: resp_ee §2.3 と同じ。a_i(x) = φ(z⁰_i(x)) + [φ(z_i(x)+d_i(x)) − φ(z⁰_i(x)+d_i(x))]、z⁰ は凍結した p₀ から毎ミニバッチ再計算、場 d_i(x) = z^(src)_i(x) − z^(br)_i(x) を画像 id で張る（RL は同じ 1200 枚なので id は固定。エンジンはバッチを index で引くので id が取れる）、一様 d = −Δ。訓練の微分は φ′(z+d)。エンジンの ELU Act の phi/dphi に差し込む。

腕（seed ごと・各 1 タスク）: N1・N10（自然の継続）、N1r・N10r（Adam 初期化）、R1_10（t10 の網に t1 の場・Adam 継続）= P1、R1_10r、S1_10r（t1 の網に t10 の場・Adam 初期化）= P2、S1_10、S1u5r・S1u10r・S1u20r（一様 −Δ の階段）。Adam の初期化／継続の理由づけは resp_ee §2.4 を引き継ぐ。層 1 への対照（S1 側の第 1 層版）は分岐点一覧に出す。

測る量: 次タスクの online（E）と memo、第 2 層の訓練の微分の平均・<1e−6 の割合・n_eff（箱内較正）。

判定（resp_ee §5 と同じ算術）: P1 = E(R1_10) − E(N10)、P2 = E(N1r) − E(S1_10r)、97.5% 対応差 t 区間（Bonferroni 2）。適用条件 (B): E(N1) − E(N10) の 95% 下端 > 0 かつ全 seed で第 2 層の φ′ 平均が t1 > t10、満たさなければ NOT_REPRODUCED。ラベル RESPONSE_BOTH_WAYS / RESTORE_ONLY / SINK_ONLY / RESPONSE_NOT_SHOWN / RESPONSE_REVERSED。回復率 ρ1・ρ2 は報告。一様の階段は「場（形）で落ちるか大きさで落ちるか」の記述ラベルを登録し、ε の段は置かない。

検査（変異対照つき）: S-prefix（再走 R=10 の t1–t10 が自分自身の再実行と bit 一致。バトルの R=20 とは一致しないことも記録）、S3（分岐点で特徴・logit・損失が自然腕と bit 一致。d を 0 にした変異で一致が崩れないこと＝恒等、d ≠ 0 で崩れないことが本検査）、S4（訓練の微分が φ′(z+d)。d を落とすと差が出る）、S5（Adam 初期化の最初の一歩 = lr·g/(|g|+ε)）、S-field（移植先の分岐点の応答が src の応答と 2·eps·max の中で一致）。

費用: 接頭部 10 タスク × R=10 ≈ 6 分、腕 11 × 1 タスク × R=10 ≈ 1 時間。実装 半日。

Issa の判断が要る分岐: 健康側の分岐点（t1 末 / t2 末）、第 1 層の対照腕を入れるか、Δ の階段の値、raw でも 1 本回すか。

起案セッションの Claude の予測: RESPONSE_BOTH_WAYS 0.5、SINK_ONLY 0.2、RESTORE_ONLY 0.15、RESPONSE_NOT_SHOWN 0.15。P1 が自然の差の半分以上 0.5。
```

## S5 — W 増大 → 進行を背骨の箱で

```
# S5: CIFAR std の ELU に上限を置く（作業リスト S5・l2cap の背骨版）

穴: 「W の成長を止めると崩壊が止まる」の介入証拠（l2cap `RESCUED` 10/10、mucap は遅らせるだけ）は MNIST ELU→ELU にしか無い。CIFAR では ref が初期ノルムのまま死に、CH は伸びても輸送しない、という読みまで。

箱: rlcifar_mlp_battle_0918.py の ELU・std・seed 0–9・50 タスク・R=10（std だけ）。ref は同じ束ねで新規に走らせる（バトルの ELU std は R=20 なので再利用しない）。

上限（l2cap の型。半径はその run の task 1 終端値、task 2 から各 Adam 更新の直後に射影）:
- cap1: 第 1 層の行ノルム ‖w_{1,i}‖ の上限。std では µ₁ ≈ 0 なので mucap の「µ̂ 方向成分 q と直交成分 v」は定義できない。行ノルム全体で a₁ の尺度、つまり ‖µ₂‖ の伸びを抑える（‖w₁‖ は 3.6 → 14 と伸びる）。
- cap2: 第 2 層の行ノルム ‖w_{2,i}‖ の上限（1.0 → 2.2）。
- cap12: 両方。
- cap12_bfix: 両方＋ b₁・b₂ を task 1 終端値に固定。
射影は静的な演算なので CUDA グラフに入る。

主 endpoint（主窓 t31–50。20 タスクに縮めるなら t11–20、分岐点に出す）: E1 = online、E2 = 第 2 層の訓練の微分の平均（e^z）の task 1 からの変化。床は l2cap と同じ規則（主窓の online 平均 ≤ そのタスクのラベルでの最良定数予測 + 3 SD/√窓）。ラベル RESCUED / COLLAPSED / SPLIT / IMPAIRED、崩壊時刻 T½（適合率 (A(t)−0.1)/(A(1)−0.1) が 1/2 を割るタスク）の符号検定 LATER/SAME。輸送の副 endpoint: 主窓の Δz̄₂ の ref との差、‖µ₂‖・‖w₂‖・b₂ の軌跡（A6 の帳簿と同じ列）。交互作用 δ_cap12 − δ_cap1 − δ_cap2 を報告。

検査: S-off（射影を外すと ref と bit 一致）、cap 有効（各更新後に行ノルム ≤ 半径 + 2·eps）、変異（半径 ×1000 で ref と一致・×0.5 で差が出る）、S-resume、bfix（b の勾配が 0 で値が動かない）。

費用: 5 腕 × R=10 × 50 タスク。バトルは R=20 の 1 腕が約 55 分だったので R=10 で 35 分前後、計 3 時間。20 タスクなら 1.2 時間。実装 2–3 時間。

Issa の判断が要る分岐: cap1 の定義（行ノルム／別の量）、50 タスクか 20 タスクか、raw を足すか（raw の ELU は第 1 層が µ で t1 から −3.2 sd にいて上限では扱えない。足すなら別の問い）。

起案セッションの Claude の予測: cap12 RESCUED 0.6、cap1 単独は COLLAPSED で LATER 0.6、cap2 単独は SPLIT か COLLAPSED 0.7、cap12 でも b₂ は沈み続ける 0.6。
```

## A3 — 「BN でいいのでは」に答える 4 腕

```
# A3: relu_doors に std+H・BN・mean-only BN・LN+H を足す（作業リスト A3・CH の売りの対照）

穴: CH は raw でしか走っていない。「実務は std 済みで、BN か LN を入れる」に対して、std の上で H が要るか、BN で足りるか、足りるなら平均側か分散側か、を対照で持っていない。Lyle 2402.18762 付録 D.2（分散側が主）と E.9（入力中心化で大半再現）に正面から答える表になる。

箱・エンジン: src/relu_doors_0919.py（DOORS 表に腕を足す。norm の値に "batchnorm"・"meanonly" を足す）。raw・seed 0–9・50 タスク・R=10。ref は relu_doors_h_ref_0920 の fresh ref（R=10）を S-reuse で再利用、C・CH は relu_doors_0919（R=10）を S-reuse で再利用。

腕:
- Hs: --conds std で扉 H（入力は L&C の定数で標準化。C は無し）。
- BN: c=True（raw + 入力中心化）、両隠れ層の線形写像の後・ReLU の前に BatchNorm（バッチ 16 の統計で平均を引き分散で割る・affine γβ あり・評価は running 統計・torch 既定の momentum）。LN と同じ位置。
- mBN: 同じ位置で mean-only BatchNorm（Salimans & Kingma 2016。バッチ平均を引くだけ・分散で割らない・affine 無し・評価は running mean）。
- LNH: relu_doors の LN（c=True・affine あり）に扉 H を足す。
BN の affine の有無は交絡（β が bias 経路を足す）なので、BN0（affine 無し）を 5 本目に置くかは分岐点に出す。

登録する判定（窓 = t31–50 online の seed 中央値。帯は relu_doors_h の型: 既存 CH の seed 差 1 組の RMS を許容損失として導く）:
- J1 Hs − CH: TIE / STD_H_BETTER / STD_H_WORSE。「標準前処理の上で H だけで足りる」の証拠。
- J2 BN − CH: BN_SUFFICES（帯の中）/ BN_WORSE / BN_BETTER。
- J3 mBN − BN: MEAN_ONLY_SUFFICES / VARIANCE_NEEDED。
- J4 mBN − CH: バッチ統計と EMA の差。TIE を予測。
- J5 LNH − LN: H_RESCUES_LN / H_NOT_ENOUGH。LN の正側の死（実効ランク 63 → 0）を H が止めるか。
- 診断（登録列）: z̄₂/sd₂、gate_zero_frac₂、|b₂|/sd（BN の β の分）、eff_rank₂、r_a1。

検査: S-off（全扉と norm を外すと fresh ref と bit 一致）、S-BN（torch の F.batch_norm と 2·eps·max の中で一致・γβ が動く）、S-mBN（分散の経路が無いこと: 入力を 3 倍にすると mBN の出力も 3 倍。BN では 3 倍にならない）、S-resume（running 統計が ckpt に入る。relu_doors で H の EMA が抜けていた前例）、変異対照。

費用: 4 腕 × 30 分 = 2 時間（BN0 を足すと 2.5 時間）。実装 2 時間。

Issa の判断が要る分岐: BN0 を足すか、BN の位置（ReLU の前で固定か）、Hs を CH と比べるか C と比べるか。

起案セッションの Claude の予測: J1 TIE 0.7、J2 BN_SUFFICES 0.6、J3 MEAN_ONLY_SUFFICES 0.7、J4 TIE 0.7、J5 H_RESCUES_LN 0.5。
```

## A4 — KKT1 の対照

```
# A4: 13 活性化バトルに CReLU と Deep Fourier を足す（作業リスト A4・KKT1 の売りの対照）

穴: 活性化を売る論文への最初の質問は「CReLU（Abbas et al. 2023）と Deep Fourier features（Lewandowski et al. 2024）に勝つのか」。どちらも一度も走っていない（relu_doors の spec 本文に名があるだけ）。同じ箱・同じ判定で並べる。

箱・エンジン: src/rlcifar_mlp_battle_0918.py。raw と std・seed 0–9・50 タスク・R=20（バトルと同じ束ね。KKT1・SNA・LK03・RSL の登録行を S-reuse で再利用する。同じ R でも一致しなければ再走して開示）。DIMS は固定 (3072,100,100,10) なので腕ごとの幅を通す配管が要る。

腕（特徴の幅で揃える）:
- CR: 各隠れ層 50 ユニット → [ReLU(z), ReLU(−z)] の 100 特徴。パラメータは第 1 層が半分。
- CRw: 100 ユニット → 200 特徴（パラメータは増える）。
- DF: 50 ユニット → [sin z, cos z] の 100 特徴（Lewandowski の定式化を原典で確認して写す。尺度の扱いも）。
- DFw: 100 → 200。
幅の揃え方（特徴で揃える／パラメータで揃える）は分岐点に出す。

登録する判定（バトルと同じ: 窓 t31–50 online、崩壊 = 窓 < 0.5、腕対腕は seed 対応の符号検定で相手が勝つ seed ≤ 1 かつ p < 0.05）:
- 条件ごとに KKT1 − CR・KKT1 − CRw・KKT1 − DF・KKT1 − DFw: KKT1_ABOVE / TIE / BASELINE_ABOVE。
- 崩壊の有無と低下（t1–10 − t41–50）。
- 読みの登録: DF が raw で KKT1 と TIE なら「周期の特徴でも足りる」、下なら「周期そのものが要素ではない」（K1 と合わせて読む）。CR が raw で生きるなら「両側の ReLU で片側化を逃れる」。

検査: グラフ／eager の一致（エンジン既存）、S-reuse（R=20 で既存腕の 2 タスクが bit 一致）、CReLU の厳密性（特徴 = [relu(z), relu(−z)]、変異で崩れる）、DF の厳密性、幅の配管（パラメータ数を数えて記録）。

費用: 4 腕 × R=20 × 50 タスク ≈ 4 × 55 分 = 3.5 時間。実装 2 時間。

Issa の判断が要る分岐: 幅の揃え方、DF の尺度、L&C の RReLU（RSL は既にある）以外に足すか。

起案セッションの Claude の予測: raw で KKT1_ABOVE 対 CR 0.6、対 DF 0.4（TIE 0.4）、std は全部 TIE 0.6。CR・DF は崩壊しない 0.8。
```

## A5 — μ の大きさ → 初期配置（訓練なし）

```
# A5: r から初期化時の片側ユニット率を予言する（作業リスト A5・μ の大きさの売り）

穴: 「μ の大きさが配置を決める」の一番安い予言。r = ‖x̄‖ / rms‖x − x̄‖ から初期化時の片側ユニットの割合を 2Φ(−2.33/r) で予言し、seed 0–9 では事後に合っている（raw 25.3% ± 2.5% 対 22.3%、std 0.0% 対 0.0%）。未使用 seed で登録すれば訓練なしの予言になる。

箱: バトルのエンジンの初期化（W₁ の sd = 1/√(3·3072)）と seed の 1200 枚。学習なし。seed は未使用の 20–39。

条件: raw、std、C（x − x̄）、ダイヤル x ↦ (x − x̄) + γ x̄（γ ∈ {0.25, 0.5, 0.75, 1, 1.5, 2}。共分散を保って平均だけ振る。r = γ·r_raw）。

量: 第 1 層の各ユニットで min(P(z>0), P(z<0)) を 1200 枚で測り、< 0.01 なら片側。割合 f を seed ごとに。第 2 層も同じ量を r₂ = ‖µ₂‖ / rms‖a₁ − µ₂‖（初期化時の ReLU 出力）で。

登録する予言と判定: f(r) = 2Φ(−2.33/r)（2.33 = Φ⁻¹(0.99) は 1% の定義から出る定数で、当てはめではない）。seed ごとの二項の SD √(f(1−f)/100) から 20 seed の中央値の帯を導き、その中に入れば PREDICTED、外れれば OFF（向きを書く）。第 2 層は r₂ を測ってから同じ式を当てる（半登録: r₂ は測定値）。ダイヤルの単調性（γ で f が単調増加）も登録。

検査: r の計算を別実装で照合、片側の判定を解析解の入力（ガウス）で照合、変異対照（画素を並べ替えても r と f は不変、x̄ を 0 にすると f = 0）。

費用: 分。実装 1 時間。
任意の追加（REPORT_ONLY）: ダイヤルの各 γ で ReLU を 1 タスクだけ訓練し、t1 の online を r に対して並べる（初期の片側率だけでは t1 の学べなさは決まらない。raw は f 0.22 で学べない）。膝の位置は予言しない。

起案セッションの Claude の予測: raw/std/C で PREDICTED 0.8、ダイヤル単調 0.9、第 2 層 PREDICTED 0.5。
```

## 出所

- 0920 の会話（Issa「背骨を CIFAR にします」「その上でなんのspecがいるのか」「この表をもう少し具体的に」）。
- 型: [[初版必須走S1-S3_spec起案プロンプト_0919]]、repo `specs/spec_resp_ee_0917.md` §2.3–2.4・§5、`specs/spec_l2cap_ee_0917.md`、`specs/spec_relu_doors_h_ref_0920.md`（fresh ref の型）。
- 数値: [[RL-CIFARのMLPで13の活性化をバトル_kunekune_結果_0918]] §1・§8、[[ReLUが沈む道を1本ずつ塞ぐ_relu_doors_結果_0919]]、`results/rlcifar_mlp_battle_0918/*/per_task.csv`（ELU std の t1–t10 の列）、`results/relu_doors_h_0919/summary.md`（R の教訓）。
