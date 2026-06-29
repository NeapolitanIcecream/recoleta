---
source: arxiv
url: http://arxiv.org/abs/2604.03956v1
published_at: '2026-04-05T04:23:18'
authors:
- Ravi Ranjan
- Agoritsa Polyzou
topics:
- vision-language-action
- robot-unlearning
- embodied-foundation-models
- generalist-robot-policy
- safety
- openvla
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models

## Summary
## 摘要
VLA-Forget 面向视觉-语言-动作机器人策略的选择性遗忘。它要移除不安全、虚假或敏感的行为，同时尽量保留视觉对齐、语言条件和动作性能。

## 问题
- VLA 机器人策略会把坏行为记在多个位置：视觉编码器、图像-语言连接层，以及生成动作的语言模型。
- 只针对视觉模型或只针对语言模型的标准遗忘方法，常常漏掉部分不想保留的行为，或者损害正常的机器人性能。
- 这很重要，因为 VLA 的错误会变成物理动作，比如看起来合理地抓取，却执行了错误指令。

## 方法
- 该方法把模型分成三部分：视觉编码器、跨模态投影器，以及上层动作/推理 Transformer 层。
- 它用一个基于遗忘梯度、保留梯度、参数尺度和梯度冲突的比例感知分数，选择要编辑的视觉层和投影层。
- 它用显著性比例选择动作/推理层，先从最相关的上层遗忘层开始，只有在遗忘仍然不够时才继续增加。
- 训练同时使用四个损失：保留数据上的保留损失、目标数据上的遗忘损失、把已遗忘输出推离原模型的不匹配损失，以及在保留样本和边界样本上的特征保留损失。
- 更新分阶段进行，并使用 LoRA 适配器和 PCGrad：先削弱视觉触发，再打断错误的视觉-语言绑定，最后压制残余的动作先验。

## 结果
- 在摘要中，论文声称相对强基线有 **遗忘效果提升 10%**、**感知特异性提升 22%**、**推理/任务保留提升 9%**，以及 **量化后恢复降低 55%**。
- 在 **OpenVLA-7B / Open X-Embodiment** 上，VLA-Forget 报告 **FC 93**、**RC 91**、**FAD 0.88**、**RAD 0.21**、**TSR 78**、**SVR 5**。与 **NPO** 相比，RC 从 **88 -> 91**，TSR 从 **74 -> 78**，RAD 从 **0.23 -> 0.21**，SVR 从 **8 -> 5**。与 **GA** 相比，FC 都是 **93**，但 RC 从 **60 -> 91**，TSR 从 **40 -> 78**。
- 在 **OpenVLA-7B / lerobot-pusht_image** 上，VLA-Forget 报告 **FC 95**、**RC 94**、**FAD 0.90**、**RAD 0.13**、**TSR 69**、**SVR 4**。与 **NPO** 相比，FC 从 **92 -> 95**，RC 从 **90 -> 94**，TSR 从 **65 -> 69**，RAD 从 **0.15 -> 0.13**，SVR 从 **7 -> 4**。
- 在 **pi0fast-base / Open X-Embodiment** 上，VLA-Forget 报告 **FC 94**、**RC 89**、**FAD 0.88**、**RAD 0.22**、**TSR 75**、**SVR 6**。与 **NPO** 相比，FC 从 **89 -> 94**，RC 从 **87 -> 89**，TSR 从 **72 -> 75**，RAD 从 **0.24 -> 0.22**。与 **GA** 相比，FC 从 **93 -> 94**，RC 从 **57 -> 89**，TSR 从 **38 -> 75**，而 SVR 保持 **6**。
- 从表格来看，GA 通常拿到最强或并列最强的遗忘分数，但 VLA-Forget 保留了更高的保留效用和任务成功率，这也是论文主张的主要优势。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03956v1](http://arxiv.org/abs/2604.03956v1)
