---
name: session-handoff-system
description: 飽和したセッションを別マシン／新セッションへ引き継ぐ仕組み（skill の場所・vault の引き継ぎフォルダ・ギガファイル便の manifest・最初の実走 9/6）
metadata:
  type: reference
---

**skill**: lop_analysis repo の `.claude/skills/session-handoff/`（SKILL.md・`scripts/collect_state.sh`・`scripts/pack_upload.py`・`scripts/receive.py`・`assets/handoff_template.md`・`assets/bootstrap_prompt.md`）。repo にあるので lab でも `git pull` で使える。
**vault**: `可塑性喪失/引き継ぎ/<日付>_<題>_<宛先>/` に ノート＋`memory/`（複製）＋`manifest.json`（sha256・URL・削除キー）。[[現在地]] には 1 行リンクだけ。[[運用ルール]] のフォルダ表に `引き継ぎ/` の行あり（9/6 新設）。
**最初の実走（2026-09-06）**: `引き継ぎ/2026-09-06_前活性の力_lab/セッション引き継ぎ_0906_前活性の力.md`。7 項目 12.8 GB を 4 分で上げた（6.7 GB が 100 s）。ギガファイルは 100 日で消える。

**Why:** チャットは 4 層（正本・セッション固有の状態・記憶・生データ）でできていて、どれか 1 層だけ渡しても続きは書けない。Issa は「obsidian のリンク＋ npz はギガファイル便」で引き継ぎたいと指定した（9/6）。
**How to apply:** 「引き継ぎ」「乗り換え」「飽和」と言われたら skill を使う。送り側は状態収集 → push → pack_upload（小さい束から・1 ファイル 1 プロセス）→ ノート → 現在地に 1 行 → bootstrap プロンプト。受け側は receive.py で sha256 照合して展開し、記憶を移植して受領確認を書く。関連: [[machines-and-network]] [[vault-parallel-session-collision]] [[obsidian-vault-mcp-identities]]
