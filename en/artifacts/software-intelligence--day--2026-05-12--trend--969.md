---
kind: trend
trend_doc_id: 969
granularity: day
period_start: '2026-05-12T00:00:00'
period_end: '2026-05-13T00:00:00'
topics:
- agent evaluation
- benchmark security
- agent tracing
- MCP governance
- software assurance
- code translation
- LLM testing
run_id: materialize-outputs
aliases:
- recoleta-trend-969
tags:
- recoleta/trend
- topic/agent-evaluation
- topic/benchmark-security
- topic/agent-tracing
- topic/mcp-governance
- topic/software-assurance
- topic/code-translation
- topic/llm-testing
language_code: en
pass_output_id: 148
pass_kind: trend_synthesis
---

# Agent research is treating scores and tool actions as audit targets

## Overview
The day’s strongest signal is auditability for agentic systems. BenchJack attacks benchmark harnesses before agents run. Rollout Cards asks evaluations to publish rollout evidence. Cloudflare’s Model Context Protocol (MCP) deployment shows the same control problem inside enterprise tool access.

## Findings

### Benchmark integrity
Agent benchmark numbers receive direct adversarial pressure in this period. BenchJack audited 10 agent benchmarks and generated working reward-hacking exploits for all 10, with 219 distinct flaws across its taxonomy. Its patching loop reduced hackable-task ratios below 10% on four fixable benchmarks, and fully patched WebArena and OSWorld within three iterations.

Rollout Cards addresses a related reporting problem. The paper argues that agent studies need rollout records, declared scoring views, reporting rules, and omitted-field manifests. In its audit of 50 popular repositories, none reported failed, errored, or skipped rollouts alongside headline scores. Re-grading fixed artifacts changed reported scores by as much as 20.9 points and could swap model rankings on tau-bench.

#### Sources
- [Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack](../Inbox/2026-05-12--do-androids-dream-of-breaking-the-game-systematically-auditing-ai-agent-benchmarks-with-benchjack.md): BenchJack results on benchmark exploits, flaw count, and patching outcomes.
- [Rollout Cards: A Reproducibility Standard for Agent Research](../Inbox/2026-05-12--rollout-cards-a-reproducibility-standard-for-agent-research.md): Rollout-card proposal and evidence that reporting rules change agent benchmark conclusions.

### Traceable agent operations
Operational agent work is being framed as an evidence-management problem. A pilot on decision reconstructability tested six vendor SDK regimes, including MCP and OpenTelemetry GenAI, against seven property classes. Strict governance completeness ranged from 42.9% to 85.7%, and reasoning evidence was missing or unusable across most surveyed regimes.

Cloudflare’s MCP architecture gives a production-side answer for tool access. It moves MCP servers off employee machines and behind centralized approval, OAuth-based access checks, audit logging, data-loss-prevention rules, and default-deny write controls. Its Code Mode reduces one internal portal’s tool-definition context from about 9,400 tokens across 52 tools to about 600 tokens across two portal tools.

A prompt-specification audit case study shows similar issues inside multi-agent orchestration. Claude sub-agents inspected eight AEGIS prompt and contract files across nine rounds, finding 51 consistency defects. The high-severity defects were all cross-lane schema mismatches, including a field-name mismatch that could have caused silent runtime failure.

#### Sources
- [Property-Level Reconstructability of Agent Decisions: An Anchor-Level Pilot Across Vendor SDK Adapter Regimes](../Inbox/2026-05-12--property-level-reconstructability-of-agent-decisions-an-anchor-level-pilot-across-vendor-sdk-adapter-regimes.md): Pilot results on reconstructing agent decisions across SDK evidence regimes.
- [Scaling MCP adoption: Our ref architecture – simpler,safer&cheaper deployments](../Inbox/2026-05-12--scaling-mcp-adoption-our-ref-architecture-simpler-safer-cheaper-deployments.md): Cloudflare MCP governance architecture and token-reduction claim for Code Mode.
- [Iterative Audit Convergence in LLM-Managed Multi-Agent Systems: A Case Study in Prompt Engineering Quality Assurance](../Inbox/2026-05-12--iterative-audit-convergence-in-llm-managed-multi-agent-systems-a-case-study-in-prompt-engineering-quality-assurance.md): Multi-agent prompt-specification audit results and defect taxonomy.

### Checkable software and data work
Several papers make LLM software work more inspectable by tying outputs to executable or structured evidence. Agentic Interpretation decomposes program-analysis goals into localized claims and records each judgment in a finite evidence lattice. The paper has no implementation or benchmark results yet, so its value is a formal design for auditable LLM-assisted analysis rather than measured performance.

For code migration, cozy compares C and Rust binaries under symbolic execution and asks developers to review only the behavioral differences it finds. The reported experiments are small, covering insertion sort, a watch update function, and a box blur filter, but they show a concrete path-level review process for translation assurance.

Legacy APL-to-C# translation and neuroscience data reuse both use run-based checks. The APL study builds aligned datasets and evaluates generated C# by compiling and running tests, though the excerpt does not provide final accuracy numbers. The neurodata benchmark ran Claude Code and Codex on 48 dataset-conversion tasks; every run produced output, but full error-free reuse was rare and agents-as-judges missed errors.

#### Sources
- [Agentic Interpretation: Lattice-Structured Evidence for LLM-Based Program Analysis](../Inbox/2026-05-12--agentic-interpretation-lattice-structured-evidence-for-llm-based-program-analysis.md): Agentic Interpretation’s lattice-based evidence model and stated lack of experimental results.
- [Finding a Crab in the C: Assured Translation via Comparative Symbolic Execution](../Inbox/2026-05-12--finding-a-crab-in-the-c-assured-translation-via-comparative-symbolic-execution.md): cozy’s comparative symbolic execution method and small C/Rust validation experiments.
- [Neural Code Translation of Legacy Code: APL to C#](../Inbox/2026-05-12--neural-code-translation-of-legacy-code-apl-to-c.md): APL-to-C# dataset construction and compile-and-run evaluation pipeline.
- [Neurodata Without Boredom: Benchmarking Agentic AI for Data Reuse](../Inbox/2026-05-12--neurodata-without-boredom-benchmarking-agentic-ai-for-data-reuse.md): Agentic neurodata reuse benchmark results and human-review finding.

### Testing methods for open-ended LLM outputs
Testing research in the corpus focuses on cases where exact expected answers are hard to define. The metamorphic-testing survey reviews 93 primary studies and organizes the area into two directions: using metamorphic testing to evaluate LLM systems, and using LLMs to help discover relations, transform inputs, implement tests, and run closed-loop checks. Its claims are survey-level; it reports literature scope and categories, not a benchmarked defect-detection gain.

Education-oriented code review gives a narrower example of task adaptation. A Code Llama 7B model fine-tuned with parameter-efficient fine-tuning (PEFT) reached 61% mistake-feedback accuracy and 60% next-step helpfulness, compared with 20% and 26% for baseline prompting. The student study was small, with seven CS1 students, so the strongest claim is that local open models can improve after targeted adaptation on a bounded feedback task.

#### Sources
- [Bidirectional Empowerment of Metamorphic Testing and Large Language Models: A Systematic Survey](../Inbox/2026-05-12--bidirectional-empowerment-of-metamorphic-testing-and-large-language-models-a-systematic-survey.md): Survey scope, taxonomy, and lack of benchmark-style performance claims.
- [Fine-Tuning Models for Automated Code Review Feedback](../Inbox/2026-05-12--fine-tuning-models-for-automated-code-review-feedback.md): Fine-tuned Code Llama code-review feedback setup and reported accuracy/helpfulness results.
