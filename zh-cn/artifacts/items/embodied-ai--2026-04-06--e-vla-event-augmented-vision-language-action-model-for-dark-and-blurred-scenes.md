---
source: arxiv
url: http://arxiv.org/abs/2604.04834v1
published_at: '2026-04-06T16:35:57'
authors:
- Jiajun Zhai
- Hao Shi
- Shangwei Guo
- Kailun Yang
- Kaiwei Wang
topics:
- vision-language-action
- event-camera
- robot-manipulation
- low-light-robustness
- motion-blur
- embodied-ai
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# E-VLA: Event-Augmented Vision-Language-Action Model for Dark and Blurred Scenes

## Summary
## 总结
E-VLA 将事件相机信号加入视觉-语言-行动机器人策略，使机器人在 RGB 图像过暗或过模糊时仍能继续操作物体。论文显示，简单的事件融合已经有帮助，更小的事件适配器效果更好。

## 问题
- 标准 VLA 机器人策略依赖 RGB 帧，所以一旦采集阶段的感知失效，就会出问题：极端低照度、黑场截断和运动模糊。
- 图像增强可以在采集后改善外观，但无法恢复相机从未记录的信息。这对真实机器人部署很重要，因为腕部相机移动快，光照也会变化。
- 事件相机在这些条件下仍能捕捉亮度变化，但它稀疏、异步的输出与预训练的基于图像的 VLA 主干不匹配。

## 方法
- 论文构建了 **E-VLA**，这是一个事件增强的 VLA 模型，基于类似 SmolVLA 的主干，包含冻结的 SigLIP 视觉编码器和冻结的 LLM，以及可训练的动作层。
- 它把最近的事件流转换成与 RGB 帧对齐的类图像累积事件图。作者测试了事件窗口，结果显示，**固定最近计数窗口**比固定时长窗口带来更稳定的感知-行动耦合。
- 论文研究了两种保持预训练视觉 token 结构的融合方法：**叠加融合**，把事件线索直接写到 RGB 图像上，不增加参数；以及**分层事件适配器**，一个小型 ViT 风格分支，在第 3、6、9 和 12 层把事件特征注入 SigLIP。
- 它还引入了一个真实的同步 **RGB-事件-动作** 操作数据集，使用 DAVIS346 事件相机，在远程操控的 SO100 机器人上采集，覆盖 Pick-Place、Sorting 和 Stacking 任务，以及多个照明水平。

## 结果
- 数据集规模总计 **724** 个 episode，共 **339,310** 帧；其中 **305** 个 episode 在正常光照下，**419** 个 episode 覆盖较低光照设置。
- 在低照度下的 **Pick-Place** 任务中，仅图像模型的成功率从 **75 lux 时的 100%** 降到 **25 lux 和 20 lux 时的 0%**。E-VLA 叠加融合在 **25 lux** 时达到 **65%**，在 **20 lux** 时达到 **60%**。事件适配器在 **25 lux** 和 **20 lux** 时都达到 **90%**。
- 在 **75/40/35/30/25/20 lux** 下，Pick-Place 的平均成功率分别为：仅图像 **47.5%**，RetinexNet **66.7%**，Retinexformer **60.8%**，EvLight **70.0%**，E2VID **35.8%**，叠加融合 **80.8%**，事件适配器 **94.2%**。
- 摘要报告了在 **1000 ms 曝光** 下的运动模糊提升：Pick-Place 从仅图像的 **0%** 提升到 E-VLA 的 **20-25%**，Sorting 从 **5%** 提升到 **32.5%**。
- 摘要还报告，在 **20 lux** 下，Pick-Place 从仅图像的 **0%** 提升到叠加融合的 **60%** 和事件适配器的 **90%**。
- 引言称，在完全 **black clipping** 下，E-VLA 的任务成功率保持在 **80% 以上**，而仅图像基线为 **0%**。摘录里没有包含这个设置的完整表格。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04834v1](http://arxiv.org/abs/2604.04834v1)
