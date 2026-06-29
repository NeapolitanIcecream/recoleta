---
kind: trend
trend_doc_id: 1635
granularity: day
period_start: '2026-06-24T00:00:00'
period_end: '2026-06-25T00:00:00'
topics:
- coding agents
- software engineering
- agent harnesses
- tool reliability
- code benchmarks
- test migration
- agent governance
run_id: materialize-outputs
aliases:
- recoleta-trend-1635
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/agent-harnesses
- topic/tool-reliability
- topic/code-benchmarks
- topic/test-migration
- topic/agent-governance
language_code: en
pass_output_id: 280
pass_kind: trend_synthesis
---

# Coding agents are being measured by state, recovery, and regression control

## Overview
This period treats coding agents as software systems with state, tests, failure recovery, and traceable controls. i cat-agent supplies the strongest positive result; ToolBench-X and CodeChat-Eval expose brittle behavior under tool hazards and follow-up edits.

## Clusters

### Agent harnesses and separated coding roles
The strongest engineering result is i cat-agent. It splits GitHub issue resolution across an Explorer, Patch Editor, and Validator. The agents exchange structured events, and the Validator keeps tests and assertions hidden from the Patch Editor to reduce patch overfitting. On SWE-bench Pro, i cat-agent with GPT-5.4-xhigh solves 67.4% of tasks, 8.3 percentage points above mini-SWE-agent with the same backbone. The same paper reports lower average cost than Claude Code on SWE-bench Pro.

The broader design theme appears in Code as Agent Harness, a survey that treats code as the place where agents keep state, call tools, plan, and verify work. MCPlexer gives a concrete product version of that idea for the Model Context Protocol (MCP): a small shared tool surface with routing, approvals, audit logs, memory, browser control, and workspace policies. The MCPlexer item has no benchmark evidence, so its value is operational design, not measured performance.

#### Evidence
- [Unlocking Model Potentials Through Adaptive Multi-Agent Scaffolding for Efficient Issue Resolution](../Inbox/2026-06-24--unlocking-model-potentials-through-adaptive-multi-agent-scaffolding-for-efficient-issue-resolution.md): Summary of i cat-agent architecture, SWE-bench results, and cost claims.
- [Code as Agent Harness](../Inbox/2026-06-24--code-as-agent-harness.md): Survey summary of code as the agent harness for state, tools, planning, and verification.
- [Show HN: Mcplexer.com](../Inbox/2026-06-24--show-hn-mcplexer-com.md): MCPlexer summary with cross-harness routing, approvals, audit, memory, and workspace controls.

### Benchmarks stress recovery and preservation, not clean calls
ToolBench-X tests agents on 1,106 executable multi-step tasks with 4,956 Python tools and five recoverable hazard types. No evaluated model reaches 0.60 overall accuracy. The best reported score is 0.513 from Doubao-Seed-2.0-Lite. The paper’s diagnostic subset shows that targeted recovery hints regain 25.5 to 35.5 accuracy points, while extra interaction rounds help less. The weak point is hazard diagnosis and recovery choice.

CodeChat-Eval adds a separate pressure test for coding models: can they keep code correct through 10-turn refinement dialogues? Across 542 programming tasks, functional correctness drops for every evaluated model. GPT-5 Nano loses 19.2%, and Llama 3.1 8B loses 69.2% after multi-turn refinement. SWE-Pro makes the same accountability point for performance optimization. Expert patches produce large runtime and memory gains, while current large language models often apply patches but rarely deliver measured speed or memory improvements.

#### Evidence
- [Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability](../Inbox/2026-06-24--beyond-function-calling-benchmarking-tool-using-agents-under-tool-environment-unreliability.md): ToolBench-X task count, hazard design, model scores, and diagnostic recovery results.
- [CodeChat-Eval: Evaluating Large Language Models in Multi-Turn Code Refinement Dialogues](../Inbox/2026-06-24--codechat-eval-evaluating-large-language-models-in-multi-turn-code-refinement-dialogues.md): CodeChat-Eval setup and correctness drops across multi-turn code refinement.
- [Evaluating LLMs on Real-World Software Performance Optimization](../Inbox/2026-06-24--evaluating-llms-on-real-world-software-performance-optimization.md): SWE-Pro benchmark design and measured gap between expert optimization patches and LLM patches.

### Test migration uses intent and repository context
IntentTester shows a practical use of multi-agent coding beyond patch generation. It converts source tests into a language-neutral Test Description Language, maps those intents onto a target repository graph, then generates executable tests with verification feedback. This handles cases where API signatures and direct code patterns do not line up, including Java-Python migration.

The evaluation covers nine open-source projects across JSON, HTML, and Time libraries. From 2,058 source tests, the pipeline creates 5,536 sub-tests and keeps 3,257 after filtering. IntentTester generates 2,776 syntactically correct tests with 85% correctness, compared with 51% for MUT and 43% for METALLICUS. The generated tests expose 25 real defects, including stack overflow and null dereference bugs.

#### Evidence
- [IntentTester: Intent-Driven Multi-agent Framework for Cross-Library Test Migration](../Inbox/2026-06-24--intenttester-intent-driven-multi-agent-framework-for-cross-library-test-migration.md): IntentTester method, evaluation scale, correctness gains, executable tests, and real defects.

### Agent instructions are becoming versioned engineering artifacts
The corpus also includes early work on how teams maintain coding-agent instructions. The Agent Context File study examines files such as CLAUDE.md, AGENTS.md, and copilot-instructions.md as repository artifacts with commit histories. It plans to classify changes, connect them to later agent-generated code quality, and measure timing across development windows.

This paper reports study design and feasibility, not completed results. The scale still matters for grounding the question: the authors cite AIDev with 116,211 repositories and 932,791 pull requests involving agent-generated code, plus 2,303 context files from 1,925 repositories. A preliminary pipeline produced 10,763 context-file snapshots and 8,600 commits with overlapping instruction-file and agent-code information.

#### Evidence
- [How Do Developers Maintain and Evolve Their Agents' Instructions? An Empirical Study](../Inbox/2026-06-24--how-do-developers-maintain-and-evolve-their-agents-instructions-an-empirical-study.md): Study design, datasets, planned metrics, and feasibility counts for Agent Context Files.
