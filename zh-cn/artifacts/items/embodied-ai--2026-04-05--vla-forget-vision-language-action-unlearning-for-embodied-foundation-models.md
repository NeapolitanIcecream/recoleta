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
VLA-Forget 面向视觉-语言-动作机器人策略的选择性遗忘。它删除不安全、伪相关或敏感行为，同时尽量保持视觉落地、语言条件控制和动作表现不受影响。

## 问题
- VLA 机器人策略可能会在多个位置同时记住有害行为：视觉编码器、图像-语言连接模块，以及生成动作的语言模型。
- 只针对视觉模型或只针对语言模型的标准遗忘方法，往往会漏掉一部分不想要的行为，或者损害机器人的正常表现。
- 这很重要，因为 VLA 的错误会变成物理动作，比如在抓取动作看起来合理时，仍然执行了错误的指令。

## 方法
- 该方法将模型分成三部分：视觉编码器、跨模态投影器，以及上层动作/推理 Transformer 层。
- 它用一个 ratio-aware 分数来选择需要编辑的视觉层和投影器层，这个分数基于 forget gradients、retain gradients、参数规模和梯度冲突。
- 它用 significance ratio 选择动作/推理层，从与遗忘目标最相关的高层开始，只有在遗忘效果仍然不足时才继续增加更多层。
- 训练时同时使用四种损失：保留数据上的 retain loss、目标数据上的 forget loss、用于让已遗忘输出偏离原始模型的 mismatch loss，以及作用于保留样本和边界样本的 feature preservation loss。
- 更新分阶段进行，并使用 LoRA adapters 和 PCGrad：先削弱视觉触发因素，再打破有害的视觉-语言绑定，最后压制残留的动作先验。

## 结果
- 在摘要中，论文声称相对强基线取得了以下提升：**遗忘效果提升 10%**、**感知特异性提升 22%**、**推理/任务保留提升 9%**，以及 **量化后恢复降低 55%**。
- 在 **OpenVLA-7B / Open X-Embodiment** 上，VLA-Forget 报告 **FC 93**、**RC 91**、**FAD 0.88**、**RAD 0.21**、**TSR 78**、**SVR 5**。与 **NPO** 相比，RC 从 **88 -> 91**，TSR 从 **74 -> 78**，RAD 从 **0.23 -> 0.21**，SVR 从 **8 -> 5**。与 **GA** 相比，FC 同为 **93**，但 RC 从 **60 -> 91**，TSR 从 **40 -> 78**。
- 在 **OpenVLA-7B / lerobot-pusht_image** 上，VLA-Forget 报告 **FC 95**、**RC 94**、**FAD 0.90**、**RAD 0.13**、**TSR 69**、**SVR 4**。与 **NPO** 相比，FC 从 **92 -> 95**，RC 从 **90 -> 94**，TSR 从 **65 -> 69**，RAD 从 **0.15 -> 0.13**，SVR 从 **7 -> 4**。
- 在 **pi0fast-base / Open X-Embodiment** 上，VLA-Forget 报告 **FC 94**、**RC 89**、**FAD 0.88**、**RAD 0.22**、**TSR 75**、**SVR 6**。与 **NPO** 相比，FC 从 **89 -> 94**，RC 从 **87 -> 89**，TSR 从 **72 -> 75**，RAD 从 **0.24 -> 0.22**。与 **GA** 相比，FC 从 **93 -> 94**，RC 从 **57 -> 89**，TSR 从 **38 -> 75**，而 SVR 保持 **6** 不变。
- 从展示的表格来看，GA 通常有最高或并列最高的遗忘分数，但 VLA-Forget 能保留更高的保留效用和任务成功率，这也是论文声称的主要优势。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03956v1](http://arxiv.org/abs/2604.03956v1)
