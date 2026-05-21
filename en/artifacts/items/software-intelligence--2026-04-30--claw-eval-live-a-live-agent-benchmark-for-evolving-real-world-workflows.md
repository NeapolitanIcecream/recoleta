---
source: arxiv
url: https://arxiv.org/abs/2604.28139v2
published_at: '2026-04-30T17:23:19'
authors:
- Chenxin Li
- Zhengyang Tang
- Mingxin Huang
- Yunlong Lin
- Shijue Huang
- Shengyuan Liu
- Bowen Ye
- Rang Li
- Lei Li
- Benyou Wang
- Yixuan Yuan
topics:
- agent-benchmark
- workflow-agents
- tool-use
- workspace-repair
- llm-evaluation
- human-ai-interaction
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Claw-Eval-Live: A Live Agent Benchmark for Evolving Real-World Workflows

## Summary
Claw-Eval-Live is a live benchmark for LLM workflow agents that tests whether agents complete real tasks across business services and local workspaces. Its main claim is that agent evaluation needs refreshed task sourcing and grading based on recorded actions, service state, and workspace artifacts.

## Problem
- Static agent benchmarks can age as user workflow demand changes, so their task mix may stop matching current automation needs.
- Final-answer grading can reward fluent reports even when an agent skipped required reads, wrote to the wrong object, or failed to repair the workspace.
- Real workflows often combine service actions and local file or terminal work, while many benchmarks cover only one surface.

## Approach
- The release starts from a time-stamped ClawHub Top-500 public skill snapshot, then clusters workflow patterns and weights task families by signal mass.
- Candidate tasks are built with fixed prompts, fixtures, tools, services, workspaces, and task-specific graders.
- A mixed-integer linear program selects 105 public tasks from 157 screened candidates while enforcing release size, family coverage, and pilot-model discrimination.
- Grading uses deterministic evidence when possible: tool traces, service audit logs, ground-truth fixtures, command traces, post-run files, tests, and service state.
- Structured LLM judging is used only for semantic parts such as completeness or report quality, with GPT-5.4 judging against task rubrics and recorded traces.

## Results
- The public release has 105 tasks across 22 fine-grained families: 87 service-backed workflow tasks and 18 workspace repair tasks.
- It evaluates 13 public models with a pass threshold of 0.80, with default workflow budgets of 24 turns and 300 seconds.
- Claude Opus 4.6 ranks first with 66.7% pass rate, 70 passes out of 105, and 83.6 overall completion score.
- GPT-5.4 ranks second with 63.8% pass rate, 67 passes, and 81.7 overall score.
- Claude Sonnet 4.6 and GLM-5 both pass 61.9% of tasks, with 65 passes each; their overall scores are 79.9 and 78.1.
- No evaluated model reaches a 70% pass rate; the paper reports HR, management, and multi-system business workflows as harder than local workspace repair.

## Link
- [https://arxiv.org/abs/2604.28139v2](https://arxiv.org/abs/2604.28139v2)
