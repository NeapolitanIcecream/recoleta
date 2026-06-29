---
kind: trend
trend_doc_id: 1037
granularity: day
period_start: '2026-05-17T00:00:00'
period_end: '2026-05-18T00:00:00'
topics:
- coding agents
- software engineering benchmarks
- vulnerability repair
- tool calling
- code review
- legacy modernization
run_id: materialize-outputs
aliases:
- recoleta-trend-1037
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/vulnerability-repair
- topic/tool-calling
- topic/code-review
- topic/legacy-modernization
language_code: en
pass_output_id: 158
pass_kind: trend_synthesis
---

# Code agents are being judged by delivered systems and verified repair loops

## Overview
The day’s strongest signal is concrete execution. SaaSBench and WebGameBench score delivered software behavior, while ContraFix and MemRepair improve repair by keeping runtime evidence and prior fixes inside the loop. The current emphasis is operational: setup, integration, validation, and review control decide whether agents are useful.

## Clusters

### Full-stack delivery benchmarks
SaaSBench makes enterprise software delivery the test. Its tasks include long product requirements, Docker runtimes, dependency-ordered validation nodes, multiple languages, databases, and frontend/backend stacks. The best reported Pass@1 is 20.68%, and over 95% of failures happen before deep business logic, often during setup, configuration, integration, premature stopping, or stalled debugging.

WebGameBench gives the same point a user-visible form. Agents build browser games, then a runtime evaluator controls Chrome through Playwright and checks behavior against the requirement. The best configuration reaches 76.9% usable rate, but only 20.2% excellent rate. A page can load and still miss rules, input handling, scoring, restart behavior, or win/loss conditions.

#### Evidence
- [SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering](../Inbox/2026-05-17--saasbench-exploring-the-boundaries-of-coding-agents-in-long-horizon-enterprise-saas-engineering.md): SaaSBench task design, validation setup, and failure results.
- [WebGameBench: Requirement-to-Application Evaluation for Coding Agents via Browser-Native Games](../Inbox/2026-05-17--webgamebench-requirement-to-application-evaluation-for-coding-agents-via-browser-native-games.md): WebGameBench runtime evaluation and usable versus excellent results.

### Vulnerability repair with runtime evidence and memory
Two repair papers make vulnerability fixing a feedback problem. ContraFix compares crashing and safe executions, inserts probes near the fault, and writes a repair specification before patching. On SEC-Bench it resolves 84.0% of 200 C/C++ CVE instances, and its ablation credits contrastive runtime analysis with a 27-point gain.

MemRepair takes a memory-centered route. It stores past fixes, reusable security patterns, and failed-patch-to-success trajectories. A Locator, Patcher, and Verifier loop runs vulnerability and regression tests before accepting edits. On SEC-Bench, MemRepair with DeepSeek-v3.2 resolves 58.00% of tasks, ahead of the listed OpenHands, SWE-agent, and Aider baselines.

#### Evidence
- [ContraFix: Agentic Vulnerability Repair via Differential Runtime Evidence and Skill Reuse](../Inbox/2026-05-17--contrafix-agentic-vulnerability-repair-via-differential-runtime-evidence-and-skill-reuse.md): ContraFix method, SEC-Bench result, and ablation evidence.
- [MemRepair: Hierarchical Memory for Agentic Repository-Level Vulnerability Repair](../Inbox/2026-05-17--memrepair-hierarchical-memory-for-agentic-repository-level-vulnerability-repair.md): MemRepair memory design, verification loop, and benchmark results.

### Verified tool-call data from real APIs
FireFly builds tool-use training data by executing real Model Context Protocol (MCP) APIs first and writing tasks after observed outputs exist. The pipeline filters Smithery servers to 240 servers and 993 tools, builds a directed tool graph, explores live APIs, and caches observed calls for offline reinforcement learning.

The result is a dataset of 5,144 verified tasks and 9,749 trajectories. Qwen3-4B improves from 28.1% to 41.5% pass@1 on the FireFly test after training, close to Claude Sonnet 4.6 at 42.2%. The paper also reports gains on Tau2-Bench, MCP-Atlas, and MCPMark.

#### Evidence
- [Firefly: Illuminating Large-Scale Verified Tool-Call Data Generation from Real APIs](../Inbox/2026-05-17--firefly-illuminating-large-scale-verified-tool-call-data-generation-from-real-apis.md): FireFly data-generation pipeline, dataset scale, and model results.

### Human-controlled software workflows
The code-review paper treats agentic review as a coordinated pull request process with human decision points. Its five stages cover PR creation, PR augmentation, reviewer selection, AI-assisted review, and retrospective. The paper is a vision piece: it reports no new benchmark, prototype evaluation, user study, or controlled experiment.

AgentModernize applies a more testable structure to legacy modernization. It extracts business rules into a Behavioral Specification Graph, generates Python/FastAPI code, and validates behavior through feedback. The results stay low: GPT-5.3-codex reaches 19.4% mean Behavioral Equivalence Rate, while single-prompt and chain-of-thought baselines score 0.0% across tested scenarios.

#### Evidence
- [Rethinking Code Review in the Age of AI: A Vision for Agentic Code Review](../Inbox/2026-05-17--rethinking-code-review-in-the-age-of-ai-a-vision-for-agentic-code-review.md): Agentic code-review workflow and lack of new empirical evaluation.
- [AgentModernize: Preserving Business Logic in Legacy Modernization with Multi-Agent LLMs and Behavioral Specification Graphs](../Inbox/2026-05-17--agentmodernize-preserving-business-logic-in-legacy-modernization-with-multi-agent-llms-and-behavioral-specification-graphs.md): AgentModernize specification graph, validation loop, and behavioral equivalence results.
