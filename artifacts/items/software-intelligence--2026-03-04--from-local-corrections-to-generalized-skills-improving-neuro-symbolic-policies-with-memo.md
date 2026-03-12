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
- robot-learning
- neuro-symbolic-policy
- retrieval-augmented-generation
- human-feedback
- skill-learning
relevance_score: 0.39
run_id: materialize-outputs
---

# From Local Corrections to Generalized Skills: Improving Neuro-Symbolic Policies with MEMO

## Summary
MEMO 是一种让机器人把零散的人类语言纠错积累成可复用技能的方法。它通过“检索+聚类+代码模板化”把局部修正转成能迁移到新任务的通用操作能力。

## Problem
- 神经符号机器人虽然能把复杂任务分解成语义子任务，但真正执行时仍受限于已有技能库；缺少合适技能时任务会失败。
- 仅记住某次人类纠错文本，通常只能修正当前场景，难以扩展为跨任务、跨用户可泛化的新技能。
- 随着反馈变多，记忆库会变得冗余、矛盾且上下文过长，影响检索和推理效果。

## Approach
- 构建一个检索增强的 **skillbook**，存储两类内容：人类失败纠错的改写文本，以及机器人成功完成子任务后抽象出的代码/函数模板。
- 在运行时，先把任务分解为子任务，再按“动作+对象”相似度从 skillbook 检索相关反馈或代码模板，用它们辅助生成当前子任务的新技能代码，而不是直接死板复用旧代码。
- 对人类反馈先做释义与去任务特化，同时抽取更高层、任务无关的指导语句，以提升跨场景可迁移性。
- 离线对 skillbook 中相近条目做聚类，并以成功代码模板为条件进行压缩总结，删除重复或与成功行为冲突的纠错，得到更一般化的文本指导和参数化函数模板。
- 核心机制可简单理解为：把很多次“这里错了，应该这样做”的自然语言建议，整理成“以后遇到这类对象/动作，就按这个通用程序做”。

## Results
- 论文明确声称：在**未见过的新任务**上，MEMO 的**零样本成功率**高于机器人基础模型，以及只会检索局部人类反馈的神经符号基线（如文中提到的 DROC-V / MEMO-C 对比背景）。
- 数据收集覆盖 **20 个用于反馈收集的测试任务** 和 **5 个 held-out 评测任务**，总计 **224 条人类反馈**。
- held-out 任务包括 **Place the apple on the table、Pour the can、Close the bottle、Empty the cabinet、Put the food in the oven**，用于测试泛化而非记忆训练任务本身。
- 文中给出图 4 并指出：随着 skillbook 按**用户小时数**增长，**未做聚类的 MEMO-C 和 DROC-V 性能趋于停滞**，而 MEMO 通过把局部纠错聚合成通用指导保持更好的泛化趋势。
- 摘要与引言的最强结论是：MEMO 能把多用户、多任务的局部文本反馈合成为通用代码技能模板，从而在现有基线失效的**新任务**上实现更强泛化。
- 该节选**未提供清晰的最终数值型成功率、具体百分点提升或显著性统计**，因此无法可靠列出更细的定量对比。

## Link
- [http://arxiv.org/abs/2603.04560v1](http://arxiv.org/abs/2603.04560v1)
