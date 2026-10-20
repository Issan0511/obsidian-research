---
name: vault-parallel-session-collision
description: obsidian-research は別セッションが同時に同じノートを書き直す。編集前に git log -- <file> を見て、追加は別ノート＋1行リンクで (2026-09-05 に §5b が上書きで消えた)
metadata:
  type: feedback
---

vault の結果ノートを編集する前に `git -C ~/Projects/obsidian-research log --oneline -5 -- <path>` と `git status` を見る。**別セッションが直近で commit していたら本文を書き換えず、自分の追加は別ノートに書いて本体へ 1 行だけ append する。** spec は `spec/実行済み/` へ移される（rename）ことがあるので `find` で探す。

**Why:** 2026-09-05、PermutedMNIST結果_0905 に §5b（診断 5 本）を追記した数時間後、別セッションが同ファイルを 3 commit で全面書き直し（`pmnist_lopcmp_0905` の追加・§10.5 の誤り訂正を含む）、私の §5b は消えた。`str.replace` の anchor も消えて `substring not found` で気づいた。相手の作業は正当で、こちらが上書きし返すのは最悪。→ [[PermutedMNIST_追加診断_0905]] を別ノートとして作った。

**How to apply:** (1) 編集前に git log、(2) 追加は別ノート＋リンク、(3) 相手の訂正（今回: Lillo & Cheney は Deep Fourier を評価済み、私の「周期活性化なし」は誤り）は受け入れて自分のノートに撤回を書く。関連: [[obsidian-vault-mcp-identities]] [[pmnist-0905-lessons]]
