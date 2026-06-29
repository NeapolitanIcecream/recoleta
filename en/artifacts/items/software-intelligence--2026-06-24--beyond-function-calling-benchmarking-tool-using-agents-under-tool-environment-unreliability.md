---
source: arxiv
url: https://arxiv.org/abs/2606.25819v1
published_at: '2026-06-24T13:34:34'
authors:
- Yang Tian
- Zhengpeng Shi
- Bo Zhao
topics:
- tool-using-agents
- agent-benchmarks
- unreliable-tools
- recovery-evaluation
- llm-agents
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability

## Summary
ToolBench-X tests whether LLM agents can finish multi-step tool tasks when tools fail, drift, or disagree. The paper finds that current agents often fail on recoverable hazards because they misdiagnose the tool problem and choose weak recovery actions.

## Problem
- Existing tool-use benchmarks often score correct function calls in clean environments, while real tools have stale docs, renamed fields, timeouts, changed output formats, and conflicting sources.
- This matters because an agent can call the right function and still give the wrong final answer if it trusts incomplete, shifted, or contradictory tool output.
- The benchmark needs recoverable hazards so failures can be tied to diagnosis, verification, and recovery behavior.

## Approach
- The authors build ToolBench-X with 1,106 executable tasks and 4,956 Python tools across 7 domains. Each task has deterministic tools and a canonical final answer for automatic evaluation.
- The task workflows are balanced: 378 sequential tasks (34.2%), 358 parallel tasks (32.4%), and 370 mixed tasks (33.5%).
- They inject 5 recoverable hazard types: Specification Drift 141 (12.7%), Invocation Error 173 (15.6%), Execution Failure 265 (24.0%), Output Drift 264 (23.9%), and Cross-source Conflict 263 (23.8%).
- Each injected task keeps at least 1 valid recovery path, such as retrying, using a fallback tool, normalizing output, checking evidence, or resolving conflicting sources.
- They evaluate 12 LLMs with final-task accuracy, using either backend execution-state match or explicit ground-truth answer match.

## Results
- No evaluated model reaches 0.60 overall accuracy on ToolBench-X. The best model is Doubao-Seed-2.0-Lite at 0.513, followed by GPT-5.4 at 0.453, DeepSeek-V4-Pro at 0.425, GLM-5.1 at 0.420, Qwen-3.5-35B-A3B-Thinking at 0.419, and Gemini-3.1-Flash at 0.416.
- Qwen-3.5-35B-A3B-Thinking scores 0.419, beating GPT-4o at 0.359 and improving over Qwen-3.5-35B-A3B at 0.372 by 0.047 absolute accuracy.
- Parallel tasks are easiest on average, with 0.421 accuracy. The paper reports that sequential dependencies cause more error accumulation than parallel calls.
- Output Drift is the easiest hazard, with average accuracy 0.581. Invocation Error is the hardest, with average accuracy about 0.260, a gap of about 0.321.
- After the first failed tool response, agents retry the same tool in 44% to 76% of trajectories, while direct termination stays below 12%. High retry rates do not track overall accuracy, so the failure point is diagnosis and recovery choice.
- On a 200-task diagnostic subset, clean-tool Oracle accuracy is 35 to 50 points above the exception-injected baseline. Targeted hints raise accuracy by 25.5 to 35.5 points and recover about 60% to 80% of the lost accuracy; 10 extra interaction rounds without hints help less.

## Link
- [https://arxiv.org/abs/2606.25819v1](https://arxiv.org/abs/2606.25819v1)
