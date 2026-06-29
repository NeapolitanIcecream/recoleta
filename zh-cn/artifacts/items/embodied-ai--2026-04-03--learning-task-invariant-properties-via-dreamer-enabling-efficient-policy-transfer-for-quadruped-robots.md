---
source: arxiv
url: http://arxiv.org/abs/2604.02911v1
published_at: '2026-04-03T09:27:36'
authors:
- Junyang Liang
- Yuxuan Liu
- Yabin Chang
- Junfan Lin
- Junkai Ji
- Hui Li
- Changxin Huang
- Jianqiang Li
topics:
- sim2real-transfer
- quadruped-locomotion
- world-models
- dreamer
- task-invariant-representation
- robot-adaptation
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Learning Task-Invariant Properties via Dreamer: Enabling Efficient Policy Transfer for Quadruped Robots

## Summary
## 摘要
DreamTIP 通过让 Dreamer 世界模型预测接触稳定性和地形间隙等任务不变属性，提升了四足机器人行走的仿真到现实迁移。论文称，这样做能让潜在状态不那么依赖仿真器特有的动力学，并且只需很少的现实数据就能改善迁移效果。

## 问题
- 在仿真中训练的四足机器人策略常常在真实地形上失效，因为仿真器的动力学、感知和接触行为与真实机器人不同。
- 现有迁移方法通常依赖手工特征设计、较强的域随机化，或昂贵的现实环境微调。
- 基于世界模型的策略仍可能过拟合仿真器的特定动力学，这会削弱它们在更难或未见地形上的迁移表现。

## 方法
- 在 Dreamer 的基础上使用 RSSM 世界模型，然后加入一个辅助头，从潜在状态预测任务不变属性（TIP）。
- 用大语言模型根据任务描述和特权状态输入生成 TIP 提取器；在这篇论文里，主要的 TIP 示例是接触稳定性和地形间隙。
- 用标准 Dreamer 损失加上预测 TIP 的似然项来训练世界模型，让潜在表示保留那些应当跨任务和动力学变化传递的信息。
- 通过混合回放缓冲区把仿真轨迹和真实轨迹结合起来适配真实机器人，冻结循环模块，并保持策略冻结。
- 通过把预训练世界模型复制为冻结参考，并在当前和参考的随机状态之间加入负余弦相似度损失，稳定适配过程。

## 结果
- 论文报告，在 **8 个仿真迁移任务** 上，相比基线平均性能提升 **28.1%**。
- 在一个较难的仿真 **Crawl** 任务上，基线 **WMP** 的回报从最容易级别的约 **33.51** 降到最难级别的 **5.66**，而 **DreamTIP** 从 **36.58** 降到 **25.35**。
- 同一个 Crawl 对比在难度增加时被描述为：**WMP** 下降 **83.1%**，**DreamTIP** 下降 **30.6%**。
- 在 **Unitree Go2** 的真实世界测试中，每个任务做 **10 次试验** 的成功率如下：**Stair 16 cm**：WMP **100%**，Ours w/o Adapt **100%**，Ours **100%**；**Climb 52 cm**：WMP **10%**，Ours w/o Adapt **90%**，Ours **100%**；**Tilt 33 cm**：WMP **40%**，Ours w/o Adapt **50%**，Ours **80%**；**Crawl 25 cm**：WMP **70%**，Ours w/o Adapt **80%**，Ours **100%**。
- 在仿真中的 TIP 设计变体里，**DreamTIP-GPT5** 在若干更难设置上优于表中其他 TIP 来源，包括 **Climb 61 cm: 22.40 ± 1.70** 对比 **DeepSeekV3 的 20.74 ± 1.52** 和 **DWL-style supervision 的 20.42 ± 1.23**，以及 **Tilt 35 cm: 31.71 ± 1.11** 对比 **25.79 ± 1.29** 和 **20.92 ± 1.24**。
- 这段摘录没有给出全部八个任务或所有基线的完整数值表，所以关于最先进性能的部分说法，依赖的是摘要式表述，而不是提供文本中的完整对比结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02911v1](http://arxiv.org/abs/2604.02911v1)
