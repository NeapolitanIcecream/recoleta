---
source: arxiv
url: https://arxiv.org/abs/2604.26152v1
published_at: '2026-04-28T22:27:54'
authors:
- Twinkll Sisodia
topics:
- llm-observability
- aiops
- model-monitoring
- inference-tracing
- confidence-calibration
- agent-operations
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# AI Observability for Large Language Model Systems: A Multi-Layer Analysis of Monitoring Approaches from Confidence Calibration to Infrastructure Tracing

## Summary
## 摘要
这篇综述认为，LLM 可观测性需要覆盖五层信号：模型内部状态、置信度、行为、运维和基础设施追踪。它的主要判断是，近期方法大多只在单层内起作用，而生产系统仍缺少跨层关联。

## 问题
- 生产环境中的 LLM 会出现标准服务指标捕捉不到的故障，例如高置信度幻觉、隐藏的推理失败、KV cache 效应、GPU 内存碎片和内核级变慢。
- 现有监控工作按层拆分，团队在事故中很难把模型置信度、chain-of-thought 行为、遥测数据和 GPU 追踪连起来。
- 这个缺口很重要，因为 LLM 系统需要路由、升级处理、诊断和回滚决策，而这些决策要同时用到模型层和基础设施层证据。

## 方法
- 论文把 AI 可观测性整理成五层分类：模型内部状态、置信度与校准、行为监控、运维信号综合和基础设施追踪。
- 它比较了五项 2025-2026 年的研究：MIT 的 RLCR 置信度校准、UC Berkeley 的命题探针内部状态监控、OpenAI 的 chain-of-thought 可监控性研究、AIOpsLab 的云运维代理，以及 TRUFFLD 的非侵入式推理追踪。
- 它还加入了一个实用的第 4 层参考点，即基于目录的自然语言到 PromQL 工作，包括指标查找和运维摘要。
- 它指出了四个未解决的缺口：跨层信号关联、统一评测基准、实时自适应监控，以及考虑成本的监控分配。

## 结果
- MIT RLCR 在 HotpotQA 上把 Expected Calibration Error 从 0.37 降到 0.03，同时保持准确率；在数学基准上，ECE 从 0.26 降到 0.10。论文还报告，RLCR 改善了分布外校准，而标准 RLVR 会让它变差。
- UC Berkeley 的命题探针在只用简单英文模板训练后，Jaccard Index 达到与提示词 skyline 相差不超过 10% 的水平，并且能泛化到短篇故事和西班牙语翻译。
- 这项命题探针研究报告称，在 3 种对抗场景中，它比模型输出更忠实：提示注入、后门攻击和性别偏见。
- OpenAI 的 chain-of-thought 可监控性研究覆盖 3 种原型下的 13 项评测，并使用 g-mean²，定义为 TPR × TNR。综述报告称，更长的 chain-of-thought 轨迹更容易被监控，CoT 监控在几乎所有场景里都优于只看 action 的监控，但摘录里没有给出精确分数。
- 据报告，TRUFFLD 在多节点 Qwen3-8B 推理上实现了接近完美的步骤级异常检测，开销低，而且不需要修改二进制文件。摘录没有给出精确的 F1 或延迟开销数值。
- 这个运维 PromQL 示例报告了亚秒级指标发现、少于 200 ms 的目录查找、约 1.1 s 的端到端延迟，以及约 2,000 个指标的目录。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26152v1](https://arxiv.org/abs/2604.26152v1)
