---
source: hn
url: https://github.com/sbw70/verification-constraints/blob/main/modules/integrated-constraint-demos/two-region-quorum-byzantize-drift/README.md
published_at: '2026-03-04T23:34:26'
authors:
- sbw70
topics:
- byzantine-fault-tolerance
- quorum-audit
- multi-region-failover
- distributed-systems
- observability
relevance_score: 0.63
run_id: materialize-outputs
---

# Show HN: One provider starts lying at request 50. The quorum catches it

## Summary
这是一项可重放的分布式演示：在双地域、双中继 hub、三提供方架构下，故意让一个提供方在后期开始“撒谎”，并用 2-of-3 法定人数审计检测报告漂移。它强调**权威只在 provider**，而前置入口和 hub 只做机械转发与可观测性收集。

## Problem
- 解决的问题是：当多副本/多提供方系统里某个副本开始产生**拜占庭式漂移**（内部真实执行逻辑不变，但对外回报结果开始不一致）时，如何在**不把决策权上移到网关或中继**的前提下发现异常。
- 这很重要，因为跨区域容灾、模型/服务多提供方接入、以及中立前置层常常需要保持统一请求接口；如果观测层和执行权边界混淆，系统会更难审计、更难隔离失效责任。
- 该演示还关注故障切换场景：请求在 `FAILOVER_AT` 前发往 Region 1，之后切到 Region 2，同时保持请求端恒定的 HTTP 204 接口语义。

## Approach
- 架构上每个地域包含一个 **NUVL front**、两个对等 relay hub、三个 provider。NUVL 只接收请求、计算 `SHA-256(request_bytes)` 和 `binding`，然后转发 artifact；hub 只做 peer relay、fanout 和 `/outcome` 收集，不做授权、共识或阈值判定。
- 真正的“是否发起执行”仅由 provider 独立决定：provider 检查 `binding_ok`、域阈值，并在内部生成 provider-boundary artifact；因此 authority location 被明确限制在 provider 边界。
- 为模拟拜占庭行为，在确定的 `byz_start` 之后，`Provider_B` 将约 **50%** 的 `initiated_reported` 结果翻转，但内部“真实” initiation 逻辑保持不变。这样建模的是**报告层漂移**而非执行层全面损坏。
- 审计层对 provider 回报做 **2-of-3 quorum** 聚合，仅用于可观测性，不作为授权输入；因此可以检测报告分歧，同时不让 hub 变成裁决者。
- 整个运行是**确定性可回放**的：请求序列、域选择、payload 构造以及拜占庭起点都由种子和序号确定，便于比较 failover 前后与不同运行之间的漂移事件。

## Results
- 演示声明的核心结果是：当某提供方在大约第 **50** 个请求后开始对约 **50%** 的结果撒谎时，**2-of-3 quorum 审计能够捕获该漂移**，即使 hub 和前置入口都不拥有决策权。
- 默认配置下，`TOTAL_REQUESTS = 100`，`FAILOVER_AT = TOTAL_REQUESTS // 2 = 50`，`QUORUM_THRESHOLD = 2`；系统在请求前 **50** 次走 Region 1、后 **50** 次走 Region 2，以展示双地域 failover 下的统一接口与可观测性。
- 输出指标包括：HTTP **204** 成功/错误计数、总耗时、平均每请求耗时、quorum 审计成功/失败总数、以及按 domain 统计的成功/失败数；这些被明确标注为**观测指标而非授权结果**。
- 文本没有给出具体实验表格、准确率、延迟数值或与其他系统/基线的定量对比，因此**没有可提取的正式 benchmark 数字**。
- 最强的具体主张是：在**双地域 + 双 hub mesh + 三 provider** 拓扑中，能够同时展示客户端侧 failover、provider-only authority、以及对抗性副本报告漂移的可重放检测。

## Link
- [https://github.com/sbw70/verification-constraints/blob/main/modules/integrated-constraint-demos/two-region-quorum-byzantize-drift/README.md](https://github.com/sbw70/verification-constraints/blob/main/modules/integrated-constraint-demos/two-region-quorum-byzantize-drift/README.md)
