---
name: README_reconstruction
description: Chat container で第 20 回に実施した K spectrum 対角化・段 0 分析・V-a/V-b・Term I/II・v3i_joint の再構築手順。Chat container リセット済で script 消失のため、数式と手順を残す。
sources: [chat]
aliases: [Chat container reconstruction, script 再構築, Chat スクリプト復元手順, 第 20 回 Chat 復元]
---

# Chat container で第 20 回に実施した内容の再構築手順

**目的**: Chat container (Chat Claude の code execution 環境) は各セッションで初期化されるため、
第 20 回 Chat セッションで私 (Kubo) が実施した以下 6 項目の script はすでに消失している。
中塚君が同じ検証を行うための再構築手順を残す。

**背景**: [[00_概要と5判定基準_0918]] の 5 判定は、以下 6 項目のうち V-a/V-b/Term I/II/v3i_joint (Landing A の core)
が Chat container で実施され、K spectrum/段 0 は Chat container と Claude Code の両方で実施された。
Claude Code 側は script が保存されている (`session21_scripts/step_C_t1_theory.py` 等)。
Chat container 側は消失。

**依存する data**: 全 npz は Nakatsuka repo の `session19_out/`, `session20_out/`, `session21_out/` にある
(詳細は [[large_data_reference]])。checkpoint は
`/home/kubo/project/Nakatsuka/data/act_sweep_hole1_0910_local/ckpts/LRa0p03_1216_step5000000.pt`。

**環境**: numpy 標準の環境 (Python 3.10+ / numpy 1.24+ / scipy 1.10+)。
GPU 不要 (全処理 einsum ベースで数秒-数分)。

---

## 1. K spectrum 対角化 (F_K = ℱ(𝒦) decay)

### 定義

- $\mathcal{K}$ = kernel operator: $\mathcal{K}[f](r) = \sum_s K_{rs} f(s)$
- $K_{rs} = (X_c)_r \cdot (X_c)_s / 32$: normalized similarity matrix
  - $X_c$: 32 support の centered representation (input dim 20)
  - $(X_c)_r$: r 番目 support の (20 次元) 埋め込み
- $\mathcal{F}(\mathcal{K}) = e^{-\eta T \mathcal{K}}$: SGD 内 T=10⁴ 更新の伝播 operator (approx.)

### 手順

```python
import numpy as np
from sim_act import load_ck
from model import support, oracle_g

# checkpoint load
net, T, fs, rm, act, alpha = load_ck(CKPATH)
# 各 seed s (10 個) について:
for s in range(10):
    n1 = int(fs[s].sum()); g1 = oracle_g(n1)
    X = support(fs[s])            # (32, 20)
    Xc = np.concatenate([X - g1, np.ones((32, 1))], axis=1)  # (32, 21)
    K = Xc @ Xc.T / 32.0           # (32, 32)
    # 対角化
    eigvals, eigvecs = np.linalg.eigh(K)   # ascending order
    eigvals = eigvals[::-1]                 # descending
    # 大きい mode から順に (通常 5 大 modes・15 mixed FREE-bit modes)
    print(f'seed {s}: top 5 eigvals = {eigvals[:5]}, small 15 mean = {eigvals[5:].mean()}')
    # F_K decay: 各 mode k の decay time constant = 1 / (2ηT · eigvals[k])
    for eta in [0.000156, 0.0002, 0.0005, 0.001, 0.0025]:
        F_K_decays = np.exp(-2 * eta * 10000 * eigvals / 32)
        print(f'  eta={eta}: top mode decay={F_K_decays[0]:.3f}, mean small={F_K_decays[5:].mean():.3f}')
```

### 予期される所見

- 大 5 modes: eigvals ≈ 1.0 (near unity・FIXED 15-bit の投影), decay ≈ 0 for η ≥ 0.001
- 小 15 modes: eigvals ≈ 0.1-0.5 (mixed FREE-5bit), decay ≈ exp(-few) for η ≥ 0.001

これは [[05_K_spectrumとF_K_decay_0918]] に記載した内容。

---

## 2. 段 0 分析 (0-th order operator response)

### 定義

- 段 0 = $\mathcal{F}(\mathcal{K}) \approx I$ 近似 (0-th order in $\eta T \mathcal{K}$)
- Effective per-step response: $\zeta_r \approx \delta'_r$ (δ' 生の値)
- Scale factor: $2\eta T/32$
  - η=0.000156, T=10⁴ → scale = 0.098
  - η=0.0025, T=10⁴ → scale = 1.56 (**飽和領域**)

### 手順

段 0 で T_1_i(t) を計算:

