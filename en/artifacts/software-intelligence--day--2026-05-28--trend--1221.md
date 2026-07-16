---
kind: trend
trend_doc_id: 1221
granularity: day
period_start: '2026-05-28T00:00:00'
period_end: '2026-05-29T00:00:00'
topics:
- coding agents
- software verification
- code review automation
- vulnerability repair
- agent evaluation
- program analysis
run_id: materialize-outputs
aliases:
- recoleta-trend-1221
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-verification
- topic/code-review-automation
- topic/vulnerability-repair
- topic/agent-evaluation
- topic/program-analysis
language_code: en
pass_output_id: 212
pass_kind: trend_synthesis
---

# Coding agents are being judged by operational evidence, review gates, and executable checks

## Overview
The day’s strongest signal is operational proof for AI coding systems. Papers measure how agents fail in live sessions, gate low-risk review in production, and test generated code against specs or domain invariants. RADAR, TRAILS, and Agora set the emphasis: ship only what can be checked, bounded, or reproduced.

## Findings

### Developer control and production review
Coding agents are now judged inside real developer workflows, not only on finished patches. One large study of 20,574 IDE and command-line sessions found 16,118 evidence-grounded misalignment episodes. Constraint violations were the largest symptom category at 38.33%, and only 9.33% of episodes showed visible resolution in the logs. Most visible fixes required explicit developer pushback.

RADAR shows the production side of the same issue. Meta routes low-risk diffs through source eligibility rules, a Diff Risk Score, large language model review, and deterministic checks before landing. The system reviewed more than 535K diffs and landed more than 331K, with lower revert and production-incident rates than non-RADAR diffs in the reported deployment.

#### Sources
- [How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions](../Inbox/2026-05-28--how-coding-agents-fail-their-users-a-large-scale-analysis-of-developer-agent-misalignment-in-20574-real-world-sessions.md): Large-scale real-world session analysis with misalignment categories, costs, and resolution rates.
- [Automating Low-Risk Code Review at Meta: RADAR, Risk Calibration, and Review Efficiency](../Inbox/2026-05-28--automating-low-risk-code-review-at-meta-radar-risk-calibration-and-review-efficiency.md): Production deployment of risk-calibrated automated code review at Meta.

### Executable evidence for generated software
Several papers treat correctness as a behavior claim that needs concrete checks. TRAILS targets the oracle problem for generated code by executing candidate programs on generated inputs, then asking a large language model to judge each input-output pair against the natural-language specification. On LiveCodeBench and CoCoClaNeL, it improves Matthew correlation coefficient over zero-shot chain-of-thought baselines, with higher token cost per task.

Projectional decoding adds checks during generation. It keeps a partial graph model beside the token stream and masks tokens that violate semantic constraints. On CLEVR domain-specific language programs, semantic validity reaches 73.33% to 79.67% across Qwen3 models. CODEFUSE-DeBench adds a caution for reverse engineering: recompilation alone is a weak proxy, since the best decompiler plus repair model reached 22.3% exact-plus-partial behavioral overlap and only 1.2% exact stdout match.

#### Sources
- [Inferring Code Correctness from Specification](../Inbox/2026-05-28--inferring-code-correctness-from-specification.md): TRAILS evaluates generated code by executing inputs and judging outputs against specifications.
- [Projectional Decoding: Towards Semantic-Aware LLM Generation](../Inbox/2026-05-28--projectional-decoding-towards-semantic-aware-llm-generation.md): Projectional decoding enforces semantic constraints during generation and reports CLEVR DSL validity gains.
- [CODEFUSE-DEBENCH: An Empirical Study on Readability, Recompilability, and Functionality](../Inbox/2026-05-28--codefuse-debench-an-empirical-study-on-readability-recompilability-and-functionality.md): DeBench measures readability, recompilability, and behavioral functionality for decompiled code.

### Security failures, repair memory, and pre-generation signals
Security work in this period focuses on two practical failure modes: small prompt changes that create vulnerable code, and repair agents that forget useful fixes. The prompt-fragility study uses CWEval across five languages and finds that a single-character mutation can flip secure output to vulnerable output. Hidden-state probes reach about 0.70 mean held-out AUC for predicting the joint functional-secure target, with input-handling vulnerabilities easier to predict than secure-defaults flaws.

EvoRepair addresses repair repetition by storing scored repair experience across vulnerability attempts. Its loop retrieves related CVE or CWE experience, patches in Docker, summarizes the trajectory, and updates an experience bank. Using GPT-5-mini, it reports 93.47% on PATCHEVAL and 87.00% on SEC-bench, ahead of 12 automated vulnerability repair baselines in the paper’s comparison.

#### Sources
- [Minimal Prompt Perturbations Lead to Code Vulnerabilities: Prompt Fragility and Hidden-State Signals in Coding LLMs](../Inbox/2026-05-28--minimal-prompt-perturbations-lead-to-code-vulnerabilities-prompt-fragility-and-hidden-state-signals-in-coding-llms.md): Prompt perturbation study showing security flips and hidden-state vulnerability prediction results.
- [EvoRepair: Enhancing Vulnerability Repair Agents Through Experience-Based Self-Evolution](../Inbox/2026-05-28--evorepair-enhancing-vulnerability-repair-agents-through-experience-based-self-evolution.md): Experience-based vulnerability repair agent with PATCHEVAL and SEC-bench results.

### Domain-aware agents for protocol bugs
Agora shows that protocol bug finding needs agents with explicit state and domain constraints. The system splits work across an orchestrator, a strategy agent, and a test-generation agent. It creates hypotheses with trigger conditions, action sequences, expected faulty behavior, and oracle checks.

On Raft, EPaxos, HotStuff, and BullShark implementations, Agora reports 15 previously unknown protocol-level safety bugs. ReAct-style baselines using GPT-5.2, Gemini 3.0 Pro Preview, Claude Sonnet 4.5, and Qwen3 Coder found 22 implementation bugs in total, but no protocol-level logic bugs in the reported tests.

#### Sources
- [Agora: Toward Autonomous Bug Detection in Production-Level Consensus Protocols with LLM Agents](../Inbox/2026-05-28--agora-toward-autonomous-bug-detection-in-production-level-consensus-protocols-with-llm-agents.md): Agora’s multi-agent protocol testing method and reported consensus-bug findings.
