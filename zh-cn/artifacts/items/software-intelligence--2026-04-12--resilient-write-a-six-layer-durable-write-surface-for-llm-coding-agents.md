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
Resilient Write 是一个 MCP 服务器，用来降低 LLM 编码代理在写文件时发生内容丢失、损坏或盲目重试的概率。它在写入路径周围加入了六层彼此独立的保护，并且相对朴素基线和部分防御性基线取得了明显改进。

## 问题
- LLM 编码代理通过 MCP 这类工具写入文件，但当内容过滤器拦截载荷、大输出被截断，或会话在写入过程中中断时，写入可能失败，而且没有机器可读的信号。
- 发生这类情况后，代理可能丢失草稿、反复执行同一次写入、浪费 token，并且无法恢复，因为返回的错误只是纯文本，或者根本没有错误信息。
- 这对自主编码循环很重要，因为文件修改是编辑、测试、提交工作流中的核心步骤，脆弱的写入路径会让整个任务失败。

## 方法
- 该系统在代理与文件系统之间插入了一个六层写入表面：预检风险评分、原子事务写入、可恢复分块、类型化 JSON 错误、带外草稿存储，以及跨会话交接文件。
- 风险评分用确定性的正则规则和大小规则扫描草稿内容，标记可能触发主机侧内容过滤器的模式。它返回 `[0,1]` 范围内的分数、判定结果（`safe`、`low`、`medium`、`high`）、命中的模式族以及建议操作。
- 安全写入使用临时文件、`fsync`、回读 SHA-256 校验和原子重命名。可选的 `expected_prev_sha256` 会加入乐观并发检查，使过期写入能够明确失败。
- 大型写入会被拆分为带编号的分块，先持久化存储，只有当分块索引连续且与预期数量一致时才会在后续阶段组装。
- 失败会返回带类型的封装对象，其中包含 `error`、`reason_hint`、`detected_patterns`、`suggested_action` 和 `retry_budget` 等字段，这样代理可以改变策略，而不是重复尝试同一个被拦截的写入。

## 结果
- 该实现提供了 16 个 MCP 工具，并通过一个 186 项测试套件完成验证，覆盖全部六层以及扩展功能；细分为风险评分 28 项测试、安全写入与日志记录 17 项、分块 27 项、错误处理 27 项、草稿区 21 项、交接 8 项、扩展 42 项，以及服务器/基础设施 16 项。
- 在复现的案例研究中，写入尝试次数从 6 次降到 2 次。原始运行中内容丢失、没有结构化错误、没有自我纠正，并且需要人工干预；使用 Resilient Write 的运行中没有内容丢失、返回了结构化错误、实现了自我纠正，也不需要人工干预。
- 在量化对比中，恢复时间从朴素基线的 10.0 s 和防御性基线的 5.5 s 降到 Resilient Write 的 2.0 s。
- 估计的数据丢失概率从 5.0%（朴素）和 1.0%（防御性）降到 Resilient Write 的 0.1%。
- 估计的自我纠正率从 5%（朴素）和 15%（防御性）升到 Resilient Write 的 65%，论文将其表述为相对朴素基线提升 13 倍。
- 估计的无效调用比例从 25%（朴素）和 12.5%（防御性）降到 Resilient Write 的 3.0%。论文还声称，与朴素基线相比，恢复时间减少 5 倍，数据丢失概率减少 50 倍。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10842v2](http://arxiv.org/abs/2604.10842v2)
