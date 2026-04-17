---
source: arxiv
url: http://arxiv.org/abs/2604.04806v2
published_at: '2026-04-06T16:10:23'
authors:
- XinRan Zhang
topics:
- microservice-testing
- llm-based-simulation
- integration-testing
- code-intelligence
- stateful-mocking
relevance_score: 0.79
run_id: materialize-outputs
language_code: zh-CN
---

# MIRAGE: Online LLM Simulation for Microservice Dependency Testing

## Summary
## 摘要
Mirage 通过让 LLM 在运行时直接回答依赖请求来测试微服务，而不是回放固定轨迹或使用预先构建的 mock。论文表明，在三个基准系统上，这种在线模拟比 record-replay 更接近真实依赖的行为。

## 问题
- 微服务集成测试需要下游服务具备正确的行为、状态和错误处理，但真实依赖往往不可用，或运行成本很高。
- 现有替代方案是静态的：record-replay、模式挖掘和基于规范的桩都必须在测试开始前编码好行为，因此会漏掉未见过的输入、多步状态变化和代码层面的边界情况。
- 在论文的留出场景中，record-replay 的状态码保真度只有 62%，响应形状保真度只有 16%，这意味着许多测试会让调用方面对不真实的依赖行为。

## 方法
- Mirage 在测试期间把 LLM 保留在请求路径中。对每个传入的 HTTP 请求，模型读取请求，使用之前的对话历史作为跨请求状态，并返回包含状态码、响应体和可选响应头的 JSON 响应。
- 提示词可以包含依赖源码、调用方源码和汇总后的生产轨迹。在 white-box 模式下使用这三者；在 black-box 模式下只使用调用方代码和轨迹。
- 在每个场景开始前，Mirage 会接收计划中的 HTTP 方法和路径序列，这样它可以为多步骤流程做准备，但看不到预期答案。
- 核心机制很直接：LLM 不是提前生成 mock 服务器，而是按需模拟依赖，并记住该场景中之前发生的事。
- 该系统作为 FastAPI mock 服务器运行，保留最近 20 次交互历史，遇到无效 JSON 时重试一次，并在场景之间重置状态。

## 结果
- 在 110 个场景、14 个调用方-依赖对和 3 个系统上，Mirage 在 white-box 模式下实现了 99% 的状态码保真度和 99% 的响应形状保真度，对应状态码 109/110 个场景正确，响应体形状为 99%。
- 在相同基准上，record-replay 的状态保真度为 62%，响应形状保真度为 16%。在 Demo 上，pattern-mining 达到 61%，Contract IR 达到 55%。
- 在 black-box 模式下，Mirage 仍然实现了 94% 的状态保真度（103/110）和 75% 的响应形状保真度（82/110），说明源码对结构准确性的帮助大于对状态预测的帮助。
- 在检查的 8/8 个场景中，使用 Mirage 和使用真实依赖的端到端调用方集成测试得到的通过/失败结果相同。
- 信号消融发现，在他们的测试中，仅依赖源码通常就足以达到完整保真度：单独使用时为 100%。没有依赖源码时，Mirage 的状态保真度仍有 94%，但响应体形状保真度只有 75%。仅使用轨迹时，状态保真度为 92%，响应体形状保真度为 53%。
- 类型化中间表示在复杂服务上效果较差：Contract IR 在 Demo 上得到 55%，在 Demo 的有状态场景中只有 29%，而 Mirage 在那里达到 100%。在更简单的 OB product-catalog 子集上，IR 为 86%，Mirage 为 100%。报告的成本是每个依赖 $0.16-$0.82，三类 LLM 的结果差异在 3% 以内。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04806v2](http://arxiv.org/abs/2604.04806v2)
