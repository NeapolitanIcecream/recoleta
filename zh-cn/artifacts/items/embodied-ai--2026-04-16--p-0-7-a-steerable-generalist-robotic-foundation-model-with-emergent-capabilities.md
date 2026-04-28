---
source: arxiv
url: http://arxiv.org/abs/2604.15483v2
published_at: '2026-04-16T19:18:07'
authors:
- Physical Intelligence
- Bo Ai
- Ali Amin
- Raichelle Aniceto
- Ashwin Balakrishna
- Greg Balke
- Kevin Black
- George Bokinsky
- Shihao Cao
- Thomas Charbonnier
- Vedant Choudhary
- Foster Collins
- Ken Conley
- Grace Connors
- James Darpinian
- Karan Dhabalia
- Maitrayee Dhaka
- Jared DiCarlo
- Danny Driess
- Michael Equi
- Adnan Esmail
- Yunhao Fang
- Chelsea Finn
- Catherine Glossop
- Thomas Godden
- Ivan Goryachev
- Lachlan Groom
- Haroun Habeeb
- Hunter Hancock
- Karol Hausman
- Gashon Hussein
- Victor Hwang
- Brian Ichter
- Connor Jacobsen
- Szymon Jakubczak
- Rowan Jen
- Tim Jones
- Gregg Kammerer
- Ben Katz
- Liyiming Ke
- Mairbek Khadikov
- Chandra Kuchi
- Marinda Lamb
- Devin LeBlanc
- Brendon LeCount
- Sergey Levine
- Xinyu Li
- Adrian Li-Bell
- Vladislav Lialin
- Zhonglin Liang
- Wallace Lim
- Yao Lu
- Enyu Luo
- Vishnu Mano
- Nandan Marwaha
- Aikys Mongush
- Liam Murphy
- Suraj Nair
- Tyler Patterson
- Karl Pertsch
- Allen Z. Ren
- Gavin Schelske
- Charvi Sharma
- Baifeng Shi
- Lucy Xiaoyang Shi
- Laura Smith
- Jost Tobias Springenberg
- Kyle Stachowicz
- Will Stoeckle
- Jiaming Tang
- Jimmy Tanner
- Shalom Tekeste
- Marcel Torne
- Kyle Vedder
- Quan Vuong
- Anna Walling
- Haohuan Wang
- Jason Wang
- XuDong Wang
- Chris Whalen
- Samuel Whitmore
- Blake Williams
- Charles Xu
- Sukwon Yoo
- Lili Yu
- Wuming Zhang
- Zhuoyang Zhang
- Ury Zhilinsky
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- cross-embodiment-transfer
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# $π_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities

## Summary
## 摘要
$\pi_{0.7}$ 是一个用于机器人控制的 50 亿参数通用视觉-语言-动作模型。它使用信息更丰富的提示，从质量不一、来源多样的数据中学习。论文称，这种提示设计让模型在任务、环境和机器人形态之间具备更强的零样本泛化能力，并且在灵巧的长时程任务上具有开箱即用的表现。

## 问题
- 以往的机器人基础模型在组合泛化上表现不足：它们常常无法把已学会的技能组合起来完成新任务，即使任务与训练数据接近，也可能需要针对任务微调。
- 用大规模、多样化的机器人数据训练很难，因为轨迹在策略和质量上都有差异；如果直接训练，模型可能会把好坏行为平均起来，输出较弱的动作。
- 这很重要，因为有用的机器人基础模型需要能在未见过的家庭环境中工作，遵循多样的语言指令，在不同机器人之间迁移，并且能从失败、自主 rollout 和非机器人数据中获益，而不是把这些数据丢掉。

## 方法
- 核心思路是用更丰富的提示来条件化机器人策略，同时说明**做什么**和**怎么做**。提示可以包含任务指令、步骤级子任务指令、episode 元数据、控制模式和子目标图像。
- Episode 元数据会为每条轨迹标注速度、1 到 5 的质量分数，以及某一片段是否包含错误等属性。这样模型就可以使用失败数据、次优示范和自主 rollout 进行训练，而不会把它们都当作要盲目模仿的目标。
- 子目标图像展示期望的近未来场景状态。一个单独的世界模型从 BAGEL 初始化，根据当前观测和子任务文本生成这些图像，因此动作模型得到的目标比单靠语言更具体。
- 基础策略是一个 flow-matching VLA，建立在 Gemma3 40 亿参数视觉语言骨干、MEM 风格的视频历史编码和一个 8.6 亿参数动作专家之上，总参数量约为 50 亿。
- 训练时会随机丢弃提示中的部分内容，这样模型在测试时可以使用任意子集运行。子目标图像用于 25% 的训练样本；元数据有 15% 的概率被完全丢弃；单个元数据字段有 5% 的概率被丢弃。

## 结果
- 该模型约有 **50 亿参数**：由 **40 亿** Gemma3 VLM 骨干和一个 **8.6 亿** 动作专家组成。
- 论文称，该模型在**操作意式咖啡机、叠衣服、取出垃圾袋、折盒子、削蔬菜**等灵巧的长时程任务上具有很强的开箱即用表现，不需要针对任务进行额外训练。
- 论文称它具备**零样本跨形态迁移**能力，包括**在一台没有衣物折叠训练的机器人上折叠 T 恤**，并表示这**与专家遥操作员首次尝试时的表现相当**。
- 论文称，该模型能在**未见过的厨房和卧室环境**中遵循指令，并能组合泛化到**把红薯放入空气炸锅**等新任务。
- 摘要称，意式咖啡机任务的表现可与**专门经过 RL 微调的模型**相当；引言则称，该系统有时能在灵巧任务上超过经过 RL 训练或单任务后训练的策略，因为它能从多样且次优的数据中学习。
- 给出的摘录中**没有任务表、成功率或基准测试数值**，因此这里可用的定量证据主要限于模型和训练设置的数字，而不是评测指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15483v2](http://arxiv.org/abs/2604.15483v2)
