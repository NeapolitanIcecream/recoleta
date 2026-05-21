---
kind: trend
trend_doc_id: 279
granularity: day
period_start: '2026-05-05T00:00:00'
period_end: '2026-05-06T00:00:00'
topics:
- robotics
- VLA
- world models
- spatial reasoning
- benchmarks
- multimodal models
run_id: materialize-outputs
aliases:
- recoleta-trend-279
tags:
- recoleta/trend
- topic/robotics
- topic/vla
- topic/world-models
- topic/spatial-reasoning
- topic/benchmarks
- topic/multimodal-models
language_code: zh-CN
---

# 机器人策略和世界模型正按记忆、接触和动作保真度接受评判

## Overview
今天最清晰的信号是具身 AI 面临更高的评测压力。经过几天的 Vision-Language-Action (VLA) 部署工作后，当前论文把成功与记忆、接触感知、动作条件预测和空间一致性绑定起来。RLDX-1、RoboAlign-R1 和 iWorld-Bench 提供了最强证据。

## Clusters

### 灵巧操作 VLA 策略
RLDX-1 将灵巧操作视为多信号控制问题。该策略在基于 Qwen3-VL 的 VLA 中加入视频运动、小型记忆存储，以及触觉或扭矩输入。它的 Multi-Stream Action Transformer 先将认知、本体感知和物理流分开处理，再通过跨流注意力合并这些信息，用于动作预测。

报告中的提升主要出现在只看当前图像的策略容易失败的任务上。RLDX-1 在 ALLEX 人形机器人任务上报告 86.8% 的成功率，而 π₀.₅ 和 GR00T N1.6 约为 40%。在需要大量记忆的 ALLEX Object-in-Box Selection 任务上，它报告 91.7% 的成功率，而两个基线都在 30% 区间。报告还把部署与延迟联系起来：推理优化将 RTX 5090 上的单步延迟从 71.2 ms 降至 43.7 ms。

#### Evidence
- [RLDX-1 Technical Report](../Inbox/2026-05-05--rldx-1-technical-report.md): 摘要详细说明了 RLDX-1 的架构、训练阶段、成功率、记忆任务结果和延迟降低。

### 机器人视频世界模型
RoboAlign-R1 让机器人视频预测对任务层面的行为负责，而不只优化像素损失。它微调一个 8B 多模态评判器，将其蒸馏成一个 98M 奖励模型，并把该奖励用于后训练。评判器从指令遵循、操作成功、动作-结果一致性、时间一致性、接触真实感和物理遵循六个方面打分。

论文报告的 RobotWorldBench 分数为 8.52±0.15，iVideoGPT 为 7.74±0.62。它的 Sliding Window Re-encoding 方法会在长预测过程中刷新 rollout 上下文，并在约 1% 额外延迟下报告更好的 SSIM、PSNR、LPIPS 和 ROI-LPIPS。实际结论很明确：长时程机器人视频模型需要行为奖励，也需要 rollout 维护。

#### Evidence
- [RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models](../Inbox/2026-05-05--roboalign-r1-distilled-multimodal-reward-alignment-for-robot-video-world-models.md): 摘要给出了蒸馏奖励设置、六个评判维度、基准结果和滑动窗口 rollout 指标。

### 交互式世界模型基准
iWorld-Bench 针对交互式世界模型的一个测量缺口：生成的未来是否遵循动作并保留记忆。它在文本命令、one-hot 控制和相机参数之间标准化动作输入，使控制格式不同的模型可以面对可比较的任务。

该基准覆盖范围很大。它包含 330,000 个视频片段，选取 2,100 个评测视频，并围绕动作控制难度、记忆和相机跟随定义 4,900 个测试任务。其数据覆盖四种视角、九种室外天气、五种室内光照和 18 个模拟器环境。给定文本没有提供模型排行榜，因此有依据的贡献是基准规模和动作映射。

#### Evidence
- [iWorld-Bench: A Benchmark for Interactive World Models with a Unified Action Generation Framework](../Inbox/2026-05-05--iworld-bench-a-benchmark-for-interactive-world-models-with-a-unified-action-generation-framework.md): 摘要提供了数据集规模、任务数量、动作标准化、覆盖范围，以及缺少排行榜数值这一限制。

### 统一视觉模型的空间推理
JoyAI-Image 围绕空间监督连接图像理解、生成和编辑。系统使用 Qwen3-VL-8B-Instruct 进行多模态理解和指令解析，再以此条件化一个 16B 扩散 Transformer，用于生成和编辑。它的 OpenSpatial 数据引擎基于 3D 框、掩码、可见性检查和多视角一致性检查构建空间问答与编辑数据。

报告中最强的结果出现在空间理解上。JoyAI-Image-Und 在九个空间基准上的平均分达到 64.4，比 Qwen3-VL-8B-Instruct 高 5.3 分，并在给定摘要中与 Gemini-2.5-Pro 持平。通用基准分数接近基础模型，这一点有实际意义，因为报告的测试显示，新增的空间训练没有抹掉广泛的视觉能力。

#### Evidence
- [Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation](../Inbox/2026-05-05--awaking-spatial-intelligence-in-unified-multimodal-understanding-and-generation.md): 摘要给出了 JoyAI-Image 架构、OpenSpatial 数据构建、训练混合方式和空间基准结果。
