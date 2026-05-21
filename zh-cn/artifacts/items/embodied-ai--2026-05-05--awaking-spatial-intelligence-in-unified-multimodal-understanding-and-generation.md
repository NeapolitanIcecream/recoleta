---
source: arxiv
url: https://arxiv.org/abs/2605.04128v1
published_at: '2026-05-05T15:49:47'
authors:
- Lin Song
- Wenbo Li
- Guoqing Ma
- Wei Tang
- Bo Wang
- Yuan Zhang
- Yijun Yang
- Yicheng Xiao
- Jianhui Liu
- Yanbing Zhang
- Guohui Zhang
- Wenhu Zhang
- Hang Xu
- Nan Jiang
- Xin Han
- Haoze Sun
- Maoquan Zhang
- Haoyang Huang
- Nan Duan
topics:
- spatial-reasoning
- multimodal-foundation-model
- image-generation
- image-editing
- world-models
relevance_score: 0.56
run_id: materialize-outputs
language_code: zh-CN
---

# Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation

## Summary
## 摘要
JoyAI-Image 是一个统一的图像理解、生成和编辑模型。它在基于 Qwen3-VL 的 MLLM 和 160 亿参数扩散 Transformer 上加入了更强的空间推理能力。

## 问题
- 现有统一视觉模型通常对理解、生成和编辑的连接较弱，因此图像编辑和生成视角不能稳定地利用场景几何信息。
- 论文关注布局、深度、物体关系、视角变化和跨视角一致性。这些能力对可控图像编辑很重要，也可能帮助后续的视觉-语言-动作系统和世界模型。

## 方法
- 模型使用 Qwen3-VL-8B-Instruct 作为 MLLM，用于图像/文本理解和指令解析。
- 在生成和编辑中，MLLM 输出隐藏状态特征，用来调节 160 亿参数的 MMDiT 扩散模型；Wan-2.1 VAE 将图像压缩为潜在 token。
- 作者构建了 OpenSpatial，这是一个以 3D 框为中心的数据引擎。它使用 3D 有向框、投影掩码、可见性检查和多视角一致性检查，把扫描数据和网络视频转换为空间问答对。
- 训练使用约 1130 万个样本，包括 610 万个通用理解样本、340 万个空间理解样本、140 万个指令改写样本和 13.74 万个空间编辑样本。
- MLLM 只在通用数据上使用监督学习加 KL 蒸馏进行微调，因此它在学习新空间技能的同时保留通用能力。

## 结果
- 在 9 个空间基准上，JoyAI-Image-Und 报告的空间平均分为 64.4，比 Qwen3-VL-8B-Instruct 的 59.1 高 5.3 分，与 Gemini-2.5-Pro 的 64.4 持平。
- 相比基础模型，增幅最大的项目是 AllAngles +11.5、3DSR_C +7.7、MMSI +7.7、ERQA +4.9 和 VSI +4.5。
- 在通用基准上，它保持了相近表现：MMBench_CN 83.7，相比基础模型 83.3；MathVista 74.4，相比 75.0；MMStar 71.3，相比 70.1；OCRB 87.9，相比 90.3。
- OpenSpatial 包含约 300 万条数据，覆盖 5 个空间能力组和 19 个子任务；完整空间训练子集报告为 340 万个样本。
- 摘录称该模型在生成、长文本渲染和编辑方面达到最先进或有竞争力的结果，但所提供文本没有给出详细的生成/编辑数值表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04128v1](https://arxiv.org/abs/2605.04128v1)
