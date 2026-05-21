---
source: arxiv
url: https://arxiv.org/abs/2605.08013v1
published_at: '2026-05-08T17:02:31'
authors:
- Haoyang Su
- Ying Wen
topics:
- cli-agents
- agentic-rl
- code-intelligence
- credit-assignment
- workspace-context
- software-agents
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Learning CLI Agents with Structured Action Credit under Selective Observation

## Summary
## 摘要
这篇论文通过更准确地给 shell 动作分配 credit，并选择有用的初始工作区视图，来训练 CLI 编码 agent。主要主张是，基于 AST 的动作 credit 加上 σ-Reveal，可以提升 Qwen3-14B 在多轮文件系统任务上的表现。

## 问题
- CLI agent 必须在只有部分上下文的大型代码仓库中行动，因此模型在运行任何命令前可能漏掉与任务相关的文件。
- 训练反馈通常是来自终端输出或文件状态的稀疏最终奖励，因此标准 RL 很难判断哪些 shell 命令有帮助，哪些有害。
- 这一点对代码 agent 很重要，因为真实的软件工作会在多轮中进行搜索、执行、编辑和验证，而不是单次输入输出预测。

## 方法
- σ-Reveal 在 token 预算内选择初始文件树视图。它根据任务名匹配、树深度和文件扩展名先验为文件和目录打分，然后保留一个子树闭合的上下文。
- A3 使用 bash AST 解析每条 shell 命令，并将其转换为包含控制节点、命令动词和归一化字面量的结构签名。
- 该方法在这些 AST 签名上使用归一化 Levenshtein 距离比较 shell 动作，因此即使路径或字面量不同，相似命令也可以共享 credit。
- A3 从三个信号构建每一轮的 advantage：episode 级相对回报、相对于结构相似动作的轮级残差，以及抽象动作历史分支上的树级 margin。
- 融合后的 advantage 使用序列级 PPO 风格损失来训练策略，不需要学习型 critic，也不需要外部 judge 来做 credit assignment。

## 结果
- ShellOps 包含 1,624 个任务，其中 714 个分布内任务用于训练和评估。ShellOps-Pro 增加了 150 个更难的分布外任务，包含 4,063 个文件，覆盖 42 种可读文本扩展名以及无扩展名文件，平均每个任务 27.1 个文件。
- 在精确匹配 ShellOps 字符串任务上，带 σ-Reveal 的 A3 得分为 48.5%，表中最强的非 A3 baseline 为 27.5%。在 ShellOps 混合任务上，它得分为 24.6%，最强的非 A3 baseline 为 11.3%。
- 在 ShellOps 文件编辑任务上，A3 vanilla 得分为 26.5%，带 σ-Reveal 的 A3 得分为 25.7%，最强的非 A3 baseline 为 11.9%。
- 在 DataBench 精确匹配上，带 σ-Reveal 的 A3 得分为 77.9%，GSPO 为 70.1%。在 TableBench 上，它得分为 31.6%，RetroAgent 为 25.0%。
- ShellOps 上的 Pass@3 / Pass@5 在 A3 加 σ-Reveal 下达到 46.2% / 55.7%，所示最强非 A3 baseline 为 22.3% / 28.6%。
- ShellOps-Pro 摘录报告了 horizon 6 / 8 / 10 下的 frontier baseline：Kimi-K2.6 得分为 45.9 / 47.9 / 53.3，GLM-5.1 得分为 34.7 / 39.1 / 40.7，Qwen3-235B-A22B 得分为 26.7 / 29.3 / 28.3。摘录称 A3 在更长 horizon 下达到 Qwen3-235B-A22B 的区间，但所提供文本中看不到 A3 在 ShellOps-Pro 上的确切数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08013v1](https://arxiv.org/abs/2605.08013v1)
