---
source: arxiv
url: http://arxiv.org/abs/2604.01799v1
published_at: '2026-04-02T09:13:52'
authors:
- Guoqing Wang
- Chengran Yang
- Xiaoxuan Zhou
- Zeyu Sun
- Bo Wang
- David Lo
- Dan Hao
topics:
- test-generation
- reinforcement-learning
- code-llms
- software-testing
- submodular-optimization
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# TestDecision: Sequential Test Suite Generation via Greedy Optimization and Reinforcement Learning

## Summary
TestDecision treats unit test generation as a sequential decision problem and trains an open-source LLM to pick the next test that adds the most new value to the current suite. The paper claims this greedy-plus-RL setup lifts coverage, execution success, and bug finding enough for a 7B model to match GPT-5.2 on parts of the evaluation.

## Problem
- Existing LLM-based test generation often builds suites one test at a time, but open-source models do a poor job choosing the next test based on what the suite already covers.
- This matters because redundant tests waste a fixed test budget, miss uncovered branches, and lower bug-finding ability.
- The paper argues that prompting with feedback alone does not fix this: in its pilot study, guided iteration gave little or no gain over blind iteration on ULT.

## Approach
- The authors model test suite generation as a finite-horizon Markov Decision Process where the state is the current suite's checked status and each action is one new test case.
- They prove the suite utility objective is monotone submodular under their assumptions, so picking the test with the largest marginal gain at each step gets a classic \((1-1/e)\approx 63.2\%\) approximation bound to the optimum.
- TestDecision uses this idea in inference: generate tests step by step, execute them, update coverage and other feedback, and keep selecting the next test for maximum added value.
- They also train the base LLM with step-level reinforcement learning so the model learns to produce valid tests with higher marginal gain and gets penalized for invalid execution.
- The paper frames the main failure mode of open models as "structural myopia": the model sees local prompts but does not reliably plan suite-level gains across steps.

## Results
- On the ULT benchmark, TestDecision improves branch coverage by 38.15% to 52.37% over all base models in the abstract; the introduction reports 38.15% to 65.87%.
- On ULT, execution pass rate improves by 298.22% to 558.88% over base models.
- TestDecision finds 58.43% to 95.45% more bugs than vanilla base LLMs.
- The paper claims a 7B backbone reaches performance comparable to proprietary GPT-5.2.
- It also claims better out-of-distribution generalization on LiveCodeBench, but the excerpt does not provide detailed LiveCodeBench numbers.
- In the pilot study before TestDecision, guided prompting alone barely helped: for Qwen2.5-Coder-7B on ULT, line coverage was 52.43% for Iter-Blind vs 52.34% for Iter-Guided, branch coverage 43.52% vs 43.49%, and mutation score stayed 33.81% in both settings.

## Link
- [http://arxiv.org/abs/2604.01799v1](http://arxiv.org/abs/2604.01799v1)
