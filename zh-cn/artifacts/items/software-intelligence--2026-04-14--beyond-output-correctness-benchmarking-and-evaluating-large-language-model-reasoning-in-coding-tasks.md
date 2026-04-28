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
这篇论文认为，只检查最终代码输出会漏掉 LLM 的推理是否正确。论文提出了 CodeRQ-Bench，这是一个面向编程任务推理质量的基准；还提出了 VERA，这个评估器会根据证据检查推理，并对任务歧义进行调整。

## 问题
- 现有编程基准如 HumanEval 和 SWE-bench 只给最终输出打分，因此模型可能在推理有缺陷的情况下得到正确答案，也可能在推理部分合理的情况下失败。
- 现有推理评估器如 ReCEval、SocREval 和 CaSE 是为通用 NLP 任务构建的，不适用于带有程序语义、代码仓库上下文、API 和执行行为的编程任务。
- 此前没有一个基准覆盖主要编程任务类型中的推理质量：生成、摘要和分类。

## 方法
- 论文构建了 **CodeRQ-Bench**，这是一个推理质量基准，包含 4 个数据集，共 732 个实例：CoderEval-RE（230）、SWEbench-RE（111）、ClassEval-RE（139）和 DebugBench-RE（252）。
- 为了覆盖更广的任务类型，基准新增了两个部分：用于代码摘要的 ClassEval-RE，以及用于缺陷检测 / 分类的 DebugBench-RE。每个实例都由 3 名专家标注者给出一致标签。
- 新数据集的标注质量较高：ClassEval-RE 的 Fleiss' kappa 为 0.91，DebugBench-RE 为 0.95，裁决率分别为 4.32% 和 3.57%。
- 作者分析了 1,069 个评估器不匹配案例，识别出 5 种反复出现的失败模式，包括缺少证据支撑、对歧义处理不佳、分数聚合方式差、自生成参考带来的偏差，以及对代码缺乏足够感知。
- 他们提出了 **VERA**，这是一个两阶段评估器：第一阶段，LLM 评审通过基于搜索的证据检查给推理打分；第二阶段，另一个评审估计任务歧义，并对歧义处理不佳的推理施加惩罚。最终分数为 `max(p + δ, 0)`。

## 结果
- 在 **CoderEval-RE** 上，VERA 达到 **AUCROC 0.6905** 和 **AUPRC 0.4615**，高于所列基线中的最好结果 **0.5700 AUCROC** 和 **0.3516 AUPRC**。
- 在 **SWEbench-RE** 上，VERA 达到 **AUCROC 0.6399** 和 **AUPRC 0.3058**，高于所列基线中的最好结果 **0.5778 AUCROC** 和 **0.2165 AUPRC**。
- 在 **ClassEval-RE** 上，VERA 达到 **AUCROC 0.7090** 和 **AUPRC 0.8869**，高于所列基线中的最好结果 **0.6250 AUCROC** 和 **0.8502 AUPRC**。
- 在 **DebugBench-RE** 上，VERA 达到 **AUCROC 0.7176** 和 **AUPRC 0.7939**，高于所列基线中的最好结果 **0.6769 AUCROC** 和 **0.7431 AUPRC**。
- 摘要指出，该方法相对已有方法的最大提升为四个数据集上的 **最高 +0.26 AUCROC** 和 **+0.21 AUPRC**。
- 现有评估器在编程推理上的表现常常接近随机。在不匹配分析中，作者收集了 **1,069** 个错误，其中包括 **709 个漏检错误** 和 **360 个误报**，并据此说明了 VERA 的设计依据。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.12379v1](http://arxiv.org/abs/2604.12379v1)
