---
source: arxiv
url: http://arxiv.org/abs/2603.09292v1
published_at: '2026-03-10T07:22:51'
authors:
- Tingjun Dai
- Mingfei Han
- Tingwen Du
- Zhiheng Liu
- Zhihui Li
- Salman Khan
- Jun Yu
- Xiaojun Chang
topics:
- robotic-manipulation
- vision-language-action
- progress-awareness
- error-recovery
- ood-robustness
relevance_score: 0.53
run_id: materialize-outputs
---

# See, Plan, Rewind: Progress-Aware Vision-Language-Action Models for Robust Robotic Manipulation

## Summary
SPR 是一个面向机器人操作的进度感知视觉-语言-动作框架，把语言任务分解为可验证的二维空间子目标，并在进度异常时自动“回退”后再继续执行。它的价值在于提升长时程操作、分布外场景和真实机器人中的鲁棒性，而无需额外失败数据或辅助模型。

## Problem
- 现有机器人 VLA 方法通常能“看见并行动”，但缺少对任务进行到哪一步的**显式、可执行进度感知**，导致长任务中错误会累积。
- 许多进度监控信号是抽象文本描述或二值标记，**缺乏空间落地性**，难以直接指导机械臂动作与判断是否真的推进了任务。
- 现有恢复方法常依赖额外失败数据、人工提示工程或辅助模型，成本高且对未见场景适应性差。

## Approach
- 将任务从演示中自动分解为一串**空间化子任务里程碑**：对抓取类任务用夹爪开合变化找边界；其他任务用 Gemini-3 标注子任务区间与语义描述。
- 用 **DINOv3 + SAM** 自动提取夹爪的 2D 位置，生成每个子任务的目标坐标和从当前状态到下一子目标的 1-5 个轨迹航点，作为训练监督。
- 模型按自回归方式依次输出：深度感知、剩余子任务数、每个子任务的语义+2D 坐标、到下一个子目标的 2D 轨迹、最终动作；核心思想就是“先判断还差几步，再朝最近一步走”。
- 设计 **Rewind** 恢复机制：维护最近 4 步的子任务计数和最近 8 步的规划轨迹；若计数持续上升或轨迹长时间完全不变，就认为执行失败或卡住。
- 恢复时不引入新模型，而是把成功演示反向构造成“返回初始位置”的训练数据；运行中一旦检测到异常，就切换到回退指令执行固定步数（文中设为 **N=3**），再恢复原任务。

## Results
- 在 **LIBERO** 上，SPR 超过 **MolmoAct**：摘要称提升 **5%**，正文表 2 显示从 **86.8%** 提升到 **90.6%**（+**3.8** 个百分点）；联合训练版本 **Ours\*** 达到 **91.8%**，比 90.6% 再高 **1.2** 个百分点。
- LIBERO 分项结果（表 2）：**Spatial 92.4%**、**Object 93.0%**、**Goal 94.2%**、**Long 82.8%**；联合训练版分别为 **93.2% / 95.4% / 93.2% / 85.4%**，平均 **91.8%**。
- 在 **LIBERO-Plus** 分布外鲁棒性测试中，SPR 取得最高平均成功率 **71.8%**，且平均性能下降仅 **18.8%**；优于 **OpenVLA-OFT 70.6%, drop 27.0%** 和 **UniVLA 57.7%, drop 37.5%**。
- LIBERO-Plus 各扰动成功率分别为：**Background 86.0%**、**Robot 47.7%**、**Language 78.5%**、**Layout 69.6%**、**Light 85.0%**；对应性能下降为 **4.6% / 42.9% / 12.1% / 21.0% / 5.6%**。
- 在真实机器人 3 个任务上，相比 **MolmoAct** 的 **50% / 0% / 0%**，SPR 达到 **70% / 30% / 40%**（Pick up / Tidy up / Push-T），说明在长时程整理和连续接触推物任务上也更稳健。
- 论文还声称该闭环纠错能力**无需额外训练数据或辅助模型**，主要依靠空间子目标进度监控与反向演示构造的回退策略实现。

## Link
- [http://arxiv.org/abs/2603.09292v1](http://arxiv.org/abs/2603.09292v1)
