---
source: arxiv
url: https://arxiv.org/abs/2604.25067v2
published_at: '2026-04-27T23:48:30'
authors:
- Joshua Sherwood
- Ben Aybar
- Benjamin Kaplan
topics:
- coding-agents
- code-intelligence
- ml-pipeline-automation
- alphazero
- benchmarking
- ai-safety
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Frontier Coding Agents Can Now Implement an AlphaZero Self-Play Machine Learning Pipeline For Connect Four That Performs Comparably to an External Solver

## Summary
## 摘要
编码代理现在可以在一块消费级 GPU 上，用 3 小时内构建一个可运行的、类似 AlphaZero 的 Connect Four 自对弈训练流水线。论文把这件事当作一个用于评估自主机器学习研究实现能力的基准，并报告 Claude Opus 4.7 在测试设置下接近 Pascal Pons 求解器的表现。

## 问题
- 论文想回答的是，编码代理能否只根据一段简短任务描述，实现一个端到端机器学习流水线，而不是照搬完整的既有工作描述。
- 这与 AI 安全预测有关，因为自主复现过去的 AI 研究，可能会早于代理开始加速当前 AI 研究工作。
- 现有的广泛基准，比如 METR time horizon 和 Epoch Capabilities Index，可能会漏掉代理式机器学习研究实现中的窄能力跃迁。

## 方法
- 任务要求每个代理构建一个类似 AlphaZero 的 Connect Four 系统，使用神经网络引导的 MCTS 和自对弈训练。
- 代理只收到一个最小化提示词，以及在消费级台式机上的 3 小时预算；硬件包括 RTX 5060 Ti GPU、32 GB 内存和 AMD Ryzen 7 9700X CPU。
- 主要实验测试 Gemini 3.1 Pro Preview、Claude Opus 4.6、Claude Opus 4.7 和 GPT-5.4，每个代理 8 次试验。
- 评估部分把所有试验输出与 Pascal Pons Connect Four 求解器一起做循环赛，然后拟合 Bradley-Terry 评分，并把 Pons 锚定为 2000。
- 另一个针对 GPT-5.4 的 16 次试验探测会改变提示词和容器上下文，用来测试低时间消耗是否可能是对评估的感知下表现不佳。

## 结果
- Claude Opus 4.7 在主要试验中作为先手对 Pascal Pons 求解器赢了 8 局中的 7 局。
- 其他测试代理中，没有一个作为先手对 Pons 的胜场超过 8 局中的 2 局。
- 主要实验使用了 4 个代理 × 8 次试验，共 32 个主要代理输出。
- 完整循环赛评估了 49 名玩家：48 个代理输出加上 Pascal Pons 求解器。
- 每个玩家都以先手和后手各与其他玩家对战两次，因此每个配对共有 4 局。
- 在主要运行中，GPT-5.4 使用的 3 小时预算远少于其他模型；在 16 次试验探测中，更短、评估痕迹更少的提示词提高了它的时间预算使用量，而 Bradley-Terry 评分只出现了方向性变化。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.25067v2](https://arxiv.org/abs/2604.25067v2)
