# 多層 Phase 0 spec（自己生成 µ の実測）

親: [[LoP防止アーキテクチャ_0829]] §6.4 / 状態: **事前登録（Issa 確認待ち・未実行）** / 作成 2026-08-29 / 出典チャット: `arch_lop_0829`

関連: [[中心主張v4草案_0829]] µ 考察 §1・§3 / [[論点マップ]] §12 / [[blindspot_0820]] §6 / [[自己項の恒等式]] / [[運用ルール]] §2 / [[引用禁止]]

> **実行前に §7 の事前予測欄を記入し、本 spec と config を repo へ commit・push すること。** repo 側 commit が push 確認できて初めて事前登録として有効（[[運用ルール]] §2）。
>
> **本 spec は介入を含まない。** 候補 A・B は入れない。測るだけ。

---

## 0. 一行

condA（m=20・f=15・T=10⁴・batch=1・std）で**隠れ 2 層 × 100 の ReLU 網**を 10 seed × 1M step 走らせ、(i) 2 層網でそもそも LoP が出るか（G0）、(ii) 第2層の入力に ReLU が自己生成した µ が壁座標をどれだけ押しているかを、32 パターン全サポート上の厳密計算で測る。

## 1. 何を決める実験か

[[中心主張v4草案_0829]] µ 考察 §3 は「正規化なしの ReLU 網では、前層の非負出力が次層の µ を自己生成する」を**論証として**置いており、【論証・未測定】の格が付いている。多層での µ/Σ の実測は [[blindspot_0820]] §6 で未着手。本走はこの一点だけを埋める。

**結論を先取りしない。** 「自己生成 µ が第1層より強い／弱い／同程度」のどれが出るかは §7 に実行前に書く。

## 2. スコープと前提

- condA のみ。**condB・他幅・他教師へ外挿しない**
- 素の SGD・共通 lr・正則化なし（Adam / weight decay は入れない。[[命題リスト]] Q15 の成立条件、および Chiley §3.4 / Dohare 図 4b の交絡を持ち込まないため）
- **多層化は 8/29 の Issa 判断で解禁済み**（[[LoP防止アーキテクチャ_0829]] §0）。[[論点マップ]] §12 の「2層 ReLU 限定」はこれまでの測定範囲の記述であって禁止ではない

## 3. 設計

### 3.1 腕（2 本・介入なし）

| 腕 | 学習器 | 用途 |
|---|---|---|
| `L1` | 隠れ 1 層 × 100（現行 `VecMLP` 相当） | 実装の同一性検査（S0）＋ 第1層の分解の基準 |
| `L2` | 隠れ 2 層 × 100 → 100 | 本命 |

共通: m=20, f=15, target_hidden=100, β=0.7, T=10⁴, enc=std, batch=1, lr_main=0.01, seed 0–9, total_steps=1e6, device=cpu。

**深さ間はペアにならない。** 層を足すと generator の消費が変わるので、`L1` と `L2` は乱数実現が一致しない。**深さ間の paired bootstrap は禁止**。G0 は `L2` 内の時間比較で判定する（§5.1）。

### 3.2 初期化

各隠れ層は既存則を踏襲（`envs.kaiming_mlp_params`）: 入力重み `U(-b, b)`、`b = sqrt(6/fan_in)`（relu gain）、bias = 0。読み出しは `sqrt(3/h_last)`、`c = 0`。第2層の `fan_in = 100` なので `b = sqrt(6/100)`。

### 3.3 実装

現行 `src/nets.py` の `VecMLP` は 1 隠れ層固定なので、**深さ L を取る新クラスが要る**（`VecMLPL` 仮称）。勾配は既存同様に閉形式で書く（係数 2 込み、`dL/dyhat = 2·delta`）。autograd に切り替えない（既存走との bit 一致検査ができなくなる）。

## 4. Phase 0 の前段チェック（本走前に完了させる。結果は見ない）

