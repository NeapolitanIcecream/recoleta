---
source: arxiv
url: https://arxiv.org/abs/2605.00528v1
published_at: '2026-05-01T09:05:28'
authors:
- Dongxin Guo
- Jikun Wu
- Siu Ming Yiu
topics:
- agent-inference-serving
- gpu-scheduling
- kv-cache-management
- workflow-scheduling
- llm-serving
- software-agents
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters

## Summary
## 摘要
SAGA 在 GPU 集群上以整个 AI-agent 任务为单位进行调度，不再单独调度每次 LLM 调用。它的主要收益来自在工具调用间隔中保留可复用的 KV cache，并把后续步骤路由回同一 worker。

## 问题
- Agent 任务通常会发起 10-100 次链式 LLM 调用，中间穿插工具调用；按请求级别工作的 GPU 调度器会丢弃会话状态，并把端到端延迟增加 3-8x。
- 在一项使用 vLLM v0.6.0 的 32-GPU SWE-bench 测量中，38% 的执行时间用于重新生成 KV cache，平均 GPU 内存使用率为 42%，端到端延迟是仅推理基线的 6.0x。
- 这会影响 coding agents、browser agents 和其他交互式 agents，因为用户可见的指标是跨所有步骤的完整任务完成时间。

## 方法
- SAGA 将 agent workflow 作为可调度单元，因此调度器会在推理、工具调用和后续 LLM 调用之间跟踪整个任务。
- Agent Execution Graphs 记录预期的步骤结构，并帮助预测某个会话的 KV cache 在工具调用后是否会被复用。
- 带 TTL 的 workflow-aware LRU 会在工具空闲期间把高价值 KV cache 保留在 GPU 内存中，并在内存压力下先驱逐低价值 cache。
- Session-affinity batching 将相关请求路由到同一 worker 以复用 cache；当负载不均时，随机化 work stealing 会迁移任务。
- Agent Fair Share 按预期任务完成时间调度租户，并包含有界偏差的公平性保证。

## 结果
- 在 64 个 A100 GPU 上，相比启用 Automatic Prefix Caching 的 vLLM v0.15.1，SAGA 在 SWE-bench 上将任务完成时间降低了 1.73x ± 0.11，在 WebArena 上降低了 1.55x ± 0.09；几何平均值为 1.64x，p < 0.001。
- 相比没有 workflow awareness 的系统，报告的任务完成改进达到 3.01x。
- 在生产 agent traces 上，它的 workflow-aware eviction 与 Bélády 的最优离线 cache 策略相差在 1.31x 以内。
- GPU 内存利用率提高了 1.22x ± 0.05；摘录还报告，在 SWE-bench 测量中，SAGA 的利用率为 71%，vLLM 为 42%。
- SAGA 在多租户干扰下达到 99.2% 的 SLO attainment。
- 延迟收益有吞吐成本：峰值吞吐量比吞吐最优的批处理调度低约 30%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00528v1](https://arxiv.org/abs/2605.00528v1)
