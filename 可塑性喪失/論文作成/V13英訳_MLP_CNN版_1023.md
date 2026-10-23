# V13 英訳：MLP+CNN 版（arXiv v1 用）1023

状態: **英訳の下書き v0.2（校正前）** / 2026-10-23 / 訳: Claude（Opus 5.5 のサブエージェント）、照合と直し: Claude（Opus 5.5、MLP+CNN 版のセッション）。元は [[V13通し稿_MLP_CNN版_1023]] **v0.2** の本文（--- より後）。本線の英訳 [[V13英訳_全文_1023]] は v0.9 が元で（§3/§4 は v0.3）、v0.10 の kunekune の書き直しも入っていないので、そこから削らずに v0.2 の日本語から訳し直した。用語と、意味が同じ文の言い回しは本線の英訳に合わせた。Issa の決定（1023 夜）で、英訳もこの版に同期する。

**照合。** 日本語と英訳で、数の並び（小数と 3 桁以上の数は全部一致。差は「二つ」などの語にした小さな整数と見出しのコメントだけ）、節の参照（§n.m）、付録の参照（A・C・D・E・F・H）、引用（[著者 年] の組）を python で突き合わせ、全部一致した。そのうえで全文を日本語と並べて読んだ。

**訳で補った所（日本語の本文は変えていない）。**
- 「90〜100%」（§4.1）・「99〜100%」「50〜55%」（§5.1）は、付録 D.1・H.1・H.2 の定義どおりユニットの割合として "of units" と訳した。§3.1 の「押しの向きの96〜98%が割り当てに依らない」も、§5.1 と同じユニットの割合として訳した。
- §5.3 の kunekune の「位置は−0.81から−0.27へ戻って」は相対位置 $r$ の値なので（[[実ラベル5p1CNN_課題あたり更新数の延長_結果_1019]] の FC2 の表、KKT1 の境界 30 の r）、"its relative position $r$" と訳した。**本線の日本語も「相対位置」にすると揃う。**
- §5.3 の幅 cap の「testは平均で0.2ポイント上回った」は、付録 H.5（natural 75.372 → cap 75.616%）のとおり cap の側として訳した。
- 要旨の末尾と §5.3 の「課題全体のonlineは98.2%」は日本語のまま曖昧さを残した（前者は「CNN の予算延長での劣化」が ELU の劣化を指す、後者は 7,800 更新の ELU を指す、と読める）。

**語数。** python で「## 」区切り、空白で分けて数えた（見出し・表・数式込み、日本語見出しのコメントと参考文献は除く）。

| 節 | 語 |
|---|---:|
| 要旨 | 282 |
| §1 | 545 |
| §2 | 482 |
| §3 | 1,587 |
| §4 | 1,630 |
| §5 | 1,087 |
| §6 議論 | 327 |
| 計 | 5,940 |

本線の英訳の実測（§3 1,387 語 = 1.57 頁、§4 1,442 語 = 1.55 頁、[[V13英訳_全文_1023]]）の比で換算すると本文は約 6.5 頁、図 2 枚で約 7.1 頁。組版での実測はまだしていない。日本語見出しは `<!-- 日本語見出し: … -->` のコメントで残した（組版では外す）。

---

# Asymmetric Activations Keep Sinking Preactivations

Subtitle candidate: A Mechanism of Plasticity Loss in MLPs and CNNs, with the kunekune Activation

<!-- 日本語見出し: ## 要旨 -->
## Abstract

Preactivation sinking, response reduction, and linearization in continual learning are known phenomena. We connect them through a single mechanism. Each time a task is learned, the readout aligns with the current task. This alignment pushes preactivations downward at the next switch. The input-mean and bias pathways, together with upstream pathways that move with learning, carry the push to the position. Asymmetric activations sink deeply, and growth of the width increases this depth. Units that have sunk lose their response, which reduces relearning. For a linear readout with cross-entropy, we derive a condition for positive alignment. In a fixed-feature model, we show that the push at the switch is proportional to the product of the activation value and its slope. We verified each link in this chain through interventions or analyses of saved states in two architectures, MLPs and CNNs. Blocking the input-mean and bias pathways preserved relearning (200 tasks in MLPs, 30 tasks in CNNs). Limiting the width prevented the collapse of ELU in random-label MLPs. Response-field exchange with matched initial activities and predictions changed relearning in both directions in both architectures. The aspects that changed across architectures were the identity of the carrier (from a fixed input mean to upstream layers that move with learning) and the layers in which sinking accumulates (below the final hidden layer in CNNs). As an intervention from the activation side, we used kunekune, whose derivative returns to 1 in both tails and whose curvature scale tracks the width. With kunekune, the position did not deepen and the response was preserved as the width grew (CNN), and the collapse of ELU in random-label MLPs and the degradation under the extended budget in CNNs disappeared.

<!-- 日本語見出し: ## 1 序論 -->
## 1 Introduction

