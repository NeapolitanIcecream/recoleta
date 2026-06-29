---
kind: trend
trend_doc_id: 1549
granularity: day
period_start: '2026-06-17T00:00:00'
period_end: '2026-06-18T00:00:00'
topics:
- coding agents
- software engineering benchmarks
- security agents
- agent harnesses
- LLM infrastructure
- software architecture
run_id: materialize-outputs
aliases:
- recoleta-trend-1549
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/security-agents
- topic/agent-harnesses
- topic/llm-infrastructure
- topic/software-architecture
language_code: zh-CN
---

# 编码代理正按证据链和运行框架接受评判

## Overview
这一时期把编码代理视为需要可审计任务来源、可执行安全证据和感知运行框架评分的产品。SWE-Future 处理基准污染；Code-Augur 把安全假设记录为断言；Cursor + Claude Fable 5 显示，同一模型在另一种代理运行框架下的得分可能差异很大。

## Clusters

### 面向未来条件的编码基准
SWE-Future 针对一个棘手的基准问题：真实的代码仓库任务往往来自公开 issue 和 pull request，这些内容可能泄漏到训练数据或模型选择流程中。它的做法是只使用快照前证据来预测未来可能出现的仓库工作，再用后续 pull-request 元数据验证这些任务族，最后从通过验证的任务族合成可执行任务。

证据强于单纯的方案设想。在一项覆盖 80 个仓库的回顾性研究中，预测器在 76 个仓库中生成了 260 个任务族。论文报告称，其中 151 个与后续工作形成强匹配或相关匹配，111 个为强匹配。发布的数据集包含 61 个仓库中的 200 个可执行任务，并附有隐藏测试、标准补丁、验证标签、来源信息和执行日志。

#### Evidence
- [SWE-Future: Forecast-Conditioned Data Synthesis for Future-Oriented Software Engineering Agents](../Inbox/2026-06-17--swe-future-forecast-conditioned-data-synthesis-for-future-oriented-software-engineering-agents.md): 摘要给出了基准污染问题、以预测为条件的合成方法、验证设置和主要结果。

### 安全评分取决于代理运行框架
Endor Labs 在 200 项漏洞修复基准上重跑 Claude Fable 5，使运行框架成为明确的评测变量。使用 Cursor 时，同一模型在反作弊和严格测试调整后达到 72.6% FuncPass 和 29.0% SecPass。较早的 Claude Code 运行达到 59.8% FuncPass 和 19.0% SecPass。

安全指标很重要，因为通过功能测试不能证明漏洞已经修复。在 Cursor 独有的安全修复成功案例中，许多补丁对应的另一组运行通过了功能测试，却未通过隐藏安全测试。研究也跟踪了作弊问题：Cursor + Fable 5 有 29 个确认作弊案例，大多归因于记忆或训练召回。

#### Evidence
- [Claude Fable 5: The harness matters more than the model](../Inbox/2026-06-17--claude-fable-5-the-harness-matters-more-than-the-model.md): 摘要报告了 Cursor 与 Claude Code 的比较、FuncPass/SecPass 分数、作弊数量，以及安全完整性发现。

### 用于漏洞检测的可执行假设
Code-Augur 为大语言模型（LLM）安全代理给出了一个具体模式：当代理判断代码安全时，它把理由写成源代码内断言。随后，一个引导式灰盒模糊测试器会尝试推翻该断言。失败的断言会变成漏洞报告，或成为推断规格错误的信号。

报告的结果很具体。论文称，在 DARPA AIxCC 和 OSV 基准来源上，Code-Augur 发现的漏洞多于 Claude Code 和 Atlantis；按不同设置，报告的差距为 34 到 370 个漏洞。它还在开源项目中发现了 22 个新漏洞；截至论文撰写时，开发者已修复或确认其中 16 个。

#### Evidence
- [Code-Augur: Agentic Vulnerability Detection via Specification Inference](../Inbox/2026-06-17--code-augur-agentic-vulnerability-detection-via-specification-inference.md): 摘要涵盖了威胁模型、基于断言的规格推断、模糊测试循环，以及报告的漏洞结果。

### 代理基础设施需要有证据支撑的记忆、反馈和协议
多项内容关注代理周边的支撑层。CAPRA 使用专门代理审查软件架构报告，但它的关键控制是证据锚定：每个问题都需要源文引用、严重性和置信分数，随后用确定性的模糊匹配检查该引用是否存在于文档中。在 10 份评测报告上，CAPRA 在严格聚合下通过了 88.8% 的标准，并在四分多钟内处理完每份报告。

Vlk 用一个 Model Context Protocol 服务器处理长时间编码会话；该服务器把代理记忆存储在 SQLite 中，并允许代理在保存新经验时删除过期条目。证据来自产品摘录，不是基准，因此结论应保持狭窄：它暴露了一个工具 `vlk_time_travel`，并支持 Zed、Cursor 和 Claude Desktop 等客户端。

一篇协议分类论文补充了更宽的基础设施视角。它从对手方、载荷、状态、发现和模式灵活性等维度分析了九个仍在维护的开源代理通信协议。样本显示，代理到代理协议会保留会话状态，多数协议包含多个预定义模式，去中心化发现较少见。

#### Evidence
- [CAPRA: Scaling Feedback on Software Architecture Deliverables with a Multi-Agent LLM System](../Inbox/2026-06-17--capra-scaling-feedback-on-software-architecture-deliverables-with-a-multi-agent-llm-system.md): 摘要报告了 CAPRA 的证据锚定、多代理审查流程、成本/时间和评测结果。
- [Vlk: MemAct for the IDE – persistent working memory agents can prune themselves](../Inbox/2026-06-17--vlk-memact-for-the-ide-persistent-working-memory-agents-can-prune-themselves.md): 摘要描述了 Vlk 的持久化 SQLite 记忆、`vlk_time_travel` 工具、受支持客户端，以及缺少基准证据的情况。
- [A Technical Taxonomy of LLM Agent Communication Protocols](../Inbox/2026-06-17--a-technical-taxonomy-of-llm-agent-communication-protocols.md): 摘要给出了九个代理通信协议的分类维度和发现。
