# 先生の Claude Code への依頼: chargpt_detlabel_1023 を回す

2026-10-23 / Issa から。下の「---」より後を、そのまま Claude Code に渡してください。研究データの URL は別にお送りします。

---

あなたへの依頼は、事前登録の spec `chargpt_detlabel_1023` を、このマシンで最後まで回すことです。実装・検査・本走・解析・判定・報告まで行ってください。依頼主は Issa（研究の主担当）で、実行の場所は Kubo 先生のマシンです。

## 1 何を確かめる走か

研究は、継続学習で学び直しの力が失われる仕組み（可塑性喪失）です。対象の一つは、2 ブロックの文字 GPT（pre-LN、ReLU の FFN、LN は γ だけ）を、課題ごとに違う乱数の 2 次マルコフ言語（箱 M）で 100 課題続けて学ばせる設定です。この設定では、読み出しの一つ手前の FFN（L0）の重みが課題の中で伸びて固まり、unit が死に、後の課題の学び直しが遅れます。

箱 M のラベルは確率的です（次の記号は毎回、遷移の分布からサンプルされる）。そのため、課題を当てはめた後も誤差が残り、更新が止まりません。問いは、L0 の成長・死・喪失を駆動しているのが、このラベル雑音かどうかです。

spec は次の 3 つの腕を、既存の対照 A2（α = 0.01）と比べます。

| 腕 | 中身 | 役割 |
|---|---|---|
| A4 | 遷移の分布を作る Dirichlet の濃度 α を 1e−4 に下げる（ラベルがほぼ決定的） | 主 |
| A3 | α = 1e−3 | 記録 |
| S2 | α = 0.01 のまま、損失の目標をサンプルでなく真の条件付き分布にする（ラベル雑音の項だけを勾配から除く） | 判定する腕（下の §3） |

詳しい問い・既知・予測・判定・検査は spec にあります。spec が正本です。この依頼文と spec が食い違ったら、§3 の決定を除いて spec に従い、食い違いを報告に書いてください。

## 2 材料の場所

- repo: https://github.com/Issan0511/lop_analysis （公開）
- **spec**: ブランチ `claude/chargpt_detlabel_1023`（HEAD 9f561b7b）の `specs/spec_chargpt_detlabel_1023.md`。最初に全文を読んでください。登録前の計算（`analysis/chargpt_detlabel_1023/prereg/`・`results/chargpt_detlabel_1023/prereg/`）も同じブランチにあります。
- **学習コードと対照 A2 の記録**: ブランチ `claude/chargpt_cl_1019`（HEAD 033679e0）
  - `src/chargpt_cl_1019.py`（blob cc524f85）・`src/chargpt_cl_1019_kune.py`（blob 272e7554）・`src/chargpt_cl_1019_m2_seeds.sh`
  - `analysis/chargpt_cl_1019_quicklook/three_phase.py`・`judge_m2.py`
  - `results/chargpt_cl_1019/M2/C3/seed0〜9/`（A2 の per_task.csv・online.npz・unit_stats.npz・provenance.json など。git に入っている）
  - 親 spec `specs/spec_chargpt_cl_1019.md`（追補 6・7）
- **J6 の解析コードと参照値**: main の `analysis/chargpt_loadsign_1023/`（commit 6aa4c490・3baa567f・af1eadff・099530e9）、`analysis/chargpt_seed10_1022/load10.py`、`results/chargpt_loadsign_1023/`、`specs/spec_chargpt_loadsign_1023.md`・`specs/spec_chargpt_seed10_1022.md`
- **A2 の checkpoint**（git に無い。A2 の再生と S-J6 の照合に使う）: 研究データのサーバ（URL は Issa から別に届く。`https://research-data.issan.dev/<秘密の文字列>/`）の `chargpt_seed10_1022/transfer/` にあります。
  - `chargpt_seed10_1022_bundle.tar`（3.3 GB、1,459 ファイル。tar の sha256 は 5729ec0279f25d884cfec0aef8c4234d2f9788d57208fed99a5c7eff4ad23e61）
  - `bundle_manifest.json`（ファイルごとの path・bytes・sha256）
  - tar の中の path は `results/chargpt_cl_1019/M2/C3/seed<k>/ckpts/...` です。`claude/chargpt_cl_1019` の checkout の直下に展開すると、spec が読む場所に入ります。展開後に manifest の sha256 で全件を照合してください。
  - 落とし方: `curl -C - -O "<URL>chargpt_seed10_1022/transfer/chargpt_seed10_1022_bundle.tar"`（切れても `-C -` で続きから再開できる）
  - URL は他へ書き写さないでください（repo・ログ・報告に URL を残さない）。

