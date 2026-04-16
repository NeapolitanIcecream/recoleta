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
SandMLE 通过用合成的微型沙盒替代缓慢的真实 MLE 任务，让面向机器学习工程智能体的 on-policy 强化学习变得可行。这些沙盒保留了任务结构，同时缩短了执行时间。论文称，这种方法比监督微调带来更好的 MLE 表现，并且可以迁移到不同的智能体 scaffold。

## 问题
- 用 on-policy RL 训练 MLE 智能体成本很高，因为每个 rollout 步骤都可能需要在大型数据集上完成完整的数据预处理、模型训练和评估。
- 在标准 MLE 设置中，一次代码执行平均接近 200 秒，而 RL 每次更新需要许多多步轨迹和分组样本。
- 以往工作常退回到监督微调或离线/代理奖励 RL，这会减少探索并削弱泛化能力。

## 方法
- 核心思路是生成带有极小数据集的合成 MLE 任务，每个任务只有 50 到 200 个训练样本。这样完整流程仍然是 MLE 任务的样子，但运行速度足够快，能够支持按轨迹进行的 on-policy RL。
- SandMLE 用四种 LLM 角色构建每个任务：Data Strategist 定义任务结构和隐藏规则，ML Developer 生成数据和基线方法，MLOps Engineer 构建评估器，Technical Writer 产出最终任务说明。
- 系统通过创建隐藏测试集、确定性的评估代码，以及基于基线方法设定的里程碑阈值来保证任务可验证。它还会用自动化的 sanity check 检查指标排序，过滤损坏的任务。
- 训练采用轨迹级 GRPO，并在 ReAct 风格循环中进行；稠密奖励由格式合规、执行成功和基于里程碑的分数阈值组成。
- 策略梯度只应用于模型自己的动作和推理 token，环境输出会被 mask；超过时间限制的轨迹也会被 mask。

## 结果
- SandMLE 将平均执行时间缩短了 13 倍以上，把代码执行时间约 200 秒的标准问题，变成了 15 秒以内的合成任务。
- 从 60 个种子任务出发，这条流水线构建了 848 个合成训练任务和 64 个留出的合成验证任务。
- 在 MLE-bench-lite 上，经过 SandMLE 训练的模型在 Qwen3-8B、Qwen3-14B 和 Qwen3-30B-A3B 上都超过了 SFT 基线，Any Medal rate 的相对提升范围是 20.3% 到 66.9%。
- 在 MLE-Dojo 上，训练后的策略可以泛化到未见过的智能体 scaffold，并将 HumanRank 相对提高最多 32.4%。
- 评估覆盖了 Easy split 中 22 个未见过的 MLE-bench-lite 任务，以及 62 个 MLE-Dojo 任务。
- 这段摘录没有提供每个模型的完整绝对分数、完整的基线表，或训练总成本。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04872v1](http://arxiv.org/abs/2604.04872v1)
