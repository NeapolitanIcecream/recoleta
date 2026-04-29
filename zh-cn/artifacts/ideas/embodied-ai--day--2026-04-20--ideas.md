---
kind: ideas
granularity: day
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-21T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- long-horizon manipulation
- reasoning
- spatial modeling
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/long-horizon-manipulation
- topic/reasoning
- topic/spatial-modeling
language_code: zh-CN
---

# 受监督的 VLA 执行与评测

## Summary
最近最明确的变化是：长时程 VLA 执行应被当作一个带记忆、动作检查和恢复机制的受监督控制循环来处理，而不只是给策略更大的上下文。团队在相信 benchmark 提升之前，也需要更难的重组和 grounding 测试。把推理说明用于微调看起来适合作为定向训练步骤，但应和这些更难的测试配套使用，才能判断它提升的是因果任务理解，还是只是更容易的 benchmark 表面表现。

## 用于长时程操作的执行 harness：带记忆条件动作检查与回滚
做长时程操作的机器人团队，现在有了一个明确理由：在冻结的 VLA 外围加一层执行 harness。HELM 报告称，常见失败模式不是某一个动作出错，而是控制循环出了问题：策略会丢失已完成子目标的状态，在没有检查的情况下执行不可行的动作，并且在任务状态已经被破坏后继续往下执行。它们的封装用情节记忆检索、执行前状态验证器和基于回滚的恢复来处理这些问题，且在 LIBERO-LONG 上的提升很大：OpenVLA 从 58.4% 提升到 81.5%，而单纯增加上下文长度在 H=32 时只有 63.8%，在 H=64 时是 65.1%。同一篇论文还报告，恢复成功率从 12.3% 提高到 54.2%。

这里可落地的实现是一层用于已部署操作策略的轻量运行时：存储带检查点的任务状态，为当前子目标检索一小段结构化历史，在执行前给候选动作打分以判断其失败概率，并允许有限次数的回滚尝试。这是一层支持模块，很多实验室不用重训基础策略就能测试。一个低成本的第一步是对现有失败的长时程 episode 做回放研究：统计有多少失败本可以在接触或运动执行前被验证器拦下，然后在一小组多阶段 pick-place 任务中加入回滚，比较已完成的子目标数量，而不只看最终成功率。

### Evidence
- [HELM: Harness-Enhanced Long-horizon Memory for Vision-Language-Action Manipulation](../Inbox/2026-04-20--helm-harness-enhanced-long-horizon-memory-for-vision-language-action-manipulation.md): 摘要给出了执行循环问题的诊断、组件设计，以及 LIBERO-LONG 上的主要提升。
- [HELM: Harness-Enhanced Long-horizon Memory for Vision-Language-Action Manipulation](../Inbox/2026-04-20--helm-harness-enhanced-long-horizon-memory-for-vision-language-action-manipulation.md): 内容说明了相对 OpenVLA 提升 23.1 个百分点，以及单纯增加上下文长度效果有限。

## 在 VLA 评测门禁中加入重组压力测试
在团队相信 VLA 模型的 headline 成功率之前，评测需要先加入重组测试集。BeTTER 说明了原因。看起来在标准任务上表现不错的模型，一旦任务要求把熟悉部件重组成新的子目标组合，就会明显失效。在未见过的 B->C 序列上，pi_0.5 的成功率降到 5.0%，GR00T-N1.6 降到 15.0%，Being-H0.5 降到 0.0%，而它们在见过的 A->B 和 A->C 组合上分数高得多。这个基准还显示，在 top 与 bottom、red 与 blue 这类小的语义变化下，指令 grounding 也不稳定。

工作流上的改动很直接：对于任何声称推理能力或长时程性能更好的模型更新，都在评测门禁中加入受控干预测试。这个门禁至少应包括未见过的子目标重组、布局变化和语义干扰项，并记录能把推理错误和底层执行噪声区分开的日志。已经在跑 benchmark 回归的团队，可以在新 checkpoint 进入机器人试验前，把这些测试作为一个小型压力套件加进去。低成本的验证步骤是选一个现有 benchmark 任务，生成几种重组后的目标顺序和属性替换，然后比较它相对基础版本的成功率下降。如果模型只在原始顺序上还能维持表现，说明当前评测栈漏掉了一类对部署很重要的失败模式。

### Evidence
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md): 摘要包含了 BeTTER 基准的设计，以及子目标重组和 grounding 失败。
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md): 内容描述了有针对性的因果干预，用来区分推理失败和执行能力限制。

## 面向高错误率操作任务的推理说明微调
对想提升组合泛化能力的团队来说，用教师编写的推理说明来微调 VLA，作为一种小范围训练改动是可信的，但它需要比论文中更严格的后续测试。ReFineVLA 用教师生成的解释来增强机器人轨迹，解释内容包括观察、情境分析、空间推理和任务规划，然后联合训练动作预测与理由生成。论文在 SimplerEnv 上报告的提升有参考价值：WidowX 上平均成功率 47.7%，variant aggregation 上 68.8%，visual matching 上 76.6%，在 Move Near 和 Open/Close Drawer 上也有更大的提升。

可执行的一步是在部分轨迹上做推理标注，而不是全面重做数据。已经有 VLA 微调流水线的团队，可以在几个高错误率任务族上加入理由生成，冻结 backbone 的大部分参数，并训练联合的动作加理由损失。第一步检查应把新模型放到更难的评测切片上，比如未见过的子目标组合或布局扰动。BeTTER 在这里很相关，因为 benchmark 分数变高本身不能说明模型学到了因果任务结构。如果理由微调能提升标准测试集表现，却在重组测试上失效，那这个训练配方提升的更像是模式匹配，而不是具身推理。

### Evidence
- [ReFineVLA: Multimodal Reasoning-Aware Generalist Robotic Policies via Teacher-Guided Fine-Tuning](../Inbox/2026-04-20--refinevla-multimodal-reasoning-aware-generalist-robotic-policies-via-teacher-guided-fine-tuning.md): 摘要提供了理由监督的方法和 SimplerEnv 上的主要提升。
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md): BeTTER 提醒我们，benchmark 提升可能掩盖重组与 grounding 方面的失败。
