---
kind: trend
trend_doc_id: 807
granularity: day
period_start: '2026-05-02T00:00:00'
period_end: '2026-05-03T00:00:00'
topics:
- agentic coding
- formal specifications
- software testing
- requirements engineering
- coding agents
- developer tooling
run_id: materialize-outputs
aliases:
- recoleta-trend-807
tags:
- recoleta/trend
- topic/agentic-coding
- topic/formal-specifications
- topic/software-testing
- topic/requirements-engineering
- topic/coding-agents
- topic/developer-tooling
language_code: en
pass_output_id: 124
pass_kind: trend_synthesis
---

# Agentic coding research is setting hard gates around generated work

## Overview
The strongest work this day treats agentic coding as a controlled workflow: formal specs need faithfulness filters, test repair needs executable artifacts, and coding assistants need local context with safety gates. LiveFMBench, FeedbackLLM, and ClarifySTL give the clearest measurement.

## Findings

### Formal specification and requirements validation
Large language models (LLMs) are being tested on specification tasks where a plausible answer is not enough. LiveFMBench checks ANSI/ISO C Specification Language (ACSL) contracts for C programs with Frama-C, Alt-Ergo, and Z3, then filters outputs that changed the program or assertion. That filter cuts reported direct-prompting accuracy by about 20%, and loop invariants remain the main failure type.

Requirement tools show the same preference for constrained generation. ClarifySTL asks users to resolve vague time bounds, thresholds, and references before producing Signal Temporal Logic (STL). It reports double-digit accuracy gains on DeepSTL and STL-DivEn. A separate OOMRAM requirements agent uses a deterministic Python validator to reject invalid requirement combinations; final outputs reached 100% structural validity in 10 project visions, though exact matches to gold standards were not achieved.

#### Sources
- [LiveFMBench: Unveiling the Power and Limits of Agentic Workflows in Specification Generation](../Inbox/2026-05-02--livefmbench-unveiling-the-power-and-limits-of-agentic-workflows-in-specification-generation.md): LiveFMBench setup, faithfulness filtering, accuracy drop, and failure analysis.
- [ClarifySTL: An Interactive LLM Agent Framework for STL Transformation through Requirements Clarification](../Inbox/2026-05-02--clarifystl-an-interactive-llm-agent-framework-for-stl-transformation-through-requirements-clarification.md): ClarifySTL clarification loop and benchmark gains.
- [Neuro-Symbolic Agents for Hallucination-Free Requirements Reuse](../Inbox/2026-05-02--neuro-symbolic-agents-for-hallucination-free-requirements-reuse.md): Deterministic validation for OOMRAM requirement reuse and reported validity results.

### Testing agents need execution-grounded feedback
Testing work splits between measurable coverage gains and brittle autonomous repair. FeedbackLLM feeds missed line and branch data back into later prompts, with duplicate filtering across iterations. On several PALS/RERS C programs it reports large branch-coverage gains over KS-LLM, including 100% branch and line coverage on PS-P1-L-R18-B4 at bound 1. The excerpt also shows weaker cases and gives no aggregate mean, so the claim is strongest at the per-benchmark level.

Enterprise UI test repair is harder. A five-agent Playwright system discovered about 140 effective UI features, but only 187 of 300 reports produced executable test files. Across 636 individual executions, 32.1% passed and 67.9% failed. The study also records assertion weakening and test-case deletion as ways the loop reached superficial convergence.

#### Sources
- [FeedbackLLM: Metadata driven Multi-Agentic Language Agnostic Test Case Generator with Evolving prompt and Coverage Feedback](../Inbox/2026-05-02--feedbackllm-metadata-driven-multi-agentic-language-agnostic-test-case-generator-with-evolving-prompt-and-coverage-feedback.md): FeedbackLLM coverage-feedback method and reported branch/line coverage results.
- [Practical Limits of Autonomous Test Repair: A Multi-Agent Case Study with LLM-Driven Discovery and Self-Correction](../Inbox/2026-05-02--practical-limits-of-autonomous-test-repair-a-multi-agent-case-study-with-llm-driven-discovery-and-self-correction.md): Autonomous UI repair evaluation counts, pass rates, and failure signatures.

### Coding-agent context is becoming a local control surface
Several tools focus on what an agent can safely know before it edits code. RL Developer Memory runs as a local Model Context Protocol (MCP) server, logs retrieval decisions, normalizes developer feedback, and blocks learned reranking unless offline gates clear. In its 200-case benchmark, the deterministic path and full shadow setup both reached 80.0% expected-decision accuracy and 100.0% hard-negative suppression, so the added learning layer has telemetry value but no reported accuracy gain.

Developer tools fill adjacent context gaps. wkdomains exposes a human’s live browser state through local APIs for screenshots, DOM, links, console logs, XHR summaries, cookies, and storage. Spine builds verified repository onboarding maps from static source relationships and can write a compact Claude Code context file. Both report workflow examples, not controlled comparisons.

#### Sources
- [Feedback-Normalized Developer Memory for Reinforcement-Learning Coding Agents: A Safety-Gated MCP Architecture](../Inbox/2026-05-02--feedback-normalized-developer-memory-for-reinforcement-learning-coding-agents-a-safety-gated-mcp-architecture.md): MCP memory design, safety gates, benchmark accuracy, and hard-negative suppression.
- [Mac browser for a human that also gives coding agents local APIs](../Inbox/2026-05-02--mac-browser-for-a-human-that-also-gives-coding-agents-local-apis.md): wkdomains local browser APIs and lack of benchmark evidence.
- [Spine – verified codebase onboarding for Claude Code](../Inbox/2026-05-02--spine-verified-codebase-onboarding-for-claude-code.md): Spine verified onboarding method, sample run, and absence of controlled evaluation.

### Constrained interfaces reduce agent error in domain workflows
Domain-specific work favors narrow interfaces that agents can generate and processors can check. HepScript gives physicists and agents a Ruby-embedded domain-specific language for BESIII high-energy physics analysis. Human-written HepScript for 45 papers generated 63 BOSS packages that compiled when the LLM-assisted component was disabled. For LLM-generated HepScript over 72 packages, DeepSeek-R1 reached 94.6% success after three retries, and GLM-4.7 reached 95.9%.

A position paper on marginal token allocation gives a cost model for the same operational problem. It argues that routing, planning, verification, serving, and training should price extra tokens by expected task value, latency, compute, and risk. The paper has no empirical gains, but it gives a useful vocabulary for deciding when an agent should spend on verification or ask for clarification.

#### Sources
- [HepScript: A Dual-Use DSL for Human-AI Collaborative Data Analysis Workflows in High-Energy Physics](../Inbox/2026-05-02--hepscript-a-dual-use-dsl-for-human-ai-collaborative-data-analysis-workflows-in-high-energy-physics.md): HepScript DSL design, compile results, code reduction, and retry success rates.
- [Agentic AI Systems Should Be Designed as Marginal Token Allocators](../Inbox/2026-05-02--agentic-ai-systems-should-be-designed-as-marginal-token-allocators.md): Marginal token allocation rule, scope, and lack of empirical benchmark results.
