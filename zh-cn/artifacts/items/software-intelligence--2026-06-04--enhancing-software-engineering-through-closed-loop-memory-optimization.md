---
source: arxiv
url: https://arxiv.org/abs/2606.05646v1
published_at: '2026-06-04T03:17:21'
authors:
- Xuehang Guo
- Zora Zhiruo Wang
- Qingyun Wang
- Graham Neubig
- Xingyao Wang
topics:
- software-engineering-agents
- agent-memory
- code-intelligence
- swe-bench
- reinforcement-learning
- llm-finetuning
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Enhancing Software Engineering Through Closed-Loop Memory Optimization

## Summary
## 摘要
MemOp 通过只保留能改善下游任务指标的记忆，来训练软件工程代理的记忆模型。论文声称，这种方法在 SWE-Bench Verified 上带来更好的成功率和效率，同时降低了计算成本。

## 问题
- 软件工程代理把每个问题都当作独立回合处理，因此它们会重新摸清仓库结构、重复错误修改，并花费 token 重新构建上下文。
- 现有记忆方法缺少一个与任务无关的效用检验，所以一条已存储的笔记可能有用、冗余或有害，却没有清晰的测量方式。
- 这个问题之所以重要，是因为仓库任务共享约定和失败模式；可复用记忆可以提高解决率并减少代理迭代次数。

## 方法
- MemOp 用下游效果定义记忆效用：让代理在有候选记忆和无记忆基线两种情况下运行，并在 10 个指标上比较结果，包括成功率、定位准确率、解决效率和定位效率。
- 当所有指标都至少不变，且至少有一个指标提升时，这条记忆会被接受。失败的候选项会成为被拒绝样本。
- 系统在 SWE-Bench Verified 上使用基于轨迹的拒绝采样来构建训练数据；论文报告了来自 10 个仓库的 3,200 个记忆候选项、100 个任务样本、每个任务 4 条轨迹，以及每条轨迹 4 条记忆。
- 训练分为两个阶段：先对被接受的记忆进行监督微调，再用基于相对无记忆基线的度量增益来定义奖励进行强化学习。
- 评估覆盖单回合复用和跨回合记忆演化，使用 Devstral-Small-2507 和 Qwen3-Coder-30B-A3B 作为软件工程代理，并配合多个小型记忆模型骨干。

## 结果
- 在单回合记忆增强中，MemOp 报告相对无记忆基线的成功率绝对提升最高达 +5.25 个百分点，解决效率提升最高达 +4.63 个百分点。
- 在跨回合记忆演化中，它报告相对无记忆基线的成功率提升最高达 +3.00 个百分点，定位准确率提升最高达 +3.17 个百分点。
- 在不同软件工程代理和记忆模型骨干上，论文报告 Devstral-Small-2507 的成功率最高提升 +9.00 个百分点、解决效率最高提升 +5.24 个百分点；Qwen3-Coder-30B-A3B 的成功率最高提升 +6.75 个百分点、解决效率最高提升 +7.45 个百分点。
- 相比基线，计算成本至少下降 9.79%。
- 经过微调的 MemOp 变体在单回合成功率上比 Claude-4-Sonnet 生成的记忆最高高 +3.25 个百分点，在跨回合成功率上最高高 +1.75 个百分点。
- 在 GRPO、DAPO 和 GSPO 设置下，MemOp 报告成功率最高提升 +3.50 个百分点，定位准确率最高提升 +4.03 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.05646v1](https://arxiv.org/abs/2606.05646v1)
