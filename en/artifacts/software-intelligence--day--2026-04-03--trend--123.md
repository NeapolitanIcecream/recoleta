---
kind: trend
trend_doc_id: 123
granularity: day
period_start: '2026-04-03T00:00:00'
period_end: '2026-04-04T00:00:00'
topics:
- coding-agents
- evaluation
- software-engineering
- security
- benchmarks
- competitive-programming
run_id: materialize-outputs
aliases:
- recoleta-trend-123
tags:
- recoleta/trend
- topic/coding-agents
- topic/evaluation
- topic/software-engineering
- topic/security
- topic/benchmarks
- topic/competitive-programming
language_code: en
pass_output_id: 12
pass_kind: trend_synthesis
---

# Coding-agent research is getting harder to game and easier to verify

## Overview
This period is strongest on coding agents that face real state, real failure modes, and real execution consequences. SWE-STEPS and ABTest make evaluation more concrete. GrandCode adds a headline live result, while IndustryCode keeps the ceiling grounded with harder industrial tasks. The current emphasis is less on one-shot patch success and more on whether an agent holds up across time, tools, and repository history.

## Clusters

### Stateful evaluation is becoming the default bar
Evaluation is getting closer to real repository life. SWE-STEPS tests dependent pull-request chains on six Python repositories and shows that isolated PR scoring can overstate success by up to 20 points. Claude Sonnet 4.5 drops from 66.25% to 43.75% on one split, and Gemini 3 Flash drops from 56.52% to 36.59%. The same paper also reports worse repository health under agent-written code, with higher cognitive complexity and technical debt than human baselines. ABTest pushes the same idea from another angle: it converts 400 confirmed user failures into 647 executable cases and finds 642 new true anomalies across Claude Code, Codex CLI, and Gemini CLI. The common message is simple: coding-agent quality now depends on long-horizon behavior, workspace state, and recovery from messy interactions, not only whether a single patch passes tests once.

#### Evidence
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md): Sequential PR benchmark shows inflated isolated scores and repository-health concerns.
- [ABTest: Behavior-Driven Testing for AI Coding Agents](../Inbox/2026-04-03--abtest-behavior-driven-testing-for-ai-coding-agents.md): Behavior-driven fuzzing on real repositories finds many new agent anomalies.

### Coding-agent risk now includes poisoned skills and documentation
Security work is moving into the agent supply chain itself. The skill-poisoning paper shows that a coding agent can copy malicious logic from trusted-looking documentation and execute it during normal setup or coding work. Across 1,070 adversarial skills, the reported bypass rate is 11.6% to 33.5% over four frameworks and five models. Static analysis blocks most attacks, but 2.5% still evade both static checks and model alignment, and the authors report four confirmed vulnerabilities. This matters for current agent products because the attack path runs through ordinary examples and templates inside third-party skills, not only through explicit prompt injection.

#### Evidence
- [Supply-Chain Poisoning Attacks Against LLM Coding Agent Skill Ecosystems](../Inbox/2026-04-03--supply-chain-poisoning-attacks-against-llm-coding-agent-skill-ecosystems.md): Concrete supply-chain attack path and measured bypass rates for coding-agent skills.

### Capability claims are stronger, and the tests are harder
The period also has two strong capability claims, but both come with stricter measurement. GrandCode reports first place in three live Codeforces rounds, ahead of all human participants, and attributes the result to a multi-agent reinforcement learning setup with adversarial test generation and online updates. In a different setting, IndustryCode widens the target for code generation to 125 industrial problems and 579 sub-problems across Python, C++, MATLAB, and Stata. Even the best overall model reaches 68.1% Pass@1 on sub-problems and 42.5% on main problems. Together these papers show that coding performance is being tested at the edges: live contests on one side, production-style industrial tasks on the other.

#### Evidence
- [GrandCode: Achieving Grandmaster Level in Competitive Programming via Agentic Reinforcement Learning](../Inbox/2026-04-03--grandcode-achieving-grandmaster-level-in-competitive-programming-via-agentic-reinforcement-learning.md): Live competitive programming result with repeated first-place finishes.
- [IndustryCode: A Benchmark for Industry Code Generation](../Inbox/2026-04-03--industrycode-a-benchmark-for-industry-code-generation.md): Industrial benchmark quantifies the remaining gap on project-level coding tasks.

### Agent scaffold design is now part of the research signal
One paper in the set asks why agent results vary so much even when model families look similar. The scaffold taxonomy inspects 13 open-source coding agents at the source-code level and finds that 11 combine multiple loop primitives. Tool counts range from zero in Aider to 37 action classes in Moatless Tools, and context compaction spans seven strategies. That does not give a leaderboard result, but it gives a practical explanation for why benchmark numbers are hard to compare across agents. Control loops, tool interfaces, state handling, and execution isolation are still moving parts in their own right.

#### Evidence
- [Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures](../Inbox/2026-04-03--inside-the-scaffold-a-source-code-taxonomy-of-coding-agent-architectures.md): Source-code taxonomy identifies scaffold variation that affects reliability and comparability.
