---
source: arxiv
url: http://arxiv.org/abs/2603.06001v1
published_at: '2026-03-06T08:01:36'
authors:
- Ninghao Zhang
- Bin Zhu
- Shijie Zhou
- Jingjing Chen
topics:
- vision-language-action
- linguistic-grounding
- attention-recalibration
- ood-robustness
- robot-safety
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Restoring Linguistic Grounding in VLA Models via Train-Free Attention Recalibration

## Summary
本文揭示了视觉-语言-动作（VLA）模型中的“语言失明”问题：在指令与场景矛盾时，机器人仍会执行看似合理的动作。作者提出无需训练的推理时方法 IGAR，通过重校准注意力来增强语言对动作生成的约束，并用 ICBench 系统评测这一问题。

## Problem
- 论文解决的是 **VLA 模型在 OOD 矛盾指令下忽视语言语义、过度依赖视觉先验** 的问题。
- 这很重要，因为机器人一旦在现实环境中无视用户语言约束，就可能导致错误操控、破坏物体或安全事故。
- 现有评测多只看“正常指令下是否成功”，无法区分模型是真正理解语言，还是只是靠视觉启发式完成任务。

## Approach
- 作者提出 **ICBench**：基于 LIBERO 构建的诊断基准，在**保持视觉场景不变**的前提下，向指令注入受控矛盾，用来测量语言是否真正影响动作生成。
- ICBench 包含 4 类矛盾：操作对象属性替换（V1）、目标属性增强矛盾（V2）、双属性矛盾（V3）、空间关系替换（V4）。如果模型仍高成功率完成任务，说明语言 grounding 弱。
- 作者提出 **IGAR (Instruction-Guided Attention Recalibration)**：一种**免训练、推理时**的注意力重校准机制，不改模型结构、不更新参数。
- 其核心机制可以简单理解为三步：**找出注意力“黑洞”token**（视觉主导的 sink）、**找出与跨模态 grounding 相关的注意力头**、**把部分注意力从 sink token 重新分配给指令 token**，让动作预测更“听指令”。
- 论文还定义了 **LGS (Linguistic Grounding Score)**，即正常指令成功率减去矛盾指令成功率；LGS 越高，说明语言对动作的约束越强。

## Results
- 在 **30 个 LIBERO 任务**、**每个任务变体 50 次 rollout** 上，作者评估了 **\(\pi_0\)、\(\pi_{0.5}\)、OpenVLA-OFT** 三类代表性 VLA。
- 基线结果显示明显“语言失明”：例如在 **Spatial** 套件下，**OpenVLA-OFT** 在矛盾指令下仍有 **97.8% SR (V1)**、**96.4% SR (V2)**、**96.2% SR (V3)**；对应 **LGS 分别仅 -0.2、1.2、1.4**，说明几乎不受语言影响。
- **\(\pi_{0.5}\)** 同样严重：在 **Spatial-V4** 下 **SR 97.6%**、**LGS -0.2**；在 **Object-V1/V3** 下分别 **96.2% / 96.4% SR**，表明矛盾语言几乎未改变动作。
- **\(\pi_0\)** 相对稍好，但仍常在矛盾下高成功：如 **Spatial-V2 96.2% SR, LGS 0.6**；**Object-V3 98.2% SR, LGS 0.6**。
- 加入 **IGAR** 后，论文声称矛盾指令下的错误执行显著下降、LGS 大幅上升；文中给出的代表性数字是：在 **Goal suite 的空间矛盾 V4** 中，**SR 最低降到 36.4%**，**LGS 提升到 59.4**，表明模型更倾向于拒绝执行不符合语义的动作。
- 论文还声称 **IGAR 基本保持正常指令下的基线性能**，并在**真实 Franka 机械臂**上验证：当指令与场景不一致时，IGAR 能有效阻止错误操作。但给定摘录中未提供更完整的真实机器人量化对比表。

## Link
- [http://arxiv.org/abs/2603.06001v1](http://arxiv.org/abs/2603.06001v1)
