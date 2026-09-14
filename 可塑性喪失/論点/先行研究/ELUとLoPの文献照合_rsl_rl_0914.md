# ELU × LoP の文献照合（rsl_rl への接続・2026-09-14）

状態: 調査メモ（登録走ではない）/ 起点: Issa「rsl_rl の ELU で LoP が報告されてる事例ないですか」/ 作成: Claude
関連: [[層別キメラでELU崩壊の所在を決める_結果_0914]]／[[ELU沼_spec_0830]] §10-3（「rsl_rl の既定活性化を原典で確認」→ **本ノートで解消**）／[[文献照合_W増大メカニズム_0909]]

## 0. 一行

**rsl_rl / legged_gym の既定が ELU なのは原典で確認した。rsl_rl 系で ELU の LoP を報告した文献は見つからない。** 最も近い一次資料は Lillo & Cheney（ICLR 2026）の PPO × MuJoCo で、ELU は Plasticity Score 最下位群。教師ありでは同じ ELU が Random Label MNIST で ReLU に 64 pt 勝つ。環境で符号が反転する点は当方の PM/RL の結果と同じ向き。

## 1. rsl_rl の既定（原典）

| 出典 | 事実 |
|---|---|
| legged_gym `legged_robot_config.py` | `activation = 'elu'`・actor/critic `[512, 256, 128]`・Adam lr 1e−3・max_iterations 1500 |
| rsl_rl `utils/resolve_nn_activation` | elu / selu / relu / crelu / lrelu / tanh / sigmoid を解決。既定は設定側 |
| RSL-RL-SAC 技報 arXiv 2605.24975 Table C10 | PPO ベースライン: ELU・[512,256,128]。SAC は SiLU・[1024,512,256]。plasticity / dormant の記述なし |
| RSL-RL 論文 arXiv 2509.10771 | plasticity の記述なし |

## 2. legged 系で LoP に触れた文献

- **Entropy 2024「Continual RL for Quadruped Robot Locomotion」（PMC11154561）**: [512,256,128] MLP・**ReLU**・Adam 1e−3。「the plasticity of the RL network will be soon saturated after learning several tasks」→ 未使用パラメータの再初期化（Piggyback）。**ELU ではない。**
- GPO（arXiv 2601.20668）の「growing」は行動空間の拡張で、plasticity と無関係。

## 3. ELU × LoP の一次資料

### Dohare et al. 2024（Nature・arXiv 2306.13812）
- **Fig. B.10**（Slowly-Changing Regression・sigmoid/tanh/ELU/leaky/ReLU/Swish）: 「For some activations like ReLU and tanh, loss of plasticity is severe... **While for other activations like ELU, loss of plasticity is less severe, but still there is a significant loss of plasticity.**」
- Adam では「loss of plasticity with Adam is usually worse than with SGD」（活性化を変えても）。
- **PPO Slippery-Ant は tanh**（App. C「tanh activation as it performs the best with on-policy algorithms like PPO」）、公開 repo `lop/rl/cfg/*/std.yml` は `act_type: 'ReLU'`。**ELU で RL の LoP は測っていない。**

### Lillo & Cheney（ICLR 2026・arXiv 2509.22562）「Activation Function Design Sustains Plasticity in Continual Learning」
教師あり（Table 2・online acc %・5 seed）:

| 活性化 | Permuted MNIST | Random Label MNIST | RL-CIFAR | CIFAR 5+1 | C-ImageNet |
|---|---|---|---|---|---|
| ReLU | 78.85 | 20.03 | 25.79 | 4.76 | 73.71 |
| Leaky-ReLU | 84.14 | 91.53 | 98.34 | 48.86 | 85.28 |
| **eLU** | 80.50 | **84.23** | 57.45 ± 20.16 | 47.64 | 80.10 |
| CeLU | 82.93 | 37.16 | 29.64 ± 10.44 | 54.23 | 81.15 |

RL（Table F1・PPO・HalfCheetah→Hopper→Walker2d→Ant を 3 周・各 1M step・共有 2×256 MLP・Adam・Plasticity Score IQM）:

| 活性化 | Plasticity Score |
|---|---|
| Rand. Smooth-Leaky | 0.385 |
| Sigmoid | 0.330 |
| Swish | 0.313 |
| ReLU | 0.159 |
| Leaky-ReLU | 0.158 |
| **eLU** | **0.148 ± 0.107** |
| CeLU | 0.143 |
| CReLU | 0.120 |

分類: ELU/CELU/SELU は「one-sided smooth ＝ effective non-zero floor」。「when they recover, they do so quickly, but failures still occur frequently at strong shocks」。**当方の読み**: 教師ありの RL-MNIST では eLU が ReLU に 64 pt 勝ち、PPO では最下位群。**同じ活性化で環境により符号が反転**するのは当方の PM/RL と同じ向き。ただし彼らの eLU の RL-CIFAR が ±20 と不安定なのは、当方の RL-MNIST での崩壊（80 epoch・第 2 層）と整合する可能性がある（未照合・箱が違う）。

### 「Rethinking the Role of Dynamic Sparse Training for Scalable Deep RL」（arXiv 2510.12096・MR.Q・DMC Dog Run / Humanoid Run）
- encoder: 「ELU significantly outperforms ReLU」、critic も ELU が有利。
- actor: 「Switching from ReLU to ELU activation functions significantly degrades actor performance」。
- **層と役割で符号が変わる**。当方の「第 2 層の床」と同じ層依存の話だが、機構は未同定。

### Klein et al. survey（arXiv 2411.04832）§5.6
CReLU（Abbas 2023）・PELU（Delfosse et al. ICLR 2024・Atari の分布シフトで ReLU/CReLU に勝つ）・Deep Fourier を列挙。「活性化は dead unit を減らすが、[24,107] は異なる活性化でも LoP を示す」。Abbas 2023・Lyle 2023 は ELU を試していない。

## 4. 引用制限

- 「rsl_rl で ELU の LoP が報告されている」とは**書けない**（見つからない）。「既定が ELU」までが原典。
- Lillo & Cheney の PPO は MuJoCo 4 環境の巡回で、legged_gym の箱（4096 並列・数千イテレーション・単一課題）とは非定常の種類が違う。
- 「ELU は RL で悪い」を一般化しない。2510.12096 は encoder/critic では ELU 有利。

## Log
- 2026-09-14: web 検索 5 本・一次資料 PDF 6 本（Dohare・Lillo & Cheney・RSL-RL・RSL-RL-SAC・survey・Plasticine）・GitHub API で legged_gym / rsl_rl / loss-of-plasticity の設定ファイルを直接確認。
