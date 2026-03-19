---
source: arxiv
url: http://arxiv.org/abs/2603.04715v1
published_at: '2026-03-05T01:32:40'
authors:
- Gavin Wong
topics:
- world-model
- model-based-rl
- dreamer
- particle-filter
- uncertainty-estimation
relevance_score: 0.85
run_id: materialize-outputs
language_code: zh-CN
---

# Probabilistic Dreaming for World Models

## Summary
本文提出 ProbDreamer，在 Dreamer 世界模型中引入粒子滤波式的概率“做梦”，以同时保留多个可能未来而不是只想象一条轨迹。它在多模态未来预测的简单 RL 场景中带来小幅但稳定的性能与鲁棒性提升，同时也暴露了主动剪枝和不确定性估计的明显局限。

## Problem
- 现有 Dreamer 虽然学习了潜变量分布，但想象阶段通常只采样**单个 latent state**并展开**单条 imagined trajectory**，会遗漏互斥未来的多样性。
- 连续高斯潜变量有良好的梯度性质，但面对“向左/向右”这类**多峰未来**时，单峰高斯可能平均成不存在的“中间状态”，导致决策迟疑或错误。
- 这很重要，因为世界模型 RL 的样本效率和稳健性很大程度取决于 agent 能否在想象中正确表示不确定、多模态的未来，并据此学习策略。

## Approach
- 基于 Dreamer-v3 搭建 baseline，但将离散 categorical latents 改回**连续 Gaussian latents**，以测试是否能结合连续潜变量的平滑优化优势与概率方法的多假设表示能力。
- 用**particle filter**替代单一样本想象：在每个时间步保留 K 个 latent particles，并行传播，形成对未来 latent 分布的经验近似，从而同时维护多个互斥假设。
- 用**latent beam search**让每个 particle 对 N 个候选动作分支，得到 K×N 条 imagined branches，以扩大想象时的动作探索覆盖面。
- 用**free-energy 风格剪枝**控制计算量：按 critic 预测价值和 prior ensemble 分歧近似的 epistemic uncertainty 对分支打分，保留高价值/高信息增益轨迹，目标写为 \(F_t^k = V_\phi(h_t^k,z_t^k) + \beta \sigma_{ens}^2\)。
- 在 MPE SimpleTag 上评估；训练时每轮收集 \(10^3\) 个真实环境步，再进行 \(2\times10^4\) 步 latent imagination；通过 150 次 Bayesian Optimization 搜索超参，并从中选 6 个 finalist 在 5 个随机种子、100 个固定测试 episode 上比较。

## Results
- 在 **MPE SimpleTag** 上，最佳模型是 **ProbDreamer Lite 1**（\(K=2, N=1, T=10\)），得分 **-8.79 ± 0.68**；优于 **BaseDreamer 1** 的 **-9.21 ± 0.80** 和 **BaseDreamer 2** 的 **-9.74 ± 0.79**（文中注明 **0 is perfect performance**）。
- 论文明确声称：相对标准 Dreamer，**ProbDreamer Lite 平均提升 4.5% 分数**，并带来 **28% 更低的 episode return 方差**，说明策略更稳健。
- 种子层面，作者称 Lite 版本在 **5 个 seed 中有 4 个**优于 BaseDreamer，并在定性分析中表现为更快响应 predator 从“CHASE”到“INTERCEPT”的策略切换，而 baseline 更容易短暂停滞。
- 更复杂的 **Full ProbDreamer** 并未成功：例如 **ProbDreamer Full 1**（\(K=2,N=4,T=10\)）只有 **-53.78 ± 12.14**，**ProbDreamer Full 2**（\(K=8,N=1,T=22\)）为 **-26.84 ± 23.03**，显著差于 baseline，说明 beam search + pruning 在该实现下会严重退化。
- 结果还显示粒子数并非越大越好：从 **\(K=1\)** 到 **\(K=2\)** 有收益，但更高 **\(K\)** 可能出现“particle saturation”，作者推测与该任务主要只有 **2 种 predator 策略模式**有关。
- 关于不确定性建模，文中没有给出单独的定量 ablation 数字，但明确报告：ensemble disagreement 很快塌缩，去掉 curiosity 项后差异很小，表明当前 free-energy 剪枝和 epistemic uncertainty 估计未能带来预期收益。

## Link
- [http://arxiv.org/abs/2603.04715v1](http://arxiv.org/abs/2603.04715v1)
