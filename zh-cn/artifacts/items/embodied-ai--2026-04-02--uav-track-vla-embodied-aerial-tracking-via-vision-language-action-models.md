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
UAV-Track VLA 面向按指令执行的空中视觉跟踪，使用端到端视觉-语言-动作模型，并提出了一个新的无人机跟踪基准。论文在基于 \$\pi_{0.5}\$ 的策略上加入时间建模和空间定位，并在 CARLA 中报告了更好的跟踪成功率和更低的推理延迟。

## 问题
- 论文研究具身无人机跟踪：无人机需要根据视觉输入、语言指令和自身状态跟随目标，同时输出连续飞行动作。
- 这个问题重要，是因为当前的无人机跟踪常依赖手动控制或仅基于视觉的主动跟踪，无法处理城市场景中对自然语言任务的描述，例如行人、车辆、遮挡和快速运动。
- 现有用于跟踪的 VLA 模型有两个已指出的缺口：对多帧时间信息利用不足，以及缺少用于精确连续控制的空间几何先验。

## 方法
- 作者构建了 **UAV-Track**，这是一个基于 CARLA 的基准和数据集，包含 **892,756 帧**、**176 个任务** 和 **85 个对象**，覆盖城市场景、天气变化、目标速度变化和语言指令。
- 模型以 **\$\pi_{0.5}\$** 为起点，输入包括 **4 帧 RGB 图像**（当前帧加 3 帧历史帧）、一条语言指令和无人机本体感知状态。
- **时间压缩网络** 会减少 3 帧历史图像的 token 数量，再与当前帧 token 结合，使模型在不大幅增加计算量的情况下保留运动历史。
- **双分支解码器** 将输出分成两部分：(1) 空间定位头，用于预测目标相对 3D 位置和偏航角，作为辅助监督；(2) **flow-matching 动作专家**，用于预测用于无人机控制的 **25 步**连续位移序列。
- 训练使用混合损失：定位分支使用位置损失，动作分支使用 flow-matching 损失，使共享编码器学习对控制有用的几何信息。

## 结果
- 在具有挑战性的**长距离行人跟踪**任务中，UAV-Track VLA 报告了 **61.76% 的成功率** 和 **269.65 的平均跟踪帧数**。
- 摘要称这些结果**显著优于现有基线**，但给出的摘录没有包含完整的对比表，因此无法量化相对各个基线的具体领先幅度。
- 与原始 **\$\pi_{0.5}\$** 相比，该模型将单步推理延迟降低了 **33.4%**，达到每步 **0.0571 秒**。
- 该基准包含 **892,756 帧**，其中约 **20 万**帧来自专家演示，约 **69 万**帧来自自动采集。
- 论文声称模型在未见环境中具备**零样本泛化**能力，但给出的摘录没有包含对应的定量分数。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02241v1](http://arxiv.org/abs/2604.02241v1)
