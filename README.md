# Research Vault

研究ノート専用の Obsidian Vault。

- アプリ開発用の `operatingsis` リポジトリとは履歴とremoteを分離する。
- MCPのファイル操作はこのVault内だけに限定する。
- Git操作は対象ファイルを明示したcommitと通常pushだけを許可し、force pushは行わない。
- `.git/` と `.obsidian/` はMCPから操作しない。

## 現在のテーマ

- `可塑性喪失/`

## MCPでの変更追跡

MCPからcommitするときは`author`と`message`を渡し、commit subjectを`[author]:message`に統一する。
行の最終変更者は`obsidian_git_blame`で確認する。

## MCPでの安全な編集

- `obsidian_search` → `obsidian_outline` / 部分`obsidian_read` → `obsidian_str_replace`の順で、必要な箇所だけ確認・変更する。
- 全文更新が必要な場合は`obsidian_read`の`sha256`を`obsidian_write(expected_sha256=...)`へ渡し、競合を検出する。
- 履歴確認には`obsidian_git_log(name_only=True)`、`obsidian_git_show`、`obsidian_git_diff`を使う。
- コミット前に`obsidian_git_commit_push(dry_run=True)`で対象ファイルとsubjectを確認する。
