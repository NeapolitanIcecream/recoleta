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
## 摘要
SmartEval 是一个基准，用于评估 LLM 根据自然语言规格生成的 Solidity 合约。它将 9,000 份生成合约与专家实现配对，并用五项指标评分，重点检查规格保真度和状态机行为。

## 问题
- LLM 可以编写 Solidity，但智能合约需要准确的业务逻辑、状态转换、访问控制和安全检查，因为部署后的缺陷可能锁定或造成资金损失。
- 现有评估通常检查语法或编译情况，无法发现合约是否遵循自然语言需求和 FSM 规格。
- 论文针对一个测量缺口：研究人员需要一种可重复的方法，用来比较 LLM 生成的智能合约和专家实现。

## 方法
- SmartEval 使用 FSM-SCG 数据集，该数据集包含 21,976 份规格，配有自然语言、FSM 和专家编写的 Solidity 代码；主发布版本评估 9,000 份生成合约。
- 多智能体流水线将每份规格解析为结构化模式，生成 Solidity，审计结果，在出现中等或更高级别问题时优化代码，并为最终合约评分。
- 分数由五项指标合成：功能完整性 25%、变量保真度 15%、状态机正确性 15%、业务逻辑保真度 35% 和代码质量 10%。
- 综合分数根据原始指标值重新计算，避免直接接受 LLM 评估器生成的汇总分数。
- 验证使用三项检查：人类专家评分、Slither 静态分析，以及每个条件 300 份合约的五条件消融研究。

## 结果
- 在 9,000 份生成合约上，SmartEval 报告的平均综合分数为 81.54，标准差为 12.87；在 8,824 份受检合约中，编译成功率为 86.54%。
- 生成合约得分为 81.54，专家真值实现为 73.25；按论文的评分规则，提升为 +8.29 分，即 +11.3%。
- 生成合约各项指标得分为：功能完整性 84.45、变量保真度 84.62、状态机正确性 83.12、业务逻辑保真度 76.73、代码质量 83.85；业务逻辑保真度是最低的一项。
- 等级分布为 7.3% A、66.4% B、23.1% C 和 3.2% D/F，完全失败比例为 2.2%。
- 在 2,398 份表现较低的合约中，主要失败模式包括 35.3% 的逻辑遗漏和 23.4% 的状态转换错误；包含 8+ 个函数和 5+ 个状态的高复杂度规格平均得分为 71.8，而低复杂度规格为 87.2。
- 验证结果显示，人类专家一致性在 0.34 分以内，Slither 与 LLM 审计器的一致率为 79.4%；在门控消融中，禁用优化会使标准差从 4.89 升至 10.31，并使编译率下降 5.2 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09610v1](https://arxiv.org/abs/2605.09610v1)
