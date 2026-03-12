---
source: hn
url: https://surfingcomplexity.blog/2026/03/07/grow-fast-and-overload-things/
published_at: '2026-03-07T23:13:16'
authors:
- azhenley
topics:
- llm-reliability
- service-availability
- resilience-engineering
- capacity-planning
- ai-infrastructure
relevance_score: 0.62
run_id: materialize-outputs
---

# Grow Fast and Overload Things

## Summary
这篇文章认为，当前主流 AI 服务的可靠性差，主要不是因为“开发太快”，而是因为用户对 LLM 的采用速度过快、用法不断涌现，导致系统频繁过载。作者将这一现象概括为“grow fast and overload things”，并从韧性工程视角解释其成因与改进方向。

## Problem
- 文章讨论的问题是：为什么 OpenAI 和 Anthropic 等 LLM 服务商的在线服务可靠性不高，以及这种不稳定性为何重要。
- 这很重要，因为 LLM 正在成为广泛依赖的基础能力，但服务可用性不足会直接影响用户工作流、产品集成与行业信任。
- 作者反驳“高开发速度导致低可靠性”的简单解释，认为更核心的问题是需求增长和使用方式创新带来的不可预测负载与系统饱和。

## Approach
- 核心机制很简单：新能力出现后，用户会快速、大规模地尝试新用法，形成作者借用韧性工程术语所说的 **florescence**（繁盛式扩张）。
- 这种扩张会让服务负载以提供方事先难以预测的方式激增，进而触发 **saturation**（饱和/过载），导致服务中断或性能下降。
- 作者通过 OpenAI 与 Anthropic 公开状态页上的可用性数据，作为对“可靠性不佳”这一现象的直接信号。
- 文章提出的改进方向不是单纯继续扩容，而是提升过载恢复能力，例如资源重分配、load shedding（负载削减）和 graceful degradation（优雅降级）。

## Results
- 文中给出的直接证据是状态页可用性数据：除 Sora 外，两家公司服务**都未达到 99.9% uptime**（three nines）。
- **ChatGPT uptime 为 98.86%**，作者指出这甚至**没有达到 99%**。
- 文章没有提供受控实验、基准测试或论文式定量对比结果，因此**没有严格的实证性能提升数字**。
- 最强的具体主张是：当前可靠性问题更像是“**grow fast and overload things**”而非“move fast and break things”；随着经验积累，厂商可能会在过载恢复、资源调度和优雅降级方面逐步改进。

## Link
- [https://surfingcomplexity.blog/2026/03/07/grow-fast-and-overload-things/](https://surfingcomplexity.blog/2026/03/07/grow-fast-and-overload-things/)