Plasticity loss, in which continued training impairs relearning, has been associated with unit closure, weight growth, and reduced representation rank [Dohare 2024]. As the preactivation distribution shifts, units close or become nearly linear and lose response. In ReLU networks immediately after a task switch, preactivations were also observed to be pushed toward the negative side, causing units to die [Lyle 2025]. Another account describes preactivations being pushed into the tails of the activation, where gradients shut down [Lillo & Cheney 2026]. In a ReLU network at initialization, random readout weights yield a positive expected gradient with respect to a positive preactivation. Gradient descent therefore acts to shrink that preactivation [Li 2023; Shvetsov 2026]. Formal proofs are limited to ReLU. Similar drift in GELU and SiLU was reported experimentally [Shvetsov 2026]. We ask why this push is rebuilt at every task switch, which pathways carry it to the position, and what function is lost to reduce relearning.

The answer is a four-stage mechanism. (i) Learning a task aligns the features and the readout with the labels of the current task. At the next switch, this alignment creates a push proportional to the product of the activation value and its slope. (ii) The input-mean and bias pathways carry the push to the position. In layers whose upstream changes with learning, they also carry that displacement. (iii) Asymmetric activations sink deeply under the push. Growth of the width increases the depth. (iv) Units that have sunk lose their response. This reduces relearning. Blocking the pathways or preserving the response preserves relearning. We do not claim that all units always sink. We state the conditions under which each stage holds.

Our verification has three pillars: interventions on the position pathways, bidirectional interventions on the response, and rescue and non-rescue by growth caps. We establish a reference in MLPs (Section 4). We verify the same four stages in CNNs (Section 5). The aspects that changed across architectures were the identity of the carrier and the layers in which sinking accumulates. We move the width stage from two sides: with a cap that stops the width, and with kunekune, an activation that preserves response while letting the width grow (Sections 4.3 and 5.3).

Relation to prior work. In a ReLU network at initialization, a random readout yields a positive expected gradient with respect to a positive preactivation [Li 2023; Shvetsov 2026]. Li et al. state that their theorem does not apply after learning begins. Experiments with purely random labels in a one-hidden-layer ReLU network showed that the bias drifted toward the negative side and ReLU units died [Cornacchia 2021]. A decrease in preactivations for many inputs immediately after a switch was also reported as an observation in ReLU networks [Lyle 2025]. We add that the learned readout reloads the push at every switch. We identify the carriers as the input-mean, bias, and upstream pathways. We identify response as the function lost and link this loss to width growth. We verify these claims through interventions and analyses of saved states in two architectures. Sections 3.3 and 4.3 discuss the relation to activation design [Lillo & Cheney 2026]. Appendix F compares performance levels with weight shrinkage, regularization, and unit reinitialization [Ash & Adams 2020; Kumar 2025; Dohare 2024; Sokar 2023].

<!-- 日本語見出し: ## 2 設定と測定 -->
## 2 Setup and measurements

<!-- 日本語見出し: ### 2.1 学び直しの評価 -->
### 2.1 Evaluating relearning

We define plasticity loss as a decline in the ability to learn later tasks under conditions in which the network could learn initially. Tasks are learned sequentially. The weights and optimizer state are carried over at each task switch. We measure adaptation to new tasks, not retention of past tasks.

For image classification, we use online accuracy, the minibatch accuracy before each update averaged within a task. Even if two networks reach the same end-of-task accuracy, slower adaptation along the way yields lower online accuracy. For real-label tasks whose difficulty itself changes, we compare with a fresh network trained on the same task (Appendix A).

<!-- 日本語見出し: ### 2.2 位置、幅、応答 -->
### 2.2 Position, width, and response

Let the input to a layer be $x$ and let $\mu$ be the mean of the input distribution used for evaluation. We decompose the preactivation of unit $i$ as $z_i(x)=w_i^\top x+b_i=m_i+w_i^\top(x-\mu)$, with $m_i=w_i^\top\mu+b_i$. We call $m_i$ the common position, $s_i=\operatorname{sd}_x[z_i(x)]$ the width, and $r_i=m_i/s_i$ the relative position ($s_i>0$). We call movement of the common position toward the negative side sinking. Whereas $m$ represents the raw change in position, $r$ represents position relative to width. Changes in $r$ therefore also include changes in the denominator $s$.

We define the open fraction as $p_i=\Pr_x[z_i(x)>0]$. We define the local response as the derivative used in training, $d_i(x)=\varphi'(z_i(x))$. For MLPs, the death rate is the fraction of units with $\max_x|d_i(x)|<10^{-6}$ over all training images of each task. For CNNs, death is measured by the open fraction on a fixed evaluation set (probe; thresholds in Appendix A).

<!-- 日本語見出し: ### 2.3 課題と構造の役割 -->
### 2.3 Roles of the tasks and architectures

We use one-hidden-layer networks to study the fixed-feature analysis and the formation of the push. We use two-hidden-layer MLPs for interventions on the position pathways and the response. CNNs test the mechanism in an architecture whose upstream changes. Real-label 5+1 CIFAR tests the case of learning new classes sequentially and supports design comparisons. In random-label tasks, a fixed set of 1,200 images from MNIST or CIFAR-10 receives independent random labels from 10 classes at each task (following the setup of [Kumar 2025]). The task design of real-label 5+1 CIFAR also follows Kumar et al. Hard tasks with 5 classes and easy tasks with 1 class from CIFAR-100 alternate without revisiting classes (networks in Appendix A). We evaluate on the hard tasks. Prior work on plasticity has measured the ability to relearn on tasks whose targets are chosen independently of the network's current parameters [Lyle 2022]. It has also used sequential memorization of random labels as a test of relearning that does not require generalization [Lee 2024].

