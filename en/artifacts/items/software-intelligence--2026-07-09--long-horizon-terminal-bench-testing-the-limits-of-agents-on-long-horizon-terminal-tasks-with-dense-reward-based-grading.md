---
source: arxiv
url: https://arxiv.org/abs/2607.08964v1
published_at: '2026-07-09T21:56:37'
authors:
- Zongxia Li
- Zhongzhi Li
- Yucheng Shi
- Ruhan Wang
- Junyao Yang
- Zhichao Liu
- Xiyang Wu
- Anhao Li
- Yue Yu
- Ninghao Liu
- Lichao Sun
- Haotao Mi
- LeoweiLiang
topics:
- terminal-agents
- long-horizon-planning
- code-intelligence
- software-engineering-agents
- agent-evaluation
- dense-reward-grading
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks with Dense Reward-Based Grading

## Summary
Long-Horizon-Terminal-Bench evaluates whether AI agents can sustain progress across terminal workflows lasting tens of minutes to hours. Its dense subtask grading exposes partial progress and failure patterns that binary pass/fail benchmarks miss.

## Problem
- Existing terminal benchmarks focus on short tasks and final-state grading, which obscures intermediate progress and treats near-complete runs like total failures.
- Real workflows such as software repair, experiment reproduction, data auditing, and scientific computing require hundreds of actions, long-context management, debugging, and completion within a time budget.

## Approach
- The benchmark provides 46 containerized terminal tasks across nine broad domains, including software engineering, experiment reproduction, interactive games, multimodal analysis, and scientific computing.
- Each task is divided into meaningful subtasks with binary, continuous, thresholded, or episode-aggregated checks. The overall reward is a weighted average of subtask scores.
- Hidden stress cases test generalization beyond public examples, including renamed fields, missing values, noisy inputs, altered image geometry, and different coordinate or time conventions.
- The authors evaluate 15 frontier models through shared terminal-agent harnesses and report pass rate, mean reward, token use, episode count, execution time, and estimated cost.

## Results
- Agents used an average of 9.9 million tokens, about 231 episodes, and 85.3 minutes per task, making the benchmark substantially more demanding than prior terminal benchmarks.
- GPT-5.5 was the strongest tested model, solving 7 of 46 tasks, or 15.2%, at a reward threshold of 0.95, and 10.9% at a perfect reward threshold of 1.0.
- Across models, mean pass rates were 4.3% at the 0.95 threshold and 1.7% at the 1.0 threshold. Ten of 15 models solved zero tasks at the strict threshold.
- Dense grading found 433 of 690 runs with partial reward, including 180 runs with reward of at least 0.5, while 227 runs scored below 0.05. Binary grading would group these outcomes as identical failures.
- Near-complete runs were more than twice as common as full passes, with 73 runs scoring between 0.75 and 0.95 compared with 30 passes at or above 0.95.
- Timeouts caused 79% of unresolved runs, indicating that sustained planning, verification, and completion within the 90-minute budget remain major weaknesses.

## Link
- [https://arxiv.org/abs/2607.08964v1](https://arxiv.org/abs/2607.08964v1)