## 3 Issa の決定（1023 夜。spec の「判断待ち」への答え）

1. **腕**: A4・A3・S2 の 3 つを回す。S2 には §7 の判定（J1〜J6）を A4 と同じ規則で S2 と A2 の対に当て、A4 と並べて報告する。A3 は spec どおり記録。
2. **J4 の主**: net5k（各課題の後半 5,000 更新の変位、spec §6.3 (r1)・§7.4）。A2 の値は、保存 checkpoint から 290 課題を再生して出す（spec §6.4）。
3. **A2 は回し直さない。** A4・A3・S2 の対の相手は、white-san（RTX 5060 Ti）で回した既存の A2 です。
4. **予測**: spec §3 の Issa の欄は空欄です。Issa から先生経由で届いていれば、登録の commit に書いてください。届いていなければ「空欄のまま登録」と書いて進めてください。

### 台が white-san と違うとき（GPU が RTX 5060 Ti でない、または torch・CUDA の版が違う）

A2 は white-san の RTX 5060 Ti（torch 2.13.0+cu130、CUDA 13.0、Python 3.12.3、numpy 2.5.1）で回しています。台が違うと、同じ seed・同じデータ列でも GPU の数値の丸めで軌道がビット一致しません。決定 3 のとおり、台の違いは受け入れて進めます。そのとき spec の検査を次のように読み替え、読み替えたことを登録の commit と報告に書いてください。

- **S-stream**（CPU の乱数で作る rule_sha・data_sha・probe_sha・init_sha）は台によらないので、spec どおり A2 と一致しなければ止める。
- **S-code** は spec どおり（blob が一致しなければ止める）。
- **S-recorder**: 「A2 とビット一致」の代わりに、(a) この台で記録器ありと記録器なしの走（α = 0.01・seed 0・課題 1〜2）がビット一致すること、(b) 同じ走と A2 の seed 0 の `online.npz` の差（更新ごとの最大差・平均差）を記録すること。止める条件は (a) だけ。
- **S-replay**（A2 の再生）: ビット一致しなくても止めずに 290 課題を回す。各課題で、A2 の `online.npz` との差と、終わりの状態と `task<t>.pt` の差（重みの相対差の最大）を記録する。この値は spec §9 の言い方に従い「元の軌道の値」とは呼ばず、「この台での再生」と呼ぶ。台が white-san と同じ RTX 5060 Ti で版も同じなら、spec どおりビット一致を要求し、外れたら止めて報告する。
- 記録として、J4 の量 net100（更新 100 → 10,000）も A4・A3・S2・A2 の再生で出し、spec §7.4 の A2 の参照値（L0 で 1.66 [1.37, 1.78]、保存状態から出したもので台によらない）と並べる。主の判定は net5k のまま。

## 4 手順

