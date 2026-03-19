---
source: arxiv
url: http://arxiv.org/abs/2603.14375v1
published_at: '2026-03-15T13:29:31'
authors:
- Xiangbo Gao
- Mingyang Wu
- Siyuan Yang
- Jiongze Yu
- Pardis Taghavi
- Fangzhou Lin
- Zhengzhong Tu
topics:
- video-generation
- temporal-grounding
- physical-simulation
- benchmarking
- motion-analysis
relevance_score: 0.36
run_id: materialize-outputs
language_code: zh-CN
---

# The Pulse of Motion: Measuring Physical Frame Rate from Visual Dynamics

## Summary
本文提出 **Visual Chronometer**，用于仅凭视频中的运动线索估计真实的物理帧率（PhyFPS），从而测量并纠正生成视频中的“时间尺度幻觉”。作者还构建了两个基准，显示当前主流视频生成模型普遍存在物理时间尺度错位与不稳定。

## Problem
- 现有视频生成模型通常只生成“看起来流畅”的运动，但没有稳定、可控、符合真实世界的时间尺度。
- 训练数据把慢动作、延时摄影和正常视频统一按标准帧率处理，导致模型学不到“每一帧对应多少真实时间”。
- 这会造成作者定义的 **chronometric hallucination**：生成视频的运动速度含糊、不稳定、且难以控制；这对把视频模型当作世界模型很重要，因为物理模拟不仅要对空间正确，也要对时间正确。

## Approach
- 核心机制很简单：训练一个回归器 **Visual Chronometer**，输入一段视频，直接预测该视频运动所隐含的真实物理帧率 **PhyFPS**，而不是依赖不可靠的元数据 FPS。
- 为了获得监督信号，作者从时间标注可靠的数据源收集高保真视频，并先上采样到 240 FPS，再通过三种受物理启发的时间重采样方式合成不同 PhyFPS：**sharp capture**、**motion blur**、**rolling shutter**。
- 模型结构上，使用 **VideoVAE+** 作为视频编码器，再加一个基于 attention 的查询池化头，最后回归 `log(PhyFPS)`；在对数空间用 MSE 训练，以更稳定地覆盖 2 到 240 FPS 的范围。
- 作者构建了两个评测集：**PhyFPS-Bench-Real** 用于验证真实视频上的预测精度，**PhyFPS-Bench-Gen** 用于审计生成模型的 meta FPS 与实际 PhyFPS 对齐程度，以及视频内/视频间时间稳定性。
- 还将预测到的 PhyFPS 用作后处理信号，对生成视频进行全局或局部重定时，测试是否能提升人类感知的自然度。

## Results
- 训练集覆盖 **18 个目标 PhyFPS**（2, 5, 10, ... , 240），共 **465,535** 个视频片段，统一为 **128 帧**；训练时使用最长 **32 帧** 的窗口。
- 在 **PhyFPS-Bench-Gen** 上，主流生成模型普遍存在严重错位。例如：**LTX-Video** 的 meta FPS 为 **24**，但预测 PhyFPS 为 **46.52**，平均误差 **23.67 FPS**、百分比误差 **99%**；**InfinityStar (10s)** 的 meta FPS 为 **16**，PhyFPS 为 **36.15**，平均误差 **20.19 FPS**、百分比误差 **126%**。
- 相对较好的对齐结果也仍有明显误差：开源中 **Wan2.1-T2V-1.3B** 平均误差 **7.54 FPS**、百分比误差 **31%**；闭源中 **Sora-2** 平均误差 **8.40 FPS**、百分比误差 **28%**；**Seedance-1.0-Lite** 为 **8.31 FPS / 35%**。
- 时间稳定性方面，各模型的 **Intra CV** 大致在 **0.10–0.17**，**Inter CV** 大致在 **0.25–0.52**，说明同一视频内部和不同视频之间都存在明显时间抖动；例如 **CogVideoX-5B** 的 Inter CV 为 **0.52**，而 **Seedance-1.5-Pro** 的 Inter CV 为 **0.25**。
- 用户研究收集了 **1,490** 次成对比较、超过 **15** 名参与者。原始视频的偏好得分为 **19.0%**，基于平均 PhyFPS 的全局校正 **Pred** 为 **44.2%**，局部动态校正 **Pred Dyn** 为 **36.9%**，表明基于 PhyFPS 的后处理显著提升了人类感知的时间自然度。
- 文中还明确声称：强大的通用 **VLM** 作为 PhyFPS 评判器“非常不可靠”，但在给定摘录中未提供其具体量化分数。

## Link
- [http://arxiv.org/abs/2603.14375v1](http://arxiv.org/abs/2603.14375v1)
