# CIFAR層別成長制限 S5 — 両層capで救済、bias固定の上乗せなし

2026-09-20 / 実装・測定・記録: Codex / 状態: 本走と登録判定完了。親: [[背骨CIFAR_S4S5_A3-A6_spec起案プロンプト_0920]]、[[中心主張v11作業リスト_0920]]。前段: [[CIFAR応答場移植_S4_結果_0920]]、[[CIFARの崩壊層と輸送帳簿_A6_結果_0920]]。

**登録主判定はRESCUED。** 主窓task31–50のonlineはref 10.09%に対しcap12 85.98%。全10seedで床を上回り、機能・第2層局所応答の両主対応差が正。初期悪影響なし。ただし初回98.27%より12.30ポイント低く、完全保持ではない。

## 正本と設計

run `cap_cifar_ee_0920`。spec `f524cac`、採用 `5705359`、本走実装 `318c72276690479bd816cf352874b64bba9d44a6`、結果 `c017fe01cc7c47eb750941100952d46730754e78`。

- [登録spec](https://github.com/Issan0511/lop_analysis/blob/5705359/specs/spec_cap_cifar_ee_0920.md)
- [結果要約](https://github.com/Issan0511/lop_analysis/blob/c017fe01cc7c47eb750941100952d46730754e78/results/cap_cifar_ee_0920/summary.md)
- [解釈・帳簿・検査・限界](https://github.com/Issan0511/lop_analysis/blob/c017fe01cc7c47eb750941100952d46730754e78/results/cap_cifar_ee_0920/interpretation.md)
- [図](https://github.com/Issan0511/lop_analysis/blob/c017fe01cc7c47eb750941100952d46730754e78/results/cap_cifar_ee_0920/summary.png)

両specの推奨設計・予測内容をIssaがS4の新規結果より前に採用。S5自身の新規R10・task1終端から分岐。固定CIFAR1200枚、ELU/std、3072–100–100–10、seed0–9、50task×30,000更新、主窓31–50。各行のt1ノルムを上限にAdam後に射影。bfixはb1/b2だけをt1値へ書き戻し、生勾配とmomentは通常更新。半径・窓・腕の事後変更なし。

## 主窓の結果

| 腕          | 登録判定              | 床seed | online |        G2 |
| ---------- | ----------------- | ----: | -----: | --------: |
| ref        | REFERENCE_FLOORED | 10/10 | 10.09% | 0.0000144 |
| cap1       | SPLIT（副）          |  4/10 | 11.91% |  0.000930 |
| cap2       | SPLIT（副）          |  1/10 | 25.10% |  0.020976 |
| cap12      | RESCUED（主）        |  0/10 | 85.98% |  0.132380 |
| cap12_bfix | RESCUED（副）        |  0/10 | 78.85% |  0.093538 |

共通初回online 0.98273354、G2 0.35270345。G2はnative F.eluの局所微分を画像・unit平均した量。床は各seedのラベル構成から作る登録の操作的帯。

cap12−ref: online **+75.8889ポイント、97.5% CI [75.1465,76.6312]**、G2 **+0.132366、97.5% CI [0.126901,0.137831]**。2主量Bonferroni補正。refは10/10床、G2前後差95%区間上端−0.341838で適用条件B成立。全介入の初期悪影響フラグなし（task2で登録中点未満0/10）。

単独腕にも効果はあるが、cap1 11.91%、cap2 25.10%に留まる。2×2交互作用online +0.590554、95% CI [0.529443,0.651666]（副）。T_halfはref全seed t3、cap1 t4–5、cap2 t4–6。単独腕の遅延符号10/10、両側p=0.001953125。両層腕は全seed t50で右打切り。

**bias固定を加えるとcap12よりonlineが記述的に7.123ポイント低い。** 直接差を新たな主検定にはしていない。自由biasのcap12でもb2平均はt1→t50で−0.979094動きながら救済。固定すればより良いとは言えない。b1/b2を同時に固定したため個別効果は未分離。

## 帳簿（副）

毎タスクの4項分解を足したt1→t50総和（unit→seed平均）は、ref: 自己−101.636、上流−752.325、交差−112.516、bias−0.286、正味−966.764。cap12: 自己−1.050、上流+19.862、交差−25.849、bias−0.979、正味−8.016。cap12のt30→t50正味平均は+0.526。種別の総和・1task率・中央値・誤差・定義可能な符号付き寄与率を全窓で正本CSVに残した。

平均||mu2||は共通t1 52.568から、t50でref 1157.213、cap1 207.749、cap2 2668.004、cap12 40.195、cap12_bfix 62.230。この走で両層capは入力平均の増大と大きな負側輸送を抑えた。帳簿の項別値は恒等式であり、独立の因果効果ではない。

## 検査・予測・限界

13必須検査・43変異検査合格。無改変宿主とR10・2task×400epochで全状態・乱数・online bit一致。本走全2,500行、全ラベル/順列/接頭部の一致を検査。対象60 seed×層すべてでcap発火、登録norm上界違反0、bfix固定後bit誤り0。台帳閉包も合格。S5 refとS4自然行はt1–11×10seedのonlineが一致。完了後、別実装のt分位積分・ラベル再生成で判定を照合し全一致（CI最大差1.10e−14）。**独立監査なし**。

Codexの登録予測は適用条件を含む8項目中7的中、1不的中、binary Brier平均0.1165625。外れはcap1 COLLAPSED（p=.65、実測SPLIT）。cap12救済、cap2 SPLIT/COLLAPSED、bfix救済、cap1遅延、cap12 b2負変化、初期悪影響なしは的中。Issaは予測内容に同意し、数値確率はCodexのものとして保持。

S4 RESPONSE_BOTH_WAYS（復元+46.74ポイント・沈降−67.86ポイント）とS5 RESCUEDを同じCIFAR箱に加えた。ただしS4は人工的固定場・1task、S5は特定半径・50task。capが応答だけを介して救ったという自然な全媒介、未使用seedや別箱への一般化、永久的救済は未検証。A6のR20とS4/S5のR10を同一軌道として扱わない。

本走17:08:59–19:52:51 JST、9,832.37秒。GPU1プロセス。途中は生存・完全性だけを確認し、全腕終了後に成績を開いた。待機・状態確認はIssaの指示により10分間隔へ延長した。


## 退避・main統合（2026-09-20）

main `6bf41b676436b67ef4b855830c98ec3052670fc8` へpush済み。git外の884ファイル・1,432,598,330 bytes（raw配列・checkpoint・全検査attempt・ログ）を `/home/issan/Projects/obsidian-research-data/cap_cifar_ee_0920/` へ退避し、全ファイルのサイズとSHA256を照合した。[backup_manifest.json](https://github.com/Issan0511/lop_analysis/blob/6bf41b676436b67ef4b855830c98ec3052670fc8/results/cap_cifar_ee_0920/backup_manifest.json) に元パス・退避先・bytes・SHA256を記録。登録ソースは本走commitのままで、raw参照はmanifestから解決する。
