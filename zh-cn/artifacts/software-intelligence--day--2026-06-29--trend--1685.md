---
kind: trend
trend_doc_id: 1685
granularity: day
period_start: '2026-06-29T00:00:00'
period_end: '2026-06-30T00:00:00'
topics:
- coding agents
- interactive benchmarks
- long-horizon coding
- LLM serving
- agent security
- MCP
- software engineering evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-1685
tags:
- recoleta/trend
- topic/coding-agents
- topic/interactive-benchmarks
- topic/long-horizon-coding
- topic/llm-serving
- topic/agent-security
- topic/mcp
- topic/software-engineering-evaluation
language_code: zh-CN
---

# 编码代理研究正在测量用户负担、运行时成本和工具风险

## Overview
当天最强的工作把编码代理视为需要会话级评测的长时间运行系统。SWE-Together、SWE-INTERACT 和 MirrorCode 让用户反馈、完整程序行为和计算预算进入评分。

## Clusters

### 交互式编码代理基准
两个基准把用户重新纳入软件工程评测。SWE-Together 从真实用户-代理会话中重建 109 个仓库任务，同时评分最终代码质量和 User Correction；后者衡量明确纠正和较轻的提示。Claude Opus 4.8 在已报告的运行中以 63% pass@1 领先，而参考补丁基线约为 78%。

SWE-INTERACT 显示，模糊请求和延迟给出的需求会让任务难很多。在相同的底层任务上，Opus 4.8 从单轮 50.7% 的解决率降到交互设置下的 26.7%。GPT-5.5 从 48.0% 降到 24.7%，同时每次试验成本从 $2.78 升到 $9.84。失败标签说明了问题：许多代理找到了大部分目标，之后仍会遗漏需求或引入实现 bug。

#### Evidence
- [SWE-Together: Evaluating Coding Agents in Interactive User Sessions](../Inbox/2026-06-29--swe-together-evaluating-coding-agents-in-interactive-user-sessions.md): 摘要报告了 SWE-Together 的 109 个任务构建、User Correction 指标、模型分数、参考基线，以及该指标与能力的相关性。
- [SWE-INTERACT: Reimagining SWE Benchmarks as User-Driven Long-Horizon Coding Sessions](../Inbox/2026-06-29--swe-interact-reimagining-swe-benchmarks-as-user-driven-long-horizon-coding-sessions.md): 摘要报告了 SWE-INTERACT 的任务设计、单轮与多轮解决率、成本增加，以及失败分析。

### 长周期重实现与真实服务成本
MirrorCode 测试代理能否只根据行为重建命令行程序。该设置向代理提供目标程序、文档和测试的仅执行访问权限，然后检查 stdout 和 stderr 是否完全匹配。Claude Opus 4.7 在 25 个目标上的平均完美解决率为 56%；其中一次运行重写了 `gotree`，这是一个约 16,000 行的 Go 生物信息学工具包，耗时 14 小时、花费 $251，2,001 个测试中通过了 2,000 个。

TraceLab 给出了这一目标的系统侧数据。它的轨迹覆盖 4,265 个 Claude Code 和 Codex 会话，包含 357,161 个大型语言模型（LLM）步骤和 432,510 次工具调用。中位步骤读取约 119K 个前缀 token，并写出 214 个输出 token。前缀读取占估算 API 成本的 59.5%，因此缓存策略和上下文复用是编码代理产品的关键运行问题。

#### Evidence
- [MirrorCode: AI can rebuild entire programs from behavior alone](../Inbox/2026-06-29--mirrorcode-ai-can-rebuild-entire-programs-from-behavior-alone.md): 摘要报告了 MirrorCode 的任务设置、模型分数、隐藏测试、gotree 结果，以及尚未解决的困难目标。
- [TraceLab: Characterizing Coding Agent Workloads for LLM Serving](../Inbox/2026-06-29--tracelab-characterizing-coding-agent-workloads-for-llm-serving.md): 摘要报告了 TraceLab 数据集规模、token 形态、前缀缓存行为，以及成本拆分。

