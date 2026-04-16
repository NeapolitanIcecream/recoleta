---
kind: trend
trend_doc_id: 180
granularity: day
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-07T00:00:00'
topics:
- coding-agents
- reinforcement-learning
- verification
- repository-repair
- workflow-automation
run_id: materialize-outputs
aliases:
- recoleta-trend-180
tags:
- recoleta/trend
- topic/coding-agents
- topic/reinforcement-learning
- topic/verification
- topic/repository-repair
- topic/workflow-automation
language_code: en
pass_output_id: 20
pass_kind: trend_synthesis
---

# Software-agent research is converging on explicit rewards and hard verification gates

## Overview
This day’s strongest work makes software agents easier to train, easier to check, and easier to audit. The clearest evidence comes from atomic-skill reinforcement learning, editable test loops in repository repair, and compiled or solver-checked execution paths. The common standard is concrete feedback: unit tests, hidden evaluators, proof obligations, or deterministic code paths.

## Clusters

### Reward design is becoming a core research object
Reinforcement learning work is getting more specific about what the agent is rewarded for and where the reward comes from. The strongest coding result trains one shared policy on five reusable skills, then shows transfer to harder repository tasks: SWE-bench Verified rises from 0.507 to 0.585 and SWE-bench Multilingual from 0.300 to 0.389. SandMLE applies the same idea to machine learning engineering by shrinking full pipelines into verifiable micro-tasks. That cuts execution time from about 200 seconds to under 15 seconds and improves Any Medal rate on MLE-bench-lite by 20.3% to 66.9% relative, with up to 32.4% HumanRank gain on MLE-Dojo.

#### Evidence
- [Scaling Coding Agents via Atomic Skills](../Inbox/2026-04-06--scaling-coding-agents-via-atomic-skills.md): Atomic-skill RL with transfer results across coding benchmarks.
- [Synthetic Sandbox for Training Machine Learning Engineering Agents](../Inbox/2026-04-06--synthetic-sandbox-for-training-machine-learning-engineering-agents.md): Synthetic sandbox RL for MLE agents with large speed and benchmark gains.

### Validation loops now include the spec, the tests, and the simulator
Repository repair papers are treating tests as editable evidence, not just a final gate. Agent-CoEvo keeps populations of code patches and test patches, scores them against each other, and reports 41.33% resolved on SWE-bench Lite and 46.4% on SWT-bench Lite. That is paired with 56.0% ΔC on test quality. The same control-minded attitude appears in StatsClaw, which splits planning, coding, testing, and simulation into isolated roles. In its probit package build, the workflow checks MLE outputs against R `glm` at 10^-6 to 10^-8 tolerance and reports 7 of 7 Monte Carlo acceptance checks passed.

#### Evidence
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): Coevolution of code and tests with benchmark results on SWE-bench Lite and SWT-bench Lite.
- [StatsClaw: An AI-Collaborative Workflow for Statistical Software Development](../Inbox/2026-04-06--statsclaw-an-ai-collaborative-workflow-for-statistical-software-development.md): Isolated workflow and independent validation in statistical software generation.

### External verification is moving into the product path
A second thread is stricter external control over what an agent may ship. Nidus puts requirements, architecture, traceability, and proof obligations into one solver-checked artifact and reports a 100,000-line self-hosted system checked on every commit. Compiled AI pushes control even further for repetitive workflows: the model writes a small function once, then production runs as deterministic code. On BFCL, it reports 96% task completion, 4.5 ms median latency, and break-even against direct LLM use at about 17 transactions. On DocILE, its bounded Code Factory variant reaches 80.4% line item recognition with lower latency than direct runtime inference.

#### Evidence
- [Nidus: Externalized Reasoning for AI-Assisted Engineering](../Inbox/2026-04-06--nidus-externalized-reasoning-for-ai-assisted-engineering.md): Solver-checked engineering governance with every-change verification.
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): Deterministic compiled workflows with cost, latency, and accuracy data.

### Human oversight is being built into the interface, not left to prompt craft
Developer-facing systems are also trying to keep humans oriented while agents do more work. Aporia records explicit design decisions in a Decision Bank and turns them into tests; in a 14-person study, participants' mental models were 5x less likely to disagree with the code than with Claude Code. Tonone takes a different route with a role-based agent pack: 23 specialists and 125 skills for engineering, product, security, and operations. The evidence there is operational and descriptive, not benchmarked, but it shows how quickly multi-role orchestration is becoming a product pattern.

#### Evidence
- [Decision-Oriented Programming with Aporia](../Inbox/2026-04-06--decision-oriented-programming-with-aporia.md): User study on explicit design decisions and understanding accuracy.
- [Inspired by gstack: I stopped prompting Claude and gave it job titles instead](../Inbox/2026-04-06--inspired-by-gstack-i-stopped-prompting-claude-and-gave-it-job-titles-instead.md): Open-source multi-role orchestration system with concrete scope claims but no benchmark.
