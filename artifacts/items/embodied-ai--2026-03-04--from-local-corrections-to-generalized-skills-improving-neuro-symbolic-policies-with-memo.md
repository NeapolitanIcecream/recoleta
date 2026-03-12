---
source: arxiv
url: http://arxiv.org/abs/2603.04560v1
published_at: '2026-03-04T19:44:55'
authors:
- Benjamin A. Christie
- Yinlong Dai
- Mohammad Bararjanianbahnamiri
- Simon Stepputtis
- Dylan P. Losey
topics:
- neuro-symbolic-robotics
- human-feedback
- retrieval-augmented-generation
- skill-learning
- robot-manipulation
relevance_score: 0.87
run_id: materialize-outputs
---

# From Local Corrections to Generalized Skills: Improving Neuro-Symbolic Policies with MEMO

## Summary
MEMO 研究如何把机器人任务失败后的局部自然语言纠正，积累成可检索、可泛化的技能模板，从而提升神经符号操作策略在新任务上的零样本表现。核心思想是把人类反馈和成功代码写入一个持续演化的 skillbook，并通过聚类把零散纠正压缩成更通用的文本指导与参数化代码。

## Problem
- 神经符号机器人策略虽然能把复杂任务拆成语义子任务，但真正执行时仍受限于已有技能库；缺少合适技能时，高层推理再好也会失败。
- 现有基于反馈的方法通常只会记住某次局部纠正或微调已有技能，难以把“这次修正”变成“以后都能用的新技能”。
- 这很重要，因为通用操作机器人面对新物体、新机构和新任务时，瓶颈往往不是规划，而是缺少能把语言落地成动作的可泛化技能。

## Approach
- MEMO 构建一个检索增强的 **skillbook**，把人类自然语言纠正、提炼后的高层指导，以及任务成功后生成的代码模板统一存成向量数据库条目。
- 运行时，机器人先把任务分解成子任务，再按“动作 token + 物体 token”检索相关反馈或函数模板，将这些内容作为上下文辅助生成当前子任务代码，而不是机械复用旧代码。
- 对用户反馈，系统会先做释义/泛化：去掉过于任务特定的描述，并尽量抽取跨任务可用的高层规则；对成功子任务，系统会把执行代码抽象成参数化函数模板。
- 离线阶段，MEMO 按嵌入对 skillbook 条目聚类，并在成功代码模板条件下让语言模型压缩、重写和去冲突，得到更紧凑、更一致的通用反馈与技能模板。
- 论文共收集 **224 条** 人类反馈，来自多种训练任务；评测在若干 held-out 新任务上进行，包括 *Place the apple on the table*、*Pour the can*、*Close the bottle*、*Empty the cabinet*、*Put the food in the oven*。

## Results
- 论文明确声称：在**此前未见任务**上，MEMO 的**零样本成功率高于**机器人基础模型，以及只检索相关人类反馈而**不做泛化聚类**的神经符号基线。
- 从给出的实验设置看，作者使用 **224 条** 人类反馈构建 skillbook，并在 **5 个 held-out 任务**上评估跨任务泛化能力；这支持其“从局部修正到通用技能”的核心主张。
- 图 4 的文字说明指出：随着 skillbook 规模增大，**MEMO-C** 与 **DROC-V** 这类**不进行聚类泛化**的方法性能会趋于停滞，而 MEMO 通过把局部纠正聚合成通用指导，能继续带来收益。
- 摘要还声称 MEMO 能在**仿真和真实世界**中超过现有基线，并能泛化到新任务；文段展示了真实机器人在 *Empty the Cabinet* 上的**zero-shot** 使用案例。
- 但在提供的摘录中，**没有出现完整的定量结果数值**（例如具体成功率百分比、方差、相对提升幅度、逐基线对比表），因此无法准确列出“比某基线高 X%”这类数字。

## Link
- [http://arxiv.org/abs/2603.04560v1](http://arxiv.org/abs/2603.04560v1)
