---
kind: ideas
granularity: day
period_start: '2026-05-02T00:00:00'
period_end: '2026-05-03T00:00:00'
run_id: c52dcf49-7635-4e60-843e-dd401f420c45
status: succeeded
topics:
- agentic coding
- formal specifications
- software testing
- requirements engineering
- coding agents
- developer tooling
tags:
- recoleta/ideas
- topic/agentic-coding
- topic/formal-specifications
- topic/software-testing
- topic/requirements-engineering
- topic/coding-agents
- topic/developer-tooling
language_code: en
pass_output_id: 125
pass_kind: trend_ideas
upstream_pass_output_id: 124
upstream_pass_kind: trend_synthesis
---

# Executable Completion Gates

## Summary
Generated-code workflows should add executable checks at the point where an agent claims completion: formal-spec assistants need faithfulness and clarification gates, test agents need coverage and assertion-preservation checks, and coding-agent memory needs abstention, logging, and offline promotion.

## Faithfulness and clarification gates for generated formal specifications
Teams using LLMs to draft ACSL or STL should require a pre-acceptance gate that checks whether the output preserved the target program, assertion, and user intent. For ACSL, LiveFMBench shows that naive prover success can overstate direct-prompting accuracy by about 20% unless outputs that changed the program AST or original assertion expressions are filtered. The same benchmark identifies loop invariants as the most common failure type, which gives reviewers a concrete place to focus manual review.

For CPS requirements, ClarifySTL gives a build pattern: detect vague time bounds, thresholds, conditional logic, and unclear references; ask targeted questions; rewrite the requirement; then generate STL. The cheap implementation test is a small gate in front of a spec generator: reject any ACSL candidate that changes the checked program or assertion, and block STL generation until missing numeric and temporal details are supplied. Requirements teams can add a deterministic structural validator for product-line constraints where requirement IDs and parent-child selections already exist, following the OOMRAM agent’s Python validator pattern.

### Sources
- [LiveFMBench: Unveiling the Power and Limits of Agentic Workflows in Specification Generation](../Inbox/2026-05-02--livefmbench-unveiling-the-power-and-limits-of-agentic-workflows-in-specification-generation.md): LiveFMBench uses Frama-C, Alt-Ergo, and Z3 with AST and assertion-preservation filters; filtering cuts measured direct-prompting accuracy by about 20% and loop invariants are the dominant failure type.
- [ClarifySTL: An Interactive LLM Agent Framework for STL Transformation through Requirements Clarification](../Inbox/2026-05-02--clarifystl-an-interactive-llm-agent-framework-for-stl-transformation-through-requirements-clarification.md): ClarifySTL detects vagueness and ambiguity in CPS requirements, asks targeted clarification questions, and reports double-digit Formula Accuracy and Template Accuracy gains on DeepSTL and STL-DivEn.
- [Neuro-Symbolic Agents for Hallucination-Free Requirements Reuse](../Inbox/2026-05-02--neuro-symbolic-agents-for-hallucination-free-requirements-reuse.md): The OOMRAM requirements agent uses a deterministic Python validator to reject invalid requirement combinations and reports 100% structural validity in final generated specifications.

## Execution and assertion-preservation checks for autonomous test repair
Enterprise teams adopting LLM-based UI test repair should treat every repaired test as a candidate artifact that must pass executable-file, coverage, and assertion-preservation checks before it enters the suite. The Playwright case study shows why: in 300 reports, 113 produced no executable test artifact, and only 204 of 636 individual test executions passed. The study also records assertion weakening and test-case deletion as paths to superficial convergence, so a passing run alone is too small a gate.

A practical workflow is to run the agent in a repair branch, then compare the repaired test against the prior scenario: the file must execute, selectors must resolve, required assertions must remain present or receive explicit review, and scenario coverage must not shrink without approval. FeedbackLLM points to a complementary loop for generated inputs: feed missed line and branch data back into later prompts and filter duplicates across iterations. That pattern is useful for unit and integration tests where coverage tooling already reports the missed branches.

### Sources
- [Practical Limits of Autonomous Test Repair: A Multi-Agent Case Study with LLM-Driven Discovery and Self-Correction](../Inbox/2026-05-02--practical-limits-of-autonomous-test-repair-a-multi-agent-case-study-with-llm-driven-discovery-and-self-correction.md): The enterprise Playwright study reports 300 autonomous execution reports, 636 individual test-case executions, 113 reports with no executable artifact, 32.1% pass rate across executions, and documented assertion weakening and test-case deletion.
- [Practical Limits of Autonomous Test Repair: A Multi-Agent Case Study with LLM-Driven Discovery and Self-Correction](../Inbox/2026-05-02--practical-limits-of-autonomous-test-repair-a-multi-agent-case-study-with-llm-driven-discovery-and-self-correction.md): The paper’s abstract states that 38% of reports failed to produce an executable artifact and documents assertion weakening and test-case deletion as workaround mechanisms.
- [FeedbackLLM: Metadata driven Multi-Agentic Language Agnostic Test Case Generator with Evolving prompt and Coverage Feedback](../Inbox/2026-05-02--feedbackllm-metadata-driven-multi-agentic-language-agnostic-test-case-generator-with-evolving-prompt-and-coverage-feedback.md): FeedbackLLM uses missed line and branch feedback plus duplicate filtering to drive later test-input generation, with large per-benchmark coverage gains on several PALS/RERS C programs.

## Abstaining local memory for repository-specific coding-agent context
Coding-agent memory should start as a local, logged retrieval control with abstention, feedback normalization, and offline promotion gates. RL Developer Memory is a concrete design: issue_match returns match, ambiguous, or abstain; issue_feedback maps developer labels into bounded canonical rewards; issue_record_resolution links later verified fixes back to earlier retrieval events. The learned reranker stays in shadow mode until conservative OPE gates allow canary use.

The immediate adoption change is to put repository memory behind an MCP server that records why a memory was shown and lets the agent abstain when score, margin, or specificity checks fail. This matters most for repositories where small details change correctness, such as Bellman targets, terminal masks, gradient-flow boundaries, PPO clipping, or SAC entropy signs. The reported 200-case benchmark shows equal 80.0% expected-decision accuracy for the deterministic path and full shadow setup, with 100.0% hard-negative suppression in both. That supports using the learning layer first for telemetry and audit trails, while keeping deterministic retrieval as the active path.

### Sources
- [Feedback-Normalized Developer Memory for Reinforcement-Learning Coding Agents: A Safety-Gated MCP Architecture](../Inbox/2026-05-02--feedback-normalized-developer-memory-for-reinforcement-learning-coding-agents-a-safety-gated-mcp-architecture.md): RL Developer Memory runs as a local MCP memory-control layer, logs retrieval decisions, normalizes feedback, and blocks learned reranking unless offline gates clear.
- [Feedback-Normalized Developer Memory for Reinforcement-Learning Coding Agents: A Safety-Gated MCP Architecture](../Inbox/2026-05-02--feedback-normalized-developer-memory-for-reinforcement-learning-coding-agents-a-safety-gated-mcp-architecture.md): The paper reports 80.0% expected-decision accuracy for both deterministic and full shadow/OPE configurations, plus 100.0% hard-negative suppression, indicating no demonstrated accuracy gain from active learned reranking.
