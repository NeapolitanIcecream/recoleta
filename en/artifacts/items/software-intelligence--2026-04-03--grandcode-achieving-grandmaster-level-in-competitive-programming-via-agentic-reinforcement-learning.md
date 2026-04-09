---
source: arxiv
url: http://arxiv.org/abs/2604.02721v1
published_at: '2026-04-03T04:26:56'
authors:
- DeepReinforce Team
- Xiaoya Li
- Xiaofei Sun
- Guoyin Wang
- Songqiao Su
- Chris Shum
- Jiwei Li
topics:
- competitive-programming
- multi-agent-rl
- code-generation
- test-time-rl
- code-intelligence
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# GrandCode: Achieving Grandmaster Level in Competitive Programming via Agentic Reinforcement Learning

## Summary
GrandCode is a multi-agent reinforcement learning system for competitive programming. The paper claims it is the first AI system to place first in multiple live Codeforces contests, ahead of all human participants.

## Problem
- Competitive programming is still a hard coding setting for AI because solutions must be correct, efficient, and robust to hidden test cases under live time pressure.
- Standard single-model prompting and ordinary RL struggle with long multi-stage solving loops, delayed rewards, and off-policy drift during asynchronous training.
- This matters because competitive programming is a strong test of code reasoning, debugging, verification, and timed problem solving.

## Approach
- GrandCode uses several cooperating components: a main solver for reasoning and code, a hypothesis model for conjectures, a summarization model for long-context compression, and a test-case generator for adversarial checks.
- The system trains these components through continued pretraining, supervised fine-tuning, joint multi-component RL, and online test-time RL during contests.
- Its main RL method, Agentic GRPO, updates the policy as soon as intermediate rewards arrive, then applies a later correction when the final reward is known. This is meant to handle delayed rewards in long agent rollouts.
- For verification, it generates adversarial tests by finding inputs that separate candidate solutions, attacking candidate solutions against gold solutions during training, and refreshing the test pool online before submission.
- For harder problems, the system also proposes compact hypotheses, checks them on small brute-force instances, and feeds verified hypotheses back into the solver prompt.

## Results
- In live Codeforces Rounds 1087, 1088, and 1089, GrandCode placed 1st in all three contests and finished all tasks first each time.
- Reported live contest scores: Round 1087: 9269 separate, 8334 joint, finish time 00:51:11; Round 1088: 16511 separate, 15008 joint, finish time 01:40:35; Round 1089: 11596 separate, 9506 joint, finish time 00:56:43.
- On 50 real Codeforces problems, its test suite pipeline raised pass count from 42/50 with the base suite to 48/50 after difference-driven generation plus solution attack, then to 50/50 after submission feedback and continued online generation.
- On a 200-problem hypothesis-generation evaluation, Qwen-3.5-27B scored 34% pass@1 and 44% pass@5; +SFT reached 45% and 52%; +SFT+RL reached 52% and 57%.
- The paper also reports a benchmark of frontier models on 100 problems: Gemini 3.1 Pro 75% accept rate and 7/20 on Level 5, Claude Opus 4.6 73% and 8/20, GPT-5.4 72% and 7/20. These numbers provide context for the claimed gain, though the excerpt does not give a direct ablation against GrandCode on the same benchmark.

## Link
- [http://arxiv.org/abs/2604.02721v1](http://arxiv.org/abs/2604.02721v1)
