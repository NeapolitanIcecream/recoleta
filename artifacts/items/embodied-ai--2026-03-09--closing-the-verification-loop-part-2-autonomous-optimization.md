---
source: hn
url: https://www.datadoghq.com/blog/ai/fully-autonomous-optimization/
published_at: '2026-03-09T23:05:28'
authors:
- chrisra
topics:
- autonomous-optimization
- llm-code-evolution
- formal-verification
- wasm-sandbox
- distributed-systems
relevance_score: 0.06
run_id: materialize-outputs
---

# Closing the verification loop, Part 2: autonomous optimization

## Summary
这篇文章提出一个用于分布式时序聚合服务的全自主代码优化系统：LLM 自动生成候选实现，经过形式化验证、影子流量校验和 WASM 沙箱部署后，可在生产中无人工热更新。其核心贡献是把“能否验证”变成闭环，使按租户、按工作负载、实时演化优化代码成为可能。

## Problem
- 要优化的是时序数据库中高频运行的聚合热路径；在数百亿级时间序列与多租户动态负载下，微小低效都会累积成显著成本。
- 传统 JIT/PGO 更擅长微架构层面的局部优化，难以在线发现并安全部署新的算法结构；而以往 LLM 演化又依赖人工挑选目标、评审和发布，速度太慢。
- 关键难点是：如何让 AI 在没有人工介入的情况下，既能大胆搜索更优算法，又能被机器可靠地判错、验真和安全上线。

## Approach
- 采用“两服务器”架构：聚合服务器处理真实流量；演化服务器持续用 LLM 驱动的进化搜索生成优化后的 Rust/WASM 模块。
- 五阶段验证流水线形成闭环：**specialization**（把 org_id 和聚合配置绑定为编译期常量）→ **LLM evolution**（从历史高分候选中进化生成新代码）→ **formal verification**（用 Verus 证明底层 codec 安全性质）→ **shadow evaluation**（对保留验证流量做输出哈希比对）→ **live hot-swap**（通过 WASM 模块零停机替换）。
- 最核心的机制是先把具体租户/查询配置“烘焙”进代码，让编译器和 LLM 都能围绕已知工作负载做专门化重写，再用未见过的真实流量检查结果是否与基线完全一致。
- 安全与隔离依赖 WASM 沙箱、wasmparser 校验、Ed25519 签名，以及 host/guest 的受控接口；模块可在不重启服务的情况下按组织 ID 和聚合配置热切换。
- 作者强调，突破点不只是编译器常规优化，而是 LLM 在验证闭环约束下发现了结构性算法变化，例如把每点遍历全部过滤条件的 **O(N)** 流程改写成初始化建表后每点单次查找的 **O(1)** HashMap 方案。

## Results
- 在一个具体 Unicron 工作负载上（某组织监控 **100** 个服务、每个查询按不同 service name 过滤、做 **SUM**、**30 秒**窗口），基线吞吐为 **7,106 msg/s**。
- 对该工作负载，经过专门化、**3 代**基于 **Claude Opus 4.6** 的演化、保留流量哈希一致性验证后，热更新部署达到 **26,263 msg/s**，相对当前生产通用聚合函数提升 **270%**。
- 在第二个工作负载上（同一指标的 **100** 种不同 group-by tag 组合），相对同一基线的吞吐提升达到 **541%**。
- 论文明确声称这些改进可在**数分钟内**完成验证并自主部署，而不是过去需要人工评审与发布、通常耗时**数小时**的流程。
- 作者还给出定性结论：**specialization** 是最稳定、最大的单项收益来源；LLM 演化则进一步发现传统 JIT/PGO 难以自动得到的算法级重构。

## Link
- [https://www.datadoghq.com/blog/ai/fully-autonomous-optimization/](https://www.datadoghq.com/blog/ai/fully-autonomous-optimization/)
