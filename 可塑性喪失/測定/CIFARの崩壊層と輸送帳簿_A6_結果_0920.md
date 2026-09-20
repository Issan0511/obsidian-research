# CIFARの崩壊層と輸送帳簿_A6_結果_0920

親: [[中心主張v11作業リスト_0920]] A6 / 起案: [[背骨CIFAR_S4S5_A3-A6_spec起案プロンプト_0920]] / 実施: Codex / 2026-09-20 / 状態: **実装・解析完了、mainへ統合済み**。

## 結論

ELU・GELU・SiLUでは、rawは第1層、stdは第2層が先に低応答化した（各条件10/10 seed）。S4のELU/std・第2層を移植先候補にする根拠になる。ELU/stdの沈下を主窓で「上流が単独で運ぶ」とした予測は外れ、登録判定は **MIXED（10/10）**。初期は重みと上流平均が同時に変わる交差項が大きく、後半は上流項が大きい。

これは既知軌道に解析規則を事前固定した再解析。元の結果に盲検の登録でも独立標本でもない。独立監査は未実施。

## 登録と実装

- spec初回登録 `f034e9a`、Issaの全予測採用・実装GO `4aec348`（2026-09-20 14:04 JST）。
- 再生実装 `45b12f2`、初回判定 `e3acd44`、結果 `ec1a0dd`、退避manifestを含む完了 `d7e09b9`。
- 元バトルの6腕 × raw/std × 10 seed × t00–t50 = 6,120模型状態。学習更新なし。元のCUDA・R=20・slot順で再生し、訓練の局所微分は元phiへのautogradで測った。
- 主量Qは全画像×unitで `abs(g_train) < 1e-6` の割合。初期低応答を区別し、t1–t10でQが厳密に半数を超える先行層をR1とする。主窓はt00→その到達時点T*（上限t10）。
- 第2層の帳簿は、自己 `ΔW μ_old`、上流 `W_old Δμ`、交差 `ΔW Δμ`、bias `Δb` の4項。時間和→unit算術平均→seed内の比の順に集約。比は符号つきで、負値・100%超を許す。
- 全再生後、初回判定を読む前の合成検査で「ちょうど半数」の浮動小数平均誤差を修正した。整数pair数を合計してから割り、登録の厳密な閾値を実装した。閾値・窓・多数決は変更していない。

## 主判定

| 腕       | raw R1                        | std R1                        | raw R2                  | std R2                  |
| ------- | ----------------------------- | ----------------------------- | ----------------------- | ----------------------- |
| ELU     | L1_FIRST 10/10                | L2_FIRST 10/10                | MIXED 10/10             | MIXED 10/10             |
| GELU    | L1_FIRST 10/10                | L2_FIRST 10/10                | SPLIT                   | MIXED 10/10             |
| SiLU    | L1_FIRST 10/10                | L2_FIRST 10/10                | SPLIT                   | MIXED 10/10             |
| ReLU    | INITIAL_LOW_SIMULTANEOUS 9/10 | INITIAL_LOW_SIMULTANEOUS 8/10 | INITIAL_LOW_REPORT_ONLY | INITIAL_LOW_REPORT_ONLY |
| KKT1・LR | REPORT_ONLY                   | REPORT_ONLY                   | REPORT_ONLY             | REPORT_ONLY             |

ReLUの残りはSIMULTANEOUS（raw 1/10、std 2/10）。初期から負側微分が0のため、このQ>0.5規則では新たな故障層の先後を決められない。GELU/rawのR2はMIXED 4・NO_NET_SINK 5・SELF_CARRIES 1、SiLU/rawはMIXED 5・NO_NET_SINK 1・SELF_CARRIES 4。分母が定義できないseedを除いて多数決の分母を減らすことはしていない。

ELU/stdの主窓T*中央値はt2。seed内比の中央値は上流16.5%、自己23.0%、交差60.0%、bias 0.024%。中央値どうしの和は閉包の検査量ではない。上流項のうちμの伸びが占める割合の中央値は90.7%。伸びが上流項の半分以上、bias絶対寄与が沈下の5%未満という予測は、それぞれ10/10で成立した。

GELU/stdも上流単独過半という予測は不支持（上流中央値2.47%、交差96.14%）。層の予測はELU・GELU・SiLUで的中、ReLUは登録理由ラベルが予測と異なった。

## 登録補助窓（REPORT_ONLY）

ELU/std・第2層の上流寄与中央値:

| 窓       |   上流比 |
| ------- | ----: |
| t00→t10 | 72.9% |
| t01→t10 | 73.4% |
| t10→t50 | 99.4% |

初期の形成と後半の輸送は比率が違う。補助窓で主判定MIXEDを置換しない。交差項は端点間にWとμの両方が動いた分で、単一の原因名ではない。帳簿の比は因果的媒介率ではない。

またQの初回超過とonline<0.5は一致しない（ELU/stdの中央値はそれぞれt2、t3）。R1は先行低応答層であり、機能的LoPそのものの発生時点ではない。

## S4・S5へ渡すこと

- S4: ELU/std・第2層候補を支持。起案文の「手書きphi'が訓練の差し込み口」という前提は訂正が必要。元エンジンの訓練はautogradで、dphiは診断用。
- S5: A6だけでcap1かcap2の一方に絞る因果根拠は得られない。初期の大きい交差項と窓依存を踏まえ、介入の比較は別specで登録する。
- S4/S5の実装・走はこのA6には含めていない。

## 検証・成果物

306束ね状態の再生照合（初期6・隣接区間300）は全件PASS。保存z(float16)・hist平均・登録CSV列と照合し、4項閉包の最大誤差/上界は0.186。合成変異25/25、実状態の入力・seed・時点・V取り違え6/6を検出。再開による55配列のbit一致も確認した。同一実装者による検査である。

- [結果表・図・解釈](https://github.com/Issan0511/lop_analysis/blob/d7e09b9/results/cifar_ledger_0920/summary.md)
- [specと完了追記](https://github.com/Issan0511/lop_analysis/blob/d7e09b9/specs/spec_cifar_ledger_0920.md)
- [実行方法・修正履歴](https://github.com/Issan0511/lop_analysis/blob/d7e09b9/analysis/cifar_ledger_0920/EXECUTION.md)
- [最終検証](https://github.com/Issan0511/lop_analysis/blob/d7e09b9/results/cifar_ledger_0920/verification.json)
- CSV: per_seed 120行、per_task 12,240行、windows 1,120行。
- git外出力615ファイル・488,510,431 bytesを `/home/issan/Projects/obsidian-research-data/cifar_ledger_0920/` へ退避。source・backup・bytes・SHA-256を[manifest](https://github.com/Issan0511/lop_analysis/blob/d7e09b9/results/cifar_ledger_0920/backup_manifest.json)に保存し全件照合。元バトルの入力は動かしていない。
