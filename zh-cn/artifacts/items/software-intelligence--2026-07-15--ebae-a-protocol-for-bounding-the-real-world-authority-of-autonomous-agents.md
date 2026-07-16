---
source: hn
url: https://zenodo.org/records/21385239
published_at: '2026-07-15T23:26:46'
authors:
- Akumaskills
topics:
- autonomous-agents
- agent-security
- access-control
- attested-execution
- cryptographic-protocols
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# EBAE: A protocol for bounding the real-world authority of autonomous agents

## Summary
## 摘要
EBAE 是一种通过将行动提议与受保护执行分离，来限制自主代理现实世界权限的协议。只有当行动意图、授权、策略状态、新鲜度和防回滚状态在同一纪元内保持一致时，系统才会释放该行动。

## 问题
- 自主代理可能提出看似有效的行动，同时拥有过多权限，能够直接执行这些行动。
- 如果不将授权绑定到特定行动和当前安全状态，系统可能允许重放、过时或已回滚的命令。
- 摘录未提供实验历史或基准测试结果，因此该协议在实践中的有效性仍未量化。

## 方法
- 将提出行动的代理与能够释放行动的受保护执行器分离。
- 将权限组织为多个纪元，为有效授权划定有界的时间段。
- 要求活动清单、针对确切意图的一次性证书、加密配置、策略、新鲜度状态和防回滚状态均与同一纪元及同一行动匹配。
- 将这种一致性表示为 Authorization Closure Digest；工作参考实现旨在拒绝不满足闭合条件的行动。

## 结果
- 论文报告了一个工作参考实现，但所提供的摘录不包含定量评估、数据集、延迟测量或基线比较。
- 最明确的具体主张是：除非所有必需的授权输入都对同一行动和同一纪元达成一致，否则执行会被阻止。
- 该记录将这项工作标为 July 16, 2026 的 v1 预印本；摘录在此之前被截断，因此无法评估该实现阻止重放的详细结果。

## Problem

## Approach

## Results

## Link
- [https://zenodo.org/records/21385239](https://zenodo.org/records/21385239)
