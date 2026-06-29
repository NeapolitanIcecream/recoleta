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

# 监督式 VLA 执行与评测

## Summary
最清楚的近期变化，是把长时程 VLA 执行当作一个带记忆、动作检查和恢复机制的监督控制回路，而不只是更大的策略上下文。评测也需要更难的重组和对齐测试，团队在相信基准提升之前应先过这些门槛。基于推理理由的微调看起来适合作为定向训练步骤，但它应该和这些更难的测试一起用，才能看出它提升的是因果任务理解，还是只提升了更容易的基准表面表现。

## 带记忆条件动作检查和回滚的执行外壳，用于长时程操作
机器人团队在长时程操作上，现在有了一个明确理由，在冻结的 VLA 外面加一层执行外壳。HELM 的结果表明，常见失败模式不是某一个动作做错，而是一个循环问题：策略丢失已完成的子目标，在没有检查的情况下执行不可行动作，然后在任务状态已经被破坏后继续往下走。它的包装层用情景记忆检索、执行前状态验证器和基于回滚的恢复来处理这些问题，LIBERO-LONG 上的提升也很大：OpenVLA 从 58.4% 提升到 81.5%，而只拉长上下文长度在 H=32 时只能到 63.8%，在 H=64 时到 65.1%。同一篇论文还报告，恢复成功率从 12.3% 升到 54.2%。

实际可落地的做法是给已部署的操作策略加一层轻量运行时模块：保存带检查点的任务状态，检索当前子目标对应的一小段结构化历史，在执行前给候选动作打失败分数，并允许有限次数的回滚尝试。这个支持层很多实验室都可以在不重训基础策略的情况下测试。一个成本较低的初步检查，是在现有失败的长时程回放上做研究：统计有多少失败本可以在接触或运动执行前被验证器拦下，然后在一小组多阶段抓取放置任务上加入回滚，对比完成的子目标数，而不只看最终成功率。

### Evidence
- [HELM: Harness-Enhanced Long-horizon Memory for Vision-Language-Action Manipulation](../Inbox/2026-04-20--helm-harness-enhanced-long-horizon-memory-for-vision-language-action-manipulation.md): Summary gives the execution-loop diagnosis, component design, and main LIBERO-LONG gains.
- [HELM: Harness-Enhanced Long-horizon Memory for Vision-Language-Action Manipulation](../Inbox/2026-04-20--helm-harness-enhanced-long-horizon-memory-for-vision-language-action-manipulation.md): Content states the 23.1 point gain over OpenVLA and the weak effect of longer context alone.

## VLA 评测门槛中的重组压力测试
VLA 模型的评测在团队相信头部成功率之前，需要一套子目标重组测试。BeTTER 说明了原因。那些在标准任务上看起来表现不错的模型，在任务需要把熟悉部分重新组合成新子目标时会崩掉。在未见过的 B->C 序列上，pi_0.5 的成功率降到 5.0%，GR00T-N1.6 降到 15.0%，Being-H0.5 降到 0.0%，而它们在见过的 A->B 和 A->C 组合上分数高得多。这个基准还显示，像 top 和 bottom、red 和 blue 这类小语义变化会让指令对齐变得不稳定。

流程上的改动很直接：只要某个模型更新声称推理能力或长时程表现更好，就在评测门槛里加入受控干预测试。这个门槛至少要包含未见过的子目标重组、布局变化和语义干扰项，并记录能区分推理错误和底层执行噪声的日志。已经在跑基准回归的团队，可以在新 checkpoint 进入机器人试验前，把这些内容加成一个小型压力测试集。一个低成本验证方法，是拿现有基准里的一个任务，生成几种重组后的目标顺序和属性替换，和原始版本比较成功率下降幅度。如果模型只在原始顺序上表现稳定，评测栈就漏掉了部署中真正重要的一类失败模式。

### Evidence
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md): Summary includes the BeTTER benchmark design and the subgoal recomposition and grounding failures.
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md): Content describes targeted causal interventions that separate reasoning failures from execution limits.

## 用于高错误率操作任务的推理理由微调
把 VLA 用教师写的推理理由做微调，看起来是一个适合想提升组合泛化能力团队的窄改动，但它需要比论文里更严格的后续测试。ReFineVLA 用教师生成的解释来扩充机器人轨迹，内容包括观察、情境分析、空间推理和任务规划，然后把动作预测和理由生成一起训练。它在 SimplerEnv 上的提升是实在的：WidowX 的平均成功率达到 47.7%，variant aggregation 达到 68.8%，visual matching 达到 76.6%，在 Move Near 和 Open/Close Drawer 上也有更大的提升。

真正可做的步骤，是先在一部分轨迹上补推理标注，而不是全面重做数据。已有 VLA 微调流水线的团队，可以先给少数高错误任务族加上理由生成，冻结大部分骨干网络，再训练联合的动作加理由损失。第一轮检查应该把新模型放到更硬的评测切片上，比如未见过的子目标组合或布局扰动。这里 BeTTER 很相关，因为更高的基准分数本身并不能说明模型学到了因果任务结构。如果理由微调在标准套件上有帮助，但在重组测试上失效，说明这套训练配方提升的更多是模式匹配，而不是具身推理。

### Evidence
- [ReFineVLA: Multimodal Reasoning-Aware Generalist Robotic Policies via Teacher-Guided Fine-Tuning](../Inbox/2026-04-20--refinevla-multimodal-reasoning-aware-generalist-robotic-policies-via-teacher-guided-fine-tuning.md): Summary provides the rationale-supervision method and the main SimplerEnv gains.
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md): BeTTER provides the caution that benchmark gains can hide failures in recomposition and grounding.
