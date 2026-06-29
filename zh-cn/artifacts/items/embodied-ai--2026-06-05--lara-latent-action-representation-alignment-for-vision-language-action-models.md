---
source: arxiv
url: https://arxiv.org/abs/2606.07100v1
published_at: '2026-06-05T09:51:25'
authors:
- Mengya Liu
- Baoxiong Jia
- Jiangyong Huang
- Jingze Zhang
- Siyuan Huang
topics:
- vision-language-action
- latent-action-models
- robot-data-scaling
- diffusion-policy
- representation-alignment
- robot-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# LARA: Latent Action Representation Alignment for Vision-Language-Action Models

## Summary
## 总结
LARA 通过对齐内部动作表示，联合训练一个潜在动作模型和一个基于扩散的视觉-语言-动作策略。论文用未标注视频中的动态信息缓解机器人动作数据瓶颈，同时在策略学习时不冻结潜在动作模型。

## 问题
- VLA 策略需要大量带动作标注的机器人数据，但真实机器人演示成本高，数量也少。
- 潜在动作模型可以从未标注的人类或机器人视频中学习运动表示，但以往流程通常先单独训练 LAM，再将其冻结。
- 冻结的 LAM 可能编码与控制无关的视觉变化，而 VLA 策略也可能生成看起来合理、却不会带来预期状态变化的动作轨迹。

## 方法
- LARA 先用一个 LAM 将当前帧和未来帧映射到连续潜在动作，再用 VQ 风格码本对其量化，并由前向动力学模型重建未来帧。
- VLA 部分使用带 DiT 骨干的流匹配扩散策略，基于视觉语言特征、本体感觉和噪声生成动作片段。
- 在联合训练中，LARA 通过余弦相似度损失和一个可学习投影头，把 LAM 的潜在动作与 DiT 的中间特征对齐。
- 完整目标函数结合动作流匹配、LARA 对齐损失和 LAM 重建损失，因此 LAM 和 VLA 策略会一起更新。
- 这种方法可用于 VLA 预训练、对现有 VLA 模型进行后训练，或细化用作伪标签的 LAM 潜在动作标记。

## 结果
- 摘要称，在 3 个仿真基准和 1 个真实世界操作基准上，完整 VLA 训练平均提升约 10%，后训练增强约 5%，LAM 细化约 15%。
- 在 OXE 约束的 LIBERO 对比中，LARA full 的平均成功率为 88.6，高于 OpenVLA 的 76.5、Octo 的 75.1、LAPA 的 65.7，以及仅 DiT 的 LARA 的 84.4。
- 在 LIBERO Long 上，LARA full 为 86.0，高于 OpenVLA 的 53.7 和仅 DiT 的 LARA 的 76.5。
- 在 OXE 约束的 SIMPLER-ENV 对比中，LARA full 的平均成功率为 65.2，高于 Moto-GPT 的 61.4、OpenVLA 的 32.7、Octo 的 14.6，以及仅 DiT 的 LARA 的 55.8。
- 作为 GR00T-N1.6 的后训练附加模块，GR00T-N1.6-LARA 在 LIBERO 上报告的平均分为 95.6，高于 GR00T-N1.6 的 95.0；在 SIMPLER-ENV 上为 79.9，高于 78.9。
- 表格也显示，LARA full 并不是所有报告基准上的最高无约束模型：例如，GR00T-N1.6-LARA 在 SIMPLER-ENV 上为 79.9，villa-X 为 77.7，GR00T-N1.6 为 78.9；在 LIBERO 上，UniVLA 为 95.2，GR00T-N1.6-LARA 为 95.6。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.07100v1](https://arxiv.org/abs/2606.07100v1)