The main MLP experiments use Adam without normalization layers. We call the condition with pixel values divided by 255 raw. We call the condition standardized with per-channel constants std. Each comparison specifies the seeds, branch points, evaluation windows, and aggregation method. Appendix A collects the details.

<!-- 日本語見出し: ## 3 機構：学習した状態が位置を動かす -->
## 3 Mechanism: the learned state moves the position

This section states the mechanism in four stages. (i) At every task switch, each unit moves in the direction that suppresses its output, and learning the task is what creates this push. (ii) The input-mean and bias pathways carry the push to the position; when the upstream layers move, their displacement is carried as well. (iii) Asymmetric activations sink deeply, and the growth of the width increases the depth. (iv) A unit that has sunk loses its response. Section 4 verifies the four stages in this order in MLPs, and Section 5 carries them to convolutional networks.

<!-- 日本語見出し: ### 3.1 学習が切替の押しを作る -->
### 3.1 Learning creates the push at the switch

Learning before the switch aligns the features and the readout with the labels of the current task, and this alignment creates the push at the switch; we call this loading. Let $\phi_n$ be the features of input $n=1,\ldots,N$, let $y_n$ be the one-hot vector of the old label ($C$ classes), and let the logits be $\ell_n=V\phi_n+b$. Let $V^c$ and $b^c$ denote the readout and the bias centered across classes. We measure the strength of the alignment by the coefficient $\kappa$ of the projection of $V^c$ onto the direction of $F=\sum_n(y_n-\mathbf1/C)\phi_n^\top$. Let $\mathcal L$ be the mean cross-entropy. When $F\ne0$,

$$
\kappa=\frac{\langle V^c,F\rangle_F}{\|F\|_F^2}
\ge\frac{N(\log C-\mathcal L)-\Gamma}{\|F\|_F^2}
$$

holds (proof in Appendix C). The term $\Gamma=\sum_c(n_c-N/C)b^c_c$ comes from the imbalance of the class counts $n_c$ and from the bias, and it vanishes when the classes are balanced. Hence $\kappa>0$ whenever $\mathcal L<\log C-\Gamma/N$; neither independence between the features and the labels nor perfect classification is required.

This alignment becomes the push at the switch. Consider a fixed-feature model with one hidden layer. Fix $\phi_{in}=\varphi(z_i(x_n))$ and $d_{in}=\varphi'(z_i(x_n))$, let the old labels be independent and uniform across inputs, and let the new labels be independent of the network state and uniform as well. Write the readout as $v_{ic}=v^0_{ic}+\kappa\sum_m(y_{mc}-1/C)\phi_{im}$, and keep $\kappa>0$ fixed when taking the expectation over the old labels. We further assume that the correlation between $v^0$ and the old labels averages out, and that the prediction before the switch is in the limit of a confident correct answer, $\pi_n\to y_n$. We call these assumptions H1 (Appendix C). The independence of the new labels is a property of random labels. Even with real labels, however, updates are carried only by the examples whose error remains [Katharopoulos & Fleuret 2018]. In training with noisy labels, the mislabeled examples carry the gradient after early learning [Liu 2020]. The push at the switch splits identically into two terms (Appendix C). One does not depend on the label assignment and is determined by the prediction before the switch and the class frequencies of the new task. The other is the label term, the covariance across new classes between the unit's readout weights and its activity. If the readout for the new classes is unlearned, the label term is small, and random labels are the limit in which it is exactly zero. In real-label CNNs, the label term is 7–12% of the model term, and for 96–98% of units the direction of the push does not depend on the assignment (Section 5.1).

Fix the layer input and update the weights and the bias by one-sample SGD with the same learning rate $\eta$. With $\delta_{in}=\partial\ell_n/\partial z_i(x_n)$, the position moves by $\Delta m_i=-\eta\,\delta_{in}K_n$ with $K_n=\mu^\top x_n+1$ (the meaning of $K_n$ is given in Section 3.2). Define the push that sinks the position, averaged over the new labels, as

$$
S_i=\sum_nK_nd_{in}\langle v_i,\pi_n-\mathbf1/C\rangle
$$

Then the expected displacement of one full-batch step on the mean loss is $-(\eta/N)S_i$, so $S_i>0$ is the sinking direction. Averaging also over the old labels under H1 gives

$$
\mathbb E_{\rm old}S_i
=\kappa(1-1/C)\sum_nK_n\varphi'(z_{in})\varphi(z_{in})
$$

This is because the label correlations between different inputs vanish and only the diagonal terms of the same input remain. We call the sum on the right-hand side, the weighted sum of the product of the value and the slope, the self-form. In this model, the sign of the product of the activation value and its slope sets the direction of the push, and its magnitude is proportional to the alignment $\kappa$ that learning has created.

<!-- 日本語見出し: ### 3.2 押しを位置へ運ぶ経路 -->
### 3.2 The pathways that carry the push to the position

