---
source: arxiv
url: https://arxiv.org/abs/2605.04361v1
published_at: '2026-05-05T23:46:33'
authors:
- Saranyan Vigraham
topics:
- multi-agent-software-engineering
- agent-orchestration
- code-intelligence
- software-design
- context-injection
- llm-evaluation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# When Context Hurts: The Crossover Effect of Knowledge Transfer on Multi-Agent Design Exploration

## Summary
## 摘要
论文表明，在多智能体软件设计中，上下文迁移可能提高也可能降低设计权衡覆盖率，取决于任务在无上下文条件下的基线探索水平。作者提出先运行一次无上下文试验，用它诊断是否应注入工件。

## 问题
- 多智能体编码系统通常默认加入对话记录、设计文档、代码或检索到的文档，并假设额外上下文会改进工作结果。
- 对软件设计来说，额外上下文可能让智能体锚定在某个方案上，减少对架构权衡的探索。
- 这影响智能体编排，因为看起来正确的代码可能掩盖了狭窄的设计搜索。

## 方法
- 作者在 10 个软件设计任务上运行了 2,700 多次 Claude Sonnet 4 多智能体设计实验。
- 每个团队使用 5 个具有不同角色设定的智能体；条件包括对话记录、拓扑/权衡列表、设计文档、反模式、代码、无上下文和无关上下文。
- 他们用直接权衡评估来衡量设计探索：一个评估 LLM 检查每次讨论是否涉及已知权衡，并计算覆盖率。
- 他们在 2 个任务上设置 4 个提示压力水平来测试机制，以区分自然收敛和由指令驱动的收敛。

## 结果
- 基线权衡覆盖率从限流器任务的 0.033 到 LRU 缓存任务的 0.540 不等，每个任务 n=20 次试验。
- 在限流器任务上，反模式把覆盖率从 0.033 提高到 0.700（+0.667，p<0.001，d=3.41），对话记录把覆盖率提高到 0.592（+0.558，p<0.001，d=2.71）。
- 在 Kubernetes operator 任务上，对话记录把覆盖率从 0.475 降到 0.256（-0.219，p<0.001，d=-1.14），代码把覆盖率降到 0.325（-0.150，p=0.016）。
- 基线探索能够预测最佳工件效果，Pearson r=-0.821（p<0.001），Spearman rho=-0.624（p=0.024）。
- 在 ML 训练流水线任务上，无关上下文优于所有相关工件：覆盖率为 0.444（+0.087），相比之下，拓扑为 0.431，基线为 0.356，对话记录为 0.231（相对基线 p=0.005），代码为 0.256（相对基线 p=0.030）。
- 论文主张有条件地注入上下文：先运行一次成本低的无上下文基线试验，然后只在基线探索较低时加入工件。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04361v1](https://arxiv.org/abs/2605.04361v1)
