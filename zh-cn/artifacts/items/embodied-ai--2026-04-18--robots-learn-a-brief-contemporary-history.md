---
source: hn
url: https://www.technologyreview.com/2026/04/17/1135416/how-robots-learn-brief-contemporary-history/
published_at: '2026-04-18T22:11:04'
authors:
- billybuckwheat
topics:
- robot-learning-history
- vision-language-action
- sim2real
- robot-foundation-models
- humanoid-robots
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Robots learn: A brief, contemporary history

## Summary
## 摘要
这篇文章简要回顾了机器人学习如何从手写规则转向数据驱动模型、仿真训练和类似基础模型的策略。文章认为，这一转变是机器人投资和部署在 2020 年代中期快速上升的主要原因之一。

## 问题
- 传统机器人技术依赖工程师为每种情况明确写出规则，但这种方法在应对折叠衣物、处理新物体或与人互动等杂乱的现实任务时很快失效。
- 只在仿真中训练出的策略常常无法在真实机器人上正常工作，因为摩擦、光照、材料和传感等方面的细小差异都会改变结果。
- 通用机器人需要在多种任务中把语言、视觉和状态映射为动作，但较早的脚本化系统语言能力弱，适应性也差。

## 方法
- 文章梳理了三次主要的学习方式转变：基于规则的控制、仿真中的强化学习，以及基于多模态数据的大规模动作预测。
- 在基于仿真的学习中，机器人通过带奖励信号的试错来改进。领域随机化会在许多仿真世界中改变物理参数和视觉条件，让策略更容易迁移到现实环境。
- 在类似基础模型的机器人系统中，系统接收摄像头画面、传感器读数、关节状态和语言指令，然后以每秒多次的频率预测机器人的下一个动作。
- 一些公司会从已部署在仓库或其他工作场景中的机器人收集数据，再用这些现实反馈持续改进模型。
- 文章用了几个案例：Jibo 说明社交互动方面的局限，OpenAI Dactyl 说明从仿真到现实的灵巧操作，Google RT-1/RT-2 说明视觉-语言-动作控制，Covariant RFM-1 说明仓库拣选，Agility Digit 说明人形机器人的部署。

## 结果
- 根据文章，人形机器人投资在 **2025 年达到 61 亿美元**，约为 **2024 年**投资额的 **4 倍**。
- Google 为构建 RT-1 在 **17 个月**里收集了覆盖 **700 项任务**的数据。RT-1 在见过的任务上成功率达到 **97%**，在未见过的指令上达到 **76%**。
- OpenAI 的 Dactyl 后来把基于仿真的方法用于求解魔方，总体成功率为 **60%**，在特别困难的打乱状态下为 **20%**。
- Covariant 在 Crate & Barrel 等客户现场部署了仓库机器人系统，并在 **2024 年**发布了 RFM-1，但文章没有给出基准测试表或总体成功率。
- 文章称 Agility 的 Digit 是最早用于 Amazon、Toyota 和 GXO 真实仓库工作的几种人形机器人之一。一个明确限制是载重：Digit 可举起 **35 磅**。
- 这篇文章是新闻综述，不是研究论文，因此量化证据是有选择性的，也没有对不同方法或系统做统一的实验比较。

## Problem

## Approach

## Results

## Link
- [https://www.technologyreview.com/2026/04/17/1135416/how-robots-learn-brief-contemporary-history/](https://www.technologyreview.com/2026/04/17/1135416/how-robots-learn-brief-contemporary-history/)
