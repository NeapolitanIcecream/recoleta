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
## 摘要
HiveMind 是一个透明的 HTTP 代理，它按操作系统调度竞争进程的方式来调度并发 LLM 代理流量。它针对编码代理工作负载中的一个常见故障场景：多个代理共享一个有速率限制的 API，发生冲突，即使总容量足够也会失败。

## 问题
- 论文处理的是并行 LLM 编码代理共享同一个 API key 或端点时的失败。没有协调时，代理会碰到速率限制、连接上限、延迟尖峰和 HTTP 502、`ECONNRESET` 这类瞬时服务器错误。
- 这类失败很重要，因为编码代理是长时间运行的有状态会话。运行中途的 API 故障会浪费 50k-500k token，丢失上下文，并在文件编辑和工具调用已经发生后迫使重启。
- 促发案例里，11 个 Claude Code 代理并发使用一个 Anthropic key；其中 3 个失败，失败率为 27%，浪费了大约 135k token 和大约 15 分钟。论文认为问题出在协调上，而不是 API 总容量，因为如果把启动时间错开 5 秒，11 个都能完成。

## 方法
- HiveMind 在代理和上游模型 API 之间放一个本地代理层，因此现有代理不需要改代码。代理继续发普通 HTTP 请求，由代理层决定何时以及如何转发。
- 核心机制是一组五个类操作系统的调度控制加上透明重试：接纳控制限制在途请求，速率限制跟踪监控 RPM/TPM 和提供方头信息，AIMD 背压在延迟或错误上升时降低并发，token 预算限制失控代理，优先队列按优先级和估计成本安排工作。
- 熔断器会在最近错误率过高时快速失败新请求，然后在冷却期后探测恢复。像 429、502、503、529 和连接重置这类可重试错误会带指数退避和抖动重试，对代理隐藏。
- 系统会自动识别 Anthropic、OpenAI、Azure OpenAI、Google AI、Ollama 和通用 OpenAI 兼容端点的提供方配置。它也支持 SSE 流式输出，并从流事件或响应正文中提取 token 数。
- 论文强调的一项实现细节是用 `asyncio.Condition` 做动态并发控制，而不是直接修改 semaphore，这样在高负载下调整容量是安全的。

## 结果
- 在 7 个场景、5 到 50 个并发代理下，未协调执行在冲突条件下的失败率是 72%-100%，而摘要称 HiveMind 把失败率降到 0%-18%。
- 在表 5 中，直接执行与 HiveMind 的失败率分别是：`micro-10` 100% -> 10%，`micro-20` 100% -> 10%，`micro-50` 100% -> 0%，`replay-11` 73% -> 18%，`stress` 100% -> 10%，`lat.-spike` 100% -> 0%。`micro-5` 在两种模式下都是 0%，因为没有冲突。
- 死亡代理造成的浪费计算在评估场景中下降了 48%-100%。表 5 报告的 token 浪费减少幅度是：`replay-11` 为 48%，`micro-20` 为 94%，`micro-10`、`micro-50`、`stress` 和 `lat.-spike` 为 100%。
- 对 `replay-11` 的消融研究显示，完整 HiveMind 达到 11 个存活、0 个死亡、失败率 0.0%。关闭重试后，结果降到 4 个存活、7 个死亡、失败率 63.6%，说明重试是最重要的单项机制。只保留接纳控制时，结果是 2 个存活、9 个死亡、失败率 81.8%，说明单纯限制并发不够。
- 去掉背压后，11 个代理中有 1 个死亡，失败率 9.1%。去掉接纳控制或速率限制跟踪时，在那个场景里仍然是 0.0% 失败，作者把这解读为其余控制机制起到了补偿作用。
- 面向 Ollama 的真实验证在摘要中报告，每个请求的代理开销低于 3 ms。提供的摘录没有给出表 7 的完整数值，只提到这项开销结论。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17111v1](http://arxiv.org/abs/2604.17111v1)