1. **環境**: `nvidia-smi`・CUDA・空きディスク（checkpoint だけで約 9.4 GB、tar と展開で約 7 GB）・CPU のコア数・メモリを確かめる。Python 3.12 の venv に、できれば A2 と同じ torch 2.13.0+cu130 と numpy 2.5.1 を入れる。入らなければ入った版を記録する。
2. **取得**: repo を clone し、`claude/chargpt_detlabel_1023` を checkout する。`claude/chargpt_cl_1019` は別の作業ツリー（`git worktree add`）に読むだけで置き、そこに A2 の tar を展開して照合する。
3. **読む**: spec の全文、親 spec の追補 6・7、loadsign の spec の §2・§7。
4. **登録**: §3 の決定、台と版、S2 の役割、Issa の予測（あれば）を spec に書き、状態を「登録」にして commit する。この commit の後は、判定・閾値・予測の数を書き換えない。
5. **実装**: spec §10.1 のとおり、学習コードの blob をそのまま写し（`RUN_ID = "chargpt_cl_1019"` を変えない。乱数の種がこの文字列から作られる）、薄い wrapper `src/chargpt_detlabel_1023.py`（記録器 r1〜r5、π の読み込み、S2 の損失）、`judge.py`、J6 の解析の写しを作る。
6. **検査**: spec §8 の S-code・S-stream・S-recorder（§3 の読み替え）・S-pi（π を先に計算するなら）・S-soft（S2）・S-J6 を、本走の前に通す。落ちたら本走を始めずに報告する。S-chain・S-entropy は走りながら確かめ、外れたら止める。
7. **本走**: A4・A3・S2 を各 10 seed × 100 課題（fresh は課題 10・25・50・100）。spec §10.3 のとおり、連鎖の準備が CPU の律速になるので、π を先に別のプロセスで並べて計算しておくか、1 枚の GPU に 4 本まで並べてください（どちらにしたかを provenance に書く）。
8. **A2 の再生**: 課題 2〜10・41〜50・91〜100 の 29 課題 × 10 seed（spec §6.4）。
9. **J6**: A4（判定）と S2（判定）、A3（記録）の保存状態で、spec §6.5 のとおり。
10. **判定**: `judge.py` で spec §7 の判定と予測の採点を出し、`results/chargpt_detlabel_1023/judge.md`・`judge.json` に置く。
11. **commit**: 20 MB を超えるファイルと checkpoint は git に入れない。生データの置き場（このマシンの path）と、ファイルごとの bytes・sha256 を `results/chargpt_detlabel_1023/backup_manifest.json` に書いて commit する。

計算量は spec §10.3 の換算（RTX 5060 Ti）で、A4・A3 が約 15 GPU 時間、S2 が約 7.6、A2 の再生が約 2.0、連鎖の準備が約 43 CPU 時間（π を並べて計算すれば短くなる）、J6 は 1 腕あたり数分です。台が違えば変わります。長い走は tmux や nohup で裏に回し、ログを残してください。

## 5 守ること

- 学習コードの blob と `RUN_ID` を変えない。
- 登録の後に判定・閾値・予測を変えない。外れても数を書き換えない。
- main に push しない。push するのは `claude/chargpt_detlabel_1023` だけ。ほかのブランチは読むだけ。
- spec §9 の「言わないこと」を守る。結果を箱 M・この Adam・lr の外へ一般化しない。
- このマシンを落とさない。GPU の並列は 1 枚 4 本まで。メモリとディスクの残りを見ながら並べる。
- 迷ったとき、検査に落ちたとき、spec が決めていないことに当たったときは、自分で設計を変えずに止めて、先生に報告する（Issa に伝わるように書く）。

## 6 返すもの

- push の権限があれば、`claude/chargpt_detlabel_1023` に commit を push する。無ければ `git bundle create chargpt_detlabel_1023.bundle origin/claude/chargpt_detlabel_1023..HEAD` で bundle を作り、先生から Issa に渡してもらう。
- checkpoint などの生データ（約 9 GB）はこのマシンに置いたままにする。受け渡しの方法は Issa と決める。
- 報告（日本語、`results/chargpt_detlabel_1023/report.md` にも置く）は次の順に書く。
  1. 結論: A4 と S2 の J1〜J6・J6-LN のラベルと、条件を満たした seed の数
  2. 予測の採点（P1〜P6-LN）
  3. 検査の結果（§3 の読み替えを含む）と、台・版・A2 との差
  4. spec からずれた所の一覧と理由
  5. 掛かった GPU 時間・CPU 時間
  6. A3 の記録
