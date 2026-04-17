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
这篇论文测试机器人是否能在训练时使用额外传感器来学会更轻柔的接触动作，同时在部署时不依赖这些传感器。在按钮按压任务上，带仪器监督的音频训练降低了接触力，但没有提高成功率。

## 问题
- 仅依靠相机输入和本体感觉，很难学习接触密集型操作，因为关键的接触事件只能被部分观察到。
- 对按钮按压来说，光有成功还不够；机器人还应以较低的力度按下按钮，避免过于生硬的交互。
- 论文提出的问题是：训练时的仪器化是否能提高策略质量，同时不让推理依赖带传感器的物体。

## 方法
- 实验装置包括 UR3e 机械臂、腕部 RGB 相机、指尖麦克风、腕部力矩传感器，以及一个仅在训练时提供二值按下/未按下信号的按钮。
- 作者自动采集示范：机器人从随机初始位姿接近按钮，通过带仪器的按钮信号检测按压事件，然后回撤。
- 他们使用特权按钮状态标签，将在 AudioSet 上预训练的 Audio Spectrogram Transformer 微调为二值点击检测器；该检测器在验证集上达到 **F1 = 0.988**，**假阴性率为 1.2%**。
- 他们使用视觉和音频训练 Diffusion Policy，并测试三种集成方式：使用微调后 AST 嵌入的 Deep Fusion、使用微调后 AST logits 的 Deep Fusion，以及 Soft Sensor。Soft Sensor 在训练时使用真实按钮状态，在测试时换成 AST 预测。
- 他们将这些方法与一个基线比较：该基线使用在 AudioSet 上预训练、但未针对任务微调的通用 AST。

## 结果
- 点击检测器可以作为有效的训练信号来源：验证集上 **F1 = 0.988**，**假阴性率为 1.2%**。
- 各策略的任务成功率接近：每个模型进行 **40 次 rollout** 时，成功率在 **45% 到 55%** 之间，且 **贝叶斯 95% 可信区间** 相互重叠。
- 专家示范在成功 rollout 中的垂直峰值力中位数为 **3.41 N**。
- 通用音频基线的动作更重，峰值力中位数为 **6.98 N**；Deep Fusion 将其降到 **5.87 N**（使用微调嵌入）和 **5.95 N**（使用微调分类器输出）。
- Soft Sensor 在力度表现上最差，达到 **9.37 N**。作者将其归因于训练测试不匹配，以及频谱图生成带来的最多 **50 ms** 延迟。
- 与专家力分布的 Wasserstein 距离也呈现相同趋势：Soft Sensor 为 **5.0 N**，通用 AST 为 **4.6 N**，使用微调分类器的 Deep Fusion 为 **2.8 N**，使用微调嵌入的 Deep Fusion 为 **2.5 N**，最接近专家行为。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05954v1](http://arxiv.org/abs/2604.05954v1)
