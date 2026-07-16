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
language_code: en
pass_output_id: 292
pass_kind: trend_synthesis
---

# Coding-agent research is measuring user burden, runtime cost, and tool risk

## Overview
The day’s strongest work treats coding agents as long-running systems that need session-level evaluation. SWE-Together, SWE-INTERACT, and MirrorCode make user feedback, full-program behavior, and compute budget visible in the score.

## Findings

### Interactive coding-agent benchmarks
Two benchmarks put the user back into software-engineering evaluation. SWE-Together rebuilds 109 repository tasks from real user-agent sessions and scores both final code quality and User Correction, a measure of explicit corrections and softer nudges. Claude Opus 4.8 leads its reported runs at 63% pass@1, while the reference patch baseline reaches about 78%.

SWE-INTERACT shows how much harder vague requests and delayed requirements are. On the same underlying tasks, Opus 4.8 drops from 50.7% single-turn resolve to 26.7% in the interactive setting. GPT-5.5 drops from 48.0% to 24.7%, while its per-trial cost rises from $2.78 to $9.84. The failure labels matter: many agents discover most goals, then still lose requirements or introduce implementation bugs.

#### Sources
- [SWE-Together: Evaluating Coding Agents in Interactive User Sessions](../Inbox/2026-06-29--swe-together-evaluating-coding-agents-in-interactive-user-sessions.md): Summary reports the 109-task SWE-Together construction, User Correction metric, model scores, reference baseline, and correlation with capability.
- [SWE-INTERACT: Reimagining SWE Benchmarks as User-Driven Long-Horizon Coding Sessions](../Inbox/2026-06-29--swe-interact-reimagining-swe-benchmarks-as-user-driven-long-horizon-coding-sessions.md): Summary reports SWE-INTERACT task design, single-turn versus multi-turn resolve rates, cost increase, and failure analysis.

### Long-horizon reimplementation and real serving cost
MirrorCode tests whether agents can rebuild command-line programs from behavior alone. The setup gives execute-only access to a target program, documentation, and tests, then checks exact stdout and stderr matches. Claude Opus 4.7 averages a 56% perfect-solve rate across 25 targets, and one run reimplements `gotree`, a roughly 16,000-line Go bioinformatics toolkit, with 2,000 of 2,001 tests passing after 14 hours and $251.

TraceLab supplies the systems side of that ambition. Its trace covers 4,265 Claude Code and Codex sessions with 357,161 large language model (LLM) steps and 432,510 tool calls. The median step reads about 119K prefix tokens and writes 214 output tokens. Prefix reads account for 59.5% of estimated API cost, so cache policy and context reuse are central operating concerns for coding-agent products.

#### Sources
- [MirrorCode: AI can rebuild entire programs from behavior alone](../Inbox/2026-06-29--mirrorcode-ai-can-rebuild-entire-programs-from-behavior-alone.md): Summary reports MirrorCode task setup, model scores, hidden tests, gotree result, and unresolved hard targets.
- [TraceLab: Characterizing Coding Agent Workloads for LLM Serving](../Inbox/2026-06-29--tracelab-characterizing-coding-agent-workloads-for-llm-serving.md): Summary reports TraceLab dataset scale, token shape, prefix-cache behavior, and cost breakdown.

### Tool security and MCP design
Agent safety work focuses on what happens after a model can call tools. The jailbreak essay argues that alignment changes output probabilities without creating hard execution rules, then connects prompt injection to ReAct-style agents where untrusted content and control instructions share a context window. Its examples include tool-using systems that can edit files, run shell commands, or act through account workflows.

trajeckt is a concrete runtime answer for Model Context Protocol (MCP) agents. It installs a sealed commitment graph before execution, checks each tool call against allowed order and data-flow rules, and blocks missing commitments by default. Its smoke test allows `read_database` and `summarize`, then blocks `send_email_external` with HTTP 403 when sensitive data would reach an external sink. A separate MCP pattern study adds design guidance: static tool aggregation can reduce tool-selection accuracy once visible tools grow past roughly 10–15 for Claude Haiku 4.5 and 20–30 for Claude Sonnet 4.

#### Sources
- [The Impossibility of Mitigating AI Jailbreaks](../Inbox/2026-06-29--the-impossibility-of-mitigating-ai-jailbreaks.md): Summary explains the probabilistic jailbreak argument, tool-agent risk, and limits of broad mitigation.
- [Show HN: A Firewall for AI agents with auditing](../Inbox/2026-06-29--show-hn-a-firewall-for-ai-agents-with-auditing.md): Summary reports trajeckt’s sealed graph, taint tracking, default fail-closed behavior, smoke test, and limited evaluation evidence.
- [MCP Server Architecture Patterns for LLM-Integrated Applications](../Inbox/2026-06-29--mcp-server-architecture-patterns-for-llm-integrated-applications.md): Summary reports MCP server patterns, anti-patterns, and the tool-count accuracy study.

### Measured assistance in narrow coding tasks
Several papers narrow the task and measure where extra agent structure helps. In README generation with retrieval-augmented generation (RAG), a single-agent system slightly beats an autonomous multi-agent system on ROUGE-L F1 while using about one seventh of the tokens. Human-written plans produce the best judged documentation, but they also cost more time and tokens.

Education papers add process-level measurements. Clover logs how students accept, ignore, edit, and delete AI code-completion suggestions, then inserts bad suggestions as attention checks. In a 55-student CS1 study, tab-acceptance rate strongly correlates with failed attention checks. PyMETA adds a separate diagnostic benchmark: 48,646 Python submissions with interpreter-derived labels and a 14-class error taxonomy. Together, these items treat code assistance as a behavior to audit, not just an output to score.

#### Sources
- [The Illusion of Agentic Complexity in README.md Generation: Evaluating Single-Agent vs. Multi-Agent RAG Systems](../Inbox/2026-06-29--the-illusion-of-agentic-complexity-in-readme-md-generation-evaluating-single-agent-vs-multi-agent-rag-systems.md): Summary reports the README RAG comparison, token and runtime costs, and Dev-Plan results.
- [To Tab or Not to Tab: Measuring Critical Engagement in AI Code Completion Tools Using Behavioral Signals and Attention Checks](../Inbox/2026-06-29--to-tab-or-not-to-tab-measuring-critical-engagement-in-ai-code-completion-tools-using-behavioral-signals-and-attention-checks.md): Summary reports Clover’s logged behaviors, attention-check design, student study, and correlations.
- [PyMETA: A Benchmark Dataset for Hierarchical Student Code Error Classification with Python-Interpreter-Based Labels](../Inbox/2026-06-29--pymeta-a-benchmark-dataset-for-hierarchical-student-code-error-classification-with-python-interpreter-based-labels.md): Summary reports PyMETA dataset size, taxonomy, evaluated models, and prompted LLM behavior.
