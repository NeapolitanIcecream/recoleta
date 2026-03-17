---
source: arxiv
url: http://arxiv.org/abs/2603.09497v1
published_at: '2026-03-10T10:58:59'
authors:
- Maximilian Harnot
- Sebastian Komarnicki
- Michal Polok
- Timo Oksanen
topics:
- rag
- llm-testing
- embedded-c
- unit-test-generation
- code-intelligence
relevance_score: 0.92
run_id: materialize-outputs
---

# EmbC-Test: How to Speed Up Embedded Software Testing Using LLMs and RAG

## Summary
本文提出 EmbC-Test：一个面向嵌入式 C 单元测试生成的 RAG+LLM 流水线，用项目内代码、文档和历史测试来约束生成结果。其目标不是完全替代人工，而是把测试工程师从手写测试转向高效审核与修订，从而显著加速工业验证流程。

## Problem
- 嵌入式 C 的自动化测试仍高度依赖人工编写，耗时且难以跟上更快的软件发布节奏，验证因此成为开发瓶颈。
- 直接用零样本 LLM 生成测试不可靠：容易幻觉出不存在的 API、类型或断言，即使能运行也可能给出错误预期，尤其在安全相关场景中风险很高。
- 现有 AI/自动测试研究更多聚焦高级语言，较少把项目特定文档、旧测试和代码结构系统性地用于嵌入式 C 测试生成。

## Approach
- 构建项目知识库：收集 C 头文件、源代码和历史 Python 测试，并用固定长度、brace-aware、AST-based、test-unit 等方式切块。
- 对知识块做本地嵌入与索引，在线阶段将需求文本作为查询，从向量检索和 BM25 词法检索中做混合召回，并用 RRF 融合，取 top-5 上下文。
- 将检索到的代码片段、测试模板、项目环境说明和软件需求一起放入提示词，让云端 LLM 生成符合项目约定的测试。
- 配套质量评估与保障：比较 RAG、随机检索、无检索基线，并从语法、运行正确性、覆盖率、检索质量、性能和人工评审多个维度验证。

## Results
- 工业评估中，RAG 生成测试达到 **100.0%** 语法正确率、**84.5%** 运行验证通过率；对比随机检索 **100.0% / 62.4%**、无检索 **96.8% / 50.5%**，RAG 在运行正确性上明显更强。
- 覆盖率方面，RAG 最佳配置达到 **43% branch coverage** 和 **67% line coverage**；人工现有测试套件为 **76% branch**、**93% line**，但后者经历了数月迭代，而 RAG 结果来自单次生成、无反馈优化。
- 人工评估中，最佳 RAG 配置在 5 分量表上达到：**4.33**（relevance）、**4.61**（assertion correctness）、**4.06**（edge-case completeness）、**4.83**（readability）。
- 最佳配置的测试可用率达到 **94.4%**；其中 **38.9%** 可直接接受，**55.6%** 需少量修改，仅 **5.6%** 需要重写。
- 生成效率约为 **270 tests/hour**，而人工在该框架下约 **1 test/hour**。
- 在 **57** 条软件需求的案例中，总测试工作量可从 **57 小时** 降至 **19.2 小时**，宣称节省 **66%** 时间。

## Link
- [http://arxiv.org/abs/2603.09497v1](http://arxiv.org/abs/2603.09497v1)
