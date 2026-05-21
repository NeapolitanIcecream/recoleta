---
source: arxiv
url: https://arxiv.org/abs/2605.09018v2
published_at: '2026-05-09T15:56:10'
authors:
- Zongmin Yu
- Liu Yang
topics:
- code-intelligence
- coding-agents
- multi-agent-systems
- evolutionary-search
- automated-research
- operator-learning
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Evolutionary Ensemble of Agents

## Summary
## 摘要
EvE 将编码智能体组织成一个实时种群，在算法搜索期间同时改进代码求解器和智能体指导。论文在 ICON 位置编码上测试了该方法，并报告其样本数量泛化效果优于静态智能体变体。

## 问题
- ICON 模型使用固定数量的上下文样本训练，例如 k=5，但用户在测试时可能需要 k=6 到 k=10。
- 原始的学习式位置表在第五个样本之后没有训练过的条目，因此当序列超过训练限制时，准确率会下降。
- 这一点很重要，因为修复该问题需要在模型代码、训练和评估中协调修改代码，适合作为编码智能体搜索的目标。

## 方法
- EvE 保留两个带评分的种群：求解器代码变体和智能体指导状态。
- 在每次迭代中，被采样的智能体使用相同的参考求解器、参考智能体和基础代码库来编辑相同的工作区。
- 每个智能体会生成一个新的求解器，也可以修改自己的指导或技能。
- 系统评估求解器后，根据求解器输出的两两胜负为智能体更新 Elo，因此采样会偏向在当前搜索阶段带来价值的智能体。
- 新的智能体变体及其工作日志进入种群，使后续智能体能够复用具体的成功经验和失败记录。

## 结果
- ICON 任务使用 k=5 个样本训练，并在 k=1 到 k=10 上评估；k=6 到 k=10 在序列长度上属于分布外。
- 搜索使用 15 次迭代，每次迭代 2 个工作智能体、8 个参考求解器和 4 个参考智能体；搜索期间每个候选项训练 2,000 步。
- 基准使用带随机三次通量的一维守恒律、1,000 个算子实例，以及每个实例 100 个初始条件；误差是在 100 个空间网格点上取平均的平均绝对误差。
- EvE 发现了一种先重缩放再插值的位置编码，将未见过的样本槽映射回训练范围，并分离槽信息和角色信息。
- 在 k=10 时，EvE 使用 2,000 个训练步可将误差保持在 0.15 以下，使用 10,000 个训练步可保持在 0.08 以下；Seed ICON 位置编码在 k=5 之后失效。
- 在每种条件的两次运行中，EvE 比 Static-Initial 和 Static-Final 更稳定；一次冻结最佳智能体的运行进入平台期，误差甚至高于较差的 Static-Initial 运行，这支持了论文的主张：智能体适应必须在搜索期间持续进行。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09018v2](https://arxiv.org/abs/2605.09018v2)
