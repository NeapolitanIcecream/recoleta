---
source: arxiv
url: https://arxiv.org/abs/2605.02455v1
published_at: '2026-05-04T10:58:22'
authors:
- Shuzhao Feng
- Boqi Chen
- Brett H Meyer
- Gunter Mussbacher
topics:
- repository-level-code-generation
- spec-driven-engineering
- llm-code-generation
- software-modeling
- gherkin-testing
- code-verification
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# LLM-Assisted Repository-Level Generation with Structured Spec-Driven Engineering

## Summary
## 摘要
SSDE 使用 Gherkin 场景、领域模型和生成的 API 签名等结构化规格，引导 LLM 进行仓库级 MVC 代码生成。试点研究显示，结构化输入往往能比仅用自然语言提示提高测试通过率；同时，许多失败属于静态 API 或类型错误，工具可以捕捉到这些问题。

## 问题
- 当 LLM 代码生成从孤立函数或文件扩展到仓库级系统时，生成质量会下降。
- 自然语言提示存在歧义，也很难验证生成代码是否符合需求。
- 仓库级自动化需要生成的代码在整个系统中遵循需求、模型 API、约束和可执行行为。

## 方法
- 该方法向 LLM 提供结构化工件：Gherkin 示例、Umple 或 Ecore 领域模型、生成的模型层类和函数签名，以及控制器模板。
- LLM 生成 Python MVC 控制器业务逻辑，再与生成的模型层组合成后端系统。
- 试点使用 3 个 GitHub 系统：Symboleo、CheECSEManager 和 MeetingGroups，每个系统有 119 到 134 个测试用例。
- 研究测试 5 个 LLM：Claude Sonnet 4.5、Qwen 3 Coder 480B/A35B Instruct、GPT 5.1、GPT 5 Nano 和 Llama 3.2 3B Instruct。
- 每个 LLM 和输入设置运行 10 次，然后用 Python 单元测试通过率和人工失败检查评分。

## 结果
- 在 Claude Sonnet 4.5 的运行中，Symboleo 使用 Umple 加 Gherkin 加领域模型时，测试通过率达到 99.1% ± 2.9%；而仅用自然语言且没有模型时为 0.0% ± 0.0%。
- 对于使用 Umple 的 CheECSEManager，Claude 在自然语言加签名模型时达到 76.7% ± 0.0%，在 Gherkin 加签名模型时达到 79.2% ± 0.3%；Gherkin 加领域模型降到 25.7% ± 7.6%。
- 对于使用 Umple 的 MeetingGroups，Claude 从仅用自然语言时的 81.6% ± 0.0% 提高到自然语言加签名模型时的 85.0% ± 2.8%。
- 在所有 LLM 中，使用生成的模型层签名代替领域模型，使平均测试通过率提高 7.82 个百分点，并将标准差降低 2.47 个百分点。
- Gherkin 加模型的输入平均比自然语言加模型低 6.8 个百分点，但在 30 个 LLM/工具/系统组合中的 14 个组合里优于自然语言，在这些胜出组合中的平均提升为 7.7 个百分点。
- 失败分析发现，不存在的 API 调用占错误的 49.0%，数据类型不匹配占 20.2%，缺少约束验证占 11.5%，位置参数不匹配占 3.2%，不存在的变量占 1.0%；作者指出，超过 70% 的失败可以通过静态分析检测到。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02455v1](https://arxiv.org/abs/2605.02455v1)
