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
language_code: en
pass_output_id: 82
pass_kind: trend_synthesis
---

# Coding-agent research now lives or dies by executable proof and control layers

## Overview
This week’s coding-agent research is strongest where claims end in a checkable artifact. The center of gravity is executable proof, repository-grounded reasoning, and explicit control layers around search, tools, and evaluation. Compared with the prior two weeks in the local history, the brief is more concrete about how those controls are implemented inside the workflow, not just why they matter.

## Clusters

### Executable proof is the main bar
A weekly pattern is clear: coding-agent papers now treat execution, replay, and verified outputs as the basic proof that work was done. The day-level trend on Apr 13 centers on sandbox execution, reproducible analysis, and proof-of-concept reruns. By Apr 19, that same standard shows up in finer checks on whether an edit was precise and whether a patch matched a verified requirement. The practical consequence is simple. A passing artifact matters more than a fluent trace.

#### Evidence
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md)
- [Certified Program Synthesis with a Multi-Modal Verifier](../Inbox/2026-04-17--certified-program-synthesis-with-a-multi-modal-verifier.md)
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md)
- [CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation](../Inbox/2026-04-14--codespecbench-benchmarking-llms-for-executable-behavioral-specification-generation.md)
- [Terminal Wrench: A Dataset of 331 Reward-Hackable Environments and 3,632 Exploit Trajectories](../Inbox/2026-04-19--terminal-wrench-a-dataset-of-331-reward-hackable-environments-and-3632-exploit-trajectories.md)
- [V2E: Validating Smart Contract Vulnerabilities through Profit-driven Exploit Generation and Execution](../Inbox/2026-04-15--v2e-validating-smart-contract-vulnerabilities-through-profit-driven-exploit-generation-and-execution.md)

### Repository-grounded reasoning gets more explicit
Repository reality remains a hard constraint. The Apr 14 trend says semantic understanding, repository context, and team coordination still limit agents in real codebases. Later in the week, papers add stricter intermediate checks before retrieval or autonomous action, such as structural queries over code facts, requirement alignment, and rule enforcement tied to plan steps. This work tightens the path between task intent and repository evidence.

#### Evidence
- [Neurosymbolic Repo-level Code Localization](../Inbox/2026-04-17--neurosymbolic-repo-level-code-localization.md)
- [Agentic Frameworks for Reasoning Tasks: An Empirical Study](../Inbox/2026-04-17--agentic-frameworks-for-reasoning-tasks-an-empirical-study.md)
- [CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation](../Inbox/2026-04-14--codespecbench-benchmarking-llms-for-executable-behavioral-specification-generation.md)
- [Beyond Output Correctness: Benchmarking and Evaluating Large Language Model Reasoning in Coding Tasks](../Inbox/2026-04-14--beyond-output-correctness-benchmarking-and-evaluating-large-language-model-reasoning-in-coding-tasks.md)
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md)
- [Governing Reflective Human-AI Collaboration: A Framework for Epistemic Scaffolding and Traceable Reasoning](../Inbox/2026-04-16--governing-reflective-human-ai-collaboration-a-framework-for-epistemic-scaffolding-and-traceable-reasoning.md)

### Agent control layers become engineering work
Control layers around agents are getting more concrete. Across Apr 15 to Apr 18, the trend documents describe better results when systems filter context, prune weak trajectories early, compress reusable evidence, and specify operating rules around the model. The recurring gain is not just higher task success. Papers also report better cost, latency, auditability, and operational trust. This makes the agent stack look more like managed software infrastructure than a single model call.

#### Evidence
- [Beyond Task Success: An Evidence-Synthesis Framework for Evaluating, Governing, and Orchestrating Agentic AI](../Inbox/2026-04-18--beyond-task-success-an-evidence-synthesis-framework-for-evaluating-governing-and-orchestrating-agentic-ai.md)
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md)
- [SWE-AGILE: A Software Agent Framework for Efficiently Managing Dynamic Reasoning Context](../Inbox/2026-04-13--swe-agile-a-software-agent-framework-for-efficiently-managing-dynamic-reasoning-context.md)
- [OpenAI Says Codex Agents Are Running Its Data Platform Autonomously](../Inbox/2026-04-17--openai-says-codex-agents-are-running-its-data-platform-autonomously.md)
- [Context Kubernetes: Declarative Orchestration of Enterprise Knowledge for Agentic AI Systems](../Inbox/2026-04-13--context-kubernetes-declarative-orchestration-of-enterprise-knowledge-for-agentic-ai-systems.md)
- [Agentic Frameworks for Reasoning Tasks: An Empirical Study](../Inbox/2026-04-17--agentic-frameworks-for-reasoning-tasks-an-empirical-study.md)