```python
# per-event per-unit の T_1 (0-th order)
def T_1_zeroth_order(v_i, delta_prime, m_r, phi_prime_i, eta, T=10000):
    """
    v_i: (H,) - unit weight
    delta_prime: (32,) - residual post-flip
    m_r: (32,) - row-mean of K
    phi_prime_i: (32, H) - 1 or alpha per (r, i)
    Returns: (H,) - T_1 per unit
    """
    inner = np.einsum('r,r,rh->h', delta_prime, m_r, phi_prime_i)  # (H,)
    return -(2 * eta * T / 32) * v_i * inner
```

具体的 script は `session21_scripts/step_C_t1_theory.py` に完全実装済み (Chat container script は消失だが Claude Code 版で代替可能)。

### 予期される所見

- **η=0.0025 で段 0 は破綻**: 実測 |Δz̄| ≈ 0.3 だが 段 0 T_1_theory は median|·| = 9.4 と過大
- → T_1 と Y_i が **near-cancellation** する構造 ([[04_Term_I_II分解と3レジーム_0918]] §5)
- 真の高次修正が必要 (audit-v1b §3-9 の M(t) 漸化式で計算可)

---

## 3. V-a 真の版 (有界性証明)

### 主張

$V_a(t) = \|\mu_t - \mu^*\|^2$ (μ = 内部代表点・μ* = target)
が長時間で bounded:

$$V_a(t) \leq V_a(0) + O(\eta^2 T \sigma_\text{noise}^2 t) + O(\eta \cdot \text{finite drift})$$

### 手順 (数値検証)

```python
import numpy as np

# session 20 の 500-task v2 npz で V_a を計算
for tag, eta in zip(['0156', '02', '05', '10', '25'], [0.000156, 0.0002, 0.0005, 0.001, 0.0025]):
    d = np.load(f'session20_out/mt_U1_bareK1_500tasks_v2_lr{tag}.npz')
    zbar = d['zbar']    # (501, 10, 100)
    # μ_t: task t の per-seed average zbar over 100 units
    mu_t = zbar.mean(axis=2)  # (501, 10)
    # μ*: target = converged mean at task 500
    mu_star = mu_t[-1]   # (10,)
    V_a = ((mu_t - mu_star[None, :]) ** 2).mean(axis=1)  # (501,) mean over seeds
    # bounded 確認: max(V_a[100:]) / V_a[0]
    print(f'η={eta}: V_a(0) = {V_a[0]:.3f}, V_a[100:] max = {V_a[100:].max():.3f}, mean = {V_a[100:].mean():.3f}')
    # V_a が O(1) で有界か
```

### 予期される所見

- V_a(t) は task 100 以降で bounded (max/mean ≈ 2-5)
- η と共に O(η²) の noise contribution 増加

これは [[02_V-a真の版_有界性_0918]] に記載した内容。

---

## 4. V-b 真の版 (‖w‖不動性)

### 主張

$\|w_t\|^2$ が長時間で不動 (invariance):

$$\|w_{t+1}\|^2 = \|w_t\|^2 + \Delta_t, \quad \mathbb{E}[\Delta_t] = O(\eta^2)$$

### 手順 (数値検証)

```python
# session 20 の v2 npz には v_final のみ (weight snapshot は各 task) が入っている
# alternatively, checkpoint 5M step の W と 500 tasks 走行後の W_final を比較

# session 19 の nokahan/kahan npz には task 別 W が保存されているはず
# ここでは v_final だけ確認 (v が w に対応)
for tag, eta in zip(['0156', '02', '05', '10', '25'], [0.000156, 0.0002, 0.0005, 0.001, 0.0025]):
    d = np.load(f'session20_out/mt_U1_bareK1_500tasks_v2_lr{tag}.npz')
    v_final = d['v_final']   # (10, 100) - final v after 500 tasks

    # checkpoint の初期 v
    net, _, _, _, _, _ = load_ck(CKPATH)
    v_init = net['v']        # (10, 100)

    v_final_norm = np.linalg.norm(v_final, axis=1)   # (10,)
    v_init_norm = np.linalg.norm(v_init, axis=1)     # (10,)
    ratio = v_final_norm / v_init_norm
    print(f'η={eta}: ‖v‖ ratio final/init: mean={ratio.mean():.4f}, std={ratio.std():.4f}')
```

### 予期される所見

- ‖v‖ の変動 <0.1% (全 5 arm × 10 seed) - 500 tasks 走行後も不動性保持
- η と共に微小変動 (O(η²))

これは [[03_V-b真の版_wnorm不動性_0918]] に記載した内容。

---

## 5. Term I/II 分解

### 定義

