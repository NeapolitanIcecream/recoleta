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
- robotics-safety
- attention-recalibration
- ood-robustness
- linguistic-grounding
relevance_score: 0.42
run_id: materialize-outputs
language_code: zh-CN
---

# Restoring Linguistic Grounding in VLA Models via Train-Free Attention Recalibration

## Summary
本文揭示了视觉-语言-动作（VLA）机器人策略中的“语言失明”问题：即使指令与场景矛盾，模型仍会依据视觉先验继续执行看似合理的动作。作者提出无需训练的推理时方法 IGAR，并构建 ICBench 来诊断和缓解这一问题。

## Problem
- 论文解决的是 **VLA 模型在矛盾或分布外语言指令下仍错误执行动作** 的问题，这说明模型没有真正把语言约束用于动作生成。
- 这很重要，因为机器人不同于纯对话系统；忽略语言约束会直接造成现实世界中的错误操控、安全风险和物理损害。
- 现有评测通常只看正常指令下的任务成功率，无法区分模型是“真的理解语言”还是“只靠视觉启发式完成任务”。

## Approach
- 作者提出 **ICBench**：在保持视觉场景不变的前提下，系统性地把 LIBERO 任务指令改成语义矛盾版本，用于单独测试语言-动作耦合是否真实存在。
- ICBench 定义了 4 类矛盾：操作对象属性替换（V1）、目标属性增强（V2）、双属性扰动（V3）、空间关系替换（V4）。若模型真正依赖语言，应在这些矛盾指令下失败或拒绝执行。
- 作者提出 **IGAR（Instruction-Guided Attention Recalibration）**：一种**免训练、推理时、即插即用**的注意力重校准机制，不改模型结构也不更新参数。
- IGAR 的核心机制很简单：先找出注意力里“吸走大部分关注”的 sink token，再定位跨模态失衡的注意力头，把一部分注意力从 sink token 重新分配给语言指令 token，从而让动作生成更多参考文字约束。
- 论文还定义了 **LGS（Linguistic Grounding Score）** 来衡量正常指令与矛盾指令之间的成功率差距；差距越大，说明语言对行为影响越强。

## Results
- 在 30 个 LIBERO 任务、3 个代表性 VLA 模型（$\pi_0$、$\pi_{0.5}$、OpenVLA-OFT）上，基线模型在矛盾指令下依然常常高成功率，直接证明“语言失明”。例如：Spatial 套件中，$\pi_{0.5}$ 在 V1/V2/V3/V4 下 SR 分别为 **96.2/97.8/96.4/97.6**，对应 LGS 仅 **1.2/-0.4/1.0/-0.2**；OpenVLA-OFT 在 Spatial V1 下 SR **97.8**、LGS **-0.2**。
- 在 Goal 套件中，OpenVLA-OFT 在矛盾指令下仍几乎照常完成任务：V1/V2/V3 的 SR 为 **97.8/98.2/98.4**，LGS 仅 **0.2/-0.2/-0.4**；说明语言几乎不影响动作。
- $\pi_0$ 相对更有语言敏感性，但问题仍明显：例如 Goal-V4 下正常 SR **95.8**，矛盾指令 SR 仍有 **76.4**，LGS **19.4**；Object-V3 下矛盾 SR **98.2**，LGS 仅 **0.6**。
- 应用 IGAR 后，论文声称在所有套件中都显著降低了矛盾指令下的错误执行，并大幅提升 LGS。给出的代表性数字是：在 **Goal** 套件的 **V4 空间矛盾** 下，成功率最低可降到 **36.4%**，同时 **LGS 提升到 59.4**。
- 作者还声称，IGAR 在提升语言约束敏感性的同时，**保留正常指令下的基线任务性能**；并在真实 **Franka** 机械臂上验证，矛盾指令出现时 IGAR 能有效阻止错误操控。
- 摘要与正文摘录未给出完整的 IGAR 全量结果表或真实机器人精确对比数字，但最强定量结论是：基线在大量矛盾场景下 SR 仍常 **>90%**，而 IGAR 可把部分场景的矛盾执行 SR 压到 **36.4%**，并将 LGS 提升到 **59.4**。

## Link
- [http://arxiv.org/abs/2603.06001v1](http://arxiv.org/abs/2603.06001v1)
