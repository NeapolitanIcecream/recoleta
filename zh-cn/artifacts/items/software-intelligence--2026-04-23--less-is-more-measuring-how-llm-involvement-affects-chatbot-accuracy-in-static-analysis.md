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
本文研究在把自然语言请求转换为 Joern 的 CPGQL 查询时，静态分析聊天机器人应给大语言模型多少控制权。与直接生成查询相比，使用受 schema 约束的 JSON 中间表示效果更好，也优于这个基准上的 agentic 工具循环。

## 问题
- 论文关注的是让用户用自然语言访问静态分析工具：用户用普通英文提问，系统必须生成 Joern 的 CPGQL DSL 中的正确查询。
- 这很重要，因为静态分析工具有用，但难用；编写 CPGQL 需要 DSL 知识、图遍历语义和 schema 知识，而很多开发者并不具备这些知识。
- 以往系统在多大程度上把工作交给 LLM 这点上各不相同，但没有把“LLM 参与程度”作为被测试的变量单独拆出来。

## 方法
- 作者比较了同一任务的三种架构：**A1 直接生成** CPGQL，**A2 结构化中间表示**，即生成符合 schema 的 JSON，再由确定性映射器转换为 CPGQL，以及 **A3 agentic 工具使用**，采用类似 ReAct 的分析工具循环。
- A2 的核心机制很简单：LLM 填写一个小型有类型的 JSON 表单，字段包括查询类型、来源、汇点和输出列，普通代码再构建最终的 Joern 查询。LLM 不会写 CPGQL 语法。
- 他们在一个新的基准上评估这些设计，这个基准包含 **20 个代码分析任务**，分为 **3 个层级**：结构查询、数据流查询和组合查询，覆盖 **Apache Commons Lang** 和 **OWASP WebGoat**。
- 实验使用 **4 个开权重模型**，采用 **2×2 设计**：Llama 3.3 70B、Llama 3.1 8B、Qwen 2.5 72B 和 Qwen 2.5 7B，每个模型做 **3 次重复**。论文报告了 **720 次计划试验**，在排除大量 A3/Llama-70B 基础设施故障后，剩下 **660 次可用试验**。

## 结果
- **A2 在所有测试模型上都给出了最高的结果匹配率。** 在大模型上，它比 A1 高 **15.0 个百分点**，对应 **Qwen 72B** 的结果是 **58.3% 对 43.3%**，对 **Llama 70B** 高 **25.0 个百分点**，对应 **55.0% 对 30.0%**。
- 在小模型上，A2 仍然优于 A1，但优势更小：**Qwen 7B** 从 **31.7%** 提升到 **35.0%**，即 **+3.3 个百分点**；**Llama 8B** 从 **30.0%** 提升到 **35.0%**，即 **+5.0 个百分点**。
- **A3 表现最差**，而且成本高得多。结果匹配率在 **Qwen 72B** 上是 **25.0%**，在 **Qwen 7B** 上是 **15.0%**，在 **Llama 8B** 上也是 **15.0%**。摘要说，A3 每个任务消耗的 token 数大约是 A2 的 **8 倍**。
- A2 的收益取决于模型大小。它在 **Qwen 72B** 和 **Llama 70B** 上的执行成功率是 **100%**，但在 **Qwen 7B** 上降到 **65.0%**，在 **Llama 8B** 上降到 **53.3%**，说明小模型经常在 JSON 解析或 schema 验证上失败。
- A1 在各个模型上的执行成功率都很高，范围是 **98.3% 到 100%**，但结果正确率低于 A2。这意味着直接生成 CPGQL 往往能运行，但返回的分析结果仍然是错的。
- 论文的核心结论是：对于静态分析这类形式化领域，最好的分工是让 LLM 把请求解释成有类型的中间表示，再让确定性代码构建并运行最终查询。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21746v1](http://arxiv.org/abs/2604.21746v1)
