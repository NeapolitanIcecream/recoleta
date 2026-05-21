---
kind: trend
trend_doc_id: 838
granularity: day
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-05T00:00:00'
topics:
- coding agents
- repository repair
- tool calling
- program generation
- software quality
run_id: materialize-outputs
aliases:
- recoleta-trend-838
tags:
- recoleta/trend
- topic/coding-agents
- topic/repository-repair
- topic/tool-calling
- topic/program-generation
- topic/software-quality
language_code: en
pass_output_id: 128
pass_kind: trend_synthesis
---

# Coding agents are being judged by interfaces, token cost, and repository evidence

## Overview
The strongest May 4 work treats large language model (LLM) coding agents as engineering systems with bounded tools, explicit repository state, and measurable cost. Terminus-4B, ARISE, and TSCG give the clearest evidence: smaller specialized components can save tokens or improve repair when the agent receives the right interface.

## Clusters

### Bounded execution and tool interfaces
Agent execution is becoming a costed subsystem. Terminus-4B trains a 4B model to run terminal commands for a coding agent, then return compact summaries to the main agent. The reported Serilog example cuts main-agent tokens from 2.46M to 740k, while the subagent handles nine internal commands and reports build, test, and failure details in about 200 tokens.

TSCG attacks the same deployment pressure at the tool-catalog level. It compiles JSON tool schemas into structured text before the model sees them. The paper reports about 19,000 benchmark calls across 12 models, with large gains for small models at 20 to 50 tools and substantial token savings on production-style schemas. The practical claim is narrow and useful: agents can call tools more reliably when their interface is written for model consumption.

#### Evidence
- [Terminus-4B: Can a Smaller Model Replace Frontier LLMs at Agentic Execution Tasks?](../Inbox/2026-05-04--terminus-4b-can-a-smaller-model-replace-frontier-llms-at-agentic-execution-tasks.md): Terminus-4B summary gives the execution-subagent setup, token reductions, Serilog example, and training corpus details.
- [TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments](../Inbox/2026-05-04--tscg-deterministic-tool-schema-compilation-for-agentic-llm-deployments.md): TSCG summary gives schema-compilation method, benchmark scale, token savings, and tool-use accuracy results.

### Repository repair needs structured code evidence
Repository-level repair papers center on what evidence the agent can inspect before it edits code. ARISE adds statement-level definition-use edges to a repository graph, then exposes slicing and context tools to a SWE-agent setup. On SWE-bench Lite, it reports Function Recall@1 gains of 17.0 points, Line Recall@1 gains of 15.0 points, and 22.0% Pass@1, fixing 66 of 300 issues.

Structured spec-driven engineering (SSDE) makes a related point for generation. It gives LLMs Gherkin scenarios, domain models, generated API signatures, and templates while building Python MVC backends. The pilot shows that generated signatures often help more than raw domain models: across all tested LLMs, signatures improve average test pass rate by 7.82 percentage points and reduce variance. The failure analysis is also useful, since 49.0% of errors are non-existent API calls and 20.2% are type mismatches.

#### Evidence
- [ARISE: A Repository-level Graph Representation and Toolset for Agentic Fault Localization and Program Repair](../Inbox/2026-05-04--arise-a-repository-level-graph-representation-and-toolset-for-agentic-fault-localization-and-program-repair.md): ARISE summary gives repository graph design, SWE-bench Lite setup, localization gains, and Pass@1 results.
- [LLM-Assisted Repository-Level Generation with Structured Spec-Driven Engineering](../Inbox/2026-05-04--llm-assisted-repository-level-generation-with-structured-spec-driven-engineering.md): SSDE summary gives structured inputs, evaluation setup, test-pass changes, and failure categories.

### Program generation is using search and accumulated failure evidence
ARIADNE treats competitive programming as a search problem under a fixed budget. It uses Monte Carlo Tree Search (MCTS) with a shared blackboard that stores constraints, candidate strategies, generated tests, counterexamples, diagnostics, and repair notes. With GPT-4o, it reports Pass@1 of 41.30 on APPS, 46.67 on CodeContests, 27.27 on CodeContests+, and 20.91 on LiveCodeBench, with gains over the listed CodeSim baseline.

This line of work values execution feedback as reusable state. The important detail is the feedback format: ARIADNE combines scalar rewards with structured notes, then sends the search budget toward branches that have better tests and repairs. That design makes hidden edge cases and failed attempts part of the next coding decision.

#### Evidence
- [ARIADNE: Agentic Reward-Informed Adaptive Decision Exploration via Blackboard-Driven MCTS for Competitive Program Generation](../Inbox/2026-05-04--ariadne-agentic-reward-informed-adaptive-decision-exploration-via-blackboard-driven-mcts-for-competitive-program-generation.md): ARIADNE summary gives MCTS and blackboard design, reward structure, datasets, and Pass@1 results.

### Functional tests are not enough for generated software
One paper widens the evaluation target to maintainability. The AI-generated smells study compares LLM outputs on 90 CodeContest problems with human submissions, then audits 20 MetaGPT projects across increasing requirement stages. It reports smell patterns such as Long Method, Too Many Branches, Potential Improper API Usage, Unstable Dependency, and God Class structures.

The evidence is less numeric than the repair and tool-calling papers, but the warning is concrete. Passing code can still accumulate maintenance debt, and larger generated systems need static checks alongside test pass rates. SSDE’s failure analysis supports the same engineering need: many repository-generation errors are API and type mistakes that static analysis can catch before runtime tests.

#### Evidence
- [AI-Generated Smells: An Analysis of Code and Architecture in LLM and Agent-Driven Development](../Inbox/2026-05-04--ai-generated-smells-an-analysis-of-code-and-architecture-in-llm-and-agent-driven-development.md): AI-generated smells summary gives experiments, smell categories, and claims about maintainability debt in generated code.
- [LLM-Assisted Repository-Level Generation with Structured Spec-Driven Engineering](../Inbox/2026-05-04--llm-assisted-repository-level-generation-with-structured-spec-driven-engineering.md): SSDE summary reports static API and type error categories and notes that more than 70% of failures can be detected by static analysis.
