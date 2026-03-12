---
source: arxiv
url: http://arxiv.org/abs/2603.02083v2
published_at: '2026-03-02T17:04:49'
authors:
- Siting Wang
- Xiaofeng Wang
- Zheng Zhu
- Minnan Pei
- Xinyu Cui
- Cheng Deng
- Jian Zhao
- Guan Huang
- Haifeng Zhang
- Jun Wang
topics:
- online-rl
- vision-language-action
- flow-matching
- embodied-ai
- likelihood-free-learning
relevance_score: 0.55
run_id: materialize-outputs
---

# $π$-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs

## Summary
本文提出 **π-StepNFT**，一种面向流式视觉-语言-动作（VLA）模型的在线强化学习方法，用无critic、无显式似然的方式解决训练难题。核心观点是：**探索空间变宽后，必须用更细粒度的逐步监督来稳定对齐与泛化**。

## Problem
- 流式 VLA 在机器人控制中表现强，但其多步 ODE/SDE 采样下的动作似然难以精确计算，导致标准策略梯度和在线 RL 难以直接应用。
- 仅用监督微调（SFT）或确定性 ODE 采样，策略容易坍缩到狭窄专家流形，测试时一旦偏离就缺乏局部纠错能力；而直接加噪扩展探索，又会因只看最终结果的粗粒度监督而失稳。
- 现有 value/critic 方法虽然可绕开似然，但容易对多模态视觉特征过拟合，影响 OOD 泛化，这对真实机器人部署很重要。

## Approach
- 用 **SDE 采样** 在训练时向去噪过程注入结构化噪声，主动扩大行为/探索空间，而不是局限在确定性 ODE 的窄轨迹上。
- 将监督目标从最终去噪结果 **x0** 改为**相邻一步的去噪转移** \(x_t \rightarrow x_{t^-}\)，即做逐步、局部、方差归一化的监督，降低噪声累积带来的高方差和错配问题。
- 不训练额外 value network，也不计算显式 likelihood；而是在当前策略更新方向上构造一对对称的“镜像分支” \(v^+, v^-\)，比较哪一支更能解释观测到的单步转移。
- 用 **logistic contrastive ranking loss** 代替 Diffusion-NFT 式的 weighted-MSE：成功轨迹推动正分支优于负分支，失败轨迹反向推动，形成更明确的“push-pull”优化信号，并避免作者所说的隐式分离惩罚。
- 每次优化只需**单次前向传播**，因此在计算上更轻量，也更适合在线 RL 的迭代更新。

## Results
- 在 **LIBERO** 基准上，作者声称 π-StepNFT 在 few-shot 设置中显著释放策略潜力，**相对 SFT 提升 32.9%**。
- 在 **ManiSkill** 的视觉多样化 **OOD/unseen** 场景上，方法**比 critic/value-based baseline 高 11.1%**，作者将其归因于避免了 critic 引发的多模态过拟合。
- 论文还声称该方法在 **few-shot robustness** 上具有竞争力，并在更复杂真实场景中更具可扩展性。
- 从机制上，作者强调该框架同时做到：**critic-free、likelihood-free、单步前向优化、逐步监督对齐**；这些是相对现有流式 VLA 在线 RL 方法的主要实用改进。
- 提供的摘录中没有更细的完整表格指标、具体 baseline 名称列表或统计显著性数字；最明确的量化结论就是 **LIBERO +32.9% vs SFT** 和 **ManiSkill OOD +11.1% vs critic-based baselines**。

## Link
- [http://arxiv.org/abs/2603.02083v2](http://arxiv.org/abs/2603.02083v2)
