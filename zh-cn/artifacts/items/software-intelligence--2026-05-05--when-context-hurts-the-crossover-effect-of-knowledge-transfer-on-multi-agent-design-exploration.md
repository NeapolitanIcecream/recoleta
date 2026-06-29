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
论文表明，在多智能体软件设计中，知识传递可能提高也可能降低设计权衡覆盖率，取决于任务的无上下文基线探索水平。作者建议先做一次无上下文试验，判断是否该注入相关材料。

## 问题
- 多智能体编码系统常默认加入对话记录、设计文档、代码或检索到的文档，假设更多上下文会改善结果。
- 在软件设计里，额外上下文可能让智能体锚定到一个方案，减少对架构权衡的探索。
- 这对智能体编排很重要，因为看起来正确的代码可能掩盖狭窄的设计搜索。

## 方法
- 作者在 10 个软件设计任务上进行了 2,700 多次 Claude Sonnet 4 多智能体设计运行。
- 每个团队使用 5 个具有不同角色设定的智能体；条件包括对话记录、拓扑/权衡清单、设计文档、反模式、代码、无上下文和无关上下文。
- 他们通过直接的权衡评估来测量设计探索：一个评估用 LLM 检查每次讨论是否涉及已知权衡，并计算覆盖率。
- 他们在 2 个任务上通过 4 个层级改变提示压力，测试机制，以区分自然收敛和指令驱动的收敛。

## 结果
- 基线权衡覆盖率在 rate limiter 任务上为 0.033，在 LRU cache 任务上为 0.540，每个任务做了 n=20 次试验。
- 在 rate limiter 上，反模式把覆盖率从 0.033 提高到 0.700（+0.667，p<0.001，d=3.41），对话记录把它提高到 0.592（+0.558，p<0.001，d=2.71）。
- 在 Kubernetes operator 上，对话记录把覆盖率从 0.475 降到 0.256（-0.219，p<0.001，d=-1.14），代码把它降到 0.325（-0.150，p=0.016）。
- 基线探索对最佳材料效果有预测力，Pearson r=-0.821（p<0.001），Spearman rho=-0.624（p=0.024）。
- 在 ML training pipeline 上，无关上下文超过了所有相关材料：覆盖率为 0.444（+0.087），而拓扑为 0.431，基线为 0.356，对话记录为 0.231（相对基线 p=0.005），代码为 0.256（相对基线 p=0.030）。
- 论文主张有条件地注入上下文：先做一次低成本的无上下文基线试验，只有在基线探索较低时才加入材料。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04361v1](https://arxiv.org/abs/2605.04361v1)
