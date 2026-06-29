---
source: arxiv
url: http://arxiv.org/abs/2604.05954v1
published_at: '2026-04-07T14:46:55'
authors:
- Raman Talwar
- Remko Proesmans
- Thomas Lips
- Andreas Verleysen
- Francis wyffels
topics:
- contact-rich-manipulation
- imitation-learning
- audio-conditioned-policy
- training-time-instrumentation
- button-pressing
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# You're Pushing My Buttons: Instrumented Learning of Gentle Button Presses

## Summary
## 摘要
这篇论文测试了机器人能否在训练时使用额外传感器来学习更温和的接触行为，而在部署时不需要这些传感器。在按按钮任务上，仪器化音频监督降低了接触力，但没有提高成功率。

## 问题
- 仅靠相机输入和本体感觉很难学习接触密集型操作，因为关键接触事件只能部分观测到。
- 对按按钮任务来说，成功还不够；机器人应以低力按下按钮，避免粗暴接触。
- 论文询问，训练时的仪器化是否能提高策略质量，同时不让推理依赖被仪器化的物体。

## 方法
- 系统使用 UR3e 机械臂、腕部 RGB 相机、指尖麦克风、腕部力矩传感器，以及一个只在训练时提供按下/未按下二值信号的按钮。
- 作者自动收集示范：机器人从随机起始位姿接近按钮，从仪器化按钮信号检测按下事件，然后后退。
- 他们用 AudioSet 预训练的 Audio Spectrogram Transformer 做微调，把它训练成二分类点击检测器，使用特权按钮状态标签；这个检测器在验证集上达到 **F1 = 0.988**，**假阴性率 1.2%**。
- 他们用三种集成方式训练带视觉和音频的 Diffusion Policy：使用微调后 AST 嵌入的 Deep Fusion、使用微调后 AST logits 的 Deep Fusion，以及 Soft Sensor。Soft Sensor 在训练时使用真实按钮状态，在测试时替换为 AST 预测。
- 他们把这些方法与一个基线比较，后者使用通用的、未经任务特定微调的 AudioSet 预训练 AST。

## 结果
- 点击检测器作为训练信号来源效果很好：验证集上 **F1 = 0.988**，**假阴性率 1.2%**。
- 各个策略的任务成功率接近：每个模型 **40 次 rollout** 中约 **45% 到 55%**，贝叶斯 **95% 可信区间**有重叠。
- 专家示范在成功 rollout 中的垂直峰值力中位数为 **3.41 N**。
- 通用音频基线更粗暴，中位峰值力为 **6.98 N**；Deep Fusion 用微调嵌入时降到 **5.87 N**，用微调分类器输出时降到 **5.95 N**。
- Soft Sensor 在力表现上最差，为 **9.37 N**，作者把这归因于训练和测试不匹配，以及光谱图生成带来的最高 **50 ms** 延迟。
- 到专家力分布的 Wasserstein 距离也呈现相同模式：Soft Sensor 为 **5.0 N**，通用 AST 为 **4.6 N**，使用微调分类器的 Deep Fusion 为 **2.8 N**，使用微调嵌入的 Deep Fusion 为 **2.5 N**，最接近专家行为。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05954v1](http://arxiv.org/abs/2604.05954v1)
