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
## 总结
Cortex 2.0 为工业视觉-语言-动作机器人策略加入了基于世界模型的规划。它会预测多个可能的未来轨迹，按进展、风险和任务完成情况打分，然后执行得分最高的方案，以提升在杂乱仓库环境中的长时程操作表现。

## 问题
- 标准的视觉-语言-动作策略从当前观测中选择下一步动作，不会评估未来结果，这让它们在长时程任务中很脆弱，因为错误会不断累积。
- 工业操作环境里有大量杂物、遮挡、反光材料和接触丰富的交互，物体分布也会变化，单次错误动作就可能打乱整个流程。
- 这篇论文关注在真实部署条件下，单臂和双臂系统等不同形态上的可靠执行。

## 方法
- 系统保留分层 VLA 栈，再加入一个视觉潜空间世界模型，在执行前沿规划时长内展开 `k` 条候选未来轨迹。
- 一个冻结的 Process-Reward Operator（PRO）在真实部署轨迹上训练，用三个信号给每条想象出来的轨迹打分：任务进展、失败风险和完成可能性。分数公式是 `S = progress - λ*risk + β*success`。
- 策略选择得分最高的轨迹，并把这个选中的未来条件输入给一个 2B-VLM flow-matching 动作头，生成一个动作块。
- 规划发生在视觉潜空间里，而不是机器人专用动作空间里，所以同一个规划循环可以跨不同形态迁移；机器人专用的动作映射由轻量适配器处理。
- 训练先用互联网视频预训练世界模型，再用每秒 30 Hz 的部署记录、开源机器人数据集、遥操作数据、合成数据，以及一个整理过的 1000 万条部署交互子集进行微调。

## 结果
- 论文称 Cortex 2.0 在四项真实世界任务上都拿到了最好的成功率：抓取放置、物品与垃圾分类、螺丝分类、鞋盒拆包。
- 它报告在单臂和双臂平台上都持续优于当前最好的反应式 VLA 基线。
- 论文还说，基准评测期间系统没有需要人工介入。
- 摘要没有给出逐任务的定量指标、具体成功率数字或基线分数，所以只能根据提供的文本判断改进方向，不能核实提升幅度。
- 训练设置里的具体规模包括 `>10M` 次部署回合、整理后的训练语料中 `>25k` 小时部署数据、约 `40k` 次遥操作回合、约 `970k` 次开源回合，以及一个包含超过 `500M` 次操作交互、以 `30 Hz` 采集的历史数据池。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20246v1](http://arxiv.org/abs/2604.20246v1)
