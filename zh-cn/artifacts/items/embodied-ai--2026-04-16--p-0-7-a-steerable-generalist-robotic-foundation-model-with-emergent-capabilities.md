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
## 总结
$\pi_{0.7}$ 是一个 50 亿参数的通用视觉-语言-动作模型，用于机器人控制。它通过更丰富的提示，从混合质量、来自多个来源的数据中学习。论文声称，这种提示设计让模型在任务、环境和机器人本体之间有更强的零样本泛化能力，并且在灵巧的长时程任务上可以直接取得可用的表现。

## 问题
- 先前的机器人基础模型在组合泛化上表现不佳：它们常常无法把已学到的技能组合到新任务中，即使任务与训练数据很接近，也可能需要针对任务的微调。
- 用大量、多样的机器人数据训练很难，因为轨迹在策略和质量上差异很大；如果直接训练，模型可能把好行为和坏行为平均掉，输出效果很弱的动作。
- 这很重要，因为有用的机器人基础模型需要能在没见过的家庭环境中工作，跟随不同的语言指令，在不同机器人之间迁移，并且能利用失败、自动 rollout 和非机器人数据，而不是把这些数据丢掉。

## 方法
- 核心思路是用更丰富的提示来约束机器人策略，提示里同时说明**做什么**和**怎么做**。提示可以包含任务指令、步骤级子任务指令、回合元数据、控制模式和子目标图像。
- 回合元数据会给每条轨迹标注属性，例如速度、1 到 5 的质量分数，以及某个片段是否包含错误。这样模型就能在训练中使用失败、次优示范和自动 rollout，而不是把它们当作要盲目模仿的目标。
- 子目标图像显示期望的近未来场景状态。一个从 BAGEL 初始化的单独世界模型会根据当前观测和子任务文本生成这些图像，让动作模型面对比单纯语言更具体的目标。
- 基础策略是一个 flow-matching VLA，建立在 Gemma3 4B 视觉-语言骨干、MEM 风格的视频历史编码和一个 8.6 亿参数的动作专家之上，总参数量约为 50 亿。
- 训练时会随机丢弃提示中的部分内容，这样模型在测试时可以只用任意子集。子目标图像会用在 25% 的训练样本中；元数据会在 15% 的情况下完全丢弃；单个元数据字段会以 5% 的概率丢弃。

## 结果
- 模型参数量约为**50 亿**：由一个**40 亿**参数的 Gemma3 VLM 骨干和一个**8.6 亿**参数的动作专家组成。
- 论文声称，它在一些灵巧的长时程任务上能直接取得很强的表现，例如**操作浓缩咖啡机、叠衣服、取出垃圾袋、折叠纸箱和削蔬菜**，而且不需要针对任务的后训练。
- 论文声称它有**零样本跨本体迁移**能力，包括**在没有叠衣服训练的机器人上完成 T 恤折叠**，并称这**匹配专家遥操作员的首次尝试表现**。
- 论文声称它能在**未见过的厨房和卧室环境**中遵循指令，也能把能力组合到新任务上，例如**把红薯放进空气炸锅**。
- 摘要说，浓缩咖啡机任务的表现与**专门做过 RL 微调的模型**相当；引言则说，这个系统有时会在灵巧任务上超过用 RL 训练或做单任务后训练的策略，因为它从多样且次优的数据中学习。
- 这段摘录**没有包含任务表、成功率或基准数字**，所以这里能看到的量化证据只限于模型规模和训练设置，而不是评测指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15483v2](http://arxiv.org/abs/2604.15483v2)
