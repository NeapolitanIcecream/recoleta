---
source: arxiv
url: https://arxiv.org/abs/2607.19682v1
published_at: '2026-07-22T02:31:10'
authors:
- Junjie Chen
- Ziqi Wang
- Lin Yang
- Chen Yang
- Xiao Chu
- Jianyi Zhou
- Guangtai Liang
- Qianxiang Wang
- Dong Wang
topics:
- code-intelligence
- automated-software-production
- unit-test-generation
- llm-agents
- program-analysis
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Context Matters: Improving the Practical Reliability of LLM-Based Unit Test Generation

## Summary
## 摘要
CATGen 通过明确项目上下文，并将测试脚手架和常见修复转移到确定性分析中，提高了 LLM 生成单元测试的实际可靠性。该经验论文报告称，在专有工业项目和 Defects4J 上，CATGen 取得了更高的编译成功率和覆盖率，同时降低了生成时间和令牌使用量。

## 问题
- 在框架复杂且存在跨文件依赖的项目中，即使测试逻辑看似合理，LLM 生成的测试也经常无法编译。
- 项目上下文缺失、脆弱的测试类脚手架以及反复的 LLM 修复循环，增加了开发者工作量、延迟和令牌消耗。
- 这一点很重要，因为在生成的测试能够编译并执行之前，覆盖率提升的实际价值有限。

## 方法
- CATGen 使用构建文件解析和轻量级基于 AST 的分析，检索五类上下文：被测类结构、被测方法细节、外部方法调用、测试框架和模拟框架。
- CATGen 确定性地构建特定于框架的测试类骨架，其中包括导入、注解、生命周期方法、模拟对象和初始化逻辑，而不是要求 LLM 生成这些样板代码。
- LLM 在固定骨架的约束下完成代码生成，生成测试方法、模拟对象和断言，同时分析被测方法的分支。
- 基于程序分析的后处理应用八种确定性修复策略，包括补全导入、修正注解、对齐签名、解析无效引用和处理异常，且无需额外的 LLM 修复轮次。

## 结果
- 在来自 8 个专有工业项目的 183 个被测方法上，与 6 个具有代表性的基线方法相比，CATGen 将编译成功率提高了 24.72%–38.05%。
- 在工业基准测试中，行覆盖率提高了 17.27%–22.17%，分支覆盖率提高了 15.31%–18.24%。
- 工业项目中的生成时间减少了 51.27%–69.00%，令牌使用量减少了 66.83%–83.86%。
- 在 Defects4J 上，与现有的基于 LLM 的方法相比，CATGen 将编译成功率提高了 10.42%–14.33%，行覆盖率提高了 6.11%–8.39%，分支覆盖率提高了 3.27%–10.56%。
- 工业基准测试包含的被测方法中，有 57.38% 涉及复杂依赖，且平均与 3.05 个外部文件交互；但摘录未提供绝对指标值或各基线方法的具体结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.19682v1](https://arxiv.org/abs/2607.19682v1)
