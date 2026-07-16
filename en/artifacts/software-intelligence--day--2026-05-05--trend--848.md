---
kind: trend
trend_doc_id: 848
granularity: day
period_start: '2026-05-05T00:00:00'
period_end: '2026-05-06T00:00:00'
topics:
- coding agents
- software security
- test generation
- multi-agent systems
- code search
- quantum software
run_id: materialize-outputs
aliases:
- recoleta-trend-848
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-security
- topic/test-generation
- topic/multi-agent-systems
- topic/code-search
- topic/quantum-software
language_code: en
pass_output_id: 130
pass_kind: trend_synthesis
---

# Executable checks are setting the bar for software agents

## Overview
May 5’s software-AI papers put large language models (LLMs) under executable checks. MOSAIC-Bench exposes staged coding-agent vulnerabilities. TDD-Bench-Java and PoVSmith test whether generated artifacts fail, pass, compile, or trigger real bugs.

## Findings

### Agent security needs executable proof
MOSAIC-Bench gives the clearest security signal. It splits each malicious objective across three ordinary engineering tickets, then checks the final application with deterministic proof-of-concept oracles in Docker. Across nine production coding agents, staged tickets produced attack success rates of 53.3% to 85.9%, with only two refusals across the benchmark. Reviewer agents also missed confirmed-vulnerable cumulative diffs: neutral review approved 24.8% as routine pull requests.

PoVSmith takes the defensive side of the same problem. It asks a coding agent to find application entry points that reach vulnerable library APIs, write JUnit proof-of-vulnerability tests, repair them with build feedback, and judge the execution logs. On 33 Java application-library pairs, it found 152 correct call paths, compiled 141 generated tests, and triggered vulnerabilities in 84 cases.

#### Sources
- [MOSAIC-Bench: Measuring Compositional Vulnerability Induction in Coding Agents](../Inbox/2026-05-05--mosaic-bench-measuring-compositional-vulnerability-induction-in-coding-agents.md): MOSAIC-Bench summary, methods, and attack-success results.
- [Generating Proof-of-Vulnerability Tests to Help Enhance the Security of Complex Software](../Inbox/2026-05-05--generating-proof-of-vulnerability-tests-to-help-enhance-the-security-of-complex-software.md): PoVSmith workflow and evaluation results.

### Java issue work is moving through fail-to-pass tests
TDD-Bench-Java makes reproduction tests the artifact to judge. A valid test must fail on the buggy version and pass after the developer fix, which gives execution evidence for both diagnosis and validation. The benchmark contains 250 Java issues from 13 open-source repositories, including Trino, Jackson Databind, RocketMQ, and Dubbo.

e-Otter++ adds practical repair loops around test generation. It localizes likely files and functions, writes one new Java test class, runs it on the old code, reads build or test logs, and revises for up to 10 iterations. On TDD-Bench-Java, it reached a 43.6% fail-to-pass rate with Claude-Sonnet-4.5 and 46.4% with GPT-5.2. Execution-based refinement added 9.4 and 13.6 percentage points over the initial generator for those models.

#### Sources
- [Reproduction Test Generation for Java SWE Issues](../Inbox/2026-05-05--reproduction-test-generation-for-java-swe-issues.md): TDD-Bench-Java construction, e-Otter++ workflow, and fail-to-pass results.

### Multi-agent coding needs context diagnostics and stability budgets
The context-transfer study shows that software design agents need a cheap task check before artifacts are injected. Across more than 2,700 Claude Sonnet 4 multi-agent runs, the best context choice depended on the task’s no-context exploration score. Anti-patterns raised rate-limiter tradeoff coverage from 0.033 to 0.700, while transcripts reduced Kubernetes-operator coverage from 0.475 to 0.256. The paper’s practical recommendation is simple: run a no-context baseline, then add artifacts when baseline exploration is low.

AMCP applies a different control to multi-agent software engineering. It treats remodularization as negotiation between cohesion and stability agents, accepting only class moves that improve cohesion while staying above an architect-set stability threshold. On Xwork 1.0 to 1.1, a strict stability threshold of 0.95 stopped after three steps with U_coh = 0.5919 and U_sta = 0.9583, showing that the budget can constrain architectural churn.

#### Sources
- [When Context Hurts: The Crossover Effect of Knowledge Transfer on Multi-Agent Design Exploration](../Inbox/2026-05-05--when-context-hurts-the-crossover-effect-of-knowledge-transfer-on-multi-agent-design-exploration.md): Context-transfer experiment setup and task-level results.
- [A Multi-Agent Consensus Protocol for Stable Software Remodularization](../Inbox/2026-05-05--a-multi-agent-consensus-protocol-for-stable-software-remodularization.md): AMCP method and Xwork stability-budget results.

### Narrow code-analysis tools are getting stronger baselines
Two papers target code-analysis settings where general code models struggle. mitRE-embed-Qwen-0.6B is tuned to match source functions with stripped Ghidra decompiled functions, where useful identifier names are missing. With filtered pools, it reached mean reciprocal rank 0.6207 and Recall@10 0.8353 for decompiled-to-source search, and kept near-identical retrieval quality after FP8 quantization.

LintQ-LLM applies LLM checks to Qiskit programs. The chain-of-thought version reached F1 = 0.70 on 55 Qiskit files, above the rule-based LintQ baseline at 0.41. The retrieved-example version reached F1 = 0.68 and the highest precision among the evaluated variants. The evidence is small, but it points to useful gains when the tool is scoped to a concrete language, bug family, and evaluation set.

#### Sources
- [Identifier-Free Code Embedding Models for Scalable Search](../Inbox/2026-05-05--identifier-free-code-embedding-models-for-scalable-search.md): Identifier-free embedding data, retrieval setup, and metrics.
- [Beyond Rules: LLM-Powered Linting for Quantum Programs](../Inbox/2026-05-05--beyond-rules-llm-powered-linting-for-quantum-programs.md): LLM-based quantum linting methods and evaluation metrics.
