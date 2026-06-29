---
source: arxiv
url: http://arxiv.org/abs/2604.02241v1
published_at: '2026-04-02T16:33:38'
authors:
- Qiyao Zhang
- Shuhua Zheng
- Jianli Sun
- Chengxiang Li
- Xianke Wu
- Zihan Song
- Zhiyong Cui
- Yisheng Lv
- Yonglin Tian
topics:
- vision-language-action
- uav-tracking
- embodied-visual-tracking
- simulator-benchmark
- temporal-modeling
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# UAV-Track VLA: Embodied Aerial Tracking via Vision-Language-Action Models

## Summary
## 摘要
UAV-Track VLA 面向指令跟随的空中视觉跟踪，提出了一个端到端的视觉-语言-动作模型和一个新的无人机跟踪基准。论文在基于 \$\pi_{0.5}\$ 的策略上加入了时间建模和空间定位，在 CARLA 中报告了更高的跟踪成功率和更低的推理延迟。

## 问题
- 论文处理的是具身无人机跟踪：无人机要根据视觉输入、语言指令和自身状态跟随目标，同时输出连续飞行动作。
- 这很重要，因为现有无人机跟踪常依赖人工控制或仅基于视觉的主动跟踪，无法处理城市场景中的自然语言任务描述、行人、车辆、遮挡和快速运动。
- 用于跟踪的现有 VLA 模型有两个明确缺口：对多帧时间信息的利用较弱，对精确连续控制所需的空间几何先验利用较弱。

## 方法
- 作者构建了 **UAV-Track**，这是一个基于 CARLA 的基准和数据集，包含 **892,756** 帧、**176** 个任务和 **85** 个对象，覆盖城市场景、天气变化、目标速度变化和语言指令。
- 模型以 **\$\pi_{0.5}\$** 为起点，将 **4** 帧 RGB 图像（当前帧加上 3 帧历史帧）、一条语言指令和无人机本体感觉作为输入。
- 一个 **时间压缩网络** 会减少 3 帧历史帧的 token 数量，再把这些 token 与当前帧 token 合并，这样模型可以保留运动历史，同时不会让计算量大幅增加。
- 一个 **双分支解码器** 将输出分成两部分：（1）空间定位头，预测目标的相对三维位置和偏航角，作为辅助监督；（2）**flow-matching 动作专家**，预测一个 **25 步** 的连续位移序列，用于无人机控制。
- 训练时使用混合损失，空间定位分支用位置损失，动作分支用 flow-matching 损失，这样共享编码器会学到对控制有用的几何信息。

## 结果
- 在具有挑战性的 **远距离行人跟踪** 任务上，UAV-Track VLA 报告了 **61.76%** 的成功率和 **269.65** 的平均跟踪帧数。
- 摘要称这些结果 **显著优于现有基线**，但给出的摘录没有包含完整对比表，因此无法量化与各个基线的差距。
- 该模型将单步推理延迟降低了 **33.4%**，相对于原始 **\$\pi_{0.5}\$**，每步达到 **0.0571 s**。
- 该基准包含 **892,756** 帧，其中大约 **20 万** 帧来自专家演示，**69 万** 帧来自自动采集。
- 论文声称模型在未见环境中有 **零样本泛化** 能力，但给出的摘录没有包含对应的量化分数。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02241v1](http://arxiv.org/abs/2604.02241v1)
