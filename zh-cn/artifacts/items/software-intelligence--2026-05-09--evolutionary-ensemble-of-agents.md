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
## 总结
EvE 将编码代理组织成一个实时种群，在算法搜索过程中同时改进代码求解器和代理指导。论文把它用于 ICON 的位置编码问题，结果显示它在示例数量泛化上优于静态代理变体。

## 问题
- ICON 模型按固定数量的上下文示例训练，例如 k=5，但用户在测试时可能需要 k=6 到 k=10。
- 原始学习到的位置表在第五个示例之后没有训练过的条目，所以当序列超过训练上限时，准确率会下降。
- 这类问题很适合用编码代理搜索来处理，因为修复它需要在模型代码、训练和评估之间做协调修改。

## 方法
- EvE 维护两个带分数的种群：求解器代码变体和代理指导状态。
- 每次迭代中，采样到的代理会在相同的工作区里修改代码，使用同一组参考求解器、参考代理和基础仓库。
- 每个代理都会生成一个新的求解器，也可能同时修订自己的指导或技能。
- 系统先评估求解器，再根据代理输出的两两胜负更新它们的 Elo 分数，因此采样会偏向那些在当前搜索阶段能带来增益的代理。
- 新的代理变体及其工作日志会进入种群，后续代理可以复用具体的成功和失败经验。

## 结果
- ICON 任务在 k=5 个示例上训练，在 k=1 到 k=10 上评估；其中 k=6 到 k=10 的序列长度超出分布。
- 搜索过程使用 15 次迭代、每次 2 个工作代理、8 个参考求解器和 4 个参考代理；搜索期间每个候选都会训练 2,000 步。
- 基准使用具有随机三次通量的一维守恒律、1,000 个算子实例，以及每个实例 100 个初始条件；误差是 100 个空间网格点上的平均绝对误差。
- EvE 发现了一种先重缩放再插值的位置编码，把未见过的示例槽位映射回训练范围，并区分槽位信息和角色信息。
- 在 k=10 时，EvE 在 2,000 步训练下把误差控制在 0.15 以下，在 10,000 步训练下控制在 0.08 以下；Seed ICON 的位置编码在 k>5 后失效。
- 每个条件运行两次时，EvE 比 Static-Initial 和 Static-Final 更稳定；有一次冻结的最佳代理运行最终停在一个甚至高于更差的 Static-Initial 运行的位置，这支持了论文的判断：搜索过程中代理适应必须持续进行。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09018v2](https://arxiv.org/abs/2605.09018v2)
