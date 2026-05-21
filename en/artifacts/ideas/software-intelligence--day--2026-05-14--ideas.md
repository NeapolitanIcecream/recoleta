---
kind: ideas
granularity: day
period_start: '2026-05-14T00:00:00'
period_end: '2026-05-15T00:00:00'
run_id: a40c39ad-074b-4504-97e5-e94c668f2920
status: succeeded
topics:
- coding agents
- software engineering
- agent safety
- open-ended coding
- sandbox infrastructure
- RAG
- program synthesis
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/agent-safety
- topic/open-ended-coding
- topic/sandbox-infrastructure
- topic/rag
- topic/program-synthesis
language_code: en
pass_output_id: 153
pass_kind: trend_ideas
upstream_pass_output_id: 152
upstream_pass_kind: trend_synthesis
---

# Coding Agent Verification Controls

## Summary
Code-agent work is converging on operational controls that teams can build and test now: sandbox services for rollouts and qualification, per-task permission gates for shell access and skills, and repository context systems with measurable retrieval and documentation quality. The common adoption blocker is verification under real workflow constraints.

## Kubernetes sandbox service for code-agent rollouts and CI qualification
Teams training or evaluating software-engineering agents should separate the execution environment from the agent harness. A small Kubernetes service can own sandbox creation, command execution, file I/O, network policy, teardown, and logs, then expose those actions through a stable API for training runs, evals, and internal pilots.

Orchard shows the shape of this layer: it injects a lightweight execution agent into task containers, avoids the slower Kubernetes exec path on repeated commands, and reports 0.280 s average command latency. The same environment service supports software-engineering, browser-use, and productivity-agent tasks, which matters for teams that already maintain separate harnesses for each domain.

The adoption case is strongest where the sandbox feeds executable qualification: unit tests, compiler output, CI state, logs, and metrics. A review of 92 studies found industrial agent use clustered in phases with executable feedback, while an interview study of 12 companies found stronger experimental agents blocked from production because human review remained the main qualification path. A practical first test is to run an existing code-agent pilot through a sandbox API and record pass rate, command latency, failed-action traces, and CI reproducibility across repeated runs.

### Evidence
- [Orchard: An Open-Source Agentic Modeling Framework](../Inbox/2026-05-14--orchard-an-open-source-agentic-modeling-framework.md): Orchard describes the Kubernetes-native environment service, sandbox lifecycle operations, latency results, and SWE-bench Verified results.
- [Orchard: An Open-Source Agentic Modeling Framework](../Inbox/2026-05-14--orchard-an-open-source-agentic-modeling-framework.md): The paper reports Orchard-SWE results after SFT and RL and describes agent training through repeated sandbox interaction.
- [Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle](../Inbox/2026-05-14--assistance-to-autonomy-a-systematic-literature-review-of-agentic-ai-across-the-software-development-life-cycle.md): The systematic review links industrial adoption to verifiable software phases and executable feedback loops.
- [Agentic AI in Industry: Adoption Level and Deployment Barriers](../Inbox/2026-05-14--agentic-ai-in-industry-adoption-level-and-deployment-barriers.md): The interview study identifies verification as the blocker that keeps stronger experimental agents out of active workflows.

## Per-task read, write, and execute policies before coding-agent shell access
Coding-agent deployments need a preflight permission step before the agent touches a repository or terminal. The step should generate path-level read, write, and execute allowlists for the requested task, audit each granted entry for task grounding and sensitive exposure, then run the agent under that policy in a sandbox.

AuthBench gives teams a concrete evaluation pattern. Full access reached 94.0% task success on sensitive tasks, with 65.8% attack success. Human-reviewed golden permissions reached 81.7% task success with 0.0% attack success. Generated policies still left exposure: Gemini 3.1 Pro reached 85.8% task success on sensitive tasks, with 28.3% attack success.

