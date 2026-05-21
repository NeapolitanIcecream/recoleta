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
这篇综述将 World Action Models（WAMs，世界行动模型）定义为同时预测未来观测和动作的机器人基础模型。文章认为，在 VLA 策略中加入世界预测，可以提升物理预判、泛化能力，并更好地使用没有动作标签的视频数据。

## 问题
- 标准 VLA 模型训练 \(p(a \mid o,l)\)：它们把观测和语言直接映射为动作，没有显式的未来状态预测目标。
- 这在具身任务中很重要，因为接触、物体运动和失败动作通常需要在机器人移动前被预判。
- 论文称，video policies、video action models、world models 和 action world models 等相关术语存在重叠，这会让方法比较变得困难。

## 方法
- 论文将 WAM 目标形式化为 \(p(o',a \mid o,l)\)，其中模型根据当前观测 \(o\) 和语言指令 \(l\) 预测未来观测 \(o'\) 和动作 \(a\)。
- 它定义了 2 个必需属性：对未来状态的前向预测建模，以及与预测状态绑定的动作生成。
- 它将 WAM 分为 2 个架构家族：Cascaded WAMs 和 Joint WAMs。
- Cascaded WAMs 将任务分解为 \(p(o',a \mid o,l)=p(a \mid o',o,l)p(o' \mid o,l)\)；Joint WAMs 训练一个共享模型来建模 \(p(o',a \mid o,l)\)。
- 这篇综述按架构、训练数据和评估标准整理已有工作。

## 结果
- 摘录没有报告新的机器人基准结果、成功率或数据集分数；主要声称的贡献是综述和分类法。
- 它提出 2 个主要 WAM 架构家族：Cascaded 和 Joint。
- 它进一步将 Cascaded WAMs 分为显式和隐式表示对齐路径，将 Joint WAMs 分为自回归形式和基于扩散的形式。
- 它回顾了 WAM 的 4 类训练数据来源：机器人遥操作、便携式人类示范、仿真，以及互联网规模的第一视角视频。
- 它将评估分为 3 个能力领域：视觉保真度、物理常识和动作合理性。
- 它对比了 3 个形式化目标：VLA \(p(a \mid o,l)\)、world model \(p(o' \mid o,a)\) 和 WAM \(p(o',a \mid o,l)\)。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12090v1](https://arxiv.org/abs/2605.12090v1)
