---
source: arxiv
url: https://arxiv.org/abs/2605.26186v2
published_at: '2026-05-25T08:33:15'
authors:
- Zihang Zhou
- Ziqian Ren
- Yukai Wu
- Yingjie Xiong
- Wei Zhou
- Chao Peng
- Dong Zhang
- Bingheng Yan
- Xuanhe Zhou
- Fan Wu
topics:
- llm-agents
- repository-setup
- code-intelligence
- automated-software-engineering
- verification
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# SetupX: Can LLM Agents Learn from Past Failures in Functionality-Correct Code Repository Setup?

## Summary
SETUPX is an LLM-agent system for setting up code repositories so their documented commands and tests run in a reproducible container. It learns reusable setup fixes from past runs, tests them with Docker rollback, and checks results with a separate prosecutor-judge audit.

## Problem
- Repository setup often fails because dependencies, build tools, package installs, and verification steps differ by project.
- Current agents tend to treat each repository as a new case, so they repeat failures instead of reusing fixes from similar repositories.
- Bad setup can look successful when a build or install command exits cleanly, which matters because later software tasks depend on a working execution environment.

## Approach
- SETUPX stores past setup fixes as eXPerience Units (XPUs). Each XPU contains error signals, plain-language advice, executable repair commands, and success/failure telemetry.
- A retriever searches XPUs using the current error state, vector similarity, historical success rate, and an LLM reranker that selects the top 3 entries from 10 candidates.
- The agent tries retrieved fixes inside Docker containers with a LIFO snapshot stack, so it can roll back after failed or later-harmful install attempts.
- An in-loop verifier runs read-only checks during setup and separates setup-induced failures from project-intrinsic bugs.
- A post-hoc Prosecutor-Judge protocol has one agent gather concrete failure charges and another agent independently verify each charge before the final pass/fail verdict.

## Results
- On a curated 100-repository Python benchmark from EnvBench, SETUPX+XPU reports a 92% pass rate.
- It beats Claude Code by 19 percentage points, ExecutionAgent by 33 points, and other specialized tools by 47–54 points under the same prosecutor-judge adjudication.
- SETUPX without XPU reaches 82%, so the XPU memory adds 10 percentage points over the base agent loop.
- On high-difficulty repositories, SETUPX+XPU reaches 79%, compared with 63% for Claude Code and 72% for SETUPX without XPU.
- In domain failure counts, SETUPX+XPU reduces failures from 27 to 8 versus the strongest CLI baseline; in Toolchain repositories, it has 0/20 failures versus 5/20 for the baseline.
- On 22 multi-repository scenarios, SETUPX and Qwen Code both get Full or Mostly on 17/22, but SETUPX gets 6 Full verdicts versus 1 for Qwen Code.

## Link
- [https://arxiv.org/abs/2605.26186v2](https://arxiv.org/abs/2605.26186v2)