The same gate should cover third-party skills. Semantic Compliance Hijacking hides malicious intent in natural-language skill instructions, causing the agent to write and run the harmful code during normal work. In the reported tests, prose-only manipulated skills had a 0.00% detection rate under the scanners cited in the paper, while complete leakage and remote-code-execution success rates were high across tested configurations. A useful internal check is a small red-team suite of repository tasks with secrets, benign skills, poisoned skills, and expected allowlists, scored on task success and attack success.

### Evidence
- [Do Coding Agents Understand Least-Privilege Authorization?](../Inbox/2026-05-14--do-coding-agents-understand-least-privilege-authorization.md): AuthBench defines permission-boundary inference and reports task success and attack success under full access, golden permissions, and generated policies.
- [Do Coding Agents Understand Least-Privilege Authorization?](../Inbox/2026-05-14--do-coding-agents-understand-least-privilege-authorization.md): The paper frames least-privilege authorization as a deployment requirement for agents with shell, repository, and file access.
- [Exploiting LLM Agent Supply Chains via Payload-less Skills](../Inbox/2026-05-14--exploiting-llm-agent-supply-chains-via-payload-less-skills.md): The skill-supply-chain paper describes SCH, its attack setup, leakage and RCE success ranges, and scanner detection results.
- [Exploiting LLM Agent Supply Chains via Payload-less Skills](../Inbox/2026-05-14--exploiting-llm-agent-supply-chains-via-payload-less-skills.md): The content chunk reports peak confidentiality and RCE success rates and the 0.00% detection rate for manipulated skill files.

## Repository context tests for coding agents using retriever bakeoffs and dependency-ordered documentation
Developer-tools teams can improve coding-agent reliability by treating repository context as a measured subsystem. Start with a retriever bakeoff for the tasks the agent actually performs: bug repair, code summarization, and code generation. Include BM25 as a baseline, compare dense and hybrid retrieval, and track whether retrieved files support the final patch or answer.

The RAG study separates query processing, retrieval, context refinement, and generation, then tests those parts on Python software tasks. Its main empirical claim is that retriever choices often affect final quality more than the generator, and that BM25 remains competitive across the tested tasks. That finding is useful for teams spending most effort on model swaps while leaving retrieval unmeasured.

Documentation can be part of the same context layer. MemDocAgent generates repository documentation in dependency order, keeps prior claims in memory, verifies consistency, and stores accepted documents for later steps. On 20 Python repositories, the GPT-5-mini run produced 3,323 documents and scored 0.958 completeness, 0.952 truthfulness, and 0.800 helpfulness. A practical rollout is to build docs for one service, run a retrieval evaluation on recent issues or pull requests, and check whether agent patches cite the files and docs that human reviewers consider relevant.

### Evidence
- [Not All RAGs Are Created Equal: A Component-Wise Empirical Study for Software Engineering Tasks](../Inbox/2026-05-14--not-all-rags-are-created-equal-a-component-wise-empirical-study-for-software-engineering-tasks.md): The RAG study compares pipeline components and reports that retriever-side choices often matter more than generator choice for software tasks.
- [Not All RAGs Are Created Equal: A Component-Wise Empirical Study for Software Engineering Tasks](../Inbox/2026-05-14--not-all-rags-are-created-equal-a-component-wise-empirical-study-for-software-engineering-tasks.md): The paper describes the component-wise RAG evaluation across query processing, retrieval, context refinement, and generators.
- [Remember Your Trace: Memory-Guided Long-Horizon Agentic Framework for Consistent and Hierarchical Repository-Level Code Documentation](../Inbox/2026-05-14--remember-your-trace-memory-guided-long-horizon-agentic-framework-for-consistent-and-hierarchical-repository-level-code-documentation.md): MemDocAgent reports dependency-ordered repository documentation, memory, verification, and aggregate documentation quality scores.
- [Remember Your Trace: Memory-Guided Long-Horizon Agentic Framework for Consistent and Hierarchical Repository-Level Code Documentation](../Inbox/2026-05-14--remember-your-trace-memory-guided-long-horizon-agentic-framework-for-consistent-and-hierarchical-repository-level-code-documentation.md): The content chunk explains repository documentation as context for human developers and coding agents navigating large codebases.
