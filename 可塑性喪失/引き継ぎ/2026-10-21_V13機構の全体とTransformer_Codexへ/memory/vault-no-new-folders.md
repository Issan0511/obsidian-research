---
name: vault-no-new-folders
description: obsidian-research にフォルダを勝手に作らない。運用ルール §1 のフォルダ表に無い置き場が要るなら作る前に Issa に聞く（2026-09-29・Issa が怒った）
metadata:
  node_type: memory
  type: feedback
  originSessionId: f7ec285b-ebc0-4371-8bbe-534e154dfc05
  modified: 2026-09-29T10:10:54.287Z
---

obsidian-research（`/home/issan/Projects/obsidian-research`）に新しいフォルダを作らない。ノートは `可塑性喪失/運用ルール.md` §1 のフォルダ表にある場所へ置く。表に無い置き場が要ると思ったら、作る前に Issa に聞く。

**Why:** 2026-09-07 に Claude が `理論/` を、09-20 に Codex が `実験/` を断りなく作った。Issa が放置しているうちに他のセッションがそこを使い始め、`論点/V8/`・`測定/` と置き場が二重になった。Issa「勝手に理論フォルダ作られててそれを放置してたら Claude が使い始めたんですよ怒」。0929 に両方とも廃止と裁定された。

**How to apply:**
- 走の結果ノートと事後解析は `測定/`。沈下・駆動の理論と検証は `論点/V8/駆動源問題/`。W 増大・実効変位の理論と先生の稿との照合は `論点/V8/W増大メカニズム/`。今の原稿作業に使うものだけ `論文作成/` 直下。
- 「このノートの親がここにあるから」で置き場を決めない。0922〜25 に W 増大のノートが親（接続面）のある `論文作成/` に 12 本たまったのが、Issa の言う「置き場が適当」の中身だった。
- リンクは `[[名前]]` 形式で書く。`[[可塑性喪失/フォルダ/名前]]` はファイルを移すと切れる。
- Codex や subagent に vault へ書かせるときも、プロンプトに置き場所を明示する。

関連: [[vault-cleanup-0929]] [[vault-parallel-session-collision]] [[obsidian-vault-mcp-identities]]
