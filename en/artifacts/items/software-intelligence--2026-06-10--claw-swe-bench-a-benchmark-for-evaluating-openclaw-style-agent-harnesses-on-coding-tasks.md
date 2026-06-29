---
source: arxiv
url: https://arxiv.org/abs/2606.12344v1
published_at: '2026-06-10T17:16:23'
authors:
- Mengyu Zheng
- Kai Han
- Boxun Li
- Haiyang Xu
- Yuchuan Tian
- Wei He
- Hang Zhou
- Jianyuan Guo
- Hailin Hu
- Lin Ma
- Chao Xu
- Guohao Dai
- Lixue Xia
- Yunchao Wei
- Yunhe Wang
- Yu Wang
topics:
- coding-agents
- swe-bench
- agent-harnesses
- code-intelligence
- benchmarking
- cost-evaluation
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks

## Summary
Claw-SWE-Bench evaluates coding-agent harnesses under one SWE-bench-style scoring contract, so model choice, harness choice, and run cost can be compared on the same tasks. It includes a 350-instance multilingual benchmark and an 80-instance Lite subset for cheaper development runs.

## Problem
- General-purpose agents such as OpenClaw do not directly satisfy the SWE-bench contract: the evaluator expects a clean Docker workspace, a patch in `model_patch`, and repository tests, not an open-ended agent transcript.
- Prior SWE-bench-style reports mix model, harness, prompt, budget, stopping rule, and patch extraction, which makes it hard to tell whether gains come from the LLM or the agent harness.
- Cost matters because coding agents make many tool and model calls; equal Pass@1 can have different API cost, wall-clock time, and cache behavior.

## Approach
- The benchmark fixes the task set, prompt template, Docker workspace, wall-clock budget, patch extraction, prediction format, and SWE-bench evaluator.
- Each harness connects through an adapter with lifecycle methods such as `create_agent`, `send_task`, `backup_session`, `delete_agent`, and `get_docker_args`.
- Candidate patches are taken from the final repository diff under `/testbed`, rather than parsed from the agent’s final text answer.
- The full set contains 350 GitHub issue-resolution instances across 8 programming languages and 43 repositories, drawn from SWE-bench-Multilingual and SWE-bench-Verified-Mini after future-commit cleanup.
- Claw-SWE-Bench Lite selects 80 instances, 10 per language, using cost-aware and rank-aware selection over 17 calibration columns.

## Results
- On the full 350-instance benchmark, OpenClaw with a minimal direct-diff adapter reaches 19.1% Pass@1, while the full adapter reaches 73.4% with the same GLM 5.1 model.
- In the OpenClaw × nine-model sweep, model choice changes Pass@1 by 29.4 percentage points.
- In the five-claw × two-model sweep, harness choice changes Pass@1 by up to 27.4 percentage points under fixed models; the spread is 12.5 pp on GLM 5.1 and 27.4 pp on Qwen 3.6-flash.
- Lite-80 tracks the full set closely across 17 calibration columns: mean Pass@1 is 0.639 on full-350 and 0.643 on Lite-80, a +0.4 pp difference.
- In the 5 claws × 2 models cross-claw check, Lite-80 has 1.88 pp mean absolute Lite-full difference and 3.68 pp maximum difference.
- Lite-80 costs about 22.9% of a full 350-instance run; reported ratios are 22.2% for input tokens, 23.6% for output tokens, 22.6% for cache-read tokens, and 23.0% for wall-clock duration.

## Link
- [https://arxiv.org/abs/2606.12344v1](https://arxiv.org/abs/2606.12344v1)
