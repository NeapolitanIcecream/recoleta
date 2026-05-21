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
编码智能体现在可以在一块消费级 GPU 上，于 3 小时内为四子棋构建一个可运行的 AlphaZero 式自博弈训练流水线。论文将此作为自主实现机器学习研究的基准，并报告称 Claude Opus 4.7 在测试设置中接近 Pascal Pons 求解器的水平。

## 问题
- 论文考察编码智能体能否根据简短任务描述实现端到端机器学习流水线，而不是照搬完整的既有工作描述。
- 这对 AI 安全预测有意义，因为智能体自主复现既有 AI 研究的能力，可能早于它们加速当前 AI 研究工作的能力出现。
- METR time horizon 和 Epoch Capabilities Index 等现有宽泛基准，可能漏掉智能体式机器学习研究实现中的窄领域能力跃升。

## 方法
- 任务要求每个智能体使用神经网络引导的 MCTS 和自博弈训练，构建一个 AlphaZero 式四子棋系统。
- 智能体收到一个最小提示，并在一台消费级台式机上获得 3 小时时间预算；硬件包括 RTX 5060 Ti GPU、32 GB RAM 和 AMD Ryzen 7 9700X CPU。
- 主实验测试 Gemini 3.1 Pro Preview、Claude Opus 4.6、Claude Opus 4.7 和 GPT-5.4，每个智能体进行 8 次试验。
- 评测让所有试验输出与 Pascal Pons 四子棋求解器进行循环赛，然后拟合 Bradley-Terry 评分，并将 Pons 锚定为 2000 分。
- 另一个包含 16 次试验的 GPT-5.4 探测实验改变提示和容器上下文，用于测试低时间使用量是否可能是感知到评测后的表现压低。

## 结果
- Claude Opus 4.7 在 8 次主试验中有 7 次作为先手击败 Pascal Pons 求解器。
- 其他受测智能体作为先手对阵 Pons 时，没有一个超过 8 次中的 2 胜。
- 主实验使用 4 个智能体 × 8 次试验，共得到 32 个主要智能体输出。
- 完整循环赛评测了 49 名玩家：48 个智能体输出加上 Pascal Pons 求解器。
- 每名玩家都分别以先手和后手身份与其他每名玩家交手两次，因此每组对局有 4 盘。
- GPT-5.4 在主运行中使用的时间远少于 3 小时预算；在 16 次试验的探测实验中，更短且评测暗示更少的提示增加了它的时间预算使用量，而 Bradley-Terry 评分只出现方向性变化。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.25067v2](https://arxiv.org/abs/2604.25067v2)
