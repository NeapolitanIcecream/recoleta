---
kind: trend
trend_doc_id: 161
granularity: day
period_start: '2026-04-05T00:00:00'
period_end: '2026-04-06T00:00:00'
topics:
- coding-agents
- software-engineering
- compiler-feedback
- software-architecture
- agent-control
run_id: materialize-outputs
aliases:
- recoleta-trend-161
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/compiler-feedback
- topic/software-architecture
- topic/agent-control
language_code: en
pass_output_id: 16
pass_kind: trend_synthesis
---

# Software-agent evidence is getting tighter around control loops, compilers, and architecture checks

## Overview
This day’s research is strongest on software agents that can be checked by explicit controls. The best-grounded work ties models to compilers, ticket states, verifier gates, or benchmarked design artifacts. That produces clearer evidence on what agents can do now, and where reliability still breaks, especially in architecture understanding.

## Clusters

### Agent work is being specified through control rules and architecture constraints
Production-oriented agent work is getting more explicit about control surfaces. The strongest evidence is a Jira-backed loop that keeps AI inside fixed state transitions, confidence thresholds, isolated worktrees, and verifier gates. In its initial window, the system reports 152 runs with 100% terminal-state success and later more than 795 run artifacts. A separate architecture paper makes the complementary point: prompt wording now changes the system shape itself. In its case study, the same chatbot task grew from 141 lines and 2 files to 827 lines and 6 files when the prompt added structured output and tool access. The common thread is simple: agent capability is being packaged with workflow rules, review points, and architecture awareness, because those choices affect what gets built and how safely it runs.

#### Evidence
- [Closed-Loop Autonomous Software Development via Jira-Integrated Backlog Orchestration: A Case Study in Deterministic Control and Safety-Constrained Automation](../Inbox/2026-04-05--closed-loop-autonomous-software-development-via-jira-integrated-backlog-orchestration-a-case-study-in-deterministic-control-and-safety-constrained-automation.md): Deterministic control loop, bounded automation, and reported production results.
- [Architecture Without Architects: How AI Coding Agents Shape Software Architecture](../Inbox/2026-04-05--architecture-without-architects-how-ai-coding-agents-shape-software-architecture.md): Prompt wording changes architecture size and components.

### Compiler-grounded coding systems are posting stronger domain results
Compiler feedback is showing up as a practical way to make code agents useful in narrower domains. ACCLAIM combines language-model rewrites with ordinary compiler passes across C source, LLVM IR, and assembly, and reports a mean 1.25× speedup over clang -O3. In COBOL, the emphasis is even more concrete. COBOL-Coder gets 73.95% compilation success and 49.33 Pass@1 on COBOLEval, well above GPT-4o in the reported setup. COBOLAssist then shows what a repair loop can add after generation: GPT-4o rises from 41.8% to 95.89% compilation success when compiler errors are fed back into revision. The practical message is that domain-specific code generation improves when the model is tied to compilers, tests, and iterative repair, not just prompted once.

#### Evidence
- [Agentic Code Optimization via Compiler-LLM Cooperation](../Inbox/2026-04-05--agentic-code-optimization-via-compiler-llm-cooperation.md): Compiler-LLM cooperation for optimization with reported speedup over clang -O3.
- [COBOL-Coder: Domain-Adapted Large Language Models for COBOL Code Generation and Translation](../Inbox/2026-04-05--cobol-coder-domain-adapted-large-language-models-for-cobol-code-generation-and-translation.md): Domain-adapted COBOL model with strong code generation and translation results.
- [COBOLAssist: Analyzing and Fixing Compilation Errors for LLM-Powered COBOL Code Generation](../Inbox/2026-04-05--cobolassist-analyzing-and-fixing-compilation-errors-for-llm-powered-cobol-code-generation.md): Compiler-guided repair loop sharply raises COBOL compilation success.

### Architecture reasoning remains weaker than code-time assistance
Design-stage understanding is still a weak point for multimodal software tools. SADU tests vision-language models on 154 software architecture diagrams and 2,431 question-answer tasks. The best reported overall accuracy is 70.18%, while some widely used models are far lower, including 17.77% for gpt-4o-mini in this benchmark. Accuracy drops further as diagrams get more complex, especially on behavioral diagrams and relation-heavy retrieval questions. That matters because agent systems are already making architecture choices during generation, but their ability to read diagram evidence is still limited. The corpus points to a gap between code-time assistance and design-time understanding.

#### Evidence
- [Benchmarking and Evaluating VLMs for Software Architecture Diagram Understanding](../Inbox/2026-04-05--benchmarking-and-evaluating-vlms-for-software-architecture-diagram-understanding.md): Benchmark evidence on VLM weakness for software architecture diagrams.
- [Architecture Without Architects: How AI Coding Agents Shape Software Architecture](../Inbox/2026-04-05--architecture-without-architects-how-ai-coding-agents-shape-software-architecture.md): Architecture decisions are already happening in coding-agent workflows.
