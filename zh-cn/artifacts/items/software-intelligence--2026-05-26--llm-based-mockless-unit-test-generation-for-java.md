---
source: arxiv
url: https://arxiv.org/abs/2605.26851v1
published_at: '2026-05-26T11:08:04'
authors:
- Qinghua Xu
- Guancheng Wang
- Lionel Briand
- Zhaoqiang Guo
- Kui Liu
topics:
- llm-test-generation
- java-unit-testing
- mockless-testing
- code-intelligence
- software-engineering-agents
- automated-software-production
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# LLM-based Mockless Unit Test Generation for Java

## Summary
## 摘要
MocklessTester 通过挖掘真实的依赖使用方式，并在项目特定约束下修复无效测试，生成不依赖 mock 的 Java 单元测试。它在 Defects4J 和一个截断时间点后的新基准 Deps4J 上都报告了比 PANTA 更高的覆盖率。

## 问题
- 当真实依赖需要按有效顺序构造、导入和调用时，LLM 生成的 Java 测试常常会失败。
- 基于 mock 的测试会用模拟行为替代真实对象，可能漏掉依赖代码中的 bug。
- 论文把失败来源概括为缺少项目上下文，以及在修复过程中对约束的遵守不够。

## 方法
- 预处理步骤会构建 Joern code property graph、可见类和成员的 ClassIndex，以及用于推断有效 API 调用顺序的 Markov typestate 模型。
- 规划器选择被测类中未覆盖的路径，然后生成器利用从项目里挖掘到的真实构造和调用示例来写测试。
- 验证器会编译并运行每个生成的 JUnit 测试，再把编译时和运行时错误交给修复器。
- 修复器分两步处理：先根据错误反馈修复，再用符号规则、typestate 规则和过去成功或失败修复的记忆做约束检查修复。

## 结果
- 在 Defects4J 上，平均行覆盖率从 PANTA 的 68.83% 提高到 88.82%，增加 19.99 个百分点。
- 在 Defects4J 上，分支覆盖率从 58.84% 提高到 83.74%，变异得分从 38.33% 提高到 52.00%。
- 在 Deps4J 上，行覆盖率从 53.29% 提高到 75.98%，分支覆盖率从 42.34% 提高到 58.12%。
- 摘要报告 Defects4J 的变异得分提升为 +13.67 个百分点，Deps4J 为 +0.17 个百分点。
- 依赖代码的行覆盖在 Defects4J 上从 819 增加到 1197，在 Deps4J 上从 224 增加到 279，说明生成的测试执行了更多真实的依赖代码。
- 报告的平均成本是 Defects4J 上每个方法 108.97 秒和 26.59k tokens，Deps4J 上每个方法 69.85 秒和 25.46k tokens。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26851v1](https://arxiv.org/abs/2605.26851v1)
