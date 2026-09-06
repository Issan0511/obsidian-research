---
name: obsidian-vault-mcp-identities
description: 「obsidian-research」= /home/issan/Projects/obsidian-research (Issa 側 main のローカルクローン)。MCP は 2 つあり 8f8c398b=Issa/main・fdad9d3d=先生/teacher。commit ツールの引数制約も。
metadata: 
  node_type: memory
  type: project
  originSessionId: 808a95ef-5351-40cc-876d-02344a4630e8
  modified: 2026-09-03T00:00:00.000Z
---

**まず場所**: 「obsidian-research」と言われたら **`/home/issan/Projects/obsidian-research`**（Issa 側 main の作業クローン）。ノートは `可塑性喪失/` 以下（`spec/`・`論点/`・`主張/`・`spec/実行済み/`）。**探し回らず直接 `cat` / `grep` / `sed` で読み書きしてよい**（MCP `8f8c398b-...` からでも同じものが見えるが、ローカルのほうが速い）。remote は `github.com:Issan0511/obsidian-research`。

proj_004（可塑性喪失）の vault には **Obsidian MCP サーバが 2 つ**つながっており、**別々の worktree・別々のブランチ**を見ている。書き込む前にどちらかを必ず確かめること。

- **`8f8c398b-...` = Issa 側**。`branch: main`、`actor: Issan`、peer は 先生/teacher。**編集・commit はこちら。**
- **`fdad9d3d-...` = 先生側**。`branch: teacher`、`actor: 先生`、`role: teacher`、peer は Issan/main。**読むだけ。** 先生の未マージノート（`v6分岐の裁定_0902` など）はこちら側にしか無いことがある。

判別は `obsidian_git_status`（`branch` と peer 名が出る）か `obsidian_research_context` の `collaboration.actor` が速い。

`obsidian_git_commit_push` の引数制約（エラーメッセージからしか分からない）:

- `author` は **スラッシュ・角括弧を含めない 1 行 80 字以内**。`Issan/Claude` は弾かれる。実際の慣習は **`Claude`**（ツール側が `[actor/author]:message` に組み立てる）
- `message` は **1 行 200 字以内**。複数行の本文は渡せないので、詳細は本文ノート側に書く
- `paths` を明示するので、**他セッションが同じ作業ツリーで編集中でも自分のファイルだけ commit できる**（proj_004 では実際に別チャットが並行して同じ vault を触っている）

同じことが repo 側にも言える: `~/Projects/claude/proj_004_drift` の作業ツリーは**複数セッションで共有**されている。`git add` は必ずパスを明示し、`git status --porcelain | grep -v '^??'` で自分の分だけが staged なのを確認してから commit する。関連: [[proj-004-drift-experiment]]

**ローカルクローン (2026-09-02 Issa 指示)**: Issa 側 vault は `~/Projects/obsidian-research` (branch `main`, remote `github.com:Issan0511/obsidian-research`) に checkout されており、**MCP より直接ファイル編集のほうが便利**。コミットは MCP の慣習に合わせて `[Issan/Claude]:[<run_id>]: <一行>` 形式で、**定期的に commit & push する**こと (作業ツリーは他セッションと共有なので `git add` はパス明示)。
