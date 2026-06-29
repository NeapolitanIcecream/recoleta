---
kind: ideas
granularity: day
period_start: '2026-05-16T00:00:00'
period_end: '2026-05-17T00:00:00'
run_id: 5f8c222f-020b-4116-9337-9f79d8b46b8b
status: succeeded
topics:
- code agents
- agent benchmarks
- execution feedback
- GPU kernels
- code safety
- token cost
- supply-chain risk
tags:
- recoleta/ideas
- topic/code-agents
- topic/agent-benchmarks
- topic/execution-feedback
- topic/gpu-kernels
- topic/code-safety
- topic/token-cost
- topic/supply-chain-risk
language_code: en
pass_output_id: 157
pass_kind: trend_ideas
upstream_pass_output_id: 156
upstream_pass_kind: trend_synthesis
---

# Controlled code agent operations

## Summary
Code agents are ready for narrower operational tests inside engineering workflows: fixed-budget acceptance runs, package-name checks before installs, and scoped code-editing pilots tied to token spend. The common thread is measurable control around an agent’s actions, outputs, and cost.

## Repository acceptance runs for code agents with time limits and hidden checks
Engineering teams can test code agents on a small set of internal tasks before broad rollout: one isolated workspace, fixed time and token budgets, no network access unless the job needs it, visible tests for iteration, and hidden checks for acceptance. The run should record commands, edits, failures, retries, final score, and cost.

The recent benchmarks point to the same operating pattern. 1GC-7RC gives agents seven ML tasks with locked data preparation, local data, one A100 GPU, no internet, and 40- to 120-minute budgets. AgentKernelArena gates GPU-kernel work through compilation, correctness, timing, and hidden input shapes. TOBench evaluates tool-using agents with executable tasks, MCP tools, workspace state, and task-specific verifiers, while the best reported model reaches 41.0% task success against a 94.0% human benchmark.

A practical internal version can start with 10 to 20 recurring jobs from one team: dependency upgrades, failing-test fixes, small feature flags, data-pipeline patches, or model-training improvements. The acceptance rule should be simple enough to run in CI. If an agent passes only the visible checks, makes broad edits, or spends heavily to finish small tasks, the team learns that before it reaches production review queues.

### Evidence
- [1GC-7RC: One Graphic Card -- Seven Research Challenges! How Good Are AI Agents at Doing Your Job?](../Inbox/2026-05-16--1gc-7rc-one-graphic-card-seven-research-challenges-how-good-are-ai-agents-at-doing-your-job.md): 1GC-7RC describes fixed-budget ML coding-agent tasks with locked preparation, no internet, one A100 GPU, deterministic metrics, and repeated runs.
- [AgentKernelArena: Generalization-Aware Benchmarking of GPU Kernel Optimization Agents](../Inbox/2026-05-16--agentkernelarena-generalization-aware-benchmarking-of-gpu-kernel-optimization-agents.md): AgentKernelArena uses an isolated workspace and gated compilation, correctness, timing, and unseen-shape evaluation for GPU-kernel agents.
- [TOBench: A Task-Oriented Omni-Modal Benchmark for Real-World Tool-Using Agents](../Inbox/2026-05-16--tobench-a-task-oriented-omni-modal-benchmark-for-real-world-tool-using-agents.md): TOBench provides executable tool-use tasks with task-specific verifiers and reports a large gap between current agents and humans.

## Package-name checks for AI-generated install commands and imports
Teams that accept code from agents should add a pre-merge check for new package names in `pip install`, `npm install`, imports, lockfiles, and generated setup files. The check can query PyPI and npm, compare against an approved dependency list, and require review for names that do not exist or have never been used in the repository.

The reason is concrete supply-chain exposure. A replication across Claude Sonnet 4.6, Claude Haiku 4.5, GPT-5.4-mini, Gemini 2.5 Pro, and DeepSeek V3.2 found overall package hallucination rates clustered between 4.62% and 6.10%. The study also found 127 nonexistent package names hallucinated by all five models, including 109 PyPI names and 18 npm names. Those shared names are useful seed data for a denylist, but the main control is registry validation at the point where generated code proposes a dependency.

This is a small CI or pre-commit addition with a clear failure mode: block unknown package names until a human confirms the registry entry, owner, age, and reason for adding it.

### Evidence
- [The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort](../Inbox/2026-05-16--the-range-shrinks-the-threat-remains-re-evaluating-llm-package-hallucinations-on-the-2026-frontier-model-cohort.md): The package-hallucination study reports 4.62% to 6.10% hallucination rates across five code-capable models and identifies 127 nonexistent names shared by all five.
- [The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort](../Inbox/2026-05-16--the-range-shrinks-the-threat-remains-re-evaluating-llm-package-hallucinations-on-the-2026-frontier-model-cohort.md): The paper frames nonexistent package suggestions in install commands and imports as a slopsquatting attack surface for PyPI and npm.

## Scoped code-editing pilots tied to token-spend reporting
Engineering platform teams can run a two-week pilot that forces selected agent edits through symbol- or function-level read and edit commands, then compares token use, edit size, review time, and revert rate against normal full-file agent sessions. The pilot should focus on languages with good Language Server Protocol support and tasks where the target function or definition is known.

The cost pressure is already visible. The Pragmatic Engineer report cites companies seeing about 10x token-spend growth in six months, a seed-stage infrastructure company rising from about $200 to about $3,000 per developer per month, and a SaaS company cutting costs 30% by changing the default model. Agent editing tools are beginning to target the same problem at the code-operation layer. `ane` exposes headless CLI commands that can read or edit a single function body, function name, function definition, line, buffer, or delimiter scope, and returns unified diffs.

The useful test is narrow: pick one repository, route common patch tasks through scoped operations, and measure whether agents stop reading whole files and producing broad patches. If token spend falls without increasing review failures, the team has a concrete editing policy to adopt for agent sessions.

### Evidence
- [Token spend breaks budgets – what next?](../Inbox/2026-05-16--token-spend-breaks-budgets-what-next.md): The token-spend report gives concrete examples of fast-growing coding-agent costs and savings from changing default models.
- [Ane: CLI editor that uses LSPs to let agents explore/edit code with fewer tokens](../Inbox/2026-05-16--ane-cli-editor-that-uses-lsps-to-let-agents-explore-edit-code-with-fewer-tokens.md): The ane summary describes LSP-backed headless commands for narrow reads and edits, with unified diffs for agent use.
- [Ane: CLI editor that uses LSPs to let agents explore/edit code with fewer tokens](../Inbox/2026-05-16--ane-cli-editor-that-uses-lsps-to-let-agents-explore-edit-code-with-fewer-tokens.md): The source text describes ane exec, language-server integration, minimal token usage, and support for Rust, Go, TypeScript/JavaScript, and Python.