The bias is not the only thing that moves the common position. The weight update that learns the features also changes the common position, through its component along the input mean. In a multilayer network, moreover, the features that enter the layer change themselves. The finite displacement from time $t$ to $t+1$ is exactly

$$
\Delta m_i=(\Delta w_i)^\top\mu_t
+w_{i,t+1}^\top\Delta\mu+\Delta b_i
$$

The first term is the weight pathway, the third term is the bias pathway, and the second term is the pathway of upstream change. This decomposition does not depend on the optimizer. The sign of each term is examined separately.

The factor $K_n=\mu^\top x_n+1$ of Section 3.1 combines what the weight pathway ($\mu^\top x_n$) and the bias pathway ($+1$) carry in one SGD step with fixed inputs. When every component of the input is non-negative, as for raw images or for ReLU outputs before centering, every $K_n\ge1$, and a positive local gradient lowers the common position. In general, $\mathbb E_xK=\|\mu\|^2+1>0$ does not make every $K_n$ positive, and for standardized inputs $K_n$ can be negative.

For exactly centered fixed inputs, $\mu=0$ and $K_n=1$; the pathway from the weights to the common position disappears, but the bias pathway remains. Whether centering alone can suppress sinking therefore also depends on the remaining action of the bias. In a layer whose upstream moves with learning, the second term $w^\top\Delta\mu$ is added to these. Its magnitude is measured in Section 5.

<!-- 日本語見出し: ### 3.3 活性化ごとの符号の境界と幅 -->
### 3.3 Sign boundaries and width for each activation

For ReLU, $\varphi'(z)\varphi(z)=\max(z,0)$. If $K_n$ is positive for every input, then, regardless of the distribution, the self-form of any fixed state with at least one open input is positive, and no contribution lifts the unit from the negative side.

