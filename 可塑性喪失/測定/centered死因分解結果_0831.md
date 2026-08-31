# centered 腕の死因分解結果（8/31・事後解析）

親: [[容量不足レジームの機構_0830]] / spec: [[centered死因分解_posthoc_spec_0831]] / 関連: [[吸収不等式の命題化_0824]]・[[中心主張v4.2草案_0830]]
状態: **決着（事後解析の登録・新規学習なし）** / 更新: 2026-08-31 / run id: `centered_death_posthoc_0831`

> **格の自己申告。** 本解析は事前登録ではない。E1–E6 に対応する数値を spec 起草前にチャット内で観察しており、判定閾値を凍結してから実装した「事後解析の登録」である。全数値は事後の格で運び、`mlp2_phase1_0829` の事前登録判定を上書きしない。

## 一行

**壁の位置は3腕で不変、5M の降下は境界窓が担い、centering は境界降下を弱めるが除去しない。centered 腕では EMA によりタスク内吸収不変性が破れる。**

## 判定

| endpoint | 判定 | 主な数値 |
|---|---|---|
| E1 | `WALL_INVARIANT` | onset β: `L1w100_A1` −2.262 [−2.281, −2.247] / `L2_A1` −2.236 [−2.255, −2.218] / `L2_none` −2.227 [−2.276, −2.204]。全3対比 CI が ±0.15 内 |
| E2（登録式） | 両 centered 腕 `MU_CHANNEL_ALIVE` | ρ_M = 0.632 [0.559, 0.740] / 0.719 [0.662, 0.805]。step 0 の EMA 初期化前の大きな M を含む |
| E2 感度（REPORT_ONLY） | 両腕 `BIAS_CHANNEL_DOMINANT` 相当 | step 10,000 起点で ρ_M = 0.0405 [0.0309, 0.0474] / 0.0453 [0.0363, 0.0590]。**登録判定を差し替えない** |
| E3 | `BOUNDARY_CARRIES_DESCENT` | `L1w100_A1`: Δβ_boundary = −4.297 [−4.590, −3.905]、Δβ_internal = +1.933 [+1.790, +2.190] |
| E4 | `CENTERING_REDUCES_BUT_NOT_REMOVES` | paired `L2_A1−L2_none`: Δβ_boundary 差 +2.442 [+1.824, +2.831]。raw bias 差 −0.170 [−0.262, −0.087] = `BIAS_DESCENT_WORSENED_BY_CENTERING` |
| E5 | `ABSORPTION_BROKEN_BY_EMA` | タスク内復活: `L1w100_A1` L1 = 25,723、`L2_A1` L1 = 28,094、`L2_none` L1 = 0。moving-input 対照の `L2_none` L2 = 9,570 |
| E6 | REPORT_ONLY | `L1w100_A1` 最終 dead の直近100タスク連続 dead 率 = 297/469 = 0.633 |

E5 件数は初期化遷移 step 0→1,000 を除く。除外件数は `verdict.csv` に保存した。

## Sanity

- S2–S6 は PASS（S5 は恒真注意の存在確認）
- **S1 は登録上の global 判定では FAIL**。違反は layer 2 のみで、登録した `β≤−√5 ⇒ p̂=0` が layer 2 の100次元・非 hypercube 入力には適用できないため。E1–E4 が使う layer 1 は全腕・全 seed で違反 0。layer 2 は E5 の moving-input 対照に限って使う
- 除外ユニット 0 / 7,000。出力は再実行で byte 一致

## 解釈

1. **「µ は壁の位置ではなく到達を支配する」**は E1 の事後結果として支持される。外挿範囲は condA・w100・T=10⁴・batch=1・lr=0.01・10 seed・5M
2. **「降下は全部 B が担う」**を登録判定としては書かない。字義どおりの E2 は step 0 の初期過渡を拾って `MU_CHANNEL_ALIVE`。step 10,000 起点の B 優勢は REPORT_ONLY の感度分析
3. 境界降下の内側で EMA 遅れと切替ショックを分離する問いは残る。E3 が発火したため [[境界窓細粒度記録_spec_0831]] と [[オラクル中心化_spec_0831]] の実行条件は満たされたが、**自動実行はしない**
4. centered 腕の `strict_dead` は吸収状態ではない。水準を引くときは E6 の連続死率を併記する

## 成果物

- repo: `results/centered_death_posthoc_0831/`
- spec commit: `849f9cb`
- implementation commit: `a7f8d2d`
- results commit: `d38a391`
- 実装: `src/centered_death_posthoc.py`
- 出力: `summary.md` / `verdict.csv` / `unit_decomposition.csv` / `provenance.json`
