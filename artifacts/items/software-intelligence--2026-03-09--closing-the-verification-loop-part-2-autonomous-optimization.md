---
source: hn
url: https://www.datadoghq.com/blog/ai/fully-autonomous-optimization/
published_at: '2026-03-09T23:05:28'
authors:
- chrisra
topics:
- llm-code-optimization
- formal-verification
- autonomous-deployment
- wasm-sandbox
- distributed-systems
relevance_score: 0.92
run_id: materialize-outputs
---

# Closing the verification loop, Part 2: autonomous optimization

## Summary
这篇文章提出一个用于分布式时序聚合服务的全自治代码优化系统：LLM 自动生成候选实现，经过形式化验证、影子流量校验和 WASM 沙箱部署后，直接热更新到生产服务中。其目标是在无需人工审核的情况下，为不同租户和工作负载持续生成“可证明正确”的更优代码。

## Problem
- 分布式与高吞吐数据系统中的关键热路径很难既高性能又正确，因为并发、故障、网络非确定性和跨机器不变量会让 bug 难以测试和复现。
- 传统 JIT/PGO 更擅长微架构层面的局部优化，难以自动发现更换数据结构或算法这类“结构性优化”；而早期 LLM 演化方法又需要人工选目标、跑基准、审核和部署，周期通常以小时计。
- 对 Unicron 这类每条消息、每个查询都要执行聚合循环的系统来说，小的低效会在数千亿时间序列规模下放大为显著成本，因此需要按租户、按工作负载、实时优化，同时还必须保证输出不变。

## Approach
- 系统采用“双服务器”架构：聚合服务器处理真实流量；演化服务器持续用 LLM 驱动的进化搜索生成优化后的 Rust/WASM 聚合模块，并可无重启热替换。
- 五阶段闭环：**specialization** 将组织 ID 和聚合配置绑定为编译期常量；**LLM evolution** 在 Git 仓库中程序化探索并生成候选代码；**formal verification** 用 Verus 证明被调用编解码库的安全性质；**shadow evaluation** 在保留验证流量上与基线比对输出哈希；**live hot-swap** 将通过校验的 WASM 模块在线切换。
- 核心机制可简单理解为：先把“这个租户的固定规则”直接写进代码，再让 LLM 反复尝试更好的实现；任何候选只有在“能编译、证明安全、对真实保留流量输出完全一致”时才允许上线。
- 与普通编译优化不同，LLM 可以进行算法级重写。例如把“每个数据点扫描全部过滤条件”的 O(N) 逻辑，改成初始化时构建 HashMap、运行时 O(1) 查找的结构性变换。
- 为保证自治运行的安全性，执行边界由 WASM 沙箱、wasmparser 校验、Ed25519 签名、WIT 接口和 held-out 验证流量共同构成，降低错误代码直接影响宿主进程的风险。

## Results
- 在一个具体工作负载中（某组织监控 100 个服务、每个查询按不同服务名过滤、30 秒 SUM 聚合），基线吞吐量为 **7,106 msg/s**，经过 **3 代**、使用 **Claude Opus 4.6** 演化并通过保留流量哈希校验后，热更新版本达到 **26,263 msg/s**，相对当前生产通用聚合函数提升 **270%**。
- 在第二个工作负载中（同一指标上的 **100** 种不同 group-by tag 组合），相对基线的吞吐提升达到 **541%**。
- 文章声称改进后的聚合算法能够在**几分钟内**完成验证并自治部署到运行中服务，无需人工干预、无需服务重启。
- 定性上，作者指出 **specialization** 是最稳定、最大的单项收益来源；而最关键的突破来自 LLM 发现了传统 JIT/PGO 不易产生的**算法级变化**，例如 O(N) 到 O(1) 的 HashMap 重构。

## Link
- [https://www.datadoghq.com/blog/ai/fully-autonomous-optimization/](https://www.datadoghq.com/blog/ai/fully-autonomous-optimization/)
