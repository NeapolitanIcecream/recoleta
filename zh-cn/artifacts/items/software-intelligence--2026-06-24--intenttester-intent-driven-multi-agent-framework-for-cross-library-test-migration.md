---
source: arxiv
url: https://arxiv.org/abs/2606.25588v1
published_at: '2026-06-24T08:59:01'
authors:
- Yi Gao
- Ziyuan Zhang
- Xing Hu
- Xiaohu Yang
- Xin Xia
topics:
- test-migration
- code-intelligence
- multi-agent-systems
- software-testing
- llm-code-generation
- repository-graphs
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# IntentTester: Intent-Driven Multi-agent Framework for Cross-Library Test Migration

## Summary
## 摘要
IntentTester 通过把源测试转换为与语言无关的测试意图，为目标代码库生成可执行测试，从而在相似库之间迁移单元测试。它面向 API 签名映射失效的场景，包括 Java-Python 迁移。

## 问题
- 单元测试会编码领域行为；相似库经常手工重写测试，造成重复劳动，也留下行为覆盖缺口。
- 当不同库用不同 API、编码风格或编程语言暴露相同功能时，基于 API 签名和代码模式的映射工具会失效。
- 可运行的迁移测试需要构造函数、fixture、返回值调用链和断言；缺少依赖通常会导致运行时失败。

## 方法
- 系统把源测试拆成更小的子测试，并把每个子测试转换为一条 Test Description Language 记录，其中包含测试数据、设置、焦点方法和断言。
- 它构建目标代码库图，包含类、方法、字段、测试，以及调用、返回、字段访问、继承、测试到方法链接等带类型的边。
- 它使用 MiniLM 嵌入和 FAISS k-NN 搜索，从 TDL 步骤中检索候选目标实体，然后沿图边扩展以收集所需依赖。
- 规划代理检查上下文是否包含足够的构造函数、方法和断言目标；它会再扩展一次，或丢弃不受支持的意图。
- LLM 根据 TDL、图上下文和参考测试生成目标测试，随后验证代理检查输出，并在需要时发送反馈。

## 结果
- 评估覆盖 Java 和 Python 中 JSON、HTML、Time 三类库的 9 个开源项目。
- 流水线从 2,058 个源测试生成 5,536 个子测试；过滤后保留 3,257 个。
- IntentTester 生成了 2,776 个语法正确的测试，正确率为 85%；相比之下，MUT 为 51%，METALLICUS 为 43%。
- 2,410 个生成测试在目标代码库中成功执行，有效率为 74%。
- 论文报告称，IntentTester 相比 MUT 的正确率提高 34 个百分点，相比 METALLICUS 提高 42 个百分点。
- 生成的测试暴露了 25 个真实缺陷，包括 NanoJSON 在循环 JSON 引用上的栈溢出，以及 JFiveParse 的空指针解引用；JFiveParse 问题已由维护者修复。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.25588v1](https://arxiv.org/abs/2606.25588v1)
