---
source: arxiv
url: http://arxiv.org/abs/2603.04715v1
published_at: '2026-03-05T01:32:40'
authors:
- Gavin Wong
topics:
- world-models
- model-based-rl
- dreamer
- particle-filter
- latent-planning
relevance_score: 0.18
run_id: materialize-outputs
---

# Probabilistic Dreaming for World Models

## Summary
本文提出 ProbDreamer，在 Dreamer 世界模型中引入粒子滤波式“做梦”，以并行保留多个可能未来并减少连续高斯潜变量对多峰未来的平均化偏差。作者在 MPE SimpleTag 上展示了该方法可提升性能与稳定性，但更激进的束搜索与剪枝版本反而显著失效。

## Problem
- Dreamer 虽然学习了潜状态分布，但想象阶段通常只采样**单一路径**，限制了对多种可能未来的探索。
- 连续高斯潜变量在面对**互斥的多峰未来**时，容易把“左/右”等不同可能性平均成不存在的中间状态，导致决策迟疑或错误。
- 这个问题重要，因为世界模型 RL 的样本效率与鲁棒性很大程度取决于“想象”未来的质量；如果想象错误，策略学习会被系统性误导。

## Approach
- 用 **particle filter** 替代单一潜变量采样：在每个时间步维护 K 个潜在粒子，形成对未来潜状态的经验分布，从而同时保留多个互斥假设。
- 在每个粒子上并行做 latent rollout，让 agent 一次训练能“梦到”多条未来，而不是只看一条 imagined trajectory。
- 进一步提出 **latent beam search**：每个粒子在每一步分叉出 N 个候选动作，得到 K×N 条分支，再用世界模型向前传播。
- 为控制计算量，作者用近似“**free energy**”打分来剪枝分支：分数由 critic 预测价值与 prior ensemble 的分歧（近似 epistemic uncertainty）共同决定，偏向高回报且高信息增益的轨迹。
- 实现上以 Dreamer-v3 为骨干，但把离散潜变量换回连续高斯潜变量，以验证“连续潜变量 + 粒子表示”能否兼顾平滑梯度与多峰表达。

## Results
- 在 **MPE SimpleTag** 上，最佳轻量版 **ProbDreamer Lite (K=2, N=1, T=10)** 取得 **-8.79 ± 0.68**，优于 **BaseDreamer 1: -9.21 ± 0.80** 和 **BaseDreamer 2: -9.74 ± 0.79**；文中总结为相对标准 Dreamer **提升 4.5%**。
- 该最佳 ProbDreamer 在 **5 个随机种子中的 4 个** 上优于基线，并带来 **28% 更低的 episode return 方差**，说明策略更稳健。
- 更复杂的完整版并未成功：**ProbDreamer Full 1 (K=2, N=4, T=10)** 只有 **-53.78 ± 12.14**，**ProbDreamer Full 2 (K=8, N=1, T=22)** 为 **-26.84 ± 23.03**，远差于基线。
- 作者据此声称：**粒子化潜状态表示本身有效**，但**高粒子数、latent beam search 与 free-energy pruning** 在当前实现下会造成严重退化。
- 文中还给出具体失败原因主张：K 从 1 增至 2 有益，但继续增大可能“拟合噪声”；value-based pruning 在无真实观测校正时会放大乐观幻觉；ensemble uncertainty 出现塌缩，去掉 curiosity 项几乎无差异。

## Link
- [http://arxiv.org/abs/2603.04715v1](http://arxiv.org/abs/2603.04715v1)
