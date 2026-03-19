---
source: hn
url: https://gimletlabs.ai/blog/sram-centric-chips
published_at: '2026-03-09T23:10:19'
authors:
- gmays
topics:
- ai-inference
- sram-centric-accelerators
- memory-hierarchy
- llm-decode
- heterogeneous-serving
relevance_score: 0.12
run_id: materialize-outputs
language_code: zh-CN
---

# The emerging role of SRAM-centric chips in AI inference

## Summary
这是一篇面向产业与系统设计的分析文章，讨论为何以 SRAM 为中心的 AI 推理芯片会在大模型推理中变得重要。核心观点是：真正的关键不只是 SRAM 对 HBM，而是“近计算内存 vs 远计算内存”的架构取舍，不同推理阶段应匹配不同硬件。

## Problem
- 文章要解决的问题是：**什么样的 AI 推理工作负载更适合 SRAM-centric 芯片，而不是传统 GPU**，以及这种差异为什么会出现。
- 这很重要，因为 LLM 推理正受到**内存墙**限制，尤其是自回归 **decode** 阶段；文中指出 agentic workloads 产生的 token 量约为传统聊天模型的 **15×**，延迟和吞吐压力都在上升。
- 如果不能理解工作负载的**算术强度（arithmetic intensity）**与内存位置的关系，就难以在训练、prefill、decode 以及推理分片调度中选对硬件。

## Approach
- 文章用一个简单框架解释问题：比较 **SRAM（片上、低延迟、低容量）** 与 **HBM/DRAM（片外、高容量、较高延迟）** 的物理与系统差异，并强调真正的取舍是**内存离计算有多近**。
- 它将 GPU 视为**分层缓存/远内存计算**架构，把 Cerebras、Groq、d-Matrix 等视为**更扁平的近内存计算**架构；前者依赖缓存和数据重用，后者牺牲部分算力换取更大的片上工作内存与更高带宽。
- 文章提出决定胜负的核心机制是**工作集大小 → 算术强度 → 最佳内存架构**：如果数据重用高、算术强度高，GPU 更优；如果数据重用低、受内存带宽限制，SRAM-centric 更优。
- 在 LLM 推理中，**prefill** 因批量处理许多 token、可摊销权重加载，通常更偏计算密集；**decode** 因逐 token 自回归、反复搬运权重，通常更偏内存密集，因此更适合 SRAM-centric 芯片。
- 基于这一点，文章主张**异构推理解耦**：把 prefill 放到高算力硬件，把 decode 或 speculative decoder 放到高内存带宽硬件，甚至跨不同厂商加速器切分同一模型执行。

## Results
- 文中给出若干关键硬件数字来支撑分析：**SRAM 读取延迟约 1 ns**，而 **DRAM/HBM 读取约 10–15 ns**，说明片上 SRAM 在访问延迟上显著更快。
- 文章比较了片上 SRAM 容量投入：**NVIDIA H100 约 50 MB SRAM，B200 约 126 MB**；而更激进的 SRAM-centric 设计投入更多片上存储。即便如此，文中也指出 **Cerebras** 这种整片晶圆方案“也只有”约 **44 GB SRAM**，大模型权重仍需跨芯片分布。
- 在产业信号上，文中列举了两个强烈佐证：**NVIDIA 于 2024 年 12 月以 200 亿美元授权 Groq IP**；**Cerebras 宣布 750 MW 的 OpenAI 推理工作负载合作**。这些不是算法 benchmark，但被作者视为 SRAM-centric 架构商业可行性的重大证明点。
- 文中引用 d-Matrix CTO 的行业数据：**计算性能约每两年增长 3×，而内存带宽仅增长 1.6×**，用来说明推理中的内存瓶颈正在加剧。
- 对于应用需求，文章称 **agentic workloads 的 token 需求约为传统 chat 的 15×**，进一步强化了 decode 延迟/吞吐优化的必要性。
- 文章**没有提供自家系统的正式定量 benchmark**（如具体 tokens/s、latency、energy、与 GPU baseline 的直接对比）；最强的定量主张主要来自硬件参数、行业事件与趋势判断，而非论文式实验结果。

## Link
- [https://gimletlabs.ai/blog/sram-centric-chips](https://gimletlabs.ai/blog/sram-centric-chips)
