---
source: arxiv
url: https://arxiv.org/abs/2605.01191v1
published_at: '2026-05-02T02:10:54'
authors:
- Wenhao Li
- Xiu Su
- Yichao Cao
- Hongyan Xu
- Xiaobo Xia
- Shan You
- Yi Chen
- Chang Xu
topics:
- vision-language-action
- generalist-robot-policy
- robot-error-recovery
- active-status-monitoring
- robot-data-scaling
- continual-learning
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery

## Summary
Sentinel-VLA adds active status monitoring to a PI0-based vision-language-action robot policy so it can plan, act, detect errors, and recover during manipulation. The paper claims higher success rates than PI0, OpenVLA, ECoT, AHA+OpenVLA, and OneTwoVLA while keeping action latency low.

## Problem
- Current VLA policies often map image and instruction inputs straight to actions, so they can keep executing after missed grasps, wrong-object actions, or pose errors.
- Step-by-step reasoning can improve decisions, but it can be too slow for real-time control; ECoT reports 1528 ms/action in the paper's real-world timing test.
- Long-horizon robot tasks need status checks and recovery behavior because small execution errors can compound into task failure.

## Approach
- Sentinel-VLA adds a Status Monitor expert to PI0. A learned `[MONITOR]` query reads the VLM key-value cache and predicts one of four states: Initial, Normal, New-subtask, or Error.
- The model keeps a thought memory with the plan, current subtask, and error reflections. It plans at the start, reuses memory during Normal steps, updates the subtask at subtask boundaries, and generates a recovery plan when it detects Error.
- The action expert predicts the next robot action from the image, task instruction, status, and thought memory. Training combines flow matching for actions with cross-entropy losses for thoughts and status labels.
- EC-Gen creates training data by injecting gripper, pose, and semantic errors into successful trajectories, adding recovery waypoints, and labeling status and reasoning traces. The dataset has 11,000 trajectories, about 2.6 million transitions, and 44 RLBench tasks.
- SECL collects successful rollouts near the model's capability boundary, defined as settings with 20-80% success rate. It trains a LoRA adapter with an orthogonal penalty and merges it into offline weights with alpha=0.9.

## Results
- On RLBench seen tasks, Sentinel-VLA reaches 63.5% average success, compared with PI0 at 57.8%, OneTwoVLA at 56.9%, ECoT at 42.4%, and OpenVLA at 35.6%.
- On RLBench disturbed tasks, it reaches 54.7% average success, compared with OneTwoVLA at 48.4% and PI0 at 46.0%.
- On RLBench unseen tasks, it reaches 51.3% average success, compared with OneTwoVLA at 44.0%, PI0 at 42.0%, and OpenVLA at 30.7%. On Wine at rack, it reports 28% versus PI0 at 18% and OpenVLA at 8%.
- On LIBERO-LONG, it reports 90.7% success, compared with OneTwoVLA at 87.8%, PI0 at 85.2%, and OpenVLA at 53.7%.
- In real-world Agilex Piper tasks, it reaches 60.0% average success across Stack cube, Pour water, and Sweep rubbish, compared with OneTwoVLA at 52.0% and PI0 at 46.0%. This is a 30.4% relative gain over PI0.
- The paper reports 13 ms/action on an RTX4090, compared with PI0 at 8.5 ms, OneTwoVLA at 37 ms, OpenVLA at 57 ms, AHA+OpenVLA at 547 ms, and ECoT at 1528 ms. The status monitor detects errors at 97.4% on RLBench and 90.6% on a real-world error set.

## Link
- [https://arxiv.org/abs/2605.01191v1](https://arxiv.org/abs/2605.01191v1)
