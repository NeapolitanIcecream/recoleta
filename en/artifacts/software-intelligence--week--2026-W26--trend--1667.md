---
kind: trend
trend_doc_id: 1667
granularity: week
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-29T00:00:00'
topics:
- coding agents
- agent evaluation
- software engineering
- security
- cost control
- repository context
run_id: materialize-outputs
aliases:
- recoleta-trend-1667
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/software-engineering
- topic/security
- topic/cost-control
- topic/repository-context
language_code: en
pass_output_id: 290
pass_kind: trend_synthesis
---

# Coding agents are being judged as controlled production software

## Overview
This week’s research treats large language model (LLM) agents as production software. The strongest work ties task success to context recovery, artifact delivery, cost accounting, permission boundaries, and credential safety. DeepDiscovery, EnterpriseClawBench, and Rel(AI)Build give the clearest evidence.

## Clusters

### Repository context and workplace delivery
Agent evaluation is moving toward the conditions that decide whether work ships: the right files, usable artifacts, preserved state, and measurable cost. DeepDiscovery shows that repository tasks need connected context across code, configuration, tests, and organizational structure. Its reported SWE-bench Verified solve rate reaches 78.6%, 8.2 points above its baseline.

EnterpriseClawBench adds the workplace side. It turns real enterprise sessions into 852 reproducible tasks with fixtures, deliverables, hard rules, traces, runtime, token use, and cost. The best audited Lite result is 0.663, which leaves plenty of room on artifact quality and delivery. The open-source census adds scale: agent traces across more than 180 million repositories require multiple detection signals, since pull requests, commits, author patterns, and config files capture different populations.

#### Evidence
- [From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases](../Inbox/2026-06-22--from-fragments-to-paths-task-level-context-recovery-for-large-industrial-codebases.md): DeepDiscovery summary with repository-context method and SWE-bench Verified result.
- [EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions](../Inbox/2026-06-22--enterpriseclawbench-benchmarking-agents-from-real-workplace-sessions.md): EnterpriseClawBench summary with workplace-task construction, scoring dimensions, and results.
- [Detecting AI Coding Agents in Open Source: A Validated Multi-Method Census of 180 Million Repositories](../Inbox/2026-06-23--detecting-ai-coding-agents-in-open-source-a-validated-multi-method-census-of-180-million-repositories.md): Validated census of coding-agent traces across more than 180 million repositories.

### Cost-aware orchestration and recovery tests
The week’s benchmark work asks whether agents can manage uncertainty during execution. Bayesian control treats coding-agent orchestration as a decision problem over candidate correctness. It keeps a posterior belief and chooses among critics, regeneration, verification, and stopping. The clearest gain is in low-prior, high-verifier-cost settings where cheap critics carry useful signals.

ToolBench-X and CodeChat-Eval expose two common failure modes. ToolBench-X injects recoverable tool hazards across 1,106 executable tasks and 4,956 tools; no evaluated model reaches 0.60 overall accuracy. CodeChat-Eval tests ten-turn code refinement and finds functional correctness drops from 19.2% to 69.2% after follow-up edits, depending on the model. These results make regression preservation and recovery choice central evaluation targets.

#### Evidence
- [Bayesian control for coding agents](../Inbox/2026-06-23--bayesian-control-for-coding-agents.md): Bayesian control summary with belief-state orchestration and cost regimes.
- [Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability](../Inbox/2026-06-24--beyond-function-calling-benchmarking-tool-using-agents-under-tool-environment-unreliability.md): ToolBench-X summary with recoverable tool hazards and accuracy results.
- [CodeChat-Eval: Evaluating Large Language Models in Multi-Turn Code Refinement Dialogues](../Inbox/2026-06-24--codechat-eval-evaluating-large-language-models-in-multi-turn-code-refinement-dialogues.md): CodeChat-Eval summary with multi-turn refinement setup and correctness drops.

### Security, permissions, and credential boundaries
Security evidence is no longer limited to generated snippets. The VibeApps study collects 10,517 mostly AI-built applications and validates 1,471 exploitable vulnerabilities in a random sample of 200 deployed web apps. The recurring issues include broken access control, cryptographic failures, injection, secret exposure, placeholder logic, and unfiltered input.

Rel(AI)Build treats agent prompts, permissions, and workflow state as managed artifacts. In 10,008 public repositories, it finds 6,145 agent config files; 10.1% of tracked config paths are exact duplicates after fork adjustment, and fewer than 1% declare permission boundaries. DevFortress adds incident-level evidence around credentials: the cited numbers include 28.6 million new secrets exposed on public GitHub in 2025 and 24,008 unique secrets found in MCP configuration files. The product claims are less tested than the incident evidence, but the risk pattern is concrete.

#### Evidence
- [Understanding the (In)Security of Vibe-Coded Applications](../Inbox/2026-06-22--understanding-the-in-security-of-vibe-coded-applications.md): Vibe-coded application security study with corpus and validated vulnerability counts.
- [A Deterministic Control Plane for LLM Coding Agents](../Inbox/2026-06-25--a-deterministic-control-plane-for-llm-coding-agents.md): Rel(AI)Build summary with agent-config prevalence, permission-boundary findings, and control mechanisms.
- [AI Agent Credential Crisis: Six Months of Incidents](../Inbox/2026-06-28--ai-agent-credential-crisis-six-months-of-incidents.md): Credential incident summary with secret exposure and MCP configuration metrics.
