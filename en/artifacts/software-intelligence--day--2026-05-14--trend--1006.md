---
kind: trend
trend_doc_id: 1006
granularity: day
period_start: '2026-05-14T00:00:00'
period_end: '2026-05-15T00:00:00'
topics:
- coding agents
- software engineering
- agent safety
- open-ended coding
- sandbox infrastructure
- RAG
- program synthesis
run_id: materialize-outputs
aliases:
- recoleta-trend-1006
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/agent-safety
- topic/open-ended-coding
- topic/sandbox-infrastructure
- topic/rag
- topic/program-synthesis
language_code: en
pass_output_id: 152
pass_kind: trend_synthesis
---

# Code agents are being built around executable feedback and explicit operating limits

## Overview
The day’s strongest signal is practical code-agent work under executable checks. FrontierSmith and DIO-Agent use scoring or execution errors to make coding tasks harder and more useful. Orchard shows the same need at sandbox scale. Safety papers make permissions and third-party skills part of the core design problem.

## Findings

### Open-ended coding data and program discovery
FrontierSmith treats open-ended coding as a data problem. It mutates closed competitive-programming tasks into optimization tasks, filters for solution diversity, and builds scoring verifiers. Training Qwen3.5 models on 200 synthesized problems raises FrontierCS by 8.82 points for the 9B model and 12.12 points for the 27B model, with large gains on ALE-bench as well.

DIO-Agent addresses a related gap: code synthesis when only input-output examples are available. It runs an evolutionary loop where a large language model (LLM) edits code, execution gives concrete errors, and a curriculum adds harder cases over time. On IO2CodeBench with DeepSeek V3.2, it reaches a 58.63 average pass rate, ahead of CodeEvolve at 49.60 and AlphaEvolve at 47.29. The common lesson is simple: stronger coding systems need task signals richer than one prompt and one answer.

#### Sources
- [FrontierSmith: Synthesizing Open-Ended Coding Problems at Scale](../Inbox/2026-05-14--frontiersmith-synthesizing-open-ended-coding-problems-at-scale.md): FrontierSmith summary, method, and reported gains on FrontierCS and ALE-bench.
- [From I/O to Code with Discovery Agent](../Inbox/2026-05-14--from-i-o-to-code-with-discovery-agent.md): DIO-Agent benchmark setup, evolutionary method, ablations, and pass-rate results.

### Sandboxed training infrastructure
Orchard makes agent training a systems problem. Its Kubernetes-native environment service handles sandbox creation, command execution, file I/O, network policy, and cleanup. The same layer supports software-engineering, browser-use, and personal-assistant agents. Orchard-SWE reports 67.5% on SWE-bench Verified after supervised fine-tuning (SFT) and reinforcement learning (RL), while the environment service reports 0.280 s average command latency.

Two broader studies explain why this matters for adoption. A systematic review of 92 primary studies finds that industrial agent use clusters where outputs can be checked by tests, compilers, logs, metrics, or continuous-integration state. An interview study of 12 companies finds most production use at assistant or task-agent levels. Four companies had stronger experimental agents, but could not deploy them because human review remained the main qualification path.

#### Sources
- [Orchard: An Open-Source Agentic Modeling Framework](../Inbox/2026-05-14--orchard-an-open-source-agentic-modeling-framework.md): Orchard environment design, training recipes, SWE-bench result, latency, and cost claims.
- [Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle](../Inbox/2026-05-14--assistance-to-autonomy-a-systematic-literature-review-of-agentic-ai-across-the-software-development-life-cycle.md): Systematic review evidence on SDLC phases, industrial contexts, and executable feedback.
- [Agentic AI in Industry: Adoption Level and Deployment Barriers](../Inbox/2026-05-14--agentic-ai-in-industry-adoption-level-and-deployment-barriers.md): Industry interview evidence on maturity levels and deployment barriers.

### Permissions and agent supply-chain risk
AuthBench turns least-privilege access into a measurable coding-agent task. Models must infer read, write, and execute allowlists before a terminal task runs. Full access gives high task success on sensitive tasks, but also a 65.8% attack success rate. Golden permissions keep attack success at 0.0%. Generated policies still trade utility against exposure: Gemini 3.1 Pro reaches 85.8% task success on sensitive tasks, with 28.3% attack success.

The skill-supply-chain paper shows a second control gap. Semantic Compliance Hijacking (SCH) hides malicious intent in natural-language skill instructions, causing the agent to write and run the harmful code itself. Across tested platforms and models, the attack reaches 36.00% to 62.11% complete leakage rates and 30.56% to 64.44% remote-code-execution success rates. Initial prose-only skills have a 0.00% detection rate under the scanners reported in the paper.

#### Sources
- [Do Coding Agents Understand Least-Privilege Authorization?](../Inbox/2026-05-14--do-coding-agents-understand-least-privilege-authorization.md): AuthBench task definition, permission metrics, sensitive-task results, and decomposition method.
- [Exploiting LLM Agent Supply Chains via Payload-less Skills](../Inbox/2026-05-14--exploiting-llm-agent-supply-chains-via-payload-less-skills.md): Payload-less skill attack setup, evaluation scope, leakage/RCE results, and detection results.

### Repository and runtime context management
Several papers focus on how agents choose and preserve the right evidence. The software-engineering retrieval-augmented generation (RAG) study separates query processing, retrieval, context refinement, and generation. Its main empirical claim is that retriever choices often affect final quality more than generator choice, and that BM25 remains strong across tested software tasks.

MemDocAgent applies a similar concern to repository documentation. It keeps one long-running memory over dependency-ordered documentation work, verifies factual consistency, and stores prior claims. On 20 Python repositories, its GPT-5-mini run produces 3,323 documents and scores 0.958 completeness, 0.952 truthfulness, and 0.800 helpfulness. RCLAgent applies evidence control to microservice failures by assigning agents to trace spans and combining local findings up the trace graph, reporting about 7.51% higher accuracy than the second-best root-cause localization method and more than 1.75× speedup over other LLM-based methods.

#### Sources
- [Not All RAGs Are Created Equal: A Component-Wise Empirical Study for Software Engineering Tasks](../Inbox/2026-05-14--not-all-rags-are-created-equal-a-component-wise-empirical-study-for-software-engineering-tasks.md): Component-wise RAG study design, corpus size, and main retriever-side claim.
- [Remember Your Trace: Memory-Guided Long-Horizon Agentic Framework for Consistent and Hierarchical Repository-Level Code Documentation](../Inbox/2026-05-14--remember-your-trace-memory-guided-long-horizon-agentic-framework-for-consistent-and-hierarchical-repository-level-code-documentation.md): MemDocAgent memory design, verification method, and repository documentation results.
- [Towards In-Depth Root Cause Localization for Microservices with Multi-Agent Recursion-of-Thought](../Inbox/2026-05-14--towards-in-depth-root-cause-localization-for-microservices-with-multi-agent-recursion-of-thought.md): RCLAgent trace-span decomposition, benchmarks, accuracy claim, and speedup claim.
