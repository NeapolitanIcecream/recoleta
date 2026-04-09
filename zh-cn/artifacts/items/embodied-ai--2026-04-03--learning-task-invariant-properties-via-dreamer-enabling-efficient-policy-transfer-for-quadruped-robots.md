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
DreamTIP 通过让 Dreamer 世界模型预测任务不变属性（如接触稳定性和地形间隙），提升了四足机器人运动控制中的 sim-to-real 迁移效果。论文称，这会让潜在状态更少依赖模拟器特有的动力学，并且只需要很少的真实世界适应数据就能改进迁移表现。

## 问题
- 在模拟中训练的四足机器人策略到了真实地形上常常失效，因为模拟器的动力学、传感和接触行为与真实机器人不同。
- 现有迁移方法往往依赖手工特征设计、大范围域随机化，或代价高的真实世界微调。
- 世界模型策略仍可能对模拟器的特定动力学过拟合，这会削弱它们在更难或未见地形上的迁移能力。

## 方法
- 基于带有 RSSM 世界模型的 Dreamer，并增加一个辅助头，从潜在状态预测任务不变属性（TIPs）。
- 使用 LLM 根据任务描述和特权状态输入生成 TIP 提取器；在这篇论文中，主要的 TIP 示例是接触稳定性和地形间隙。
- 用标准 Dreamer 损失加上 TIP 预测的似然项训练世界模型，使潜在表征保留那些应当能跨任务和动力学变化迁移的信息。
- 用混合回放缓冲区让模型适应真实机器人，该缓冲区结合模拟轨迹和真实轨迹；冻结循环模块，并保持策略冻结。
- 为了稳定适应过程，复制预训练世界模型作为冻结参考，并在当前随机状态与参考随机状态之间加入负余弦相似度损失。

## 结果
- 论文报告称，与基线相比，在 **8 个模拟迁移任务** 上平均性能提升 **28.1%**。
- 在困难的模拟 **Crawl** 任务中，基线 **WMP** 的奖励从最简单级别的大约 **33.51** 降到最困难级别的 **5.66**，而 **DreamTIP** 从 **36.58** 降到 **25.35**。
- 同一组 Crawl 对比中，随着难度增加，WMP 的降幅被描述为 **83.1%**，DreamTIP 的降幅为 **30.6%**。
- 在 **Unitree Go2** 上的真实世界测试中，每个任务进行 **10 次试验**，成功率为：**Stair 16 cm**：WMP **100%**、Ours w/o Adapt **100%**、Ours **100%**；**Climb 52 cm**：WMP **10%**、Ours w/o Adapt **90%**、Ours **100%**；**Tilt 33 cm**：WMP **40%**、Ours w/o Adapt **50%**、Ours **80%**；**Crawl 25 cm**：WMP **70%**、Ours w/o Adapt **80%**、Ours **100%**。
- 在模拟中的 TIP 设计变体比较里，**DreamTIP-GPT5** 在若干更难的设置上优于其他列出的 TIP 来源，包括 **Climb 61 cm: 22.40 ± 1.70**，对比 DeepSeekV3 的 **20.74 ± 1.52** 和 DWL-style supervision 的 **20.42 ± 1.23**；以及 **Tilt 35 cm: 31.71 ± 1.11**，对比 **25.79 ± 1.29** 和 **20.92 ± 1.24**。
- 这段摘录没有给出全部 8 个任务或所有基线的完整数值表，因此，关于最先进性能的一些说法依赖摘要式陈述，而不是所给文本中的完整对比结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02911v1](http://arxiv.org/abs/2604.02911v1)
