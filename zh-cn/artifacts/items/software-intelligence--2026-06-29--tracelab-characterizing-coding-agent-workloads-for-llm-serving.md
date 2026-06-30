---
source: arxiv
url: https://arxiv.org/abs/2606.30560v1
published_at: '2026-06-29T16:59:05'
authors:
- Kan Zhu
- Mathew Jacob
- Chenxi Ma
- Yi Pan
- Stephanie Wang
- Arvind Krishnamurthy
- Baris Kasikci
topics:
- coding-agents
- llm-serving
- workload-traces
- kv-cache
- tool-calling
- code-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# TraceLab: Characterizing Coding Agent Workloads for LLM Serving

## Summary
## 摘要
TraceLab 发布并分析了一份用于 LLM 服务的真实编码代理轨迹：来自 Claude Code 和 Codex 的 4,265 个会话、357,161 个 LLM 步骤和 432,510 次工具调用。论文认为，编码代理服务成本主要来自反复读取长上下文、自主工具循环和前缀缓存未命中。

## 问题
- 公开 LLM 服务轨迹和编码基准没有覆盖持久会话、工具调用、长上下文和由人类节奏造成的间隔中的日常编码代理行为。
- SWE-bench 和 Terminal-Bench 衡量隔离任务上的任务成功率，因此无法显示会话如何增长，也无法显示服务系统如何消耗时间和 token。
- 这一点会影响 KV 缓存策略、预填充路由、工具运行时设计和延迟目标，因为这些都依赖真实流量模式。

## 方法
- 作者收集了 43 名开发者在大约八个月内使用 Claude Code 和 Codex 产生的默认本地日志。
- 他们将不同提供商的日志规范化为步骤级 schema，其中每一行覆盖一次 LLM 调用及其工具调用。
- 他们将输入 token 拆分为前缀 token、追加 token 和输出 token，然后分析成本、延迟、上下文增长、压缩、工具使用和缓存行为。
- 他们通过替换标识符并删除原始用户文本和工具 I/O 来匿名化轨迹，同时保留时间戳、token 数、工具类型和假名化用户。
- 他们发布了数据集、采集流水线和分析代码。

## 结果
- 数据集规模：4,265 个会话、43 名用户、23 个模型版本、357,161 个 LLM 步骤、432,510 次工具调用、54.90B 个总输入 token 和 186.9M 个输出 token。
- 代理循环很长：一个会话平均有 9.2 个请求、82.5 个步骤和 101.4 次工具调用；一个请求平均有 8.8 次 LLM 调用和 10.8 次工具调用。
- token 形态偏向长读取和短生成：中位数步骤约有 119K 个前缀 token、875 个追加 token 和 214 个输出 token。
- 成本由前缀读取驱动：前缀 token 在 54.90B 个输入 token 中占 52.56B 个，并占估算 API 成本的 59.5%；相比之下，追加 token 占 29.2%，输出 token 占 11.2%。
- 前缀缓存有帮助，但未命中仍会造成损失：全局前缀缓存命中率为 95.7%，而缓存未命中导致的预填充量是真正新输入 token 的 3.8 倍。
- 工具行为分布偏斜：出现了 80 多种工具类型，每个提供商的前 3 个工具占工具调用的 80% 以上，超过 1 分钟的工具调用占调用数的 4%，但占总工具调用时间的 85%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.30560v1](https://arxiv.org/abs/2606.30560v1)
