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
Mirage 在测试微服务时，不再回放固定轨迹或使用预先构建的 mock，而是在运行时让 LLM 回答依赖请求。论文显示，这种在线模拟在三个基准系统上的行为匹配程度，明显高于 record-replay。

## 问题
- 微服务集成测试需要下游服务具备正确的行为、状态和错误处理，但真实依赖经常不可用，或者运行成本太高。
- 现有替代方案都是静态的：record-replay、模式挖掘和基于规格的 stub 都要在测试开始前把行为编码好，所以它们会漏掉未见过的输入、多步状态变化和代码层面的边缘情况。
- 在论文的留出场景中，record-replay 的状态码一致率只有 62%，响应形状一致率只有 16%，这意味着很多测试会让调用方面对不真实的依赖行为。

## 方法
- Mirage 在测试过程中把 LLM 放在请求路径上。每当收到一条 HTTP 请求，模型读取请求内容，把之前的对话历史当作跨请求状态，再返回包含状态码、正文和可选头部的 JSON 响应。
- 提示词可以包含依赖方源代码、调用方源代码和汇总后的生产轨迹。在白盒模式下使用三者；在黑盒模式下只用调用方代码和轨迹。
- 每个场景开始前，Mirage 会收到计划好的 HTTP 方法和路径序列，这样它可以在不知道期望答案的情况下，为多步流程做准备。
- 关键机制很直接：它不先生成 mock 服务器，而是在需要时由 LLM 按需模拟依赖，并记住场景前面发生的事。
- 系统作为一个 FastAPI mock 服务器运行，保留最近 20 轮交互历史，遇到无效 JSON 时重试一次，并在场景之间重置状态。

## 结果
- 在 110 个场景、14 组调用方-依赖方配对和 3 个系统上，Mirage 的白盒模式达到 99% 的状态码一致率和 99% 的响应形状一致率；按状态码算是 109/110 个场景一致，按正文形状算是 99%。
- 在同样的基准上，record-replay 的状态一致率是 62%，响应形状一致率是 16%。在 Demo 上，pattern-mining 达到 61%，Contract IR 达到 55%。
- 在黑盒模式下，Mirage 仍然达到 94% 的状态一致率（103/110）和 75% 的响应形状一致率（82/110），说明源代码对结构准确性的帮助大于对状态预测的帮助。
- 端到端的调用方集成测试中，Mirage 和真实依赖在 8/8 个检查场景里的通过/失败结果完全一致。
- 消融实验显示，依赖方源代码单独使用时，往往就足以在这些测试上达到完全一致：单独使用就能到 100%。没有依赖方源码时，Mirage 仍然得到 94% 的状态一致率，但正文形状一致率只有 75%。只用轨迹时，状态一致率是 92%，正文形状一致率是 53%。
- 带类型的中间表示会拖累复杂服务上的表现：Contract IR 在 Demo 上只有 55%，在 Demo 的有状态场景上只有 29%，而 Mirage 在那里达到 100%。在更简单的 OB 产品目录子集上，IR 达到 86%，Mirage 是 100%。报告的成本是每个依赖方 0.16 美元到 0.82 美元，三个 LLM 家族之间的结果差异在 3% 以内。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04806v2](http://arxiv.org/abs/2604.04806v2)
