# 沈降と回復の競争を検証 — erosion_race_0919

状態: 実行済み / 2026-09-19 / Codex / Issa「この仮説面白そうなので検証して」
関連: [[三理論の再統合_駆動と応答を同じ更新則で結ぶ_0919]]・[[駆動源問題_0909]]・[[ReLUが沈む道を1本ずつ塞ぐ_relu_doors_結果_0919]]。
V10作業リスト: H1/A2の初期第1層部分、H4の機構候補。長期生存条件やW増大全体を閉じたとはしない。

## 1. 結論

登録した「最初の5000更新だけ第1層の負向きconfidence由来変位を取り除けば、その後の適合が救われる」という版は **不支持**。GELUは改善0/5 seed、ELUは全5 seedで悪化した。第1層の応答を保つ操作自体は効いたが、第2層が著しく低応答化する経路になった。単に「猶予が短すぎた」と言い換えない。

同時に「Leak/Snakeはそもそも下向き移動が小さい」という予測も外れた。初期750更新では両者ともGELUより下向き移動が大きく、上向き移動の増加がそれ以上に大きかった。上向きの前活性移動を、そのまま機能・記憶の回復と同一視しない。

この結果は今回の介入の十分性を退ける。全網の競争仮説や侵食ラチェット一般を一括棄却する結果ではない。

## 2. 箱と登録

raw RL-CIFAR、同じ1200画像・初期重み・ラベル列・batch列を5 seed (1001–1005) で対応づけ、3072–100–100–10 MLP、Adam .001、2課題×30000更新。自然腕はReLU/GELU/ELU/leaky .1/leaky .01/adaptive Snake。追加はGELU early/late、ELU earlyの計9条件45本。SiLU・固定Snakeは今回未検証。

earlyは課題1更新1–5000、lateは5001–10000。課題2は介入なし。初期の画像64枚×第1層unitについて「初期z>0だった対」を固定し、実パラメータ差による前活性の上下変位を毎更新測定。負側へ移った後も同じ対を追う。

CE勾配をconfidence項とlabel項に分け、課題をまたぐAdam一次モーメントをhistoryとして独立に残す。3項は実際の同じ二次モーメント分母と全履歴のbias補正を共有。これは実軌道上の寄与帰属であって、別々のAdamを走らせる反実仮想ではない。conf=侵食、label=回復とは定義しない。

登録: spec初版 `4a69757`、実行前の明確化・engine・検査・report `8856bab42b3aad4b012566624c3825cdfa0f172b`。既知の親seed0–9を見て設計し、別seedで検証した。既知情報の開示と予測7件はspecに凍結。本走後に判定閾値を変更していない。

## 3. 登録結果

全て5 seedの課題末accuracyの中央値。online平均と取り違えない。

| 腕                   |    課題1末 |    課題2末 |
| ------------------- | ------: | ------: |
| GELU base           | 0.12250 | 0.11167 |
| GELU early          | 0.11167 | 0.11083 |
| GELU late           | 0.11333 | 0.12250 |
| ELU base            | 0.99167 | 0.89833 |
| ELU early           | 0.10667 | 0.10583 |
| leaky .1 base       | 1.00000 | 1.00000 |
| leaky .01 base      | 0.99667 | 0.92000 |
| adaptive Snake base | 1.00000 | 1.00000 |

C1: GELU early−baseの対応差中央値 −0.00917、正の差0/5、`NO_CLEAR_RESCUE`。
C2: early−late −0.00083、正0/5、`NO_EARLY_ADVANTAGE`。
C3: 課題2 onlineのearly−base −0.000983、正2/5、`NO_PERSISTENT_HELP`。
C4: ELU early−base −0.88667、正0/5。天井効果だけでは説明できない大幅悪化。
総合 `5000_STEP_GRACE_NOT_SUPPORTED`。5 seedの登録記述基準であり、有意差検定ではない。

M1は `CONF_NEGATIVE_DOMINANT`。課題1更新1–750でconf負寄与が負成分の過半を占める登録基準を、ReLU 5/5、GELU 4/5で満たした。「下向きに寄与する」と「それを除けば有益」は別である。

M2はLeak .1/Snakeとも `MORE_UPWARD`。以下は初期750更新の5 seed算術平均、初期unit標準偏差で規格化した固定probe上の総移動量。

| 腕              |   下向きE |   上向きR | 正味の下向きE−R |
| -------------- | -----: | -----: | --------: |
| GELU           | 152.28 |  74.63 |     77.65 |
| leaky .1       | 419.01 | 351.39 |     67.62 |
| adaptive Snake | 560.17 | 547.87 |     12.30 |

