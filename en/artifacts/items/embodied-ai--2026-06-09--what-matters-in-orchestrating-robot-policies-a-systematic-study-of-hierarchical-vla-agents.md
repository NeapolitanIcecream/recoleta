---
source: arxiv
url: https://arxiv.org/abs/2606.10267v1
published_at: '2026-06-09T00:24:00'
authors:
- Jiaheng Hu
- Mohit Shridhar
- Caden Lu
- Dhruv Shah
- Hao-Tien Lewis Chiang
- Jie Tan
- Annie Xie
topics:
- vision-language-action
- hierarchical-robot-policy
- robot-manipulation
- generalist-robot-policy
- robot-data-scaling
- aloha
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# What Matters in Orchestrating Robot Policies: A Systematic Study of Hierarchical VLA Agents

## Summary
This paper studies which design choices matter in hierarchical vision-language-action robot agents. Its best Hi-VLA setup beats flat VLA control and a simple hierarchy on simulated MuJoCo ALOHA tasks and a real ALOHA fruit-sorting task.

## Problem
- Flat VLA policies often fail on long-horizon manipulation because training data usually contains short trajectory segments.
- Fine-tuning VLMs on action data can weaken language reasoning, which hurts compositional tasks and indirect instructions.
- Existing Hi-VLA systems choose different planners, controllers, memory, observations, and switching rules, so it is hard to know which parts drive task success.

## Approach
- The paper defines a shared options-style control loop: a high-level VLM chooses a language subgoal, and a low-level VLA executes actions conditioned on that subgoal.
- Control returns to the VLM when a termination rule fires, such as a fixed time, a success detector, or a VLM-predicted execution time.
- The study tests high-level Gemini 2.5 VLM variants, low-level Gemini Robotics On-Device VLA variants, observation encodings, memory choices, and termination rules.
- Evaluation covers short-horizon, long-horizon, and reasoning tasks in the MuJoCo ALOHA suite, plus a real ALOHA robot task.

## Results
- Best Hierarchy reaches 78.22 ± 0.91% on short-horizon tasks, compared with 69.57 ± 1.15% for Naive Hierarchy and 69.63 ± 1.07% for Flat VLA.
- On long-horizon tasks, Best Hierarchy reaches 67.08 ± 1.38%, compared with 40.56 ± 1.37% for Naive Hierarchy and 25.30 ± 1.22% for Flat VLA.
- On reasoning tasks, Best Hierarchy reaches 80.89 ± 1.17%, compared with 66.49 ± 1.31% for Naive Hierarchy and 50.90 ± 1.20% for Flat VLA.
- On the real ALOHA fruit-to-matching-plate task, Best Hierarchy places 12/15 fruits correctly, compared with 9/15 for Naive Hierarchy and 3/15 for Flat VLA.
- The ablations claim that VLM thinking improves success across task types, while VLM size matters less once thinking is enabled.
- The paper recommends fixed VLA execution horizons around 4-8 seconds when using timer-based termination, and reports that cross-episode memory summarized from 10 prior episodes helps more than in-episode raw history.

## Link
- [https://arxiv.org/abs/2606.10267v1](https://arxiv.org/abs/2606.10267v1)
