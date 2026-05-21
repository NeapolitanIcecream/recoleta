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
SSDE 使用 Gherkin 场景、领域模型和生成的 API 签名等结构化规格，引导 LLM 生成仓库级 MVC 代码。试点研究显示，与仅使用自然语言提示相比，结构化输入通常能提高测试通过率；许多失败是静态 API 错误或类型错误，工具可以捕获这些问题。

## 问题
- LLM 代码生成从独立函数或文件扩展到仓库级系统时，质量会下降。
- 自然语言提示存在歧义，对验证生成代码是否符合需求的支持较弱。
- 仓库级自动化需要生成的代码在整个系统中符合需求、模型 API、约束和可执行行为。

## 方法
- 该方法向 LLM 提供结构化产物：Gherkin 示例、Umple 或 Ecore 领域模型、生成的模型层类和函数签名，以及控制器模板。
- LLM 生成 Python MVC 控制器业务逻辑，再与生成的模型层结合，形成后端系统。
- 试点使用 3 个 GitHub 系统：Symboleo、CheECSEManager 和 MeetingGroups，每个系统有 119 到 134 个测试用例。
- 研究测试了 5 个 LLM：Claude Sonnet 4.5、Qwen 3 Coder 480B/A35B Instruct、GPT 5.1、GPT 5 Nano 和 Llama 3.2 3B Instruct。
- 每个 LLM 和输入设置运行 10 次，然后按 Python 单元测试通过率和人工失败检查评分。

## 结果
- 在 Claude Sonnet 4.5 的运行中，Symboleo 使用 Umple 加 Gherkin 加领域模型时，测试通过率达到 99.1% ± 2.9%；无模型的自然语言输入为 0.0% ± 0.0%。
- 对使用 Umple 的 CheECSEManager，Claude 在自然语言加签名模型下达到 76.7% ± 0.0%，在 Gherkin 加签名模型下达到 79.2% ± 0.3%；Gherkin 加领域模型降至 25.7% ± 7.6%。
- 对使用 Umple 的 MeetingGroups，Claude 从仅使用自然语言的 81.6% ± 0.0% 提升到自然语言加签名模型的 85.0% ± 2.8%。
- 在所有 LLM 中，使用生成的模型层签名替代领域模型，使平均测试通过率提高 7.82 个百分点，并使标准差降低 2.47 个百分点。
- Gherkin 加模型输入的平均测试通过率比自然语言加模型输入低 6.8 个百分点，但在 30 个 LLM/工具/系统组合中有 14 个超过自然语言；这些胜出组合的平均增幅为 7.7 个百分点。
- 失败分析发现，不存在的 API 调用占错误的 49.0%，数据类型不匹配占 20.2%，缺少约束验证占 11.5%，位置参数不匹配占 3.2%，不存在的变量占 1.0%；作者称，超过 70% 的失败可以通过静态分析检测。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02455v1](https://arxiv.org/abs/2605.02455v1)
