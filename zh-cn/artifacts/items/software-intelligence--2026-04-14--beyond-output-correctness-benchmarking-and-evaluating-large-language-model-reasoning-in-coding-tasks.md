---
source: arxiv
url: http://arxiv.org/abs/2604.12379v1
published_at: '2026-04-14T07:12:46'
authors:
- Yuangang Li
- Justin Tian Jin Chen
- Ethan Yu
- David Hong
- Iftekhar Ahmed
topics:
- code-reasoning-evaluation
- benchmarking
- llm-judge
- code-intelligence
- reasoning-quality
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Output Correctness: Benchmarking and Evaluating Large Language Model Reasoning in Coding Tasks

## Summary
## 摘要
本文认为，只检查代码最终输出会忽略 LLM 是否真正做对了推理。文中提出 CodeRQ-Bench，这是一个用于评估编码任务中推理质量的基准；还提出 VERA，这是一个根据证据检查推理并对任务歧义进行校正的评估器。

## 问题
- 目前的编码基准，如 HumanEval 和 SWE-bench，只给最终输出打分，所以模型可能在推理有缺陷时仍得到正确答案，也可能在推理大体合理时得到错误结果。
- 现有推理评估器，如 ReCEval、SocREval 和 CaSE，是为通用 NLP 任务设计的，不适用于包含程序语义、仓库上下文、API 和执行行为的编码任务。
- 过去没有一个基准能覆盖主要编码任务类型中的推理质量：生成、总结和分类。

## 方法
- 论文构建了 **CodeRQ-Bench**，一个包含 4 个数据集、共 732 个样本的推理质量基准：CoderEval-RE（230）、SWEbench-RE（111）、ClassEval-RE（139）和 DebugBench-RE（252）。
- 基准中新增了两个部分，以覆盖更广的任务：ClassEval-RE 用于代码总结，DebugBench-RE 用于漏洞检测 / 分类。每个样本都由 3 位专家标注者给出一致标签。
- 新数据集的标注质量较高：ClassEval-RE 的 Fleiss' kappa 为 0.91，DebugBench-RE 为 0.95，仲裁率分别为 4.32% 和 3.57%。
- 作者分析了 1,069 个评估器不一致案例，识别出 5 种重复出现的失效模式，包括缺少证据约束、歧义处理差、分数聚合不当、自生成参考偏差，以及代码感知能力弱。
- 他们提出了 **VERA**，一个两阶段评估器：第一阶段，LLM 评审器结合基于搜索的证据检查来给推理打分；第二阶段，另一个评审器估计任务歧义，并对处理歧义较差的推理进行惩罚。最终分数为 `max(p + δ, 0)`。

## 结果
- 在 **CoderEval-RE** 上，VERA 的 **AUCROC 为 0.6905**，**AUPRC 为 0.4615**，高于最佳基线的 **0.5700 AUCROC** 和 **0.3516 AUPRC**。
- 在 **SWEbench-RE** 上，VERA 的 **AUCROC 为 0.6399**，**AUPRC 为 0.3058**，高于最佳基线的 **0.5778 AUCROC** 和 **0.2165 AUPRC**。
- 在 **ClassEval-RE** 上，VERA 的 **AUCROC 为 0.7090**，**AUPRC 为 0.8869**，高于最佳基线的 **0.6250 AUCROC** 和 **0.8502 AUPRC**。
- 在 **DebugBench-RE** 上，VERA 的 **AUCROC 为 0.7176**，**AUPRC 为 0.7939**，高于最佳基线的 **0.6769 AUCROC** 和 **0.7431 AUPRC**。
- 摘要写明，相比先前方法，四个数据集上的最大提升可达 **+0.26 AUCROC** 和 **+0.21 AUPRC**。
- 现有评估器在编码推理上的表现常接近随机。作者在不一致分析中收集了 **1,069** 个错误，其中包括 **709** 个漏判错误和 **360** 个误报，并用这些结果来说明 VERA 的设计动机。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.12379v1](http://arxiv.org/abs/2604.12379v1)
