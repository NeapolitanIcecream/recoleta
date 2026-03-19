---
source: hn
url: https://github.com/sbw70/verification-constraints/blob/main/modules/integrated-constraint-demos/two-region-quorum-byzantize-drift/README.md
published_at: '2026-03-04T23:34:26'
authors:
- sbw70
topics:
- distributed-systems
- byzantine-faults
- quorum-audit
- failover
- observability
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: One provider starts lying at request 50. The quorum catches it

## Summary
这是一个可重放的分布式演示系统：两个区域、每区双 hub 中继、三家 provider 独立执行，通过 2-of-3 法定人数审计来检测某个 provider 在第约 50 个请求后开始“撒谎”的报告漂移。其核心价值在于展示：即使发生区域切换和拜占庭式报告偏移，也能在不把决策权交给 hub 的前提下观测到异常。

## Problem
- 要解决的问题是：在多 provider、多区域的执行拓扑中，如何在**不让中间层获得执行权或裁决权**的情况下，发现某个 provider 的输出报告开始偏离真实内部执行逻辑。
- 这很重要，因为实际系统会遇到区域故障切换、复制体漂移、恶意或失真的状态上报；如果观测层无法发现这些不一致，审计与可靠性都会失效。
- 文中还强调 authority placement：不能因为要做审计/法定人数统计，就把授权或共识职责错误地下放给 hub。

## Approach
- 设计了两个区域（R1/R2），每个区域包含一个 NUVL 前端、两个仅做机械转发的 hub（A↔B mesh）、以及三个真正有执行权的 providers（A/B/C）。
- 请求先发往 Region 1，达到 `FAILOVER_AT` 后切到 Region 2；对客户端始终返回固定 `HTTP 204`，从而把“接入路径可用性”和“执行结果语义”分离。
- NUVL 只做三件事：接收 opaque bytes、计算 `SHA-256(request_bytes)` 得到 `request_repr`、再生成 `binding = nuvl_bind(...)` 并转发；它**不持有密钥、不决定 initiation、不解释 outcome**。
- Providers 独立评估 `binding_ok` 和 domain threshold，并且**只有 provider 能 initiate**；hub 只负责 relay/fanout 和接收 `/outcome` 观测信号，不参与授权、阈值判断或共识。
- 注入一个确定性的拜占庭漂移：在 `byz_start` 之后，`Provider_B` 将约 **50%** 的 `initiated_reported` 翻转，但其“真实”内部 initiation 逻辑仍保持不变；再用 **2-of-3 quorum audit** 对 provider 报告做观测聚合，以检测分歧。

## Results
- 演示声称成功覆盖了 **2 个区域**、每区 **2 个 hub**、每区 **3 个 providers** 的拓扑，并在默认 **`TOTAL_REQUESTS=100`**、默认 **`FAILOVER_AT=50`**、默认 **`QUORUM_THRESHOLD=2`** 的设置下运行。
- 关键突破性主张是：一个 provider 在计算出的 `byz_start`（标题示例指向约第 **50** 个请求）之后开始对约 **50%** 的 outcome 报告撒谎时，**2-of-3 quorum audit** 仍能在观测层捕捉到 drift，而**不把 authority 移到 hub**。
- 系统还声称能在 failover 前后保持相同请求接口语义：客户端始终命中 `/nuvl` 并收到 **HTTP 204**，region 切换只发生在入口选择层，而下游仍保持 provider-controlled、hub-neutral。
- 完成时会输出可量化观测指标：请求总数、failover 点、`byz_start`、requester HTTP success/error counts、总耗时、平均单请求时延、quorum success/fail 总数、以及 per-domain success/fail 统计。
- 但给定摘录**没有提供具体实验数值**（例如真实成功率、误检率、检测延迟、与无 quorum 基线相比的提升幅度），因此无法报告标准学术意义上的定量 SOTA 或显著优于 baseline 的数字结果。最强的具体结论仍是：在可重放条件下，默认 100 请求、2 区域 failover、单 provider 约 50% 报告翻转的设定中，法定人数审计可以观测到拜占庭式报告漂移。

## Link
- [https://github.com/sbw70/verification-constraints/blob/main/modules/integrated-constraint-demos/two-region-quorum-byzantize-drift/README.md](https://github.com/sbw70/verification-constraints/blob/main/modules/integrated-constraint-demos/two-region-quorum-byzantize-drift/README.md)
