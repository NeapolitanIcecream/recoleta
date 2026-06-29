---
kind: ideas
granularity: day
period_start: '2026-06-09T00:00:00'
period_end: '2026-06-10T00:00:00'
run_id: 2a9044be-37ab-4952-b600-9d4e82016a1f
status: succeeded
topics:
- coding agents
- software engineering
- multi-agent systems
- code security
- benchmarks
- test oracles
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/multi-agent-systems
- topic/code-security
- topic/benchmarks
- topic/test-oracles
language_code: en
pass_output_id: 243
pass_kind: trend_ideas
upstream_pass_output_id: 242
upstream_pass_kind: trend_synthesis
---

# Repository-scale code assistant safeguards

## Summary
Coding-agent evaluation is moving toward executable repository work, source-grounded test generation, and security checks on the context supplied to models. The practical work is to add acceptance tests that span files and dependencies, generate API assertions from implementation evidence, and screen comments, docs, examples, and nearby code before they enter code-generation prompts.

## Repository-scale acceptance suite for coding-agent pilots
Teams buying or deploying coding agents should test them on complete repository builds, not only issue fixes or single-file tasks. A practical suite can start with 10 to 20 internal services or libraries that already have stable Docker builds, meaningful unit tests, and clear documentation. The agent receives capability-level docs and must create the repository layout, APIs, dependencies, and cross-component behavior from scratch. The scoring run should clean out source code, tests, package caches, build artifacts, and Git history before the agent starts, then grade only through executable checks.

DeNovoSWE gives a template for this setup. It selects repositories with stable Docker environments, high original test pass rates, and test coverage filters, then maps tests and traced functions to documented capabilities. The dataset has 4,818 document-to-repository instances, and fine-tuning Qwen3-30B-A3B on it raised BeyondSWE-Doc2Repo performance from 5.8% to 47.2%. EsoLang-Bench adds a useful stress test for internal DSLs and proprietary tools: give the agent a persistent workspace, local execution, and hidden submissions, then measure whether it can learn an unfamiliar executable interface during the session.

### Evidence
- [DeNovoSWE: Scaling Long-Horizon Environments for Generating Entire Repositories from Scratch](../Inbox/2026-06-09--denovoswe-scaling-long-horizon-environments-for-generating-entire-repositories-from-scratch.md): DeNovoSWE describes whole-repository generation tasks, sandbox cleanup, Docker environments, executable checks, and the 5.8% to 47.2% fine-tuning result.
- [Frontier Coding Agents Use Metaprogramming to Adapt to Unfamiliar Programming Languages](../Inbox/2026-06-09--frontier-coding-agents-use-metaprogramming-to-adapt-to-unfamiliar-programming-languages.md): EsoLang-Bench shows how persistent workspaces, local interpreters, and hidden tests expose adaptation ability in unfamiliar executable interfaces.

## Prompt-context security gate for code generation
Code-assistant deployments need a scan of the context they send into generation: comments, docstrings, README excerpts, nearby examples, variable names, and reference snippets. The gate should run before generation and flag insecure instructions, vulnerable examples, suspicious semantic cues such as prototype shortcuts, and risky context placed close to the target function. A post-generation pass should run static analysis, taint checks, and differential checks on the produced code.

The strongest cheap validation is a red-team set built from the team’s own docs and examples. Seed safe tasks with adversarial comments or examples for SQL injection, XSS, hardcoded credentials, path traversal, and insecure cryptography, then measure whether the assistant emits vulnerable code and whether the gate blocks the prompt or output. In the adversarial-context study, vulnerability generation rose from 3.5% to 37.4% across 2,800 trials, and context placed 10 to 50 tokens before the target function reached 62.1% attack success. The paper’s combined detector reported 89.1% detection with 0.3% false positives on a held-out set.

### Evidence
- [Context-Based Adversarial Attacks on AI Code Generators: Vulnerability Analysis and Implications](../Inbox/2026-06-09--context-based-adversarial-attacks-on-ai-code-generators-vulnerability-analysis-and-implications.md): The study reports attacks through comments, documentation, variable names, and examples, with vulnerability rates, nearby-context effects, and detector results.
- [Context-Based Adversarial Attacks on AI Code Generators: Vulnerability Analysis and Implications](../Inbox/2026-06-09--context-based-adversarial-attacks-on-ai-code-generators-vulnerability-analysis-and-implications.md): The abstract states the 2,800-experiment setup and the rise in vulnerability generation under adversarial context.

## Source-grounded semantic oracles for REST API tests
API teams with broad endpoint coverage can add an agent step that reads implementation source code and drafts executable assertions for behavior the OpenAPI spec may miss. The workflow is narrow enough to pilot: for each endpoint, collect the transitive import closure, extract input constraints, response fields, exception paths, side effects, and endpoint relationships, then generate status, field, and cross-operation consistency oracles. A reviewer agent or human tester should check the source evidence behind each assertion before it enters CI.

MASTOR shows why this is worth testing on REST services. It targets failures that status-code, crash, and schema checks miss, including business-logic errors and state-dependent inconsistencies. Across 13 open-source RESTful API projects with 296 operations and 251,303 lines of code, it generated 10,022 oracles and reached a 75.4% average mutation score. On a 50-operation comparison using status and field oracles, it scored 69.9%, compared with 39.8% for Direct Prompting and 20.5% for SATORI.

### Evidence
- [MASTOR: A Multi-Agent Approach to Semantic Test Oracle Generation for RESTful APIs](../Inbox/2026-06-09--mastor-a-multi-agent-approach-to-semantic-test-oracle-generation-for-restful-apis.md): MASTOR details source analysis, oracle generation, reviewer checks, benchmark size, mutation scores, and baseline comparisons.
- [MASTOR: A Multi-Agent Approach to Semantic Test Oracle Generation for RESTful APIs](../Inbox/2026-06-09--mastor-a-multi-agent-approach-to-semantic-test-oracle-generation-for-restful-apis.md): The abstract explains the problem with simple REST API checks and the source-based multi-agent oracle-generation workflow.
