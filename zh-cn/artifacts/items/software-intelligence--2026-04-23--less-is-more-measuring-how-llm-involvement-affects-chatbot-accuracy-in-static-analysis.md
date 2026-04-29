---
source: arxiv
url: http://arxiv.org/abs/2604.21746v1
published_at: '2026-04-23T14:51:18'
authors:
- Krishna Narasimhan
topics:
- static-analysis
- llm-evaluation
- code-intelligence
- domain-specific-language
- agentic-systems
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Less Is More: Measuring How LLM Involvement affects Chatbot Accuracy in Static Analysis

## Summary
## 摘要
这篇论文研究了在把自然语言请求翻译成 Joern CPGQL 查询时，静态分析聊天机器人应当把多少控制权交给 LLM。在这个基准上，受 schema 约束的 JSON 中间表示比直接生成查询效果更好，也优于带工具循环的 agentic 方法。

## 问题
- 论文关注的是让用户通过自然语言使用静态分析工具：用户用普通英语提出代码分析请求，而系统必须生成正确的 Joern CPGQL DSL 查询。
- 这很重要，因为静态分析工具很有用，但不容易使用；编写 CPGQL 需要 DSL 知识、图遍历语义知识和 schema 知识，而很多开发者并不具备这些知识。
- 现有系统在分配给 LLM 的工作量上差异很大，但没有把“LLM 参与程度”单独作为被测试的变量。

## 方法
- 作者为同一任务比较了三种架构：**A1 直接生成** CPGQL，**A2 结构化中间表示**，即生成符合 schema 的 JSON，再由确定性映射器转换为 CPGQL，以及 **A3 agentic 工具使用**，即采用 ReAct 风格循环调用分析工具。
- A2 的核心机制很简单：LLM 填写一个小型的类型化 JSON 表单，字段包括查询类型、source、sink 和输出列等，然后由普通代码构建最终的 Joern 查询。LLM 不直接编写 CPGQL 语法。
- 他们在一个新的基准上评估这些设计。该基准包含 **20 个代码分析任务**，分为 **3 个层级**：结构查询、数据流查询和组合查询，覆盖 **Apache Commons Lang** 和 **OWASP WebGoat**。
- 实验使用了 **4 个开放权重模型**，采用 **2×2 设计**：Llama 3.3 70B、Llama 3.1 8B、Qwen 2.5 72B 和 Qwen 2.5 7B，每个模型都进行了 **3 次重复**。论文报告了 **720 次计划试验**，并在排除大量 A3/Llama-70B 基础设施故障后，得到 **660 次可用试验**。

## 结果
- **A2 在所有测试模型上都取得了最高的结果匹配率。** 在大模型上，它比 A1 高出 **+15.0 个百分点**（**Qwen 72B**：**58.3% vs 43.3%**），在 **Llama 70B** 上高出 **+25.0 个百分点**（**55.0% vs 30.0%**）。
- 在小模型上，A2 仍然优于 A1，但优势较小：**Qwen 7B** 从 **31.7%** 提高到 **35.0%**（**+3.3 个百分点**），**Llama 8B** 从 **30.0%** 提高到 **35.0%**（**+5.0 个百分点**）。
- **A3 的表现最差**，而成本却高得多。报告中的结果匹配率分别是：**Qwen 72B** 为 **25.0%**，**Qwen 7B** 为 **15.0%**，**Llama 8B** 为 **15.0%**。摘要称，A3 每个任务消耗的 token 大约是 A2 的 **8×**。
- A2 的收益取决于模型规模。它在 **Qwen 72B** 和 **Llama 70B** 上的执行成功率是 **100%**，但在 **Qwen 7B** 上降到 **65.0%**，在 **Llama 8B** 上降到 **53.3%**，这说明小模型经常在 JSON 解析或 schema 验证阶段失败。
- A1 在各模型上的执行成功率都很高，为 **98.3% 到 100%**，但结果正确性低于 A2。这说明直接生成 CPGQL 通常可以运行，但返回的分析输出仍然是错的。
- 论文的主要结论是：在静态分析这类形式化领域里，最好的分工方式是让 LLM 把请求解释为类型化的中间表示，再由确定性代码构建并执行最终查询。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21746v1](http://arxiv.org/abs/2604.21746v1)
