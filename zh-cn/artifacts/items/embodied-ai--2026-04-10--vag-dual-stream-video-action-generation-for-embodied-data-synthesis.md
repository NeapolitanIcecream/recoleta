---
source: arxiv
url: http://arxiv.org/abs/2604.09330v1
published_at: '2026-04-10T13:59:54'
authors:
- Xiaolei Lang
- Yang Wang
- Yukun Zhou
- Chaojun Ni
- Kerui Li
- Jiagang Zhu
- Tianze Liu
- Jiajun Lv
- Xingxing Zuo
- Yun Ye
- Guan Huang
- Xiaofeng Wang
- Zheng Zhu
topics:
- embodied-data-synthesis
- vision-language-action
- world-action-model
- robot-data-scaling
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# VAG: Dual-Stream Video-Action Generation for Embodied Data Synthesis

## Summary
## 摘要
VAG 是一个用于机器人数据合成的联合视频和动作生成器。它的目标是通过同时生成未来视频帧和匹配的动作轨迹，让合成的具身数据可以用于策略学习。

## 问题
- 机器人基础模型需要大规模遥操作数据，但为每个新任务或场景收集机器人示范都很昂贵，而且很慢。
- 标准世界模型可以生成未来视频，但不会输出训练机器人策略所需的配对动作。
- 先生成视频、再推断动作的两阶段方法，常常会丢失视频和动作的一致性，并在长时域上累积误差。

## 方法
- VAG 采用双流架构，一条分支生成视频，一条分支生成动作，两条分支都以首帧和语言指令为条件。
- 两条分支都使用 flow matching，并在相同的生成步骤中同步去噪，因此视频和动作会一起生成，时域长度为 93 帧，大约相当于 10 Hz 下的 10 秒。
- 视频分支基于 Cosmos-Predict2，预测未来的视频潜变量；动作分支是一个改造后的 1D U-Net，预测动作序列。
- 在每个去噪步骤中，VAG 取当前干净的视频潜变量，用自适应 3D 池化压缩成紧凑的全局嵌入，再把这个嵌入送入动作分支。
- 训练使用配对的机器人视频-动作轨迹，以及用 Qwen2.5-VL 提取、再由 T5-XXL 编码的文本指令。

## 结果
- 在 AgiBot 数据集上，VAG 在多个视频指标上优于 SVD、Wan2.2 和 Cosmos-Predict2：FVD 为 965，CP2 为 988，Wan2.2 为 1152，SVD 为 1311；LPIPS 为 0.320，对比 0.352、0.325 和 0.421；PSNR 为 15.1，对比 14.2、14.5 和 12.7。它的 FID 为 130，接近 CP2 的 135 和 Wan2.2 的 129。
- 在 AgiBot 的动作生成任务上，VAG 的 ED 为 0.81，成功率为 45%；对比之下，VAG-Video+AnyPos 的 ED 为 0.98，成功率为 29%；VAG-Video+ResNet 的 ED 为 1.54，成功率为 8%。
- 在 LIBERO 的动作生成任务上，VAG 的 ED 为 0.38，成功率为 79%；对比之下，VAG-Video+AnyPos 的 ED 为 0.55，成功率为 66%；VAG-Video+ResNet 的 ED 为 0.87，成功率为 37%。
- 在 LIBERO 的回放成功率上，VAG 在 Spatial 上为 70%，Object 为 72%，Goal 为 64%，Long 为 42%，平均为 62%。AnyPos 两阶段流程的平均成功率为 54%，ResNet 流程为 25%。
- 在一个自采集的真实机器人数据集上做下游 VLA 训练时，论文报告 VAG 的合成预训练把成功率从 35% 提高到 55%，提升了 20 个百分点。
- 论文还说，生成的动作可以在真实机器人上回放，并且可以支持可执行轨迹，但摘要没有给出更完整的真实机器人评估数字，除了 35% 到 55% 的 VLA 提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09330v1](http://arxiv.org/abs/2604.09330v1)
