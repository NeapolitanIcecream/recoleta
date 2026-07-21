---
source: arxiv
url: https://arxiv.org/abs/2607.17523v1
published_at: '2026-07-20T03:56:43'
authors:
- Yongheng Zhang
- Guang Yang
- Ruihan Hou
- Qiguang Chen
- Ziang Liu
- Xiaolong Liu
- Manman Zhang
- Yanchao Hao
- Zheng Wei
- Hao Wu
- Libo Qin
- Peishan Dai
- Yinghui Li
- Di Yin
- Xing Sun
topics:
- world-models
- video-generation
- causal-reasoning
- multimodal-evaluation
- physical-simulation
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# Thinking in Video: Can Video Generators Really Reason About the Real World?

## Summary
## 摘要
论文提出“视频中思考”（Thinking in Video），用于检验视频生成器是否能够推理现实世界中的因果动态，而不仅仅是生成看似合理的运动。其因果生成双重评判框架（Causal-Generative Dual-Judge，CGDJ）发现，模型理解因果结构的能力与生成正确未来状态的能力之间存在差距。

## 问题
- Fréchet Video Distance 等传统视频指标可以衡量视觉质量，但无法证明因果关系是否正确。
- 生成器可能通过记忆视觉模式生成逼真的结果，却并不理解导致该结果的条件。
- 对于将视频生成器视为能够进行开放世界推理和决策的世界模型而言，这一区分十分重要。

## 方法
- CGDJ 将显式因果感知与隐式生成预测分开评估。
- 在显式感知评估中，Flatten Temporal Video 将采样得到的 70 帧转换为 7×10 的空间网格，并将问题栅格化后置于网格上方，从而构成单张 1280×720 的图像输入。
- 在隐式预测评估中，将 600 个视频分别在专家标注的因果转折点处切分；使用事件发生前的 7 个关键帧作为条件，生成事件发生后的序列。
- 基准测试使用 900 个 Video-MME 视频评估因果理解，并使用 600 个视频评估因果动作生成，其中包括 300 个自然科学样本和 300 个社会学与人文学科样本。
- Gemini-3-Pro 根据语义一致性、与参考内容的一致性和物理有效性，评判因果正确性与生成质量；使用 Whisper-large-v2 转录生成音频，以进行单独的视听分析。

## 结果
- 摘录未提供数值准确率或质量分数，因此无法在此报告与基线的直接指标比较。
- 包括 Wan-2.2-14B 和 HunyuanVideo-1.5 在内的开源模型能够生成具有中等合理性的因果延续，但在扁平化视频协议下，其显式因果感知能力接近于零。
- 闭源模型 Sora-2 和 Veo-3.1 表现出可测量的显式因果感知能力，以及更强的感知与预测一致性，但这种一致性仍然有限。
- 模型在音频中用语言表达正确因果逻辑的可靠性，往往高于其渲染相应视觉结果的可靠性，暴露出视听不一致。
- 这些发现支持“感知—预测差距”（Perception-Prediction Gap）的存在：仅有合理的动态表现，并不能证明模型具备稳健的因果推理能力或可靠的世界模拟能力。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.17523v1](https://arxiv.org/abs/2607.17523v1)
