---
source: hn
url: https://inferencebench.ai/
published_at: '2026-05-20T23:37:29'
authors:
- matt_d
topics:
- ai-agents
- llm-inference
- benchmarking
- code-intelligence
- software-optimization
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# InferenceBench: A Benchmark for Open-Ended Inference Optimization by AI Agents

## Summary
## 总结
InferenceBench 测试前沿编码代理能否在固定算力预算下优化 LLM 推理服务器。主要发现是，代理可以胜过原始 PyTorch 和许多默认推理引擎设置，但仍然输给对现有引擎做简单超参数搜索的方法。

## 问题
- LLM 服务速度取决于许多运行时选择，包括批处理、前缀缓存、KV cache 设置和引擎标志。
- 代理常常知道正确的优化思路，但它们没法稳定地做干净的对照实验、保留最佳配置，或提交有效的最终服务器。
- 这对自动化软件研发很重要，因为有用的代理必须改进系统，并在正确性和完整性检查下保住这种改进。

## 方法
- 每次运行都会给代理一个基础模型、硬件环境和 2 小时的墙钟时间预算。
- 代理必须构建一个兼容 OpenAI 的推理服务器，并让它相对 PyTorch 基线实现最高加速。
- 基准覆盖 4 个场景：prefill 延迟、长文本生成、并发流量，以及平衡服务。
- 最终提交必须通过正确性检查和完整性审计。失败、无法访问、存在 reward hacking，或性能回退的服务器都会拿到 PyTorch 基线分数。
- 评分使用几何平均加速，并与 PyTorch、默认 vLLM、SGLang、TGI，以及匹配的超参数搜索基线进行比较。

## 结果
- 在全部 4 个场景中，代理都胜过原始 PyTorch 基线和大多数默认推理引擎，包括默认 vLLM、SGLang 和 TGI。
- 在相同时间预算下，代理仍然不如对现有引擎设置做简单超参数搜索。摘录里没有给出精确加速值。
- Sonnet 4.6 排在榜首，因为它把有竞争力的单场景加速和更可靠的有效最终提交结合了起来。
- 基准报告了 180 次运行。在这些运行里，代理常常能在对话记录中识别出相关优化，但无法验证、确认或保留它们。
- 93.9% 的运行提交了基于 vLLM 的服务器。
- 一条轨迹报告了一个有效的基线服务器，其生成吞吐量为 63.53 tokens/s，TTFT p50 为 51.8 ms，TTFT p90 为 400 ms，ITL p50 为 10.2 ms，TPOT p50 为 15.7 ms。

## Problem

## Approach

## Results

## Link
- [https://inferencebench.ai/](https://inferencebench.ai/)
