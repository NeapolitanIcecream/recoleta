---
source: arxiv
url: http://arxiv.org/abs/2604.04872v1
published_at: '2026-04-06T17:19:29'
authors:
- Yuhang Zhou
- Lizhu Zhang
- Yifan Wu
- Jiayi Liu
- Xiangjun Fan
- Zhuokai Zhao
- Hong Yan
topics:
- machine-learning-agents
- on-policy-rl
- code-execution
- synthetic-data
- ml-engineering
- multi-agent-systems
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Synthetic Sandbox for Training Machine Learning Engineering Agents

## Summary
## 摘要
SandMLE 通过用合成的微型沙盒替代缓慢的真实 MLE 任务，让面向机器学习工程智能体的 on-policy 强化学习变得可行。这些沙盒保留任务结构，同时缩短执行时间。论文声称，这样做比监督微调带来更好的 MLE 表现，也能迁移到不同的智能体脚手架。

## 问题
- 用 on-policy RL 训练 MLE 智能体成本很高，因为每个 rollout 步骤都可能需要完整的数据预处理、模型训练和大规模数据评估。
- 在标准 MLE 场景中，一次代码执行平均接近 200 秒，而 RL 需要很多多步轨迹和每次更新的分组样本。
- 以往方法常常退回到监督微调或离线/代理奖励 RL，这会减少探索并削弱泛化。

## 方法
- 核心思路是生成带有很小数据集的合成 MLE 任务，训练样本只有 50 到 200 个。这样，完整流水线看起来仍像一个 MLE 任务，但运行速度足以支持按轨迹的 on-policy RL。
- SandMLE 用四个 LLM 角色来构建每个任务：Data Strategist 定义任务结构和隐藏规则，ML Developer 生成数据和基线方法，MLOps Engineer 构建评估器，Technical Writer 产出最终任务说明。
- 系统通过创建隐藏测试集、确定性的评估代码，以及基于基线方法的里程碑阈值来保持任务可验证性。它还用一个自动化一致性检查，根据指标排序过滤损坏任务。
- 训练使用 trajectory-level GRPO，在 ReAct 风格循环中进行，密集奖励由格式合规、执行成功和基于里程碑的分数阈值组成。
- 策略梯度只作用于模型自己的动作和推理 token，环境输出会被掩码；超出时间限制的轨迹也会被掩码。

## 结果
- SandMLE 将平均执行时间缩短了 13 倍以上，把标准问题中大约 200 秒的代码执行降到 15 秒以下的合成任务。
- 从 60 个种子任务出发，这个流程构建出 848 个合成训练任务和 64 个留出的合成验证任务。
- 在 MLE-bench-lite 上，SandMLE 训练的模型在 Qwen3-8B、Qwen3-14B 和 Qwen3-30B-A3B 上都超过了 SFT 基线，Any Medal rate 的相对提升在 20.3% 到 66.9% 之间。
- 在 MLE-Dojo 上，训练后的策略能泛化到未见过的智能体脚手架，HumanRank 的相对提升最高达到 32.4%。
- 评估覆盖了 Easy split 中 22 个未见过的 MLE-bench-lite 任务，以及 62 个 MLE-Dojo 任务。
- 摘录没有给出各模型完整的绝对分数、完整的基线表或训练成本总计。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04872v1](http://arxiv.org/abs/2604.04872v1)
