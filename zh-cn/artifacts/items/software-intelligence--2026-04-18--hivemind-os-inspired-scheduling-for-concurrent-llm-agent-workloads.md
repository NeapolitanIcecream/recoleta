---
source: arxiv
url: http://arxiv.org/abs/2604.17111v1
published_at: '2026-04-18T18:59:33'
authors:
- Justice Owusu Agyemang
- Jerry John Kponyo
- Obed Kwasi Somuah
- Elliot Amponsah
- Godfred Manu Addo Boakye
- Kwame Opuni-Boachie Obour Agyekum
topics:
- llm-agents
- multi-agent-systems
- api-scheduling
- coding-agents
- resource-management
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# HiveMind: OS-Inspired Scheduling for Concurrent LLM Agent Workloads

## Summary
## 概要
HiveMind 是一个透明的 HTTP 代理，用操作系统调度竞争进程的方式来调度并发 LLM 代理流量。它针对编码代理工作负载中的一种常见故障：多个代理共享一个有速率限制的 API，相互冲突并失败，即使总容量其实足够。

## 问题
- 论文讨论的是并行 LLM 编码代理共享同一个 API key 或端点时出现的故障。缺少协调时，代理会撞上速率限制、连接上限、延迟尖峰，以及 HTTP 502 和 `ECONNRESET` 这类瞬时服务器错误。
- 这很重要，因为编码代理是长时间运行且带状态的会话。运行中途的 API 故障可能浪费 50k-500k token，丢失上下文，并在文件编辑和工具调用已经发生后被迫重启。
- 触发这项工作的案例是 11 个并发 Claude Code 代理共用一个 Anthropic key；其中 3 个失败，失败率 27%，浪费了约 135k token 和约 15 分钟。论文认为问题在于协调，而不是 API 总容量不足，因为如果把启动时间错开 5 秒，11 个代理都可以完成。

## 方法
- HiveMind 在代理与上游模型 API 之间放置一个本地代理，因此现有代理不需要改代码。代理仍然发出普通 HTTP 请求，由代理层决定何时以及如何转发。
- 核心机制是一组五个类操作系统的调度控制，再加上透明重试：准入控制限制进行中的请求数，速率限制跟踪监控 RPM/TPM 和提供方响应头，AIMD 背压在延迟或错误上升时降低并发，token 预算限制失控代理，优先级队列按优先级和估计成本安排工作。
- 当最近错误率过高时，熔断器会让新请求快速失败，然后在冷却后探测是否恢复。对于 429、502、503、529 和连接重置这类可重试错误，系统会用指数退避和抖动进行重试，并对代理隐藏这些过程。
- 系统会自动检测 Anthropic、OpenAI、Azure OpenAI、Google AI、Ollama 以及通用 OpenAI 兼容端点的提供方配置。它也支持 SSE 流式传输，并从流事件或响应体中提取 token 计数。
- 论文特别强调的一个实现细节是：通过 `asyncio.Condition` 实现动态并发控制，而不是直接修改 semaphore，这使得在负载下调整大小仍然安全。

## 结果
- 根据摘要，在 7 个场景、5-50 个并发代理的测试中，无协调执行在资源争用下的失败率为 72%-100%，而 HiveMind 将失败率降到 0%-18%。
- 在表 5 中，直连与 HiveMind 的失败率分别是：`micro-10` 100% -> 10%，`micro-20` 100% -> 10%，`micro-50` 100% -> 0%，`replay-11` 73% -> 18%，`stress` 100% -> 10%，`lat.-spike` 100% -> 0%。由于没有资源争用，`micro-5` 两种模式都是 0%。
- 已评估场景中，因代理失败导致的浪费计算下降了 48%-100%。表 5 给出的 token 浪费降幅是：`replay-11` 为 48%，`micro-20` 为 94%，`micro-10`、`micro-50`、`stress` 和 `lat.-spike` 为 100%。
- 在 `replay-11` 上的消融实验中，完整 HiveMind 的结果是 11 个存活，0 个失败，失败率 0.0%。禁用重试后降为 4 个存活、7 个失败、失败率 63.6%，说明重试是最关键的单一机制。仅有准入控制时，结果是 2 个存活、9 个失败、失败率 81.8%，说明简单的并发上限不够。
- 去掉背压后，11 个代理中有 1 个失败，失败率 9.1%。在该场景中，去掉准入控制或速率限制跟踪后失败率仍为 0.0%，作者将其解释为其余控制机制起到了补偿作用。
- 摘要中的真实环境验证显示，针对 Ollama 时每个请求增加的代理开销低于 3 ms。给出的摘录没有包含表 7 的完整数值，除了这条开销结论。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17111v1](http://arxiv.org/abs/2604.17111v1)
