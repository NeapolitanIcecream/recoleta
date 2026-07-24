---
kind: ideas
granularity: day
period_start: '2026-07-23T00:00:00'
period_end: '2026-07-24T00:00:00'
run_id: eb2b8fd0-b370-45c9-ad52-02b68a02a0aa
status: succeeded
topics:
- coding agents
- agent evaluation
- reliability harnesses
- human oversight
- neuro-symbolic reasoning
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/reliability-harnesses
- topic/human-oversight
- topic/neuro-symbolic-reasoning
language_code: en
pass_output_id: 347
pass_kind: trend_ideas
upstream_pass_output_id: 346
upstream_pass_kind: trend_synthesis
---

# Evaluation and review controls for ambiguous agent work

## Summary
Agent evaluations can test reliability more precisely by locating clarification, formal verification, and specialist review at the decisions where errors become expensive to reverse. The most useful changes concern when an agent asks, whether a policy verdict has an executable derivation, and which intermediate artifacts actually trigger review.

## Clarification checkpoints before irreversible implementation decisions
Coding-agent benchmark designers should evaluate whether an agent asks for a hidden constraint before the implementation decision that depends on it, rather than rewarding question volume or requirement coverage alone. ICAE-Bench finds that recovering more constraints does not automatically raise pass rates, while pAI-Econ-claude concentrates human authority at choices that are costly to reverse. Combining these observations suggests annotating each hidden requirement with its last responsible checkpoint—such as selecting an API, schema, or architecture—and scoring timely clarification separately from final test success and unnecessary interruptions. A small ICAE-Bench replay could compare unrestricted questioning with checkpoint-based access to the simulated user, measuring enhanced-test results and implementation rework.

### Sources
- [ICAE-Bench: Evaluating Coding Agents as Interactive Project Builders](../Inbox/2026-07-23--icae-bench-evaluating-coding-agents-as-interactive-project-builders.md): ICAE-Bench evaluates 480 ambiguous project-building tasks and reports persistent failures on hidden constraints, boundary cases, and long-horizon integration.
- [pAI-Econ-claude: A Gated Human-in-the-Loop Multi-Agent Architecture for AI-Assisted Economic Theory Development](../Inbox/2026-07-23--pai-econ-claude-a-gated-human-in-the-loop-multi-agent-architecture-for-ai-assisted-economic-theory-development.md): The gated workflow assigns human judgment to costly-to-reverse decisions; blinded evaluators preferred it in four of five matched tasks, although one task lost an important mechanism.

## Executable proof traces for security policy task verification
Security benchmark maintainers and compliance teams could require an agent to submit both its operational answer and a formal derivation from an independently authored policy model. Tencent WorkBuddy Bench already separates domain-specific verification and includes security work, while Euclid-MCP can rerun Horn-clause deductions and expose proof trees. The combined evaluation would distinguish a correct-looking answer from one supported by the stated rules: the benchmark verifier would execute the submitted query, compare its conclusion with the task outcome, and inspect whether the derivation uses the required policy clauses. Counterfactual mutations to permissions, thresholds, or dates offer a cheap check against hard-coded answers. This would test auditability rather than assume that the agent’s natural-language-to-logic translation is correct; Euclid-MCP does not report numerical baseline comparisons for that translation step.

### Sources
- [Tencent WorkBuddy Bench: A Multi-Domain Coding-Agent Benchmark with Contamination-Resistant Task Construction](../Inbox/2026-07-23--tencent-workbuddy-bench-a-multi-domain-coding-agent-benchmark-with-contamination-resistant-task-construction.md): WorkBuddy Bench uses different verification instruments by domain and deliberately avoids a suite-wide aggregate score.
- [Euclid-MCP: A Model Context Protocol Server for Deterministic Logical Reasoning via Prolog](../Inbox/2026-07-23--euclid-mcp-a-model-context-protocol-server-for-deterministic-logical-reasoning-via-prolog.md): Euclid-MCP exposes deterministic SWI-Prolog reasoning through MCP with proof traces and derivation logs.

## Cue-triggered specialist review in long research workflows
Teams operating agent-assisted economic research could trigger specialist review when the workflow touches a risky artifact—an equilibrium declaration, welfare claim, counterexample, or canonical-model choice—instead of running every review stage uniformly or relying on the agent to remember prior warnings. pAI-Econ-claude’s gates improved auditability but consumed 4.6 to 18 times the baseline usage allowance. Separately, cue-anchored working memory delivered scoped information reliably across compaction, whereas an agent made no memory calls in 114 turns under the strongest voluntary control. A matched study should seed known proof, premise, and lineage defects, then compare always-on gates, voluntary review, and artifact-triggered review on defect interception, reviewer calls, and token use. The evidence does not yet show that cue-based routing preserves pAI-Econ-claude’s quality gains, so that comparison is the decision-relevant test.

### Sources
- [pAI-Econ-claude: A Gated Human-in-the-Loop Multi-Agent Architecture for AI-Assisted Economic Theory Development](../Inbox/2026-07-23--pai-econ-claude-a-gated-human-in-the-loop-multi-agent-architecture-for-ai-assisted-economic-theory-development.md): Targeted gates reduced mean failure severity from 1.58 to 1.16 and raised usefulness from 2.60 to 3.10, but the full workflow required 4.6–18 times the paired baseline allowance.
- [Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents](../Inbox/2026-07-23--delivery-not-storage-cue-anchored-working-memory-as-a-harness-property-for-coding-agents.md): Voluntary memory produced 0 calls in 114 turns, while deterministic cue delivery survived repeated compaction and logged no false-alarm fires in the reported coding runs.