- **S0（実装同一性・必須）**: `VecMLPL` を L=1 で走らせ、`results/ratchet_log_0819/logs/seed0.npz` および既存 `A_w100` 走と **state_hash・既存全列が完全一致**することを確認する。M2 の再計装（[[直接機能量と開口量M2_0828]]）と同じ作法。**不一致なら本走に進まない**
- **S1（恒等式サニティ）**: 各層について、32 パターン全サポート上で直接列挙した `E[z_i]` と `sd(z_i)` が、`w_i·µ^(ℓ) + b_i` と `sqrt(w_iᵀ Σ^(ℓ) w_i)` に相対誤差 1e-10 以内で一致すること
- **S2（恒真チェック・教訓②⑩）**: S1 の検査を**判定指標だけでなくサニティ側にも掛ける**。とくに `L1` 腕の第1層で µ 項が既知の `cos_u_mu × mu_norm` 系列と整合すること
- **S3**: `OMP_NUM_THREADS=1`
- **S4（スモーク）**: seed 0 × 30k step。NaN/Inf ゼロ、全列の形状、`run_id` の生成を確認
- **本走・事前登録前に §5 の集計は一切しない。** スモークで見るのは構造だけ

## 5. 集計（事前登録）

### 5.1 G0 — 2 層網で LoP が出るか【ゲート】

T=10⁴ で 1M step なので**タスクは 100 個**。各タスクの末尾での**未フィット率**（残差分散 / 信号分散・無次元。絶対損失をレベル間で比べない、[[運用ルール]] §5 教訓⑤）をタスク番号の関数として取る。

- **初期窓** = タスク 2–11（タスク 1 は初期学習を含むので除く）
- **末尾窓** = タスク 91–100
- 統計量 `ΔU = mean(末尾窓) − mean(初期窓)`、seed ごとに算出 → **studentized bootstrap（bootstrap-t）**、B=10,000、`rng = np.random.default_rng(20260829)`。percentile CI は使わない（[[天井T0b上側窓_0829]] の教訓: seed クラスタ 10 本の percentile CI は反保守的）

**判定（実行前に凍結）**

| 条件 | verdict |
|---|---|
| `ΔU` の CI が 0 を上に外す **かつ** 末尾窓の未フィット率 ≥ 0.05 | `LOP_PRESENT` → Phase 1 へ進む |
| `ΔU` の CI が 0 を含む **かつ** 末尾窓の未フィット率 < 0.05 | `LOP_ABSENT` → **Phase 1 の設計をやり直す。これ自体が結果**（深さが LoP を消したことになる） |
| 上記以外 | `INCONCLUSIVE` → 走数・窓幅を再設計 |

閾値 **0.05 は結果を見る前に凍結**。根拠は水準の参照点として、深さ1・std の最終 `eval_loss_exact` が 0.3667 [0.2034, 0.5547]、µ を一段下げた `‖µ‖=2.333` arm（LoP ほぼ非発生側）が 0.0080 [0.0000, 0.0229] であること（[[中心主張v4草案_0829]] 柱3 の表、結果 commit `673c338`）。**この 2 値は eval_loss であって未フィット率ではない**ので、水準の直接比較には使わず、閾値の桁を決める材料としてのみ用いる。

### 5.2 壁座標の層別分解【本命】

層 `ℓ ∈ {1,2}`（`L2` 腕）と `ℓ = 1`（`L1` 腕）について、32 パターン全サポート上で厳密に

$$\boldsymbol\mu^{(\ell)}=\mathbb E[\mathbf a^{(\ell-1)}],\qquad \Sigma^{(\ell)}=\operatorname{Cov}(\mathbf a^{(\ell-1)}),\qquad \mathbf a^{(0)}:=\mathbf x$$

を計算し（一様重み・サンプリング誤差なし）、ユニットごとに

$$s_i^{(\ell)}=\underbrace{\frac{\mathbf w_i^\top\boldsymbol\mu^{(\ell)}}{\sqrt{\mathbf w_i^\top\Sigma^{(\ell)}\mathbf w_i}}}_{M_i\ (\text{µ 項})}+\underbrace{\frac{b_i}{\sqrt{\mathbf w_i^\top\Sigma^{(\ell)}\mathbf w_i}}}_{B_i\ (\text{b 項})}$$

を出す。これは µ 考察 §1 の $\|\boldsymbol\mu\|\cos\theta_i/\sqrt{\hat{\mathbf w}^\top\Sigma\hat{\mathbf w}}$ と**厳密に同じ量**（$\|\mathbf w_i\|$ が約分される）。**正規化量で力学を書かない**という禁則（[[引用禁止]] C）には抵触しない — これは静的な判定条件の側（[[吸収不等式の命題化_0824]] §2 と同じ扱い。引用時に一言添える）。