per-task per-unit の Δz̄_i を 5 項に分解:

$$\Delta \bar{z}_i(t) = \underbrace{\text{kick}_i(t) + \text{offset}_i(t)}_{T_0 \text{ (Term I)}} + \underbrace{T_1(t) + Y_i(t)}_{T_{II}} + T_4(t) + T_5(t)$$

- $T_0$ = kick + offset (Term I): flip 直後の geometric jump
- $T_1$ = kernel operator による T=10⁴ 内 SGD propagation
- $Y_i$ = residual (kernel operator の高次補正)
- $T_4$ = $\kappa(\eta) \cdot (-\bar{z})$: bare unit の drift
- $T_5$ = $-c(\eta) \cdot v^2 \cdot n_\text{band}$: on-band 損失

### 手順

```python
# per-event per-unit の各項を分離
d = np.load('session20_out/mt_U1_bareK1_500tasks_v2_lr02.npz')
zbar = d['zbar']; kon = d['kon']; kon_kick = d['kon_kick']
kick_i = d['kick_i']; offset_i = d['offset_i']
nband = d['nband']; v_final = d['v_final']
eta = 0.0002; kappa = 4.82e-5; c_v = 0.107 * eta

WARMUP = 100
dz_measured = zbar[WARMUP+1:501] - zbar[WARMUP:500]
T_0 = kick_i[WARMUP:500] + offset_i[WARMUP:500]
T_4 = kappa * (-zbar[WARMUP:500])
T_5 = -c_v * (v_final[None, :, :]**2) * nband[WARMUP:500]
# T_1 は Step C の per-event 計算値を使う (session21_out/step_C_t1_theory_per_event.npz)
# ここでは省略
R = dz_measured - T_0 - T_4 - T_5   # = T_1 + Y_i (residual)

# per-kp 群集計
kon_flat = kon_kick[WARMUP:500].ravel()
R_flat = R.ravel()
for kp_g, mask_fn in [('kp0', lambda: kon_flat==0), ('kp1', lambda: kon_flat==1),
                      ('kp2', lambda: kon_flat==2), ('kp3-5', lambda: (kon_flat>=3)&(kon_flat<=5)),
                      ('kp6+', lambda: kon_flat>=6)]:
    m = mask_fn()
    print(f'{kp_g}: T_1+Y_i mean = {R_flat[m].mean():+.4f}, std = {R_flat[m].std():.4f}, n = {m.sum()}')
```

### 3 レジーム分類

[[04_Term_I_II分解と3レジーム_0918]] §3:

- **kp0 (dead)**: R ≈ 0 (T_1 と Y_i の両方が ~0)
- **kp1-kp2 (kick)**: Y_i が dominant・T_1 は zero-th order で over-predicted
- **kp3+ (bulk)**: T_1 と Y_i が near-cancellation・R ~ small residual

---

## 6. v3i_joint Model M4 統合 (Landing A の core)

### 概要

Chat container で 2026-09-18 (Chat 第 20 回) に実装した Monte Carlo simulation。
**Landing A の 3 判定を達成** (Peak η=0.0002, width=7.40, Spearman +0.900)。
Chat container のリセットで script は消失、以下は再構築手順。

### モデル要素 (v3i_joint)

- $\Delta \bar{z}_i(t) = T_0 + T_4 + T_5 + R_i(t)$
- $R_i(t)$ = state-conditional empirical residual sampling:
  - 条件 (v² bin, z̄ bin, kon_kick bin) の 3-way empirical distribution
  - session 19 mt_v2 の 260 tasks 実測データから bootstrap
- $T_0$ = Step T joint distribution (kon, z̄) の 2-way sample
- $T_4, T_5$ = Step Q' κ, audit-v1b c=0.107η の理論
- kon 遷移: Step F Markov chain

### 実装 (再構築)

