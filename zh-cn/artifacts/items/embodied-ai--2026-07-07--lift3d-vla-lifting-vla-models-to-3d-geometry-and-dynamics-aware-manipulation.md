---
source: arxiv
url: https://arxiv.org/abs/2607.06564v1
published_at: '2026-07-07T17:59:47'
authors:
- Jiaming Liu
- Qingpo Wuwu
- Nuowei Han
- Hao Chen
- Zhuoyang Liu
- Fan Fei
- Yueru Jia
- Chenyang Gu
- Yandong Guo
- Boxin Shi
- Shanghang Zhang
topics:
- vision-language-action
- robot-foundation-model
- point-cloud-reasoning
- temporal-action-modeling
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation

## Summary
## 摘要
Lift3D-VLA 为 VLA 机器人策略加入了显式点云推理和时间动作解码。论文称，相比此前的 VLA 基线，它在仿真和真实机器人上的操作成功率更高。

## 问题
- VLA 策略通常使用 2D 图像，因此可能漏掉可达性、接触、遮挡以及其他对物理操作很重要的 3D 约束。
- 以往的 3D VLA 方法要么需要稀缺的 3D 机器人数据，要么在 2D 和 3D 格式之间投影时丢失几何信息。
- 作者此前的方法 Lift3D 改进了 3D 感知，但没有直接用随时间变化的点云几何进行训练，也没有解码具有时间结构的动作块。

## 方法
- 该模型通过把 3D 点投影到六个虚拟平面，并对匹配的预训练 2D 位置嵌入取平均，将预训练 2D VLA 视觉编码器复用于点云。
- 点云分词器对 1024 个输入点进行采样和分组，生成 256 个 token，然后将它们与 RGB token 一起送入共享的 2D 视觉编码器。
- Geometry-Centric Masked Autoencoding 训练编码器重建当前点云中的被遮蔽点，并预测下一帧点云几何。
- 系统使用 VGGT 为仅含 RGB 的机器人数据集合成伪点云，然后用 140K 条轨迹训练 GC-MAE，并用 400K 条轨迹进行机器人预训练。
- 逐层时间动作建模把一个动作块中的不同动作步骤分配给 LLaMA2-7B 的中间层和深层，使多个层共同预测序列，而不是只使用最终动作头。

## 结果
- 评估覆盖 22 个仿真任务和 8 个真实世界操作任务。
- 在 MetaWorld 上，Lift3D-VLA 报告的平均成功率比摘录中表现最好的既有 VLA 方法高 10.8%。
- 在 RLBench 上，它报告的平均成功率比摘录中表现最好的既有 VLA 方法高 11.1%。
- 在真实世界任务中，它比最强基线高 4 个百分点；摘录没有提供绝对成功率。
- 论文还声称，在未见过的物体、背景和光照上的分布外泛化更强，并且在场景条件变化下的重复舀鸡蛋长时程任务中表现更好。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.06564v1](https://arxiv.org/abs/2607.06564v1)