Leak対GELUの正味差10.03は、下向き増加による−266.72と上向き増加による+276.75の和。Snakeは−407.88と+473.23の和。下向きの小ささを生存理由に置けない。

予測はCodex **3/7的中、Brier 0.23893**。救済とLESS_DOWNWARDの予測は外れた。

## 4. 介入後に何が起きたか（事後の読み）

第1層の負向きconf変位を除く操作は、第1層の出力変動を保った。一方で上流の活動尺度が大きくなった。ELU earlyの5000更新時点では、unit平均前活性の中央値をseed間で集約すると第1層約+75、第2層約−89。

課題1末の第2層:
- GELU earlyは4/5 seedで全100unitがdead閾値に入り、出力sd比のunit中央値V₂は全5 seedで0。
- ELU earlyは3/5 seedで全unitがdead閾値に入り、V₂は4/5で0、残りも約0.000198。
- GELU/ELUのbaselineは、第2層dead比率が全seedで0だった。

deadは1200画像上のmax|φ′|<1e−6という登録診断で、厳密な微分ゼロや全seed全個体死亡とは区別する。

**第1層だけを守っても全網は救えなかった**という十分性の否定はできる。しかしこの操作は平均だけを穏やかに固定せず、幅や次層への入力も変えた。「平均増加が第2層崩壊を何割媒介したか」「弱い介入なら救えるか」は未測定。負向きconf項に活動尺度を抑える役割もあった、という読みは事後の機構候補に留める。

## 5. ELUが示した中央値の限界（事後解析）

ELU/base seed1003は課題1末accuracy=1.0でも、第1層の登録V₁は0.005148（初期の約0.5%）。同時にunitごとの出力sd比の90パーセンタイルは36.16だった。中央値が小さくても、画像差を大きく残すunitが存在する。どのunitが正解への適合を因果的に支えたかまでは測っていない。

したがってV≤.1の初回到達を機能的死亡と呼ばない。M3は登録どおり2診断連続の到達順を記録し、未到達は打切り。ELUでは応答中央値の縮小後にも適合が進んだ。集団中央値だけを競争の勝敗時計にする説明は不十分である。

## 6. 今回までの説明

同じ平均入力でも、更新の上下収支と、沈降後に各層へ残る入力依存の応答が異なる。Leak/Snakeでは「大きく下がるが、上向きにも動き続ける」ことを実測した。負側への到達自体を敗北とみなせない。

応答の床・上位側のunit・下流の補償を含む全網の残存能力が必要で、今回の単層保護は下流に低応答化を生む軌道へ変わった。侵食ラチェットは単なる一方向の力としてではなく、状態依存の両方向更新と層間の変化として吟味すべきである。ただし今回から唯一の統一機構が確定したとは言わない。

2課題の初期過程を調べた結果であり、ELU/leaky .01が50課題で低下する最終機構や、500課題CondAの先生の5項式全体を検証したものではない。追加の腕・介入・長期走を自動で開始しない。

## 7. 成果物・検査・再現

- Repo: `Issan0511/lop_analysis`、実行commit `8856bab`、結果main commit **c39767f7b977aa26d79a6e3576e93c48b5c78161**。
- `specs/spec_erosion_race_0919.md`
- `src/erosion_race_0919.py`、`src/erosion_race_0919_checks.py`
- `analysis/erosion_race_0919/{launch,report,qc,interpretation}.py`
- `results/erosion_race_0919/{summary.md,verdict.json,checks.json,qc.json,interpretation.md,interpretation.json,figure.png,figure_layers.png,backup_manifest.json}`、9走のdiagnostics.csv/per_task.csv/provenance.json。
- 全6腕の同R=5親実装一致、観測on/off、CUDA graph/eager、CE/Adam分解、介入射影、RNG/SNA状態を独立検査し全pass。45本の完走後に入力・初期重み・stream一致、課題境界の特徴不変、C1–C4の独立再計算もpass。
- 生checkpoint・unit配列・launcherログ・pilotは `/home/issan/Projects/obsidian-research-data/erosion_race_0919/`。manifestでbytes/SHA256を照合。
- 本文数値の正本はsummary/verdict。§4–5は登録判定と分離したinterpretationの事後記述。M3や既定判定を書き換えていない。

[登録結果（repo・固定commit）](https://github.com/Issan0511/lop_analysis/blob/c39767f7b977aa26d79a6e3576e93c48b5c78161/results/erosion_race_0919/summary.md) / [層別の事後解析](https://github.com/Issan0511/lop_analysis/blob/c39767f7b977aa26d79a6e3576e93c48b5c78161/results/erosion_race_0919/interpretation.md)
