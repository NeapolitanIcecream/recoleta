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

# 机器人策略和世界模型正在接受记忆、接触和动作忠实度的检验

## Overview
当天最清楚的信号是具身 AI 受到评测压力。经过几天的 Vision-Language-Action（VLA）部署工作后，这些论文把成功条件放到了记忆、接触感知、动作条件预测和空间一致性上。RLDX-1、RoboAlign-R1 和 iWorld-Bench 提供了最强的证据。

## Clusters

### Dexterous VLA policies
RLDX-1 将灵巧操作视为一个多信号控制问题。该策略在基于 Qwen3-VL 的 VLA 上加入了视频运动、小型记忆库，以及触觉或扭矩输入。它的 Multi-Stream Action Transformer 会先把认知、本体感觉和物理三条流分开，再用跨流注意力把它们合并，用于动作预测。

报告中的提升主要出现在当前图像策略难以处理的任务上。RLDX-1 在 ALLEX 人形任务上的成功率为 86.8%，而 π₀.₅ 和 GR00T N1.6 约为 40%。在 ALLEX Object-in-Box Selection 这个对记忆要求很高的任务上，它的成功率为 91.7%，而两个基线都在 30% 左右。报告还把部署和延迟联系起来：推理优化把 RTX 5090 上的单步延迟从 71.2 ms 降到 43.7 ms。

#### Evidence
- [RLDX-1 Technical Report](../Inbox/2026-05-05--rldx-1-technical-report.md): Summary details RLDX-1 architecture, training stages, success rates, memory task results, and latency reduction.

### Robot video world models
RoboAlign-R1 让机器人视频预测对任务层面的行为负责，而不只是像素损失。它先微调一个 8B 多模态裁判，再把它蒸馏成一个 98M 奖励模型，并用这个奖励做后训练。这个裁判会给指令遵循、操作成功、动作与结果一致性、时间一致性、接触真实性和物理遵循打分。

论文报告的 RobotWorldBench 分数是 8.52±0.15，而 iVideoGPT 是 7.74±0.62。它的 Sliding Window Re-encoding 方法会在长预测过程中刷新 rollout 上下文，并在只增加约 1% 延迟的情况下，报告了更好的 SSIM、PSNR、LPIPS 和 ROI-LPIPS。这个结论很直接：长时域机器人视频模型既需要行为奖励，也需要 rollout 维护。

#### Evidence
- [RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models](../Inbox/2026-05-05--roboalign-r1-distilled-multimodal-reward-alignment-for-robot-video-world-models.md): Summary gives the distilled reward setup, six judge dimensions, benchmark results, and sliding-window rollout metrics.

### Interactive world-model benchmarks
iWorld-Bench 针对交互式世界模型中的一个测量缺口：生成的未来是否遵循动作并保留记忆。它统一了文本指令、one-hot 控制和相机参数的动作输入，让不同控制格式的模型可以在相似任务上比较。

这个基准覆盖面很大。它包含 330,000 个视频片段，选出 2,100 个评测视频，并围绕动作控制难度、记忆和相机跟随定义了 4,900 个测试任务。数据覆盖四种视角、九种户外天气、五种室内光照类型和 18 个仿真环境。给出的文本没有模型排行榜，所以这里能直接确认的贡献是基准规模和动作映射。

#### Evidence
- [iWorld-Bench: A Benchmark for Interactive World Models with a Unified Action Generation Framework](../Inbox/2026-05-05--iworld-bench-a-benchmark-for-interactive-world-models-with-a-unified-action-generation-framework.md): Summary provides dataset scale, task counts, action standardization, coverage, and the limitation on missing leaderboard values.

### Spatial reasoning for unified visual models
JoyAI-Image 围绕空间监督把图像理解、生成和编辑连在一起。系统用 Qwen3-VL-8B-Instruct 做多模态理解和指令解析，再用一个 16B 扩散 Transformer 进行生成和编辑。它的 OpenSpatial 数据引擎从 3D 边界框、掩码、可见性检查和多视角一致性检查中构建空间问答和编辑数据。

报告里最强的结果出现在空间理解上。JoyAI-Image-Und 在九个空间基准上的平均分达到 64.4，比 Qwen3-VL-8B-Instruct 高 5.3 分，并与给定摘要中的 Gemini-2.5-Pro 持平。通用基准分数仍然接近基础模型，这一点很重要，因为新增的空间训练没有在报告测试里抹掉更广泛的视觉能力。

#### Evidence
- [Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation](../Inbox/2026-05-05--awaking-spatial-intelligence-in-unified-multimodal-understanding-and-generation.md): Summary gives JoyAI-Image architecture, OpenSpatial data construction, training mix, and spatial benchmark results.
