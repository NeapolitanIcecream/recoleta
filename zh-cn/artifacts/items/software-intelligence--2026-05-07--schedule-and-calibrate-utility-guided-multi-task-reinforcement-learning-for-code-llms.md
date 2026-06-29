---
source: arxiv
url: https://arxiv.org/abs/2605.06111v1
published_at: '2026-05-07T12:24:53'
authors:
- Yujia Chen
- Yang Ye
- Xiao Chu
- Yuchi Ma
- Cuiyun Gao
topics:
- code-llms
- multi-task-rl
- reinforcement-learning
- code-intelligence
- automated-software-engineering
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Schedule-and-Calibrate: Utility-Guided Multi-Task Reinforcement Learning for Code LLMs

## Summary
## 总结
ASTOR 通过任务效用来选择数据并调整 KL 正则化，用强化学习在四个编码任务上训练一个代码 LLM。论文声称，在 Qwen2.5-Coder-7B 和 Qwen3-8B 上，一个共享模型同时超过了按任务训练的 RL 专家和标准多任务 RL 基线。

## 问题
- 代码 RL 专家在各自任务上表现很好，但随着任务数增加，为每个任务部署一个模型会提高内存和计算成本。
- 单个专家迁移到其他编码任务的效果较差，因此代码理解、代码生成、单元测试生成和提交信息生成需要更好的联合训练。
- 现有多任务 RL 方法使用固定或统一的任务混合方式和单一共享更新策略，忽略了任务难度、提示价值和跨任务梯度影响。

## 方法
- ASTOR 用两个信号定义任务效用：rollout 奖励方差表示学习潜力，梯度余弦相似度表示跨任务协同。
- 它先用带温度缩放的 softmax 根据效用分配每个任务的训练配额，再按任务内的提示效用采样提示。提示效用由奖励方差和近期奖励进展计算。
- 它基于 GRPO，为每个任务设置单独的 KL 系数，并用一个与当前任务效用相关的动态乘子调整。
- 奖励设置覆盖四个任务：Code I/O Prediction、Code Generation、Unit Test Generation 和 Commit Message Generation，每个任务都有对应的可验证奖励或基于指标的奖励，以及格式奖励。
- 实验使用 Qwen2.5-Coder-7B 和 Qwen3-8B，全局 batch size 为 128，每个样本 8 次 rollout，训练 400 步，以及 32 个 Ascend 910B-B3 NPU。

## 结果
- 在 Qwen2.5-Coder-7B 上，ASTOR 的平均分达到 38.65，超过最佳按任务专家 9.0%，也超过 Joint Learning 12.8%。
- 在 Qwen3-8B 上，ASTOR 的平均分达到 44.29，超过最佳按任务专家的平均分 40.43 9.5%，也超过 Joint Learning 7.5%。
- 在 Qwen2.5-Coder-7B 的多任务基线对比中，ASTOR 比 Joint Learning 提高 12.8%，比 Curriculum Learning 提高 16.8%，比 Model Merging 提高 19.2%。
- ASTOR 在 Qwen2.5-Coder-7B 的 10 个指标中拿到 8 个最佳结果，在 Qwen3-8B 的 10 个指标中全部最好。
- Qwen3-8B 的示例任务结果包括：CRUXEval Input/Output 准确率 61.5/65.1，Aider-Polyglot pass@1/pass@2 为 51.1/54.8，Defects4J 行/分支覆盖率 38.1/32.0，编译率 56.6，MCMDEval+ 的 BLEU/ROUGE/METEOR 为 41.2/22.5/20.0。
- 消融实验显示，调度和 KL 校准都重要：在 Qwen2.5-Coder-7B 上，去掉任务和提示调度后，Code Gen pass@1 从 41.5 降到 31.9，MCMDEval+ 的 METEOR 从 20.2 降到 16.6。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06111v1](https://arxiv.org/abs/2605.06111v1)
