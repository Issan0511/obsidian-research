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
