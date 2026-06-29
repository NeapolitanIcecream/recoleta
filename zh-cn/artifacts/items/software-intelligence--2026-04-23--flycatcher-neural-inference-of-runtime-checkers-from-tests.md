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
## 总结
FlyCatcher 从现有测试中推断项目特定的运行时检查器，让软件在执行过程中捕捉静默的语义失败。它把基于 LLM 的检查器合成、静态分析和验证结合起来，并加入一个用于有状态属性的影子状态机制。

## 问题
- 许多软件故障是静默的：程序还在运行，但已经违反了预期行为，这会破坏数据或产生错误结果。
- 手工编写语义运行时检查器很难，也不常见，尽管这类检查器能捕捉测试漏掉的故障。
- 把一个具体测试转换成检查器也很难，因为检查器必须对测试负载做泛化，正确解释常量，并跟踪不断变化的程序状态。

## 方法
- FlyCatcher 接收目标测试、相关上下文测试和验证测试，然后据此推断运行时检查器。
- 它把基于 CodeQL 的静态分析和 LLM 结合起来，找出检查器应当监控的状态变化方法。
- 它提示 LLM 生成检查器代码，更新按对象划分的 **shadow state**，也就是相关属性的抽象映射，例如被跟踪的子对象或计数。
- 检查器把真实运行时行为与 shadow state 进行对比，在新的负载下强制执行原始测试编码的语义属性。
- 生成的检查器会经过一个反馈循环，包含编译检查、结构检查和在留出测试上的动态验证；失败结果会作为反馈，触发下一轮合成尝试。

## 结果
- 评估使用了来自 **4** 个复杂开源 Java 系统的 **400** 个测试。
- FlyCatcher 推断出 **334** 个检查器，其中 **300** 个通过交叉验证被判定正确。
- 与 **T2C** 相比，它产生的正确检查器多 **2.6 倍**。
- 在变异测试中，FlyCatcher 生成的检查器比 T2C 生成的检查器多检测出 **5.2 倍** 的变异体。
- 检查器生成的平均成本是 **15 秒**、**183k** LLM token，以及每个检查器约 **0.60 美元**。
- 运行时开销介于 **2.7% 到 40.3%**，取决于目标系统。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22028v1](http://arxiv.org/abs/2604.22028v1)
