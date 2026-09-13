# 初期出力を揃えてELUの応答を戻す spec 0913

状態: 事前登録済み・実装検証中 / 2026-09-13 / 起案: Codex（Issa指示）
親: [[自然に沈んだ個体の追跡と救済_結果_0913]] / [[現在地]]

## 問い
浅く戻した瞬間に特徴・予測が変わる効果と、その後に重み変化へ反応して学べる効果を分ける。初期出力を保つ固定補正を入れ、自然に沈んだELU個体の応答を回復する。これは人工的な応答介入の効果であり、自然な沈降の媒介割合を確定する実験ではない。

## 登録と担当
正式spec: [spec_elu_response_anchor_0913.md](https://github.com/Issan0511/lop_analysis/blob/c4965d09c16534ceec23e074c11171404f8840ee/specs/spec_elu_response_anchor_0913.md)
登録commit c4965d09c16534ceec23e074c11171404f8840ee（push確認済み）。
worktree /home/issan/Projects/claude/elu_response_anchor_0913
branch codex/elu-response-anchor-0913
設計・解釈は主担当、実装補助・集計・独立監査はユーザー指定GPT-5.6 Sol。

## 固定する条件
RL・task20終了・第2層・元のtarget20とdeltaをそのまま使う。3seed、同じMNIST1200枚、ELU1、同じAdam履歴、6000更新/新課題。task21を主比較、task22–25を持続性の副次とする。
6条件は A=元の特徴/元の応答、B=元の特徴/浅い応答、C=浅い特徴/元の応答、D=浅い特徴/浅い応答、および第1層W1/b1を固定したAF/BF。計18継続走。対象W2/b2と読み出しW3は学習する。

## 関数
対象だけ a_FK(theta,x)=phi(z_theta(x)+K delta)-phi(z0(x)+K delta)+phi(z0(x)+F delta)。z0は全上流を凍結した元ネットワーク。同じ生入力ごとに補正をキャッシュし、将来ラベルを使わず固定する。開始時は同じFのK条件で特徴・logitが同じ、応答の真の微分はphi'(z_theta+K delta)。AとDはそれぞれ元のELUと通常の一度の持上げに戻る。

## 判定
主指標はtask21の全6000更新における更新前ミニバッチCEの平均。各ステップを直接保存し、集計はfloat64。主差 A−B が全3seedで>.01ならDIRECTIONAL_RESPONSE_SUPPORT、全て<−.01ならDIRECTIONAL_RESPONSE_HARM、それ以外INCONCLUSIVE。方向性のパイロットであり母集団有意差や同等性を意味しない。seed別・平均・t95%区間を併記。
副次はC−D、両Fの応答差の差、AF−BF、特徴差、通常持上げ差、到達精度・CE、密な全例プローブ面積、5課題の持続性。古い6点面積の主判定は変えない。

## 検証と限定
初期W/bias/Adamの同一性、F内の初期特徴・logit、補正の固定性、真の微分とautograd/有限差分、CUDA graphと逐次計算、実凍結、全ステップの損失ログ、元RNGとの一致を実介入前に検証。コードとQAをcommit/pushしてから走る。
ゲート、現在勾配、Adam履歴、実際のW/bias更新、入力別前活性移動を分けて保存。固定deltaでも再沈降し得る。開始時のW一致は学習中のW一致を意味しない。初期特徴の効果も沈降によるLoPと両立する。

## 保存
results/elu_response_anchor_0913/ に結果・provenance・監査。pt/npzはGit対象外とし /home/issan/Projects/obsidian-research-data/elu_response_anchor_0913/files/ にSHA256照合済み保存を行う。
