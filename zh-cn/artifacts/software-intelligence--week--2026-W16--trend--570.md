---
kind: trend
trend_doc_id: 570
granularity: week
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-20T00:00:00'
topics:
- coding-agents
- verification
- evaluation
- repositories
- agent-operations
run_id: materialize-outputs
aliases:
- recoleta-trend-570
tags:
- recoleta/trend
- topic/coding-agents
- topic/verification
- topic/evaluation
- topic/repositories
- topic/agent-operations
language_code: zh-CN
---

# 编程代理研究现在取决于可执行证明和控制层

## Overview
本周的编程代理研究里，最扎实的部分是那些最终落到可检查产物上的论断。重点集中在可执行证明、以仓库为依据的推理，以及围绕搜索、工具和评估的显式控制层。和本地历史中的前两周相比，这份简报更具体地说明了这些控制是怎样在工作流内部实现的，而不只是解释它们为什么重要。

## Clusters

### 可执行证明成了主要门槛
一个每周层面的模式已经很清楚：关于编程代理的论文现在把执行、重放和经过验证的输出当作工作已经完成的基本证明。4 月 13 日的日度趋势聚焦于沙箱执行、可复现分析和概念验证重跑。到 4 月 19 日，同样的标准已经体现在更细的检查上，比如一次编辑是否精确、一个补丁是否符合已验证的需求。实际结果很直接：通过的产物比流畅的轨迹更重要。

#### Evidence
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md)
- [Certified Program Synthesis with a Multi-Modal Verifier](../Inbox/2026-04-17--certified-program-synthesis-with-a-multi-modal-verifier.md)
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md)
- [CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation](../Inbox/2026-04-14--codespecbench-benchmarking-llms-for-executable-behavioral-specification-generation.md)
- [Terminal Wrench: A Dataset of 331 Reward-Hackable Environments and 3,632 Exploit Trajectories](../Inbox/2026-04-19--terminal-wrench-a-dataset-of-331-reward-hackable-environments-and-3632-exploit-trajectories.md)
- [V2E: Validating Smart Contract Vulnerabilities through Profit-driven Exploit Generation and Execution](../Inbox/2026-04-15--v2e-validating-smart-contract-vulnerabilities-through-profit-driven-exploit-generation-and-execution.md)

### 以仓库为依据的推理变得更明确
代码仓库的现实仍然是一个硬约束。4 月 14 日的趋势指出，在真实代码库中，语义理解、仓库上下文和团队协作仍然限制着代理。到了本周后半段，论文又在检索或自主行动之前加入了更严格的中间检查，比如基于代码事实的结构化查询、需求对齐，以及与计划步骤绑定的规则执行。这些工作把任务意图和仓库证据之间的路径收紧了。

#### Evidence
- [Neurosymbolic Repo-level Code Localization](../Inbox/2026-04-17--neurosymbolic-repo-level-code-localization.md)
- [Agentic Frameworks for Reasoning Tasks: An Empirical Study](../Inbox/2026-04-17--agentic-frameworks-for-reasoning-tasks-an-empirical-study.md)
- [CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation](../Inbox/2026-04-14--codespecbench-benchmarking-llms-for-executable-behavioral-specification-generation.md)
- [Beyond Output Correctness: Benchmarking and Evaluating Large Language Model Reasoning in Coding Tasks](../Inbox/2026-04-14--beyond-output-correctness-benchmarking-and-evaluating-large-language-model-reasoning-in-coding-tasks.md)
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md)
- [Governing Reflective Human-AI Collaboration: A Framework for Epistemic Scaffolding and Traceable Reasoning](../Inbox/2026-04-16--governing-reflective-human-ai-collaboration-a-framework-for-epistemic-scaffolding-and-traceable-reasoning.md)

### 代理控制层开始成为工程工作
围绕代理的控制层正在变得更具体。4 月 15 日到 4 月 18 日的趋势文档显示，当系统过滤上下文、及早剪掉较弱的轨迹、压缩可复用证据，并在模型周围明确运行规则时，结果会更好。反复出现的收益不只是任务成功率更高。论文也报告了成本、延迟、可审计性和运行信任上的改善。这让代理栈看起来更像受管的软件基础设施，而不是一次单独的模型调用。

#### Evidence
- [Beyond Task Success: An Evidence-Synthesis Framework for Evaluating, Governing, and Orchestrating Agentic AI](../Inbox/2026-04-18--beyond-task-success-an-evidence-synthesis-framework-for-evaluating-governing-and-orchestrating-agentic-ai.md)
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md)
- [SWE-AGILE: A Software Agent Framework for Efficiently Managing Dynamic Reasoning Context](../Inbox/2026-04-13--swe-agile-a-software-agent-framework-for-efficiently-managing-dynamic-reasoning-context.md)
- [OpenAI Says Codex Agents Are Running Its Data Platform Autonomously](../Inbox/2026-04-17--openai-says-codex-agents-are-running-its-data-platform-autonomously.md)
- [Context Kubernetes: Declarative Orchestration of Enterprise Knowledge for Agentic AI Systems](../Inbox/2026-04-13--context-kubernetes-declarative-orchestration-of-enterprise-knowledge-for-agentic-ai-systems.md)
- [Agentic Frameworks for Reasoning Tasks: An Empirical Study](../Inbox/2026-04-17--agentic-frameworks-for-reasoning-tasks-an-empirical-study.md)
