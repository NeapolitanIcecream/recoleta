---
kind: trend
trend_doc_id: 163
granularity: week
period_start: '2026-03-30T00:00:00'
period_end: '2026-04-06T00:00:00'
topics:
- coding-agents
- evaluation
- runtime-verification
- context-control
- software-engineering
run_id: materialize-outputs
aliases:
- recoleta-trend-163
tags:
- recoleta/trend
- topic/coding-agents
- topic/evaluation
- topic/runtime-verification
- topic/context-control
- topic/software-engineering
language_code: en
pass_output_id: 18
pass_kind: trend_synthesis
---

# Software-agent research is tightening around executable evidence and control loops

## Overview
This week’s software-agent research is strongest when claims can be checked by execution and explicit controls. The center of gravity is practical: harder evaluation, tighter context and permission boundaries, and stronger use of compiler, test, and runtime signals. ProdCodeBench, SWE-STEPS, and Squeez capture the emphasis well.

## Clusters

### Stateful evaluation is becoming the default bar
Evaluation is getting closer to real software work. Daily trend syntheses repeatedly center on execution, replay, and repository state. SWE-STEPS and ABTest make agents act across sequential changes and behavior-driven tests. ProdCodeBench and IndustryCode keep claims tied to production-derived or industrial tasks. The common bar is simple: an agent has to survive state, tools, and longer task horizons.

#### Evidence
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md)
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md)
- [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](../Inbox/2026-04-01--reproducible-explainable-and-effective-evaluations-of-agentic-ai-for-software-engineering.md)
- [ABTest: Behavior-Driven Testing for AI Coding Agents](../Inbox/2026-04-03--abtest-behavior-driven-testing-for-ai-coding-agents.md)
- [BACE: LLM-based Code Generation through Bayesian Anchored Co-Evolution of Code and Test Populations](../Inbox/2026-03-30--bace-llm-based-code-generation-through-bayesian-anchored-co-evolution-of-code-and-test-populations.md)
- [ToolMisuseBench: An Offline Deterministic Benchmark for Tool Misuse and Recovery in Agentic Systems](../Inbox/2026-04-02--toolmisusebench-an-offline-deterministic-benchmark-for-tool-misuse-and-recovery-in-agentic-systems.md)

### Context and action control are being specified more explicitly
Control over the agent loop is now a core research surface. The week’s strongest summaries emphasize what agents may read, remember, run, and modify. Squeez targets context bloat. AmPermBench checks permission coverage. Earlier in the week, work on code-context compression and NL/PL boundary analysis set the same direction: tighter inputs and clearer action boundaries produce cleaner evidence than broad prompt expansion.

#### Evidence
- [Context Engineering: A Practitioner Methodology for Structured Human-AI Collaboration](../Inbox/2026-04-05--context-engineering-a-practitioner-methodology-for-structured-human-ai-collaboration.md)
- [Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents](../Inbox/2026-04-04--squeez-task-conditioned-tool-output-pruning-for-coding-agents.md)
- [Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures](../Inbox/2026-04-03--inside-the-scaffold-a-source-code-taxonomy-of-coding-agent-architectures.md)
- [Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode](../Inbox/2026-04-04--measuring-the-permission-gate-a-stress-test-evaluation-of-claude-code-s-auto-mode.md)
- [KAIJU: An Executive Kernel for Intent-Gated Execution of LLM Agents](../Inbox/2026-03-31--kaiju-an-executive-kernel-for-intent-gated-execution-of-llm-agents.md)
- [Architecture Without Architects: How AI Coding Agents Shape Software Architecture](../Inbox/2026-04-05--architecture-without-architects-how-ai-coding-agents-shape-software-architecture.md)

### Trusted signals come from compilers, tests, and verifier gates
Verification signals are moving inside generation and repair loops. The daily syntheses point to code execution, proof obligations, test behavior, compiler checks, and verifier gates as the signals researchers trust most. Think-Anywhere and WybeCoder fit this pattern early in the week. By the end, compiler-LLM cooperation and safety-constrained backlog orchestration extend the same idea into optimization and broader development workflows.

#### Evidence
- [WybeCoder: Verified Imperative Code Generation](../Inbox/2026-03-31--wybecoder-verified-imperative-code-generation.md)
- [VeriAct: Beyond Verifiability -- Agentic Synthesis of Correct and Complete Formal Specifications](../Inbox/2026-03-31--veriact-beyond-verifiability-agentic-synthesis-of-correct-and-complete-formal-specifications.md)
- [Measuring LLM Trust Allocation Across Conflicting Software Artifacts](../Inbox/2026-04-03--measuring-llm-trust-allocation-across-conflicting-software-artifacts.md)
- [COBOL-Coder: Domain-Adapted Large Language Models for COBOL Code Generation and Translation](../Inbox/2026-04-05--cobol-coder-domain-adapted-large-language-models-for-cobol-code-generation-and-translation.md)
- [Fuzzing with Agents? Generators Are All You Need](../Inbox/2026-04-01--fuzzing-with-agents-generators-are-all-you-need.md)
- [COBOLAssist: Analyzing and Fixing Compilation Errors for LLM-Powered COBOL Code Generation](../Inbox/2026-04-05--cobolassist-analyzing-and-fixing-compilation-errors-for-llm-powered-cobol-code-generation.md)

### Failure analysis is focusing on exposed operational risks
Risk analysis is getting concrete. The trend documents highlight prompt-injection exposure, long-term code churn, poisoned skills, and weak architecture understanding. These are not abstract safety notes. They appear alongside repository-scale studies and explicit controls, which makes failure modes easier to inspect and compare. Architecture work still looks less stable than code-time assistance, even when the rest of the loop is well instrumented.

#### Evidence
- [Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure](../Inbox/2026-04-02--beyond-resolution-rates-behavioral-drivers-of-coding-agent-success-and-failure.md)
- [No-AI code analysis found issue in HF tokenizers](../Inbox/2026-04-03--no-ai-code-analysis-found-issue-in-hf-tokenizers.md)
- [LLM-Enabled Open-Source Systems in the Wild: An Empirical Study of Vulnerabilities in GitHub Security Advisories](../Inbox/2026-04-05--llm-enabled-open-source-systems-in-the-wild-an-empirical-study-of-vulnerabilities-in-github-security-advisories.md)
- [ClawSafety: "Safe" LLMs, Unsafe Agents](../Inbox/2026-04-01--clawsafety-safe-llms-unsafe-agents.md)
- [ABTest: Behavior-Driven Testing for AI Coding Agents](../Inbox/2026-04-03--abtest-behavior-driven-testing-for-ai-coding-agents.md)
- [When Labels Are Scarce: A Systematic Mapping of Label-Efficient Code Vulnerability Detection](../Inbox/2026-03-31--when-labels-are-scarce-a-systematic-mapping-of-label-efficient-code-vulnerability-detection.md)
