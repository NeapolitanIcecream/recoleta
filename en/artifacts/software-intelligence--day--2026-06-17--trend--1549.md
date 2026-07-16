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
language_code: en
pass_output_id: 264
pass_kind: trend_synthesis
---

# Coding agents are being judged by their evidence trails and harnesses

## Overview
This period treats coding agents as products that need auditable task sources, executable security evidence, and harness-aware scoring. SWE-Future addresses benchmark contamination; Code-Augur records security assumptions as assertions; Cursor + Claude Fable 5 shows the same model can score very differently under another agent harness.

## Findings

### Future-conditioned coding benchmarks
SWE-Future targets a hard benchmark problem: realistic repository tasks often come from public issues and pull requests, which can leak into training data or model-selection loops. Its answer is to forecast likely future repository work using only pre-snapshot evidence, validate those task families against later pull-request metadata, and then synthesize executable tasks from validated families.

The evidence is stronger than a pure proposal. In an 80-repository retrospective study, the forecaster produced 260 families across 76 repositories. The paper reports 151 strong or related matches against later work, with 111 strong matches. The released dataset contains 200 executable tasks across 61 repositories, with hidden tests, gold patches, validation labels, provenance, and execution logs.

#### Sources
- [SWE-Future: Forecast-Conditioned Data Synthesis for Future-Oriented Software Engineering Agents](../Inbox/2026-06-17--swe-future-forecast-conditioned-data-synthesis-for-future-oriented-software-engineering-agents.md): Summary gives the benchmark contamination problem, forecast-conditioned synthesis method, validation setup, and main results.

### Security scoring depends on the agent harness
Endor Labs’ rerun of Claude Fable 5 on a 200-task vulnerability-fixing benchmark makes the harness visible as an evaluation variable. With Cursor, the same model reached 72.6% FuncPass and 29.0% SecPass after anti-cheating and strict-test adjustments. The earlier Claude Code run reached 59.8% FuncPass and 19.0% SecPass.

The security metric matters because passing functional tests did not prove the vulnerability was fixed. Among Cursor-only security wins, many cases involved patches where the other run passed functional tests but failed hidden security tests. The study also kept cheating in view: Cursor + Fable 5 had 29 confirmed cheating cases, mostly attributed to memorization or training recall.

#### Sources
- [Claude Fable 5: The harness matters more than the model](../Inbox/2026-06-17--claude-fable-5-the-harness-matters-more-than-the-model.md): Summary reports the Cursor versus Claude Code comparison, FuncPass/SecPass scores, cheating counts, and security-completeness findings.

### Executable assumptions for vulnerability detection
Code-Augur gives a concrete pattern for large language model (LLM) security agents: when the agent judges code as safe, it writes the reason as an in-source assertion. A guided grey-box fuzzer then tries to falsify that assertion. Failed assertions become either vulnerability reports or signals that the inferred specification was wrong.

The reported results are concrete. The paper says Code-Augur found more bugs than Claude Code and Atlantis on DARPA AIxCC and OSV benchmark sources, with a reported margin of 34 to 370 bugs depending on the setting. It also found 22 new vulnerabilities in open-source projects; developers had fixed or confirmed 16 at the time of writing.

#### Sources
- [Code-Augur: Agentic Vulnerability Detection via Specification Inference](../Inbox/2026-06-17--code-augur-agentic-vulnerability-detection-via-specification-inference.md): Summary covers the threat model, assertion-based specification inference, fuzzing loop, and reported vulnerability results.

### Agent infrastructure needs grounded memory, feedback, and protocols
Several items focus on the support layer around agents. CAPRA reviews software architecture reports with specialized agents, but its key control is evidence anchoring: each issue needs a source quote, severity, and confidence score, then a deterministic fuzzy match checks whether the quote exists in the document. On 10 evaluation reports, CAPRA passed 88.8% of criteria under strict aggregation and processed each report in a little over four minutes.

Vlk addresses long-running coding sessions with a Model Context Protocol server that stores agent memory in SQLite and lets the agent delete stale entries while saving a new lesson. The evidence is a product excerpt rather than a benchmark, so the claim should stay narrow: it exposes one tool, `vlk_time_travel`, and supports clients such as Zed, Cursor, and Claude Desktop.

A protocol taxonomy paper adds a broader infrastructure view. It analyzes nine actively maintained open-source agent communication protocols across counterparty, payload, state, discovery, and schema flexibility. The sample shows session-state persistence across agent-to-agent protocols, multiple predefined schemas in most protocols, and rare decentralized discovery.

#### Sources
- [CAPRA: Scaling Feedback on Software Architecture Deliverables with a Multi-Agent LLM System](../Inbox/2026-06-17--capra-scaling-feedback-on-software-architecture-deliverables-with-a-multi-agent-llm-system.md): Summary reports CAPRA’s evidence anchoring, multi-agent review flow, cost/time, and evaluation results.
- [Vlk: MemAct for the IDE – persistent working memory agents can prune themselves](../Inbox/2026-06-17--vlk-memact-for-the-ide-persistent-working-memory-agents-can-prune-themselves.md): Summary describes Vlk’s persistent SQLite memory, `vlk_time_travel` tool, supported clients, and lack of benchmark evidence.
- [A Technical Taxonomy of LLM Agent Communication Protocols](../Inbox/2026-06-17--a-technical-taxonomy-of-llm-agent-communication-protocols.md): Summary gives the taxonomy dimensions and findings across nine agent communication protocols.
