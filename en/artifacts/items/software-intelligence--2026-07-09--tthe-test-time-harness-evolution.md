---
source: arxiv
url: https://arxiv.org/abs/2607.08124v1
published_at: '2026-07-09T05:53:39'
authors:
- Jun Nie
- Yonggang Zhang
- Jun Song
- Qianshu Cai
- Dahai Yu
- Yike Guo
- Xinmei Tian
- Bo Han
topics:
- test-time-adaptation
- llm-agents
- code-intelligence
- automated-software-production
- agent-harnesses
- multi-agent-software-engineering
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# TTHE: Test-Time Harness Evolution

## Summary
TTHE adapts an LLM agent's executable harness during evaluation by rewriting and selecting harness programs from unlabeled execution traces. Across code, SQL, software engineering, and data-science tasks, it improves a fixed ReAct-style harness without changing model weights or using gold labels during adaptation.

## Problem
- LLM agents often use a fixed control program for context construction, tool use, verification, and failure recovery, so they cannot adjust when test-time failures differ from development failures.
- Existing prompt, workflow, and model adaptation methods usually run before evaluation, update model parameters, revise one response, or require labeled feedback.
- The problem matters because execution traces contain useful signals such as runtime errors, test results, tool outputs, and malformed intermediate artifacts, but these signals do not directly reveal task correctness.

## Approach
- TTHE treats the harness, rather than the model weights, as the state that adapts. The harness is executable Python code around a frozen LLM.
- For each unlabeled test batch, it creates multiple harness branches, runs them, and records prompts, completions, tool calls, outputs, errors, artifacts, and runtime states.
- Agentic proposers edit their own branch using these traces and proxy signals such as execution health, round-trip consistency, and public-test pass rate.
- An agentic judge selects one final branch without seeing gold answers, hidden tests, or reference outputs. The selected harness persists to the next batch.
- The method uses the same frozen backbone for solving, proposing, and judging, so adaptation occurs through code changes rather than weight updates or a separately trained adaptation model.

## Results
- On DeepSeek-V4-Flash, TTHE improved BIRD from 12.0% to 50.0%, LiveCodeBench from 30.0% to 38.3%, SWE-bench Verified from 20.0% to 35.0%, and DS-1000 from 38.0% to 44.0% against the fixed ReAct-style baseline.
- On BIRD, the method improved MiMo V2.5 from 32.0% to 52.0% and Kimi K2.5 from 28.0% to 48.0%.
- The experiments cover five execution-grounded domains, including text-to-SQL, competitive programming, software engineering, data-science coding, and agentic tool use; the excerpt gives exact headline numbers for four domains.
- The gains are transductive: each batch is measured with the harness selected using that batch's unlabeled traces, while gold labels are used only for post-selection evaluation.
- Ablations and trace audits identify non-monotonic search-budget effects, limited candidate coverage, selection regret, and judge errors caused by imperfect execution proxies as key limitations.

## Link
- [https://arxiv.org/abs/2607.08124v1](https://arxiv.org/abs/2607.08124v1)