```python
import numpy as np
from collections import defaultdict

# Step T joint 分布 (T_0 sampling)
T0_j = dict(np.load('session20_out/step_T_T0_joint_distribution.npz'))

# per-eta residual 3-way empirical distribution 抽出
def load_empirical_R_3way(eta, tag):
    d = np.load(f'session19_out/mt_U1_bareK1_v2_lr{tag}.npz')
    zbar = d['zbar']; kon = d['kon']; kon_kick = d['kon_kick']
    kick = d['kick_i']; offset = d['offset_i']
    nband = d['nband'][:-1]
    v = d['v_final']

    WARMUP = 100
    dz = zbar[WARMUP+1:261] - zbar[WARMUP:260]
    kappa = LOAD_KAPPA_FROM_STEP_Q_PRIME(eta)  # session20_out/step_Q_prime_kappa_5point.csv
    c_v = 0.107 * eta
    T_4 = kappa * (-zbar[WARMUP:260])
    T_5 = -c_v * (v[None, :, :]**2) * nband[WARMUP:260]
    R = dz - kick[WARMUP:260] - offset[WARMUP:260] - T_4 - T_5

    # 3-way bin:
    #  v2_bin: log2(v²) を 5 bins
    #  zbar_bin: [-8, 3] を 22 bins
    #  kon_bin: {0, 1, 2, 3-5, 6+}
    v2_arr = (v ** 2)[None, :, :]
    v2_bin = np.digitize(np.log2(v2_arr + 1e-10), np.linspace(-4, 4, 6))
    zbar_bin = np.digitize(zbar[WARMUP:260], np.arange(-8, 3.5, 0.5))
    kon_bin = np.digitize(kon_kick[WARMUP:260],
                          [0.5, 1.5, 2.5, 5.5, 999])  # 0,1,2,3-5,6+

    # empirical distribution per bin
    R_dict = defaultdict(list)
    for i in range(R.shape[0]):
        for s in range(R.shape[1]):
            for u in range(R.shape[2]):
                key = (int(v2_bin[0, s, u]), int(zbar_bin[i, s, u]), int(kon_bin[i, s, u]))
                R_dict[key].append(R[i, s, u])
    return {k: np.array(v) for k, v in R_dict.items()}

# Monte Carlo (v3i_joint)
def simulate_v3i_joint(eta, tag, R_dict, T0_j, ntask=260):
    """
    Δz̄_i = T_0(kon, z̄) + T_4 + T_5 + R_i(v², z̄, kon)
    R は 3-way state-conditional bin から bootstrap
    """
    # (init state, Markov, per-task simulation, alive/dead transitions)
    # ... 実装は session21_scripts/step_G_model_m4_theory_driven.py の
    #     simulate_theory_driven() を参考に、R sampling だけ 3-way に変更する
    ...

# 実行
for tag, eta in zip(['0156', '02', '05', '10', '25'], [0.000156, 0.0002, 0.0005, 0.001, 0.0025]):
    R_dict = load_empirical_R_3way(eta, tag)
    zbar_hist = simulate_v3i_joint(eta, tag, R_dict, T0_j)
    # width, med 計算
```

### Landing A 判定 (v3i_joint Chat 版・2026-09-18)

|          η | v3i_joint width | §9-4 width |
| ---------: | --------------: | ---------: |
|   0.000156 |            7.30 |       6.93 |
| **0.0002** |        **7.40** |   **7.37** |
|     0.0005 |            5.75 |       7.37 |
|      0.001 |            5.29 |       6.15 |
|     0.0025 |            2.81 |       5.13 |

- Peak η = 0.0002 ✓ ([0.0002, 0.0005] 内)
- Peak value 7.40 vs 7.37 ✓ (|Δ|<2.0)
- Spearman = +0.900 ✓ (≥+0.9)

**3 判定達成** (ただし 260 tasks 判定・500 tasks では W5 で peak が η=0.000156 に移動する [[00_概要と5判定基準_0918]] §5 参照)。

Session 21 の Claude Code 版 (`step_G_model_m4_theory_driven.py`) は M4-A (empirical R + Markov) と M4-B (closed form Y_i) の 2 バリアントで、いずれも 3 判定達成せず ([[06_Model_M4_v3i_joint_3判定_0918]] §5)。v3i_joint (Chat 版) が達成した理由は R sampling を state-conditional (3-way bin) で行ったため。

---

## 参照ノート

- [[00_概要と5判定基準_0918]]: Landing A の 5 判定基準と全体構成
- [[01_実験設定と記号_0918]]: 変数・記号の定義
- [[02_V-a真の版_有界性_0918]]: V-a 節 (本 §3 の詳細)
- [[03_V-b真の版_wnorm不動性_0918]]: V-b 節 (本 §4 の詳細)
- [[04_Term_I_II分解と3レジーム_0918]]: 5 項分解 (本 §5 の詳細)
- [[05_K_spectrumとF_K_decay_0918]]: K spectrum (本 §1・§2 の詳細)
- [[06_Model_M4_v3i_joint_3判定_0918]]: v3i_joint の 3 判定 (本 §6 の詳細)
- [[08_Y_i閉形式_step_E_0918]]: Y_i = c(η)·v·Σδ' の閉形式 (Claude Code Step E)
- [[13_未達成項目と反証履歴_0918]]: 500-tasks 定常性問題・factor 3 vs 1 対立
- [[large_data_reference]]: 元 npz・checkpoint の manifest
