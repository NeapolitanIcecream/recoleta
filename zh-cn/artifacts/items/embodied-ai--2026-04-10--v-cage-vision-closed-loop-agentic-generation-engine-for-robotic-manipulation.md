---
source: arxiv
url: http://arxiv.org/abs/2604.09036v1
published_at: '2026-04-10T06:56:17'
authors:
- Yaru Liu
- Ao-bo Wang
- Nanyang Ye
topics:
- vision-language-action
- robot-data-scaling
- sim2real
- synthetic-data-generation
- long-horizon-manipulation
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# V-CAGE: Vision-Closed-Loop Agentic Generation Engine for Robotic Manipulation

## Summary
## 摘要
V-CAGE 是一条面向机器人操作的数据生成流水线，用来构建仿真场景、执行任务、用视觉语言模型检查结果，并压缩生成的视频。论文面向长时程 Vision-Language-Action 训练，这类训练中，糟糕的场景布局和未被发现的执行错误会污染大规模合成数据集。

## 问题
- VLA 模型需要大规模操作数据集，但真实数据采集成本高，而且覆盖不到许多长尾情况。
- 现有合成流水线经常在缺少足够任务上下文的情况下放置物体，导致碰撞、遮挡或目标不可达。
- 许多系统以开环方式运行：代码虽然没有运行时报错，但任务在视觉上仍可能失败，这类静默失败会污染长时程训练数据。

## 方法
- V-CAGE 使用基于 OpenClaw 的智能体流水线，将语言任务转换为可用的仿真场景和经过验证的操作轨迹。
- 它的 Inpainting-Guided Scene Construction 会先选择相关资产、无碰撞地放置它们、写出语义布局计划，然后用图像修补把物体重新排列成面向任务的场景。
- 系统用 Grounding DINO 和 DINOv2 匹配从编辑后的图像中恢复物体位置，然后通过带约束优化细化坐标，在保留目标布局的同时消除碰撞。
- 它基于预定义的操作模板搜索可执行的子任务，并使用抓取点、功能点等物体元数据，而不是从头生成全部机器人代码。
- 执行后，Gemini 3 会根据视觉观测检查每个子任务；任何一步失败，整条轨迹都会被拒绝。该流水线还通过动作感知关键帧选择和 HEVC CRF 调参压缩视频，并把感知损失控制在 0.1 JOD 阈值以内。

## 结果
- 在长时程策略学习中，论文在 **4 个任务** 上用每个任务 **100 条合成专家轨迹** 微调 **π0.5** VLA 模型，并在每个任务上评估 **100 次以上试验**。
- 零样本预训练模型在 **4 个任务** 上的成功率都是 **0%**。在原始合成数据上训练后，**AutoCheckout** 的成功率为 **54%**，**PackBreads** 为 **54%**，**PackStationery** 为 **100%**，**SortToCabinet** 为 **25%**。
- 在压缩数据上训练得到的结果相近：同样四个任务的成功率分别为 **52%**、**50%**、**100%** 和 **28%**，支持了压缩不会明显损失训练效用这一说法。
- 在 **ALOHA-AgileX** 上的 Sim2Real 实验中，只使用 **10 个真实演示** 时，在 **20 次试验** 中成功率为 **20%**。将 **10 个真实演示 + 250 条仿真轨迹** 联合训练后，成功率提高到 **55%**，绝对提升 **35 个百分点**。
- 该压缩方法声称文件大小减少 **90% 以上**；Figure 1 和方法部分报告约为 **93%**，同时将感知损失保持在 **0.1 JOD** 以下。
- 这段摘录没有给出 IGSC 或 VLM 验证模块各自独立的消融数值，只有这些端到端任务结果；不过论文声称它们提高了场景可行性，并去除了静默失败轨迹。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09036v1](http://arxiv.org/abs/2604.09036v1)
