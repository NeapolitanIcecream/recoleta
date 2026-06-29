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
SAGA 在 GPU 集群上把整个 AI 智能体任务作为一个调度单元，而不是把每次 LLM 调用单独调度。它的主要收益来自在工具调用间保留可复用的 KV cache，并把后续步骤路由回同一个 worker。

## 问题
- 智能体任务通常会进行 10 到 100 次串联的 LLM 调用，中间夹着工具调用；按请求级别调度的 GPU 调度器会丢弃会话状态，并把端到端延迟提高 3 到 8 倍。
- 在一项 32-GPU 的 SWE-bench 测量中，使用 vLLM v0.6.0 时，38% 的执行时间花在 KV cache 重建上，GPU 平均内存使用率为 42%，端到端延迟是仅推理基线的 6.0 倍。
- 这对代码智能体、浏览器智能体和其他交互式智能体很重要，因为用户可见的指标是跨所有步骤的完整任务完成时间。

## 方法
- SAGA 把智能体工作流当作可调度单元，因此调度器会跟踪整个任务在推理、工具调用和后续 LLM 调用中的状态。
- Agent Execution Graphs 记录预期的步骤结构，并帮助预测会话的 KV cache 在工具调用后是否会被复用。
- 面向工作流的 LRU 加 TTL 在空闲的工具调用期间把高价值 KV cache 保留在 GPU 内存中，并在内存压力下优先逐出价值较低的 cache。
- Session-affinity batching 会把相关请求路由到同一个 worker 以复用 cache，而随机 work stealing 会在负载失衡时迁移工作。
- Agent Fair Share 按预期任务完成时间为租户排队，并带有有界偏差的公平性保证。

## 结果
- 在 64 张 A100 GPU 上，SAGA 相比带 Automatic Prefix Caching 的 vLLM v0.15.1，把 SWE-bench 的任务完成时间降低了 1.73x ± 0.11，把 WebArena 的任务完成时间降低了 1.55x ± 0.09；几何平均值为 1.64x，p < 0.001。
- 相比没有工作流感知的系统，报告的任务完成时间提升达到 3.01x。
- 在生产智能体轨迹上，它的工作流感知逐出策略与 Bélády 的最优离线缓存策略相差 1.31x 以内。
- GPU 内存利用率提升了 1.22x ± 0.05；摘录中还报告，在 SWE-bench 测量里，SAGA 的利用率为 71%，vLLM 为 42%。
- 在多租户干扰下，SAGA 达到 99.2% 的 SLO 达成率。
- 这种延迟收益以吞吐为代价：峰值吞吐量比吞吐最优的批处理调度低约 30%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00528v1](https://arxiv.org/abs/2605.00528v1)
