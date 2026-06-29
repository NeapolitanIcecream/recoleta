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
这篇文章简要回顾了机器人学习如何从手写规则转向数据驱动模型、仿真训练和基础模型式策略。文章认为，这一变化是 2020 年代中期机器人投资和落地快速上升的主要原因之一。

## 问题
- 传统机器人技术依赖工程师为每种情况写规则，但面对折衣服、处理新物体或与人互动这类杂乱的现实任务时，这种方法会失效。
- 只在仿真中训练出的策略，到了真实机器人上常常会失败，因为摩擦、光照、材料和感知的细微差别都会改变结果。
- 通用机器人需要把语言、视觉和状态映射成动作，并覆盖很多任务，但早期脚本化系统的语言能力弱，适应性也差。

## 方法
- 文章梳理了三次主要的学习转向：基于规则的控制、在仿真中进行强化学习，以及基于多模态数据的大规模动作预测。
- 在基于仿真的学习中，机器人通过带奖励信号的试错改进。领域随机化会在许多模拟世界里改变物理和视觉条件，让策略更容易迁移到现实中。
- 在基础模型式机器人中，系统接收相机画面、传感器读数、关节状态和语言指令，然后每秒多次预测下一步机器人动作。
- 一些公司会收集仓库或其他工作场景中部署机器人产生的数据，再用这些真实世界反馈持续改进模型。
- 文章用了几个案例：Jibo 说明社交交互的局限，OpenAI Dactyl 说明仿真到现实的灵巧操作，Google RT-1/RT-2 说明视觉-语言-动作控制，Covariant RFM-1 说明仓库拣选，Agility Digit 说明类人机器人的部署。

## 结果
- 文章称，类人机器人投资在 **2025 年达到 61 亿美元**，约为 **2024 年** 的 **4 倍**。
- Google 为构建 RT-1，持续 **17 个月** 收集了覆盖 **700 项任务** 的数据。RT-1 在见过的任务上成功率为 **97%**，在未见过的指令上为 **76%**。
- OpenAI 的 Dactyl 之后把基于仿真的方法用于魔方求解，总体成功率为 **60%**，在特别难的打乱状态上为 **20%**。
- Covariant 已在 Crate & Barrel 等客户场地部署仓库机器人系统，并在 **2024 年** 发布了 RFM-1，但文章没有给出基准表或汇总成功率。
- 文章把 Agility 的 Digit 描述为亚马逊、丰田和 GXO 用于真实仓库工作的最早类人机器人之一。一个明确限制是载重：Digit 可以举起 **35 磅**。
- 这篇文章是新闻综述，不是研究论文，所以定量证据有选择性，也没有把不同方法或系统放在统一实验框架里比较。

## Problem

## Approach

## Results

## Link
- [https://www.technologyreview.com/2026/04/17/1135416/how-robots-learn-brief-contemporary-history/](https://www.technologyreview.com/2026/04/17/1135416/how-robots-learn-brief-contemporary-history/)