- **退化ガード**: $\sqrt{\mathbf w_i^\top\Sigma^{(\ell)}\mathbf w_i} < 10^{-8}$ のユニットは `NA` として除外し、件数を報告する。$\Sigma^{(2)}$ は 32 パターンしかないのでランク ≤ 31 であり、退化は起こりうる
- **報告する統計量**: 各層・各記録点で `median_i M_i`、`median_i B_i`、`M` の四分位、`NA` 件数。時系列（`lop_every=1000`）
- **副次（スカラーの用量目安・報告のみ）**: $\|\boldsymbol\mu^{(\ell)}\|/\sqrt{\operatorname{tr}\Sigma^{(\ell)}/d_\ell}$。**verdict には使わない**（柱3 の ‖µ‖ 軸とは定義が違うので直接比較しない）

**主要な問い（判定ではなく記述）**: `L2` 腕の第2層の `median_i M_i` は、同腕の第1層および `L1` 腕の第1層と比べてどの水準か。時間とともにどう動くか。

### 5.3 併記する量（すべて REPORT_ONLY）

層別に: `‖w‖` の推移、`eff_rank`（活性）、`eff_rank_W`、`strict_dead`（`p̂ ≡ 0`）、`alive`、`eff_rank / alive`。

- **`‖w‖` は主要共変量として事前登録する**（[[LoP防止アーキテクチャ_0829]] §6.6 S2）。Chiley §3.4 と Dohare 図 4b の教訓で、Phase 1 で primary が動いたとき µ 経路か ELR 経路かを分けるのに要る。**事後に足さない**
- **`strict_dead` は verdict に使わない**（cbp_harm 裁定）
- `eff_rank / alive` は候補 B の副次予測（[[LoP防止アーキテクチャ_0829]] §4）のベースライン取り

## 6. 出力

- `results/mlp2_phase0_0829/verdict.csv` — G0 の verdict と `ΔU` および CI
- `results/mlp2_phase0_0829/summary.md`
- `results/mlp2_phase0_0829/layer_stats.csv` — §5.2 の時系列
- `results/mlp2_phase0_0829/provenance.json`
- ログ `results/mlp2_phase0_0829/logs/{L1,L2}_seed{k}.npz`

**数値は `verdict.csv` と `summary.md` からのみ転記する**（[[運用ルール]] §2）。

## 7. 事前予測欄（**実行前に Issa が記入すること**）

記入されないまま実行した場合、本 spec は事前登録として無効。

1. G0 の予測（`LOP_PRESENT` / `LOP_ABSENT` / どちらとも言えない）と理由:
   -
2. `L2` 腕・第2層の `median_i M_i` は第1層と比べて（大 / 同程度 / 小）:
   -
3. 第2層の `M` は時間とともに（増える / 変わらない / 減る）:
   -
4. 上のどれかが外れたときに何を疑うか:
   -

## 8. 引用上の注意（結果が出た後に守ること）

- **深さ間の比較はペアではない**（§3.1）。`L1` と `L2` を同一個体の主張として読まない
- §5.2 の副次スカラーは**柱3 の ‖µ‖ 軸ではない**。用量反応の点として並べない
- 隠れ層では **µ と Σ を独立に振れない**（どちらも前層の出力分布が決まる）。本走から「µ を上げたら壁が強くなった」型の用量反応は言えない（[[LoP防止アーキテクチャ_0829]] §6.8-1）
- 第1層には **xr 分解・税の代数が使えない**（多層で [[自己項の恒等式]] の加法性が崩れる）。本走で書けるのは壁座標の静的分解まで
- スコープは condA・batch=1・std

## 9. config 骨子（`configs/mlp2_phase0_0829.yaml`）

```yaml
spec: specs/spec_mlp2_phase0_0829.md
common:
  total_steps: 1000000
  seeds: [0,1,2,3,4,5,6,7,8,9]
  lr_main: 0.01
  device: cpu
  eval_batch: 2000
  lop_every: 1000
  loss_bin: 1000
  checkpoints: [0, 1000000]
  dead_tol: 1.0e-7
condA:
  m: 20
  f: 15
  target_hidden: 100
  beta: 0.7
  T_values: [10000]
  encodings: [std]
arms:
  - {name: L1, hidden: [100]}
  - {name: L2, hidden: [100, 100]}
phase0:
  bootstrap_B: 10000
  bootstrap_seed: 20260829
  early_tasks: [2, 11]
  late_tasks: [91, 100]
  unfit_threshold: 0.05
  sigma_degenerate_tol: 1.0e-8
```
