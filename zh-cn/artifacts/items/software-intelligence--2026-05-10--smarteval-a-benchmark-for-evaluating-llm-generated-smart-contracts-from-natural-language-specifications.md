---
source: arxiv
url: https://arxiv.org/abs/2605.09610v1
published_at: '2026-05-10T15:47:46'
authors:
- Abhinav Goel
- Agostino Capponi
- Alfio Gliozzo
- Chaitya Shah
topics:
- smart-contract-generation
- llm-evaluation
- code-generation
- software-benchmarks
- multi-agent-pipeline
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# SmartEval: A Benchmark for Evaluating LLM-Generated Smart Contracts from Natural Language Specifications

## Summary
## 总结
SmartEval 是一个用于评估 LLM 根据自然语言规格生成的 Solidity 合约的基准。它把 9,000 份生成合约与专家实现配对，并用一个五项指标量表来评分，重点看规格一致性和状态机行为。

## 问题
- LLM 可以编写 Solidity，但智能合约需要精确的业务逻辑、状态转换、访问控制和安全检查，因为已部署的漏洞会导致资金被锁定或丢失。
- 现有评估通常只检查语法或编译结果，无法判断合约是否遵循自然语言需求和 FSM 规格。
- 论文要解决的是一个测量缺口：研究者需要一种可重复的方法，把 LLM 生成的智能合约和专家实现做比较。

## 方法
- SmartEval 使用 FSM-SCG 数据集，其中包含 21,976 份规格，配有自然语言、FSM 和专家编写的 Solidity 代码；主发布版本评估了 9,000 份生成合约。
- 一个多智能体流程先把每份规格解析成结构化 schema，再生成 Solidity，审计结果，在出现中等或更高问题时细化代码，并给最终合约打分。
- 评分由五项指标组成：Functional Completeness 25%，Variable Fidelity 15%，State Machine Correctness 15%，Business Logic Fidelity 35%，Code Quality 10%。
- 综合分数由原始指标值重新计算，避免直接接受 LLM 评估器给出的总分。
- 验证用了三项检查：人类专家评分、Slither 静态分析，以及每种条件 300 份合约的五条件消融研究。

## 结果
- 在 9,000 份生成合约上，SmartEval 报告的平均综合分数为 81.54，标准差为 12.87；在 8,824 份通过检查的合约中，编译成功率为 86.54%。
- 生成合约的分数为 81.54，专家真实实现为 73.25，按论文量表相差 +8.29 分，或 +11.3%。
- 各项指标的生成合约分数分别为：Functional Completeness 84.45、Variable Fidelity 84.62、State Machine Correctness 83.12、Business Logic Fidelity 76.73、Code Quality 83.85；其中 Business Logic Fidelity 最弱。
- 等级分布为 A 7.3%、B 66.4%、C 23.1%、D/F 3.2%，完全失败为 2.2%。
- 在 2,398 份表现较差的合约中，主要失败模式是逻辑遗漏，占 35.3%；状态转换错误占 23.4%。复杂度较高的规格如果有 8 个以上函数和 5 个以上状态，平均分为 71.8；低复杂度规格平均为 87.2。
- 验证结果显示，人类专家评分与自动评分相差不超过 0.34 分；Slither 与 LLM 审计器的一致率为 79.4%；门控消融中，关闭细化会把标准差从 4.89 提高到 10.31，并使编译率下降 5.2 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09610v1](https://arxiv.org/abs/2605.09610v1)
