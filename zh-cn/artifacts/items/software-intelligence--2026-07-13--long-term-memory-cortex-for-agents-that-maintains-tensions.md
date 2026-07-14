---
source: hn
url: https://github.com/mavaali/daftari
published_at: '2026-07-13T23:51:16'
authors:
- mavaali
topics:
- agent-memory
- llm-agents
- knowledge-provenance
- multi-agent-systems
- human-ai-interaction
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Long term memory cortex for agents that maintains tensions

## Summary
## 总结
Daftari 是一个面向 LLM 智能体的本地、可移植记忆系统。它以带有来源信息、版本历史、替代链接和未解决矛盾的结构化 Markdown 记录保存信息。系统的核心规则是：记忆库只能依据已记录的证据解决声明；智能体可以提出修改，但最终判断权仍由人保留。

## 问题
- LLM 智能体会在会话之间丢失上下文，而由服务商管理的记忆会把长期记录绑定到模型供应商。
- 检索可能用过时或相互冲突的片段重新拼出答案，却无法说明哪些来源是最新的、有依据的或存在争议的。
- 智能体可能直接依据存储的信息采取行动，无法独立核查，因此需要可靠的记忆。

## 方法
- 将文档以带 YAML frontmatter 的 Markdown 保存到本地 Git 记忆库中，使其可读、可搜索，并能在不同模型和工具之间移植。
- 通过 27 个 MCP 工具提供记忆库接口，支持读取、搜索、写入、来源凭证、矛盾跟踪、边管理、暂存操作和人工确认。
- 将矛盾保留为张力，只有在真实的证据边指向较新来源时才允许替代；整理功能会报告问题，但不会自动修复。
- 生成确定性的凭证，其中包含来源状态、置信度、来源信息、新鲜度、内容哈希、替代解析结果、未解决的张力，以及作为答案时间锚点的 Git 修订版本。
- 增加面向特定领域的整理、审计、休眠、法庭、见证和截至日期命令，用于处理过时文档队列、矛盾审查、贡献者历史记录、跨仓库链接失效，以及历史信念状态检查。

## 结果
- 实现提供 27 个 MCP 工具，并支持在 Claude Desktop、Claude Code 和智能体 SDK 中本地使用；默认配置不会发起网络请求。
- 一项一致性审计示例扫描了 2 个仓库和 47 个文档，发现 2 个失效的跨仓库引用、3 个直接过时的文档，以及 5 个传递性过时的文档。
- 见证评分规则为高风险写入分配 3 分，中风险写入分配 1 分，低风险写入分配 0 分；被裁决纠正的声明会失去其风险分值，而在完整 TTL 周期内保持有效的声明会获得积分。
- 系统可以导入现有的 Obsidian 或 Markdown 记忆库而不复制内容，也可以通过 Google 的 OKF 格式进行导出和往返转换，同时保留基于 Git 的历史视图和影响范围报告。
- 所提供的文本没有报告正式基准结果、准确率、延迟测量或与其他记忆系统的比较；其最有力的证据是已实现的功能范围和确定性的审计示例。

## Problem

## Approach

## Results

## Link
- [https://github.com/mavaali/daftari](https://github.com/mavaali/daftari)
