---
source: arxiv
url: http://arxiv.org/abs/2604.22028v1
published_at: '2026-04-23T19:43:53'
authors:
- Beatriz Souza
- Chang Lou
- Suman Nath
- Michael Pradel
topics:
- runtime-checking
- llm-for-code
- test-to-checker
- software-reliability
- silent-failure-detection
relevance_score: 0.85
run_id: materialize-outputs
language_code: zh-CN
---

# FlyCatcher: Neural Inference of Runtime Checkers from Tests

## Summary
## 摘要
FlyCatcher 从现有测试中推断项目特定的运行时检查器，使软件能在执行过程中捕获静默的语义失效。它将基于 LLM 的检查器合成与静态分析和验证结合起来，并加入了一个用于有状态属性的影子状态机制。

## 问题
- 许多软件故障是静默发生的：程序继续运行，但违背了预期行为，这可能破坏数据或产生错误结果。
- 手工编写语义运行时检查器很难，实践中也不常见，尽管这类检查器能捕获测试遗漏的故障。
- 把一个具体测试转换成检查器并不容易，因为检查器必须能泛化测试工作负载、正确解释常量，并跟踪不断变化的程序状态。

## 方法
- FlyCatcher 以目标测试、相关上下文测试和验证测试为输入，并从中推断运行时检查器。
- 它使用基于 CodeQL 的静态分析和 LLM 来识别检查器应监控的状态变化方法。
- 它提示 LLM 生成检查器代码，用来更新每个对象的**影子状态**，即与相关属性对应的抽象映射，例如被跟踪的子对象或计数。
- 检查器将真实运行时行为与影子状态进行比较，以在新的工作负载下执行原始测试所编码的语义属性。
- 生成的检查器会经过一个反馈循环，包括编译检查、结构检查，以及在留出测试上的动态验证；失败会生成反馈，用于下一轮合成尝试。

## 结果
- 评估使用了来自 **4** 个复杂开源 Java 系统的 **400** 个测试。
- FlyCatcher 推断出 **334** 个检查器，其中 **300** 个通过交叉验证被判定为正确。
- 与 **T2C** 相比，它生成的正确检查器数量多 **2.6x**。
- 在变异测试中，FlyCatcher 生成的检查器检测到的变异体数量是 T2C 生成检查器的 **5.2x**。
- 平均每个检查器的生成成本为 **15 秒**、**183k LLM tokens**，以及约 **0.60 美元**。
- 运行时开销范围为 **2.7% 到 40.3%**，具体取决于目标系统。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22028v1](http://arxiv.org/abs/2604.22028v1)
