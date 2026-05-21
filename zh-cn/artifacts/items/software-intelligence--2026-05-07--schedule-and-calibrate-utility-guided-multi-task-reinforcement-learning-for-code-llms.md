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
## 摘要
ASTOR 通过任务效用来选择数据并调节 KL 正则化，用强化学习在四类编码任务上训练一个代码 LLM。论文称，一个共享模型在 Qwen2.5-Coder-7B 和 Qwen3-8B 上都超过了按任务训练的 RL 专家模型和标准多任务 RL 基线。

## 问题
- 代码 RL 专家模型在各自任务上效果好，但每个任务部署一个模型会让内存和计算成本随任务数量增加。
- 单个专家模型对其他编码任务迁移效果差，因此代码理解、代码生成、单元测试生成和提交信息生成需要更好的联合训练。
- 现有多任务 RL 方法使用固定或均匀的任务混合方式，并采用一个共享更新策略，未充分处理任务难度、提示价值和跨任务梯度影响。

## 方法
- ASTOR 用两个信号定义任务效用：表示学习潜力的 rollout 奖励方差，以及表示跨任务协同的梯度余弦相似度。
- 它先对效用做带温度缩放的 softmax，为每个任务分配训练配额，再在每个任务内部根据提示效用采样提示；提示效用由奖励方差和近期奖励进展决定。
- 它基于 GRPO，为每个任务设置单独的 KL 系数，并使用与当前任务效用相关的动态乘数。
- 奖励设置覆盖四类任务：代码 I/O 预测、代码生成、单元测试生成和提交信息生成；每类任务都有对应的可验证奖励或基于指标的奖励，并加入格式奖励。
- 实验使用 Qwen2.5-Coder-7B 和 Qwen3-8B，全局批大小为 128，每个样本 8 次 rollout，训练 400 步，硬件为 32 个 Ascend 910B-B3 NPU。

## 结果
- 在 Qwen2.5-Coder-7B 上，ASTOR 平均分达到 38.65，比最佳任务专用专家模型高 9.0%，比 Joint Learning 高 12.8%。
- 在 Qwen3-8B 上，ASTOR 平均分达到 44.29，比最佳任务专用专家模型的平均分 40.43 高 9.5%，比 Joint Learning 高 7.5%。
- 在 Qwen2.5-Coder-7B 的多任务基线对比中，ASTOR 比 Joint Learning 高 12.8%，比 Curriculum Learning 高 16.8%，比 Model Merging 高 19.2%。
- ASTOR 在 Qwen2.5-Coder-7B 的 10 个指标中有 8 个最佳，在 Qwen3-8B 的 10 个指标中全部最佳。
- Qwen3-8B 的任务结果示例：CRUXEval Input/Output 准确率 61.5/65.1，Aider-Polyglot pass@1/pass@2 为 51.1/54.8，Defects4J 行/分支覆盖率 38.1/32.0，编译率 56.6，MCMDEval+ BLEU/ROUGE/METEOR 为 41.2/22.5/20.0。
- 消融实验显示，调度和 KL 校准都有作用：对于 Qwen2.5-Coder-7B，移除任务和提示调度后，Code Gen pass@1 从 41.5 降至 31.9，MCMDEval+ METEOR 从 20.2 降至 16.6。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06111v1](https://arxiv.org/abs/2605.06111v1)
