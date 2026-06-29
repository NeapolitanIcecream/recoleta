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
## 总结
这篇论文通过改进 shell 动作的 credit 分配，并选择一个有用的初始工作区视图，来训练 CLI 代码代理。它的核心主张是，基于 AST 的动作 credit 加上 σ-Reveal，能提升 Qwen3-14B 在多轮文件系统任务上的表现。

## 问题
- CLI 代理必须在大规模仓库里基于部分上下文执行操作，因此模型在运行任何命令之前，就可能错过与任务相关的文件。
- 训练反馈通常只来自终端输出或文件状态的稀疏最终奖励，所以标准 RL 很难判断哪些 shell 命令起了作用，哪些命令拖了后腿。
- 这对代码代理很重要，因为真实的软件工作要在多轮中完成搜索、执行、编辑和验证，而不是单次输入输出预测。

## 方法
- σ-Reveal 在 token 预算内选择初始文件树视图。它用任务名匹配、树深度和文件扩展名先验给文件和目录打分，然后保留一个子树闭合的上下文。
- A3 用 bash AST 解析每条 shell 命令，并把它转成包含控制节点、命令动词和归一化字面量的结构签名。
- 该方法在这些 AST 签名上使用归一化 Levenshtein 距离比较 shell 动作，所以即使路径或字面量不同，相似命令也可以共享 credit。
- A3 从三个信号构建每一步的 advantage：episode 级相对回报、针对结构相似动作的 step 级残差，以及针对抽象动作历史分支的 tree 级 margin。
- 融合后的 advantage 用序列级 PPO 风格损失训练策略，不需要学习 critic，也不需要外部 judge 来做 credit 分配。

## 结果
- ShellOps 包含 1,624 个任务，其中 714 个分布内任务用于训练和评估。ShellOps-Pro 额外加入 150 个更难的分布外任务，共有 4,063 个文件，按 42 种可读文本扩展名和无扩展名文件计算，平均每个任务 27.1 个文件。
- 在 ShellOps 的 exact-match 字符串任务上，A3 加 σ-Reveal 得到 48.5%，表中最强的非 A3 基线是 27.5%。在 ShellOps 混合任务上，它得到 24.6%，最强的非 A3 基线是 11.3%。
- 在 ShellOps 文件编辑任务上，A3 vanilla 得到 26.5%，A3 加 σ-Reveal 得到 25.7%，最强的非 A3 基线是 11.9%。
- 在 DataBench 的 exact match 上，A3 加 σ-Reveal 得到 77.9%，GSPO 是 70.1%。在 TableBench 上，它得到 31.6%，RetroAgent 是 25.0%。
- ShellOps 上的 Pass@3 / Pass@5 在 A3 加 σ-Reveal 下达到 46.2% / 55.7%，而图中显示的最强非 A3 基线是 22.3% / 28.6%。
- ShellOps-Pro 摘要给出了 horizon 6 / 8 / 10 上的前沿基线：Kimi-K2.6 得分为 45.9 / 47.9 / 53.3，GLM-5.1 得分为 34.7 / 39.1 / 40.7，Qwen3-235B-A22B 得分为 26.7 / 29.3 / 28.3。摘要说 A3 在更长 horizon 上达到了 Qwen3-235B-A22B 的区间，但给出的文本里没有显示 A3 在 ShellOps-Pro 上的精确数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08013v1](https://arxiv.org/abs/2605.08013v1)
