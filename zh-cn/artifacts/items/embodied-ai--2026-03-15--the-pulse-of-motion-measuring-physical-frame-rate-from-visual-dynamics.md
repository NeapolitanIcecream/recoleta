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
- world-model
- temporal-grounding
- benchmarking
- physical-simulation
relevance_score: 0.54
run_id: materialize-outputs
language_code: zh-CN
---

# The Pulse of Motion: Measuring Physical Frame Rate from Visual Dynamics

## Summary
本文提出 **Visual Chronometer**，用于仅从视频运动外观中估计真实物理帧率（PhyFPS），以测量并纠正生成视频中的“时间尺度幻觉”。作者还构建了两个基准，显示当前主流视频生成模型普遍存在物理速度与标称帧率不一致的问题。

## Problem
- 论文要解决的是：视频生成模型虽然画面和运动看起来平滑，但**缺乏与真实世界时间对应的稳定节拍**，导致动作速度含糊、漂移、不可控，作者称之为 **chronometric hallucination**。
- 这很重要，因为如果视频模型被视为**世界模型**，就不仅要会生成“看起来像在动”的画面，还要让运动速度符合真实物理时间；否则无法可靠模拟现实动态。
- 现有训练通常把慢动作、延时摄影、正常视频统一按标准帧率处理，模型学不到“每一帧到底对应现实中过了多少时间”。

## Approach
- 核心方法是 **Visual Chronometer**：输入一段视频，直接根据其中的视觉动态预测其隐含的真实物理帧率 **PhyFPS**，而不是依赖不可靠的元数据 FPS。
- 训练方法很直接：从一批确认“元数据 FPS = 真实 FPS”的高可信视频出发，先升采样到 **240 FPS**，再通过**受控时间重采样**合成不同物理帧率版本，让模型学会“这种运动看起来像 12/24/60/... FPS”。
- 为了逼近真实拍摄机制，作者合成了三类时间采样：**sharp capture**（快门快、无模糊）、**motion blur**（不同曝光长度的运动模糊）、**rolling shutter**（滚动快门畸变）。
- 模型结构上，采用 **VideoVAE+** 作为视频编码器，再接一个**attention pooling 回归头**输出 `log(PhyFPS)`，并在对数空间用 **MSE** 训练，以更稳定地处理宽范围帧率。
- 论文还提出两个基准：**PhyFPS-Bench-Real** 用于验证真实视频上的预测精度，**PhyFPS-Bench-Gen** 用于审计生成模型在 meta FPS 对齐、视频内稳定性、视频间稳定性三方面的表现。

## Results
- 训练数据覆盖 **18 个目标 PhyFPS**，最终得到 **465,535** 个视频片段，统一为 **128 帧**；训练时使用最多 **32 帧** 的窗口，训练 **125,000** 次迭代，4 张 **RTX A6000**，全局 batch size **32**。
- 在 **PhyFPS-Bench-Gen** 上，作者评测了多种开源/闭源视频生成模型，发现普遍存在明显的 **Meta FPS 与 PhyFPS 失配**。例如：**LTX-Video** 的 meta FPS 为 **24**，预测 PhyFPS 为 **46.52**，平均误差 **23.67 FPS**、百分比误差 **99%**；**InfinityStar (10s)** 为 **16 → 36.15**，平均误差 **20.19 FPS**、百分比误差 **126%**。
- 相对较好的开源模型是 **Wan2.1-T2V-1.3B**：meta FPS **24**，PhyFPS **26.28**，平均误差 **7.54 FPS**、百分比误差 **31%**。相对较好的闭源模型是 **Sora-2**：meta FPS **30**，PhyFPS **36.21**，平均误差 **8.40 FPS**、百分比误差 **28%**。
- 时间稳定性方面，不同模型的 **Intra CV** 约在 **0.10–0.17**，**Inter CV** 约在 **0.25–0.52**，说明不仅整体速度常常不准，而且同一模型不同视频、甚至同一视频不同片段之间也存在时间尺度抖动。
- 用户研究收集了 **1,490** 次两两比较、超过 **15** 名参与者。原始生成视频的时间自然度偏好仅 **19.0%**；按预测平均 PhyFPS 做全局校正的 **Pred** 达到 **44.2%**，按局部片段动态校正的 **Pred Dyn** 为 **36.9%**，表明基于 PhyFPS 的后处理能显著提升人类感知自然度。
- 摘要与正文还声称：强视觉语言模型作为 PhyFPS 评审“**非常不可靠**”，但给定摘录中未提供对应的定量数值。PhyFPS-Bench-Real 的具体精度数字在摘录里也未展开。

## Link
- [http://arxiv.org/abs/2603.14375v1](http://arxiv.org/abs/2603.14375v1)