To compare the other activations, we assume $z\sim\mathcal N(m,s^2)$ and an input-independent $K_n=\bar K>0$. With $G_s(r)=\mathbb E[\varphi'(z)\varphi(z)]/s$, the sign of the self-form is the sign of $G_s(r)$. For leaky ReLU (negative-side slope $0<a<1$), $G_s$ has a closed form $G(r)$ that does not depend on the width (Appendix C). $G(0)>0$, and there is a unique zero on the negative side. For $a=0.1$, for example, the zero is at $r\simeq-1.72$, where the open fraction is about 4%. Even in a state where positive and negative inputs are equally frequent, the product on the negative side is only $a^2$ times that of a positive input of the same magnitude, so the sinking direction remains. The zero is the sign boundary of the self-form, not a stopping point of the training trajectory.

For ELU with $0<\alpha\le1$, this Gaussian, constant-positive-$K$ self-form is positive for $m\ge0$ and has a unique zero on the negative side. For SiLU and GELU, the pointwise inequality $\varphi(z)\varphi'(z)\ge z/4$ holds regardless of the distribution, and it is strict for $z\ne0$ (proof in Appendix C). Hence, under constant positive $K$, the self-form is positive whenever $m\ge0$ and $z$ is not identically zero.

The push remains even after the self-form has weakened. In the model of phase 2 (the stage after the self-form has weakened), which fits a frozen network by squared error, the quantity that sets the sign of the push is replaced by $\operatorname{Cov}(\varphi',\varphi)$ under the conditions of Appendix C. For leaky ReLU, the push is then on the sinking side even deeper in the negative region than the zero of the self-form (checked against real states only for MLPs; Appendices C and D).

Finally, we vary only the width in the same Gaussian, constant-positive-$K$ model. For leaky ReLU, the relative zero $r$ does not depend on the width, but the corresponding absolute position $m=rs$ becomes deeper as the width grows, because $r$ is negative. For ELU, the relative zero of the self-form itself deepens as the width grows. For SiLU and GELU, a zero exists only when the width is small (numerical; Appendix C). ReLU has no zero in a living state from the start. The width thus moves the sign boundary of the self-form, but the growth of the width itself is not derived. Conversely, consider an activation whose tail slopes on both sides are 1 and whose curvature scale tracks the width (kunekune; it retains the curvature of Snake [Ziyin 2020] within a finite interval and joins it to straight lines of slope 1 outside that interval; definition in Appendix F). For kunekune, $G_s(r)$ does not depend on the width, the zero stays at $r\simeq-1.0$, and the mean derivative there is 0.55 (numerical, Appendix C; the same holds for adaptive Snake, whose tails are not cut). We predict that the position does not deepen and the response remains as the width grows.

<!-- 日本語見出し: ### 3.4 沈んだ先で失われる機能 -->
### 3.4 Functions lost after sinking

The function lost by a shift of the position toward the negative side differs across activations. ReLU has zero response on closed inputs; ELU, SiLU, and GELU have a small absolute derivative deep on the negative side. Leaky ReLU keeps a constant slope, yet when most inputs fall on the same branch, the unit approaches a linear map over that range (one-sidedness). All of these occur separately from death, in which the unit is closed on every input. How much a unit that has lost its response reduces the relearning of the whole network is not determined by the shape of the activation, so Section 4.4 measures it by exchanging only the response.

<!-- 日本語見出し: ## 4 MLP：機構の四段を順に確かめる -->
## 4 MLP: verifying the four stages of the mechanism in order

We verify the four stages of Section 3 in order, in a one-hidden-layer MLP (Section 4.1) and in two-hidden-layer MLPs (Sections 4.2 to 4.4).

<!-- 日本語見出し: ### 4.1 押しは学習で作られ、課題ごとに作り直される -->
### 4.1 The push is created by learning and rebuilt at every task

In one-hidden-layer MNIST with the five activations of Section 3.3 (two seeds each), we confirmed that the push of Section 3.1 is created by learning, is rebuilt at every task, and actually sinks the units. The expected push at the switch rose as a nearly constant multiple of $\log C-\mathcal L$, the amount by which the task-1 loss had fallen below chance, with no threshold-like step (quartiles of the ratio after 50% training accuracy: 0.18 to 0.22). In a post-hoc analysis over 30 tasks, $\kappa$ at the end of each task never fell below 0.83 times its value at the end of task 1, and from task 2 on, 74 to 95% of $\kappa$ was rebuilt by the change of the features. In the first 200 updates after a switch (Adam), 82 to 100% of the living units actually sank (range of the values over task intervals). Except for leaky ReLU, the self-form agreed in direction with the expected push in 90 to 100% of units, but it carried only 13 to 60% of the magnitude (Appendix D). The theory of Section 3.1 predicts the direction, not the magnitude. H1 freezes the features, but in actual training the change of the features carries most of the loading, and the corresponding part of the push enters the terms of other units and the residual. (For leaky ReLU, even the direction fails because, deeper than the zero, the phase-2 term remains on the sinking side; Section 3.3.) Returns within a task occurred inside the negative side: of 1,000 units that had once entered $p<1/2$, only 4 were back at $p\ge1/2$ at the end of a later task.

<!-- 日本語見出し: ### 4.2 経路を塞ぐ：中心化とbias抑制 -->
### 4.2 Blocking the pathways: centering and bias suppression

We block the two pathways of Section 3.2 separately. In two-hidden-layer random-label CIFAR with raw inputs and ReLU, we compared three operations: C subtracts the input mean, H subtracts the output mean of both hidden layers, and CH combines the two (these are names of operations, distinct from the number of classes $C$). With C alone the second layer was lost, and with H alone the first layer was lost; in each case the lost layer was the one whose input-mean pathway stayed open. The online accuracy over tasks 31 to 50 was 11.33% for C and 98.67% for CH, and 98.54% for CHB, which additionally suppresses the bias (medians over 10 seeds). CHB adds two operations to CH from task 1 on: the first-layer bias is zeroed after every update, and decoupled weight decay is applied to the second-layer bias.

Another 10 seeds (10 to 19) were run to 200 tasks. The online accuracy over tasks 181 to 200 was 62.98% for CH and 99.03% for CHB (Appendix D). CH declined in all 10 seeds, while CHB kept its high accuracy. In the first layer with centered inputs, the common position over the training images coincides with the bias ($m_1=b_1$), and under CH it sank to the negative side. As Section 3.2 states, blocking the weight pathway by centering leaves the push in the bias pathway, and long-term relearning was preserved only when that pathway was blocked as well.

<!-- 日本語見出し: ### 4.3 幅を止める：成長制限 -->
### 4.3 Stopping the width: growth caps

Section 3.3 distinguished an activation whose self-form zero is deepened by the width (ELU) from one that has no zero in a living state (ReLU). We placed a cap on the growth of the weights to stop the width from growing, and asked whether this difference appears in relearning. The radius of each unit is the row norm of its input weights at the end of task 1; from task 2 on, after every Adam update, a row that exceeds its radius is projected back onto it (cap12 for both layers, cap1 and cap2 for one layer; Appendix A).

In random-label CIFAR with standardized inputs and ELU, the online accuracy over tasks 31 to 50 was 85.98% under cap12 against 10.09% for the control, and the collapse was prevented in all 10 seeds. Capping one layer was not enough (cap1 11.91%, cap2 25.10%). The norm of the second-layer input mean grew from 52.6 to 1157 in the control between tasks 1 and 50, and stayed at 40 under cap12 (seed average).

For ReLU in the same random-label CIFAR, the control was at the floor (11.3%), and cap12 did not change it. For ReLU in real-label 5+1 CIFAR, cap12 lowered the late online accuracy by 3.6 points [97.5% confidence interval with correction for 2 comparisons: $-6.7$ to $-0.5$]; the second-layer position became shallower, but the death rate did not fall (Appendix D). Up to this point the results agree with the reading of Section 3.3: ELU, whose zero deepens with the width, is rescued when the width is stopped, and ReLU, which has no zero in a living state, does not reopen when the width is stopped. The exception is ELU in real-label 5+1, where cap12 was worse by 2.0 points. The registered prediction that the effect splits by activation alone fails here, and the cost of the cap to learning in a fresh network cannot explain it (Appendix D).

We also moved the same stage from the activation side. In MLPs on the same random-label CIFAR, the late online accuracy of ELU was at the floor of 10.1% for both raw and std inputs, whereas kunekune reached 95.7% and 98.7% (medians over 10 seeds; Appendix F). In real-label 5+1, kunekune and adaptive Snake, which match the curvature scale to the width, exceeded Snake with the scale fixed at its initial value by 4.6 to 6.1 points in late online accuracy (10/10; registered; Appendix F). Moving the same stage from the side opposite to the cap also preserved relearning.

<!-- 日本語見出し: ### 4.4 応答を入れ替える：学び直しへの効果 -->
### 4.4 Exchanging the response: the effect on relearning

We test whether the loss of response of Section 3.4 reduces relearning by exchanging only the second-layer response, while keeping the weights, the activities, and the predictions at the branch point. Let $z_i^0(x)$ be the preactivation at the branch point and $z_i^{\rm src}(x)$ the preactivation of the source network. We fix their difference $o_i(x)=z_i^{\rm src}(x)-z_i^0(x)$ and set the output after the branch to $\varphi(z_i^0)+\varphi(z_i+o_i)-\varphi(z_i^0+o_i)$. At the branch point, the activities, the logits, the loss, and the weights coincide with the control, and only the derivative used in training becomes $\varphi'(z_i^{\rm src})$. After the branch, learning of the weights and the features resumes, and the derivative moves with the preactivation as $\varphi'(z_i+o_i)$.

We exchanged the response in both directions between the early and the degraded states of the same trajectory (Table 1). The restoring direction inherits the Adam history; the direction that hands a low response to the early network resets the history in both the control and the intervention. In all three settings, restoration raised the relearning of the next task and the reverse exchange lowered it, and all 10 seeds agreed in direction in every comparison.

| Setting (branch points)                                | Early response into the degraded net | Degraded response into the early net |
| ------------------------------------------------------ | ------------------------------------ | ------------------------------------ |
| Random-label CIFAR, ELU/std (end of tasks 1 and 10)    | 10.2% → 57.0% (+46.7 [42.9, 50.6])   | 97.1% → 29.2% (−67.9 [−69.6, −66.2]) |
| Random-label MNIST, ELU/raw (end of tasks 2 and 10)    | +76.0 [74.6, 77.4]                   | −25.9 [−31.7, −20.2]                 |
| Real-label 5+1 CIFAR, ReLU/std (end of tasks 2 and 28) | 40.4% → 61.7% (+21.3 [18.4, 24.3])   | −6.0 [−7.3, −4.7]                    |

Table 1. Online accuracy on the next task after the exchange. Point differences are mean paired differences over 10 seeds, with 97.5% intervals in brackets. The tasks and budgets of each setting are in Appendix E.

We also examined the contribution of the response that the growth cap preserves, in random-label MNIST with ELU. In this setting, a growth cap constrains the norms of the two components of the first layer, split along the input-mean direction and its orthogonal complement, together with the row norms of the second layer (we write cap12′ because its form differs from that of Section 4.3). It improved on the control in all 10 seeds (online accuracy over tasks 51 to 100 about 84%, seed average). At the end of task 10, we exchanged the second-layer response between the cap12′ network and the control network, resetting the Adam history in all arms. Here the offset was not fixed but was updated to follow the natural continuation of the source network. Over the next task of 6,000 updates, handing the control's response to the cap12′ network lowered the online accuracy from 80.8% to 19.7%, and handing the cap12′ response to the control raised it from 16.9% to 84.6% (Appendix E). This is the effect of an artificial intervention that shows the contribution of the response-related function; it is not a strict mediation rate of the natural benefit of the cap.

The effect of restoring the response was not reproduced by a fixed learning rate matched to the gradient-norm ratio or to the Adam displacement ratio at restoration; both controls fell below restoration in all six comparisons of the three settings (Appendix E).

In MLPs, we verified the four stages of the mechanism in order (loading by post-hoc analysis, the others by intervention). Learning creates the push, the mean and bias pathways carry it, stopping the width stops the collapse of random-label ELU, and restoring the response restores relearning. The next section verifies the same four stages in convolutional networks, where the input to a hidden layer moves with learning.

<!-- 日本語見出し: ## 5 CNN：上流が動く層で同じ四段を確かめる -->
## 5 CNN: verifying the same four stages in layers whose upstream changes

In convolutional networks, the inputs to hidden layers change with learning. We trained a network with 2 convolutional layers and 2 fully connected hidden layers on random-label CIFAR (1,200 images, 30 tasks, 30,000 updates per task, seeds 10–19) and real-label 5+1 CIFAR (seeds 2000–2009). We verified the four stages in the same order as in Section 4.

<!-- 日本語見出し: ### 5.1 押しは最終隠れ層でも学習が作る -->
### 5.1 Learning also creates the push in the final hidden layer

In a post-hoc analysis that replayed saved states of a leaky ReLU network, the readout of the final hidden layer f2 realigned with the current task at every observed boundary (ratio of $\kappa$ to its value at the end of task 1: 1.4–7.0; 10/10). There were 0 violations of the lower bound in Section 3.1. Through f2's own weight pathway, the push at the switch was in the sinking direction for 99–100% of units. Over the 200 replayed updates, 84–100% of f2 units sank. However, 97–100% of the first-order response of the position was carried by upstream layers. The f2 units that sank at switches recovered as a group within tasks and remained near the relative position $r\simeq-0.6$. Sinking accumulated in f1, c2, and c1 below f2. The direction of the push in the input layer c1 was an exception (Appendix H). Alignment is not limited to random labels. In real-label 5+1 CIFAR, the readout also aligned with the current task in all 467 states at the ends of hard tasks. This alignment was absent before the task (cos² 0.06–0.78 versus chance 0.002; Appendix H). With real labels, the new labels are not independent of the features. We compared the one-step push at the switch with a random-label model whose labels follow the empirical label distribution of the task. The direction of the FC2 push agreed in 96–98% of units, and the label term was 7–12% of the model term (saved states for 4 conditions × 3 budgets × 10 seeds; Appendix H). The random-label model predicts the direction of the push at the switch. However, in the 3 conditions other than ReLU, this push was on the sinking side for 50–55% of units, and sinking in real-label CNNs proceeds within tasks.

<!-- 日本語見出し: ### 5.2 経路：平均とbiasの両方を塞ぐ -->
### 5.2 Pathways: blocking both the mean and the bias

In a ReLU network, we added input color centering and EMA centering of all features (channel × position) from task 1 (CH′). The input-mean pathway was closed in all 4 layers. The push shifted to the bias pathway. Biases sank in all 4 layers, and the layers closed (bias share 1.00; death rates at task 30: 0.77–0.88). Which layer sank depended on how the pathways were blocked. With centering of channel means alone, f1 sank through position-specific means. Under CH′, c1 and c2 sank first. We added B to CH′, projecting the biases of all 4 hidden layers onto the interval of ±0.2 times the current minibatch width after every Adam update. This raised online accuracy over tasks 21–30 from 49.5% to 94.2% (improvement in all 10 seeds; Appendix H). As in Section 3.2, relearning was preserved only when both pathways were blocked.

<!-- 日本語見出し: ### 5.3 幅：非対称なELUだけが幅とともに沈む -->
### 5.3 Width: only asymmetric ELU sinks as the width grows

In real-label 5+1 CIFAR, extending the number of updates per task from 780 to 2,340 and 7,800 increased the FC2 width in all 4 conditions: ReLU, ELU, and 2 variants of Snake (from 6.7 to 31.6 for ELU). Only ELU sank and lost response as the width grew ($r$ −0.19→−0.73; mean derivative 0.65→0.27). Its online accuracy over the first 780 updates of late hard tasks fell by 1.17 points at 7,800 updates. Its online accuracy over the whole task was 98.2%, nearly the same as the 98.3% of kunekune (paired difference +0.1 points). The delay is therefore confined to initial adaptation, and attainment is not lost. Under ReLU, 85% of FC2 units were already dead at 780 updates (94% at 7,800 updates); this is a loss separate from the width. Extending the budget is not an intervention that moves the width alone.

Kunekune, whose tail slopes are 1 and whose curvature scale matches the width, did not sink. Although the width grew from 5.2 to 25.1, its relative position $r$ moved back from −0.81 to −0.27 and the mean derivative stayed at 0.9. Online accuracy over the first 780 updates rose by 4.6 points at 7,800 updates (registered decision; Appendix H). As in Section 3.3, only the activation whose zero is deepened by the width lost response, and the activation whose zero tracks the width did not. In terms of level, ELU at 780 updates ($\alpha=3.6$, outside the sign conditions of Section 3.3) ranked first. The intervention asks whether loss occurs; it is not a comparison of levels (Appendix F).

ELU in this setting has no loss for a cap to rescue. In a separate run in the same setting, a width cap held the FC2 width at 1.4 (34 in the natural network at the end of task 30) and kept the mean derivative at 1.00. Online accuracy over the first 780 updates fell by 5.1 points (10/10). Both networks reached 100% training accuracy at task end, and test accuracy under the cap was 0.2 points higher on average (descriptive; Appendix H). ELU in this setting did not deteriorate in late tasks as tasks accumulated. Extending the budget slowed only the first 780 updates.

<!-- 日本語見出し: ### 5.4 応答：予防が保った応答を交換する -->
### 5.4 Response: exchanging the response preserved by prevention

Starting from the ends of task 30 under CH′ and CH′＋B, we exchanged the response fields of all 4 hidden layers using the operation in Section 4.4. Online accuracy over the first 3,000 updates of the next task rose from 14.6% to 58.2% in the CH′ recipient (10/10). It fell from 71.4% to 60.0% in the CH′＋B recipient (9/10). The improvement in the rescue direction persisted to task end (online accuracy over the last 3,000 updates: 37.4% versus 99.2%; Appendix H). In the reverse direction, the transplanted low response reopened within 100 updates, and the degradation did not persist into the late part of the task. At random-label switches, CE reflects confidence on the previous task. We therefore compared relearning using online accuracy. Adding the same B after degradation reopened the response, but the accuracy improvement remained inconclusive (+2.9 points; 7/10). Blocking the pathways is preventive rather than curative.

The four stages also held in convolutional networks. What changed was that upstream layers carried the position and that sinking accumulated below the final hidden layer.

<!-- 日本語見出し: ## 6 議論 -->
## 6 Discussion

**Common links.** A single mechanism held across two architectures. Learning creates the push at the switch. The input mean, bias, and moving upstream layers carry it to the position. Asymmetric activations and width growth deepen the sinking. Units that have sunk lose their response, which reduces relearning. We verified each link through interventions or analyses of saved states. Blocking the pathways preserved relearning (200 tasks in MLPs, 30 tasks in CNNs). Limiting the width prevented collapse (the cap for random-label ELU). Restoring the response restored relearning (three MLP settings, all 4 CNN layers). There are also settings in which initial adaptation is instead slowed even when the width and the response are preserved (ELU in real-label CNNs). The aspect that changed across architectures was the identity of the carrier, which moved from a fixed input mean to upstream layers that move with learning. In CNNs, f2, adjacent to the readout, recovers within tasks, and sinking accumulates in f1, c2, and c1 below it. The intervention from the activation side (kunekune) moved the width stage from the side opposite to the cap.

**Scope.** We distinguish prevention from recovery, online accuracy from CE, speed of attainment from level, and death on a probe (a fixed evaluation set) from strict death. We do not claim monotonic sinking in all layers or irreversibility. Evaluation covered 200 tasks in random-label MLPs, 30 tasks in CNNs, and the single task after an exchange. The MLP centering, cap, and exchange experiments, the kunekune scale control and the budget-extension decision, and the CNN B and exchange experiments were registered runs. CNN loading was analyzed post hoc on saved states. We do not report the fraction of the benefit of natural interventions mediated by response or width alone.

**Open questions.** Open questions remain about the fraction of the benefit of natural interventions carried by response and about the derivation of width growth itself. Direct response exchange in real-label CNNs is a future extension.

<!-- 日本語見出し: ## 参考文献（字数外） -->
## References (excluded from the word count)

- Ash, J. T.; Adams, R. P. (2020). On Warm-Starting Neural Network Training. NeurIPS 2020 (Advances in Neural Information Processing Systems 33), 3884–3894. arXiv:1910.08475.
- Cornacchia, E.; Hązła, J.; Nachum, I.; Yehudayoff, A. (2021). Regularization by Misclassification in ReLU Neural Networks. arXiv:2111.02154 (preprint).
- Dohare, S.; Hernandez-Garcia, J. F.; Lan, Q.; Rahman, P.; Mahmood, A. R.; Sutton, R. S. (2024). Loss of plasticity in deep continual learning. Nature 632(8026), 768–774. doi:10.1038/s41586-024-07711-7.
- Kumar, S.; Marklund, H.; Van Roy, B. (2025). Maintaining Plasticity in Continual Learning via Regenerative Regularization. CoLLAs 2024, PMLR 274, 410–430. arXiv:2308.11958.
- Li, Z.; You, C.; Bhojanapalli, S.; Li, D.; Rawat, A. S.; Reddi, S. J.; Ye, K.; Chern, F.; Yu, F.; Guo, R.; Kumar, S. (2023). The Lazy Neuron Phenomenon: On Emergence of Activation Sparsity in Transformers. ICLR 2023 (short version); full version arXiv:2210.06313v2.
- Lillo, L.; Cheney, N. (2026). Activation Function Design Sustains Plasticity in Continual Learning. ICLR 2026; arXiv:2509.22562.
- Lyle, C.; Zheng, Z.; Khetarpal, K.; van Hasselt, H.; Pascanu, R.; Martens, J.; Dabney, W. (2025). Disentangling the Causes of Plasticity Loss in Neural Networks. CoLLAs 2024, PMLR 274, 750–783. arXiv:2402.18762.
- Shvetsov, E.; Serkov, A.; Shokorov, V.; Redko, D.; Goloshchapov, V.; Burnaev, E. (2026). Bug or Feature²: Weight Drift and Activation Sparsity. arXiv:2605.17659v3 (preprint).
- Sokar, G.; Agarwal, R.; Castro, P. S.; Evci, U. (2023). The Dormant Neuron Phenomenon in Deep Reinforcement Learning. ICML 2023, PMLR 202, 32145–32168.
- Ziyin, L.; Hartwig, T.; Ueda, M. (2020). Neural Networks Fail to Learn Periodic Functions and How to Fix It. NeurIPS 2020 (Advances in Neural Information Processing Systems 33), 1583–1594. arXiv:2006.08195.
- (Added on Oct 23; bibliographic details not yet verified. To be reordered during citation checking.) Lyle, C.; Rowland, M.; Dabney, W. (2022). Understanding and Preventing Capacity Loss in Reinforcement Learning. ICLR 2022. arXiv:2204.09560.
- Lee, H.; Cho, H.; Kim, H.; Kim, D.; Min, D.; Choo, J.; Lyle, C. (2024). Slow and Steady Wins the Race: Maintaining Plasticity with Hare and Tortoise Networks. ICML 2024. arXiv:2406.02596.
- Katharopoulos, A.; Fleuret, F. (2018). Not All Samples Are Created Equal: Deep Learning with Importance Sampling. ICML 2018. arXiv:1803.00942.
- Liu, S.; Niles-Weed, J.; Razavian, N.; Fernandez-Granda, C. (2020). Early-Learning Regularization Prevents Memorization of Noisy Labels. NeurIPS 2020. arXiv:2007.00151.