### 工具安全与 MCP 设计
代理安全研究关注模型能够调用工具之后会发生什么。那篇越狱文章认为，对齐会改变输出概率，但不会形成硬性的执行规则；随后它把提示注入与 ReAct 风格代理联系起来，因为不受信内容和控制指令共享同一个上下文窗口。文中的例子包括能够编辑文件、运行 shell 命令，或通过账户工作流执行操作的工具使用系统。

trajeckt 是面向 Model Context Protocol（MCP）代理的具体运行时方案。它在执行前安装一个密封的承诺图，按允许的顺序和数据流规则检查每次工具调用，并默认阻止缺失承诺的调用。它的烟雾测试允许 `read_database` 和 `summarize`，随后在敏感数据会流向外部接收端时，用 HTTP 403 阻止 `send_email_external`。另一项 MCP 模式研究给出设计建议：当可见工具数量超过 Claude Haiku 4.5 的约 10–15 个、Claude Sonnet 4 的 20–30 个后，静态工具聚合可能降低工具选择准确率。

#### Evidence
- [The Impossibility of Mitigating AI Jailbreaks](../Inbox/2026-06-29--the-impossibility-of-mitigating-ai-jailbreaks.md): 摘要解释了越狱的概率论论点、工具代理风险，以及广泛缓解措施的限制。
- [Show HN: A Firewall for AI agents with auditing](../Inbox/2026-06-29--show-hn-a-firewall-for-ai-agents-with-auditing.md): 摘要报告了 trajeckt 的密封图、污点跟踪、默认失败关闭行为、烟雾测试，以及有限的评估证据。
- [MCP Server Architecture Patterns for LLM-Integrated Applications](../Inbox/2026-06-29--mcp-server-architecture-patterns-for-llm-integrated-applications.md): 摘要报告了 MCP 服务器模式、反模式，以及工具数量准确率研究。

### 窄范围编码任务中的可测量辅助
几篇论文收窄任务范围，并测量额外代理结构在哪些地方有用。在使用检索增强生成（RAG）的 README 生成中，单代理系统在 ROUGE-L F1 上略高于自主多代理系统，同时只使用约七分之一的 token。人工编写的计划得到评分最高的文档，但也消耗更多时间和 token。

教育论文加入了过程层面的测量。Clover 记录学生如何接受、忽略、编辑和删除 AI 代码补全建议，然后插入错误建议作为注意力检查。在一项包含 55 名 CS1 学生的研究中，tab 接受率与注意力检查失败高度相关。PyMETA 增加了一个单独的诊断基准：48,646 份 Python 提交，带有解释器生成的标签和 14 类错误分类。合在一起看，这些工作把代码辅助当作需要审计的行为，而不只是需要评分的输出。

#### Evidence
- [The Illusion of Agentic Complexity in README.md Generation: Evaluating Single-Agent vs. Multi-Agent RAG Systems](../Inbox/2026-06-29--the-illusion-of-agentic-complexity-in-readme-md-generation-evaluating-single-agent-vs-multi-agent-rag-systems.md): 摘要报告了 README RAG 对比、token 和运行时成本，以及 Dev-Plan 结果。
- [To Tab or Not to Tab: Measuring Critical Engagement in AI Code Completion Tools Using Behavioral Signals and Attention Checks](../Inbox/2026-06-29--to-tab-or-not-to-tab-measuring-critical-engagement-in-ai-code-completion-tools-using-behavioral-signals-and-attention-checks.md): 摘要报告了 Clover 记录的行为、注意力检查设计、学生研究，以及相关性。
- [PyMETA: A Benchmark Dataset for Hierarchical Student Code Error Classification with Python-Interpreter-Based Labels](../Inbox/2026-06-29--pymeta-a-benchmark-dataset-for-hierarchical-student-code-error-classification-with-python-interpreter-based-labels.md): 摘要报告了 PyMETA 数据集规模、分类体系、已评估模型，以及提示式 LLM 行为。
