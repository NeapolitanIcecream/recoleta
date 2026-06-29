---
source: arxiv
url: https://arxiv.org/abs/2606.26978v1
published_at: '2026-06-25T12:49:59'
authors:
- Zhihao Lin
- Junhua Zhu
- Mingyi Zhou
- Xin Wang
- Zhensu Sun
- Renyu Yang
- David Lo
- Li Li
topics:
- program-repair
- code-agents
- swe-bench
- test-execution
- cost-effectiveness
- code-intelligence
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair

## Summary
The paper finds that letting LLM repair agents run tests adds little repair accuracy on the studied SWE-bench tasks while adding large token, time, and environment costs. Its main claim is that agents should decide when execution is worth paying for instead of running tests by default.

## Problem
- LLM program-repair agents often use a loop of inspecting code, editing, running tests, and revising patches.
- Running project tests costs tokens, wall-clock time, and per-repository environment setup.
- Prior SWE-bench results usually mix agent design changes with execution access, so they do not isolate how much test execution itself helps.

## Approach
- The study first analyzes 7,745 public SWE-bench agent traces from SWE-agent, OpenHands, LiveSWEAgent, and Mini-SWE-agent across 12 LLMs.
- It then runs 3,000 controlled repair attempts on 200 SWE-bench instances: 100 Lite and 100 Verified.
- The controlled runs use Claude Code with Claude Sonnet 4.5, Codex with GPT-5.2-xhigh, and OpenCode with Qwen2.5-Coder-32B-Instruct.
- The researchers keep the agent and task fixed while changing execution access: Prohibited, Quota-1, Quota-3, Budget-Guided, and Unrestricted.
- They measure resolve rate, token use, wall-clock time, execution count, localization accuracy, single-edit ratio, and whether agent-run tests match official SWE-bench evaluation.

## Results
- In 7,745 public traces, agents run tests on average 8.8 times per task, with a range of 2.0 to 18.7 executions per task across agent-model pairs.
- Late-stage executions have higher pass rates than early executions; one reported case, OpenHands with Claude-3.5-Sonnet, rises from 42% early to 72% late, and the average execution success rate is 57.9%.
- On commercial agents, the resolve-rate gap between Prohibited and Unrestricted is 1.25 percentage points and is not statistically significant by McNemar's test (p > 0.05).
- Claude Code resolves 63% without execution and 64% with unrestricted execution, while Prohibited saves 56% of tokens and 48% of wall-clock time.
- OpenCode with Qwen2.5-Coder-32B resolves 10% in both Prohibited and Unrestricted modes and uses about 3x fewer tokens without execution.
- For commercial agents, 54-66% of cases finish in a single edit, localization accuracy under Prohibited stays above 95%, and 81-100% of failed cases pass the agent's own validation but fail official SWE-bench evaluation.

## Link
- [https://arxiv.org/abs/2606.26978v1](https://arxiv.org/abs/2606.26978v1)
