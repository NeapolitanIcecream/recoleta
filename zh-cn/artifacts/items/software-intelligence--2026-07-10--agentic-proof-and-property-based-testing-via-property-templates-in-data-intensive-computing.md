---
source: arxiv
url: https://arxiv.org/abs/2607.09072v1
published_at: '2026-07-10T03:33:47'
authors:
- Seongmin Lee
- Yaoxuan Wu
- Miryung Kim
topics:
- property-based-testing
- formal-verification
- agentic-software-engineering
- spark-testing
- code-generation-validation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic Proof and Property-Based Testing via Property-Templates in Data-Intensive Computing

## Summary
## 摘要
DualVeri 使用可复用的属性模板，帮助智能体证明和测试 Apache Spark 中反复出现的正确性属性。它结合了针对 Spark 模型的 Lean 4 证明与针对 PySpark 的基于属性的测试，在 400 个候选属性上减少了合成错误和成本。

## 问题
- AI 生成的代码增加了候选属性的数量，但验证每个属性是否正确，以及测试是否检查了预期行为，仍然成本高昂。
- 数据密集型系统包含大量结构相似的属性，但共享结构不能保证属性为真。研究引用了 37,971 个类型一致的聚合候选属性，其中包括全局均值等于各分区均值的均值这类错误断言。
- 形式化证明覆盖模型及模型中的所有输入，而基于属性的测试会运行真实实现。只使用其中一种方法，可能遗漏模型缺口或实现故障。

## 方法
- DualVeri 将四类 Spark 属性表示为带有类型化空位的参数化模板：聚合分解、UDF 重写、高阶表达式重写和算子包含。
- 证明模板预先证明从局部规律提升到流水线级定理的可复用过程。智能体只需在 Lean 4 中填写特定于属性的空位，并证明局部规律。
- 基于属性的测试模板生成带类型的数据、外围 Spark 工作负载，以及针对 PySpark 的可执行检查。智能体填写相同的属性专用空位，无需从头编写每个测试架构。
- 研究按每类 100 个候选属性进行评估，共 400 个，并将模板引导的合成与无模板的证明合成和基于属性的测试合成进行比较。
- 研究对证明结果和测试结果进行交叉核对：测试通过但没有证明，可能说明形式化建模存在遗漏；已证明属性出现反例，则说明模型与运行时之间存在不一致。

## 结果
- 属性模板使智能体成功合成证明的比例最高提高至 2.6 倍，平均提高 1.6 倍，并在更低成本下将证明幻觉减少了 59%。
- 模板引导的基于属性的测试将意图不一致数量从 22 降至 1，并将合成成本最高降低至原来的 1/5.7，平均降低至原来的 1/3.8。
- 四个模板成功合成了 136 个证明和 387 个忠实的基于属性的测试。
- 在代码覆盖率方面，模板引导的基于属性的测试超过了当时最先进的 Spark 模糊测试器，并接近无引导的基于 LLM 的基于属性的测试。
- 两条流程为 130 个属性同时生成了证明和通过的测试；其中的不一致揭示了 Lean 模型与 PySpark 运行时语义之间的缺口。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.09072v1](https://arxiv.org/abs/2607.09072v1)
