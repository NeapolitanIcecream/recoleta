---
source: arxiv
url: https://arxiv.org/abs/2606.27268v1
published_at: '2026-06-25T16:50:21'
authors:
- Wen Ye
- Peiyan Li
- Tingyu Yuan
- Yuan Xu
- Xiangnan Wu
- Chaoyang Zhao
- Jing Liu
- Nianfeng Liu
- Yan Huang
- Liang Wang
topics:
- vision-language-action
- robot-test-time-scaling
- robot-manipulation
- generalist-robot-policy
- robot-data-scaling
- embodied-reasoning
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# E-TTS: A New Embodied Test-Time Scaling Framework for Robotic Manipulation

## Summary
E-TTS adds inference-time search to robot manipulation policies by sampling multiple reasoning-action pairs, checking them with vision-language verifiers, and refining failed samples with history-aware feedback. It improves several VLA policies without retraining the base policy or collecting new expert robot demonstrations.

## Problem
- Existing embodied test-time scaling methods mainly resample actions, so they can choose an action that does not match the model's high-level reasoning.
- Robot manipulation needs past context because each action depends on earlier observations, reasoning, and executed motions.
- Extra robot data is expensive, so improving task success at inference time matters for latency-tolerant tasks such as object rearrangement.

## Approach
- At each timestep, E-TTS samples M reasoning candidates and N action candidates per reasoning candidate, then treats each reasoning-action pair as one candidate.
- A history buffer stores recent observations and selected reasoning-action pairs, and the verifiers use this context when scoring new candidates.
- A zero-shot Qwen2.5-VL-7B reasoning verifier scores textual, multimodal, or spatial reasoning for task fit and grounding.
- A LLaVA-7B action verifier, trained on 90k paired successful and failed demonstrations from SimplerEnv and LIBERO, scores action feasibility using a modified Bradley-Terry preference loss.
- The system multiplies normalized reasoning and action scores, uses an epsilon-greedy selection rule with a score threshold, and asks the verifier to generate feedback when a batch is rejected.

## Results
- Across 4 benchmarks, 6 environments, 3 robot embodiments, and 4 base VLA models, E-TTS reports a maximum simulated success-rate gain of 33.14 percentage points and an average gain of 13.52 points.
- In real-world experiments, the paper claims up to a 26.62 percentage-point improvement without base-policy retraining.
- On SimplerEnv WidowX Visual Matching with E-CoT, average success rises from 6.67% to 39.81%, a +33.14 point gain.
- On the same SimplerEnv WidowX setting, E-TTS beats E-CoT + naive TTS at 23.61% average success and E-CoT + RoboMonkey at 26.38%.
- Ablations on SimplerEnv WidowX show lower average success when removing components: no feedback 25.04%, no reasoning scaling 26.39%, no action scaling 30.56%, no joint scoring 31.13%, no history buffer 31.94%, and no epsilon-greedy 36.11%.

## Link
- [https://arxiv.org/abs/2606.27268v1](https://arxiv.org/abs/2606.27268v1)
