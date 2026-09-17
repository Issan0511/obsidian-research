# max-pool を avg-pool に替えて谷越えを切り分ける：結果 0917

親: [[適応αSwishをSnakeとバトルさせる_結果_0917]]（同日・同じ CNN 箱）/ [[現在地]]
事前登録: repo `specs/spec_avgpool_cnn_0917.md`（本走の前・Claude Opus 5 起草、Issa の予測欄は空）
run id: `avgpool_cnn_0917` / 状態: **実行済み・main 統合済み（`cf8f9af`）・worktree 片付け済み。独立監査なし**
起案の出所: Issa「max-pool がわるいのか」「MLP と似てる挙動の CNN どれだと思う？」→ Claude が avg-pool 版を提案し、Issa「おすすめの段取りで」

> **転記の格**: 数値は走自身の出力 `results/avgpool_cnn_0917/summary.md` の表と `verdict.json` の `labels` から転記した。独立の再計算はしていない。

## 0. 何を測ったか

RL-CIFAR × CNN（Kumar の CNN）で、**max-pool 2 か所を avg-pool に替える**と、適応 α Snake（`SNA`、c=0.6）の
**(A)** conv2 のチャネルがゲートの谷（$2\alpha\bar z=-\pi/2$）を越えるのが止まるか、**(B)** 腕の順位が MLP の向き（SNA > 固定 α）になるか。
宿主 `rlcifar_cnn_0908` を無改変で import し、`forward_cnn` だけを pool 関数を差し替えた同型の関数に置き換えた（S-reuse で pool=max のとき参照行を 10 桁再現）。腕は `SNA_avg`・`SN3_avg`（各 10 seed）、参照は `rlcifar_cnn_0908` と `swish_battle_0917` の既存走。

## 1. 登録判定（`verdict.json` の `labels`）

| 判定 | ラベル | 内容 |
|---|---|---|
| A（谷越え） | **`NEAR_SIDE`** | t50 の conv2 で谷より深いチャネルの割合 0.063（参照の max-pool `SNA` は 0.656） |
| B（順位） | **`CNN_ORDER`** | `SNA_avg` − `SN3_avg` = −0.0032（0/10 seed・p 0.002）。avg-pool にしても固定 α が上 |
| C_SNA | `TIE` | `SNA_avg` − `SNA` = +0.0019（6/10・p 0.75） |
| C_SN3 | `AVG_WORSE` | `SN3_avg` − `SN3` = −0.0129 |
| D（低下） | `DROP_KEPT` | 低下 0.0211（参照 `SNA` は 0.0284）。半減には届かない |

## 2. 読み

- **谷越えは max-pool が起こしている**（0.66 → 0.06）。max-pool は勝った位置にだけ勾配を流し、それ自体が折れ線の非線形でもある。
- **だが SNA の CNN での劣化の主因ではない**。谷越えがほぼ消えても低下は 0.0284 → 0.0211（4 分の 1 ほどしか減らない）、窓は TIE、順位も CNN のまま。
- fc の座席は avg でも谷の手前（f1 −1.20・f2 −1.48）で、MLP のユニットと同じ位置にいる。
- したがって「CNN で SNA が負ける」ことの残りは、pool ではなく **c の値**（[[適応αSwishをSnakeとバトルさせる_結果_0917]] の CNN `SNAc3` = `C_VALUE`）と fc 側の谷に残る。

## 3. 予測（Claude、本走の前）

7 項目中 4 つ的中（`A == NEAR_SIDE` 0.55・`C_SN3 == AVG_WORSE` 0.45・memo 0.75・fc の座席 0.70）。
外したのは `B == MLP_ORDER`（0.40）・`D == DROP_HALVED`（0.50）・条件つき「A が NEAR_SIDE なら C_SNA は AVG_BETTER」（0.65）。
つまり「max-pool が主因」という当方の読みは、谷越えの部分は当たり、劣化の説明としては外れた。

## 4. 限界

- 1 箱・10 seed・c=0.6 の SNA と c=3 の固定 α だけ。avg-pool 版の c ダイヤルは振っていない。
- `mob_pool` 列は avg 腕では勾配に効くゲートではない（比較のために残してある）。
- 独立監査なし。生データ（hist の npz）は `obsidian-research-data/avgpool_cnn_0917/` に退避（`backup_manifest.json`）。
