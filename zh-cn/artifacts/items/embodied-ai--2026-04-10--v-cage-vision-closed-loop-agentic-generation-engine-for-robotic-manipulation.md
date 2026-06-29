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
V-CAGE 是一个用于机器人操作的数据生成流程。它先构建仿真场景，再执行任务，用视觉语言模型检查结果，最后压缩生成的视频。论文面向长时序 Vision-Language-Action 训练，指出糟糕的场景布局和未被发现的执行错误会污染大规模合成数据集。

## 问题
- VLA 模型需要大量操作数据，但真实数据采集成本高，而且覆盖不了许多长尾情况。
- 现有合成流程常常在放置物体时缺少足够的任务上下文，容易导致碰撞、遮挡或目标位置无法到达。
- 许多系统是开环运行：代码执行没有报错，但任务在视觉上仍可能失败，这类静默失败会污染长时序训练数据。

## 方法
- V-CAGE 使用基于 OpenClaw 的 agentic 流程，把语言任务转成可用的仿真场景和已验证的操作轨迹。
- 其中的 Inpainting-Guided Scene Construction 会先选择相关资产，按无碰撞方式放置它们，写出语义布局计划，再用图像修补把物体重排成面向任务的场景。
- 它用 Grounding DINO 和 DINOv2 匹配从编辑后的图像中恢复物体位置，再用带约束优化细化坐标，在保留预期布局的同时消除碰撞。
- 它从预定义的操作模板中，结合抓取点和功能点等物体元数据搜索可执行的子任务，而不是从头生成全部机器人代码。
- 执行结束后，Gemini 3 会基于视觉观测检查每个子任务；任何一步失败，整条轨迹都会被拒绝。该流程还用面向动作的关键帧选择和在 0.1 JOD 感知损失阈值下调节 HEVC CRF 的方式压缩视频。

## 结果
- 在长时序策略学习中，论文在 **4 个任务** 上对 **π0.5** VLA 模型进行微调，每个任务使用 **100 条合成专家轨迹**，并在每个任务上做 **100 次试验**。
- 零样本预训练成功率在 **4 个任务** 上都是 **0%**。用原始合成数据训练后，**AutoCheckout** 的成功率是 **54%**，**PackBreads** 是 **54%**，**PackStationery** 是 **100%**，**SortToCabinet** 是 **25%**。
- 用压缩数据训练得到的结果相近：同样四个任务分别是 **52%**、**50%**、**100%** 和 **28%**，支持压缩不会损失训练可用性的说法。
- 在 **ALOHA-AgileX** 的 Sim2Real 中，只用 **10 个真实示范** 时，**20 次试验** 的成功率是 **20%**。和 **10 个真实示范 + 250 条仿真轨迹** 联合训练后，成功率升到 **55%**，绝对提升 **35 个百分点**。
- 该压缩方法声称文件大小减少 **90% 以上**；图 1 和方法部分给出的结果约为 **93%**，同时把感知损失保持在 **0.1 JOD** 以下。
- 这段摘要没有给出 IGSC 或 VLM 验证的单独消融数值，只给出了这些端到端结果，但论文声称它们能提高场景可行性并去除静默失败轨迹。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09036v1](http://arxiv.org/abs/2604.09036v1)
