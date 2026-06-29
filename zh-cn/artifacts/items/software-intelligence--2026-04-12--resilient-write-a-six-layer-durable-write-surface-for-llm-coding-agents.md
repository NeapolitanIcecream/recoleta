---
source: arxiv
url: http://arxiv.org/abs/2604.10842v2
published_at: '2026-04-12T22:23:55'
authors:
- Justice Owusu Agyemang
- Jerry John Kponyo
- Elliot Amponsah
- Godfred Manu Addo Boakye
- Kwame Opuni-Boachie Obour Agyekum
topics:
- llm-coding-agents
- mcp-tools
- durable-file-writes
- code-intelligence
- agent-reliability
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Resilient Write: A Six-Layer Durable Write Surface for LLM Coding Agents

## Summary
## 摘要
Resilient Write 是一个 MCP 服务器，让 LLM 编码代理写文件时更不容易丢失、损坏，或在失败后盲目重试。它在写入路径周围加了六层独立保护，并且相较于朴素基线和部分防御基线，结果提升很大。

## 问题
- LLM 编码代理通过 MCP 这类工具写文件，但当内容过滤器拦截载荷、输出过大被截断，或会话在写入中途停止时，写入可能失败，而且没有机器可读信号。
- 发生这种情况时，代理可能丢掉草稿，重复同一次写入多次，浪费 token，并且因为错误只是普通文本，或者根本没有错误，无法恢复。
- 这对自主编码循环很重要，因为文件修改是编辑-测试-提交工作流里的核心步骤，写入路径一旦脆弱，整个任务都可能中断。

## 方法
- 系统在代理和文件系统之间插入六层写入表面：预飞行风险评分、原子事务写入、可恢复分块、类型化 JSON 错误、带外临时存储，以及跨会话交接文件。
- 风险评分用确定性的正则和大小规则扫描草稿内容，标出可能触发宿主侧内容过滤器的模式。它返回 `[0,1]` 区间内的分数、`safe`、`low`、`medium`、`high` 这类判断、匹配到的模式家族，以及建议动作。
- 安全写入使用临时文件、`fsync`、回读 SHA-256 校验和原子重命名。可选的 `expected_prev_sha256` 会加入乐观并发检查，让过期写入干净地失败。
- 大写入会拆成编号分块，分块会持久保存，之后只有在块索引连续且与预期数量一致时才会重新组合。
- 失败时返回带类型的封装，字段包括 `error`、`reason_hint`、`detected_patterns`、`suggested_action` 和 `retry_budget`，这样代理可以改策略，而不是反复重试同一次被阻止的写入。

## 结果
- 该实现提供 16 个 MCP 工具，并由一个 186 项测试套件验证，覆盖全部六层以及扩展功能；其中风险评分 28 项，安全写入和日志记录 17 项，分块 27 项，错误处理 27 项，临时草稿存储 21 项，交接 8 项，扩展 42 项，服务器和基础设施 16 项。
- 在复现实例研究中，写入尝试次数从 6 次降到 2 次。原始运行丢失了内容，没有结构化错误，没有自我修正，需要人工干预；Resilient Write 的运行没有丢失内容，返回了结构化错误，完成了自我修正，也不需要人工干预。
- 在定量比较中，恢复时间从朴素基线的 10.0 秒和防御基线的 5.5 秒降到 Resilient Write 的 2.0 秒。
- 估计的数据丢失概率从朴素基线的 5.0% 和防御基线的 1.0% 降到 Resilient Write 的 0.1%。
- 估计的自我修正率从朴素基线的 5% 和防御基线的 15% 升到 Resilient Write 的 65%，论文把这写成相对朴素基线提升 13 倍。
- 估计的浪费调用比例从朴素基线的 25% 和防御基线的 12.5% 降到 Resilient Write 的 3.0%。论文还声称，相比朴素方案，恢复时间减少 5 倍，数据丢失概率减少 50 倍。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10842v2](http://arxiv.org/abs/2604.10842v2)
