---
source: arxiv
url: http://arxiv.org/abs/2604.20246v1
published_at: '2026-04-22T06:49:12'
authors:
- Adriana Aida
- Walid Amer
- Katarina Bankovic
- Dhruv Behl
- Fabian Busch
- Annie Bhalla
- Minh Duong
- Florian Gienger
- Rohan Godse
- Denis Grachev
- Ralf Gulde
- Elisa Hagensieker
- Junpeng Hu
- Shivam Joshi
- Tobias Knobloch
- Likith Kumar
- Damien LaRocque
- Keerthana Lokesh
- Omar Moured
- Khiem Nguyen
- Christian Preyss
- Ranjith Sriganesan
- Vikram Singh
- Carsten Sponner
- Anh Tong
- Dominik Tuscher
- Marc Tuscher
- Pavan Upputuri
topics:
- world-model
- vision-language-action
- industrial-robotics
- long-horizon-manipulation
- cross-embodiment
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Cortex 2.0: Grounding World Models in Real-World Industrial Deployment

## Summary
## 摘要
Cortex 2.0 在工业视觉-语言-动作机器人策略中加入了世界模型规划。它会预测多个可能的未来轨迹，按进展、风险和任务完成情况打分，然后执行分数最高的方案，以提升杂乱仓储环境中长时程操作的表现。

## 问题
- 标准视觉-语言-动作策略根据当前观测选择下一步动作，不评估未来结果，因此在长时程任务中很脆弱，错误会逐步累积。
- 工业操作环境有大量杂物、遮挡、反光材料、富接触交互，以及不断变化的物体分布，因此一次错误动作就可能打乱整个工作流程。
- 这篇论文的目标是在真实部署条件下，让系统在不同任务和不同具身形态上可靠执行，例如单臂和双臂系统。

## 方法
- 系统保留分层式 VLA 栈，并加入一个视觉潜变量世界模型，在执行动作前沿着规划时域展开 `k` 个候选未来轨迹。
- 一个冻结的 Process-Reward Operator (PRO) 基于真实部署轨迹训练，对每个想象出的 rollout 用三个信号打分：任务进展、失败风险和完成概率。评分公式是 `S = progress - λ*risk + β*success`。
- 策略选择得分最高的 rollout，并让 2B-VLM 的 flow-matching 动作头以该选定未来为条件生成一段动作。
- 规划发生在视觉潜空间中，而不是机器人特定的动作空间中，因此同一套规划循环可以迁移到不同具身形态；机器人特定的动作映射由轻量适配器处理。
- 训练先对世界模型进行互联网视频预训练，再用 30 Hz 的部署录制数据微调，另外还使用开源机器人数据集、遥操作数据、合成数据，以及经过筛选的 1000 万次部署交互子集。

## 结果
- 论文称，Cortex 2.0 在四个评估的真实世界任务上都取得了最高成功率：抓取放置、物品与垃圾分拣、螺丝分拣和鞋盒拆包。
- 文中报告称，它在单臂和双臂平台上都持续优于当前最强的反应式 VLA 基线。
- 文中还表示，系统在基准评测期间不需要人工干预。
- 给出的摘录没有提供各任务的定量指标、准确的成功率数字或点名的基线分数，因此无法仅根据这段文本核实提升幅度。
- 训练设置中给出的具体规模包括：`>10M` 次部署 episode、筛选后训练语料中 `>25k` 小时部署数据、约 `40k` 个遥操作 episode、约 `970k` 个开源 episode，以及以 `30 Hz` 采集、累计超过 `500M` 次操作交互的机器人群历史数据。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20246v1](http://arxiv.org/abs/2604.20246v1)
