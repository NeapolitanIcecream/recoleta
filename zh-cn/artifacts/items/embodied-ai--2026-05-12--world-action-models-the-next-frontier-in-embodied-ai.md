---
source: arxiv
url: https://arxiv.org/abs/2605.12090v1
published_at: '2026-05-12T13:10:52'
authors:
- Siyin Wang
- Junhao Shi
- Zhaoyang Fu
- Xinzhe He
- Feihong Liu
- Chenchen Yang
- Yikang Zhou
- Zhaoye Fei
- Jingjing Gong
- Jinlan Fu
- Mike Zheng Shou
- Xuanjing Huang
- Xipeng Qiu
- Yu-Gang Jiang
topics:
- world-action-models
- embodied-foundation-models
- vision-language-action
- robot-world-models
- generalist-robot-policy
- robot-data-scaling
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# World Action Models: The Next Frontier in Embodied AI

## Summary
## 摘要
这篇综述把世界动作模型（WAMs）定义为同时预测未来观测和动作的机器人基础模型。文中主张，在 VLA 策略中加入世界预测，可以提升对物理环境的前瞻性、泛化能力，以及对无动作标注视频数据的利用。

## 问题
- 标准 VLA 模型训练 \(p(a \mid o,l)\)：它们把观测和语言直接映射到动作，没有显式的未来状态预测目标。
- 这在具身任务中很重要，因为接触、物体运动和失败动作，往往需要在机器人移动前就被预判。
- 论文指出，视频策略、视频动作模型、世界模型和动作世界模型等相关术语有重叠，这让方法比较变得困难。

## 方法
- 论文把 WAM 目标形式化为 \(p(o',a \mid o,l)\)，也就是模型根据当前观测 \(o\) 和语言指令 \(l\)，同时预测未来观测 \(o'\) 和动作 \(a\)。
- 它定义了 2 个必要属性：对未来状态的前向预测建模，以及与预测状态绑定的动作生成。
- 它把 WAM 分成 2 类架构：级联式 WAM 和联合式 WAM。
- 级联式 WAM 把任务分解为 \(p(o',a \mid o,l)=p(a \mid o',o,l)p(o' \mid o,l)\)；联合式 WAM 则训练一个共享模型来表示 \(p(o',a \mid o,l)\)。
- 这篇综述按架构、训练数据和评估标准来组织已有工作。

## 结果
- 摘要没有报告新的机器人基准结果、成功率或数据集分数；主要贡献是综述和分类法。
- 文中提出了 2 类主要的 WAM 架构：级联式和联合式。
- 它进一步把级联式 WAM 分成显式和隐式表示对齐路径，把联合式 WAM 分成自回归和扩散式形式。
- 它回顾了 WAM 的 4 类训练数据来源：机器人遥操作、便携式人类示范、仿真，以及互联网规模的第一人称视频。
- 它把评估分成 3 个能力维度：视觉保真度、物理常识和动作合理性。
- 它对比了 3 个形式化目标：VLA \(p(a \mid o,l)\)、世界模型 \(p(o' \mid o,a)\) 和 WAM \(p(o',a \mid o,l)\)。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12090v1](https://arxiv.org/abs/2605.12090v1)
