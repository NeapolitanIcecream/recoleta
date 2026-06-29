---
source: arxiv
url: https://arxiv.org/abs/2606.03188v1
published_at: '2026-06-02T05:48:02'
authors:
- Fulong Ma
- Daojie Peng
- Wenjun Yue
- Jiahang Cao
- Bintao Wang
- Qiang Zhang
- Jun Ma
topics:
- world-action-model
- vision-language-action
- robot-manipulation
- structured-world-modeling
- semantic-supervision
- geometry-supervision
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# GeoSem-WAM: Geometry- and Semantic-Aware World Action Models

## Summary
## 总结
GeoSem-WAM 通过训练模型预测未来 RGB、几何和语义图，再在测试时用学到的潜在状态预测机器人动作，从而提升世界动作模型。它的目标是在部署时不生成未来视频的情况下，提高在杂乱场景、几何变化和语义变化下的动作成功率。

## 问题
- 只用 RGB 训练的 WAM 可能会漏掉操作任务所需的空间结构和物体语义。
- 在推理时展开未来视频会带来延迟；论文认为，WAM 的收益主要来自预测式训练对潜在特征的塑形。
- 这对真实机器人很重要，因为失败往往来自遮挡、干扰物、高度变化和长时程物体交互。

## 方法
- 以 Wan2.2-5B 视频 DiT 为基础，配合 T5 指令编码器、VAE 视频 token 和动作 DiT，采用 Mixture-of-Transformer 架构。
- 用四个损失训练：未来 RGB 潜在流匹配、动作块去噪、几何 L1 预测和语义像素级交叉熵。
- 在中间 Transformer token 上使用 DPT 风格的密集头，并为视频扩展了 3D 重组和融合模块。
- 部署时移除几何和语义头；动作预测只用当前观测和语言，然后对动作块去噪，不生成未来视频。

## 结果
- LIBERO 平均成功率为 98.55%，高于 Fast-WAM 的 97.60%、LingBot-VA 的 98.50% 和 Motus 的 97.70%；分项成功率分别是 Spatial 99.0%、Object 100.0%、Goal 98.2% 和 Long 97.0%。
- RoboTwin 2.0 平均成功率为 92.52%，高于 Fast-WAM 的 91.80% 和 LingBot-VA 的 92.20%；在无预训练情况下，clean 设置为 92.94%，random 设置为 92.14%。
- LIBERO 消融显示，仅 RGB 时平均成功率为 97.6%；加入几何后为 98.2%（+0.61），加入语义后为 98.1%（+0.51），两者都加上后为 98.6%（+1.02）。
- 真实 Franka 机器人在 7 个设置、每个设置 50 次试验中，平均成功率从 Fast-WAM 的 88.9% 提升到 GeoSem-WAM 的 95.4%（+6.6）。
- 真实泛化提升包括 Easy-Pick-B1 +10、Easy-Pick-B2 +8，以及高度变化 4 cm 的 Easy-Pick-D +12；多步任务提升包括 Multi-Pick +6、Multi-Goal +6 和 Pick-Pour +4。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03188v1](https://arxiv.org/abs/2606.03188v1)
