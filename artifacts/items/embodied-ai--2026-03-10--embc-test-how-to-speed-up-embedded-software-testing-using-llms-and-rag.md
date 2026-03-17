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
- software-verification
relevance_score: 0.01
run_id: materialize-outputs
---

# EmbC-Test: How to Speed Up Embedded Software Testing Using LLMs and RAG

## Summary
本文提出 EmbC-Test：一个面向嵌入式 C 单元测试生成的 RAG+LLM 流水线，用项目内代码、文档和历史测试为大模型提供上下文，从而更快地产生可执行测试。工业评估表明，该方法在正确性、可用性和效率上明显优于随机检索或无检索基线。

## Problem
- 目标问题：为嵌入式 C 软件自动生成测试，减少人工编写测试的高成本与低扩展性，避免验证环节成为发布流程瓶颈。
- 为什么重要：在安全相关嵌入式开发中，测试不仅要快，还要可追踪、可复现、与项目 API/规范一致；朴素零样本 LLM 容易幻觉、误用内部接口、写出错误断言，带来“虚假信心”。
- 现有缺口：以往 AI/自动化测试工作多集中在高级语言，较少覆盖嵌入式 C，且很少把项目文档、源码和遗留测试一起纳入生成过程。

## Approach
- 核心思路：先把项目工件（C 头文件、源码、遗留 Python 测试、需求文档）切分并建立可检索知识库，再让 LLM 在生成测试前先“查资料”，用检索到的上下文辅助生成。
- 为了提升检索质量，作者比较了 fixed-size、brace-aware、AST-based 等代码切分方式，以及按单个测试单元切分历史测试；随后用本地 embedding 建向量索引。
- 检索阶段采用 hybrid retrieval：把稠密向量检索与 BM25 词法检索结合，再用 Reciprocal Rank Fusion 融合，两者等权，取 top-5 片段送入提示词。
- 提示词由 system prompt 与 user prompt 组成；user prompt 中先放检索到的代码/测试片段，再放环境与项目约束，最后放软件需求，使模型先看到上下文再写测试。
- 评估覆盖 5 个维度：覆盖率、测试正确性（语法/导入/运行时）、检索质量、系统时延与吞吐、人类专家主观评审，并与随机检索和非 RAG 基线比较。

## Results
- 正确性：RAG 生成测试达到 **100.0%** 语法正确率、**84.5%** 运行时验证通过率；随机检索为 **100.0% / 62.4%**，无检索为 **96.8% / 50.5%**。说明 RAG 主要显著提升了“能正确运行”的比例。
- 覆盖率：RAG 在单次生成、无迭代优化条件下达到最高 **43% branch coverage**、**67% line coverage**；人工测试基线为 **76% branch**、**93% line**，但后者是经过数月迭代完善得到。
- 人工评估：最佳 RAG 配置在 5 分量表上得到 **4.33**（relevance）、**4.61**（assertion correctness）、**4.06**（edge-case completeness）、**4.83**（readability），测试可用率 **94.4%**。
- 接受情况：在最高人工评分配置中，**38.9%** 测试可直接接受，**55.6%** 需要修改，**5.6%** 需要重写；作者称 RAG 在所有人工评分类别上都优于随机检索和无检索。
- 效率：系统吞吐约 **270 tests/hour**，人工在该框架下约 **1 test/hour**。对 **57** 条软件需求，预计总工作量可从 **57 小时** 降到 **19.2 小时**，节省 **66%** 时间。
- 工业落地：论文称该工具已部署到 Hydac Software 工作流中，作为 AI 辅助测试生态的一环，用于把测试工程师从重复写测试转向审核、补边界条件和改进 oracle。

## Link
- [http://arxiv.org/abs/2603.09497v1](http://arxiv.org/abs/2603.09497v1)
