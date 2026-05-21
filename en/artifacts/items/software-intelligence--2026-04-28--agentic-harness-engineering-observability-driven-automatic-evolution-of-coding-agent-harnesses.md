---
source: arxiv
url: https://arxiv.org/abs/2604.25850v4
published_at: '2026-04-28T16:55:02'
authors:
- Jiahang Lin
- Shichun Liu
- Chengjun Pan
- Lizhi Lin
- Shihan Dou
- Zhiheng Xi
- Xuanjing Huang
- Hang Yan
- Zhenhua Han
- Tao Gui
- Yu-Gang Jiang
topics:
- coding-agents
- harness-optimization
- software-foundation-models
- code-intelligence
- agent-evaluation
- automated-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses

## Summary
AHE is an automated loop that edits a coding agent's harness using structured rollout evidence and measured edit outcomes. The paper claims it raises Terminal-Bench 2 pass@1 from 69.7% to 77.0% and transfers to SWE-bench-verified and other model families without re-evolution.

## Problem
- Coding-agent performance depends on the harness around the model: prompts, tools, middleware, memory, skills, and execution controls.
- Harness engineering is mostly manual, which slows adaptation when base models, tasks, and tool needs change.
- Automating harness edits is hard because raw trajectories are large, editable parts are heterogeneous, and a pass-rate change can be hard to assign to one edit.

## Approach
- AHE exposes seven editable harness component types as files in NexAU: system prompt, tool description, tool implementation, middleware, skill, sub-agent configuration, and long-term memory.
- It runs task rollouts, cleans traces, and uses Agent Debugger to turn raw trajectories into per-task reports plus a benchmark-level evidence file.
- An Evolve Agent reads that evidence, edits harness files, and writes a manifest for each change with the failure evidence, root cause, fix, expected task gains, and regression risks.
- The next iteration checks those predictions against task-level outcomes and reverts rejected edits at file level.
- The seed harness is intentionally small: one shell tool, no middleware, no skills, no sub-agents.

## Results
- On Terminal-Bench 2, 10 AHE iterations raise pass@1 from 69.7% for NexAU₀ to 77.0%, a +7.3 percentage-point gain across 89 tasks.
- AHE beats OpenCode at 47.2%, Terminus-2 at 62.9%, Codex at 71.9%, ACE at 68.9%, and Training-Free GRPO at 72.3% on Terminal-Bench 2 overall pass@1.
- By Terminal-Bench 2 difficulty, AHE scores 100.0% on Easy, 88.2% on Medium, and 53.3% on Hard; Codex is higher on Hard at 56.7%.
- On SWE-bench-verified, the frozen AHE harness reaches 75.6% success over 500 tasks versus 75.2% for NexAU₀, 74.6% for ACE, and 74.2% for TF-GRPO.
- On SWE-bench-verified token use, AHE uses 461k tokens per trial versus 526k for NexAU₀, 679k for ACE, and 582k for TF-GRPO.
- Cross-model Terminal-Bench 2 transfer is positive for all tested bases, with gains from +2.3 to +10.1 percentage points; examples include deepseek-v4-flash from 51.7% to 61.8%, qwen-3.6-plus from 56.2% to 62.5%, and gemini-3.1-flash-lite-preview from 36.5% to 41.6%. Component ablations show gains mainly from memory, tools, and middleware: memory only reaches 75.3%, tool only 73.0%, middleware only 71.9%, while system-prompt only drops to 67.4% versus the 69.7% seed.

## Link
- [https://arxiv.org/abs/2604.25850v4](https://arxiv.org/abs/2604.25850v4)
