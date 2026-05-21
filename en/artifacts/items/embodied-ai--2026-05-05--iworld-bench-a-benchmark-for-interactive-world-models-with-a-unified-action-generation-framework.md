---
source: arxiv
url: https://arxiv.org/abs/2605.03941v2
published_at: '2026-05-05T16:30:03'
authors:
- Jianjie Fang
- Yingshan Lei
- Qin Wan
- Ziyou Wang
- Yuchao Huang
- Yongyan Xu
- Baining Zhao
- Weichen Zhang
- Chen Gao
- Xinlei Chen
- Yong Li
topics:
- interactive-world-models
- world-model-benchmark
- action-control
- camera-trajectory
- robot-data-scaling
- embodied-ai
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# iWorld-Bench: A Benchmark for Interactive World Models with a Unified Action Generation Framework

## Summary
iWorld-Bench is a benchmark and dataset for testing whether interactive world models follow action inputs and keep scene memory. It standardizes action commands across text, one-hot, and camera-parameter control so different models can be compared on the same tasks.

## Problem
- Current world-model benchmarks use narrow scene sources, limited viewpoints, and little weather or lighting coverage, which weakens tests for agent training settings.
- Interactive models accept different controls, such as text, keyboard-like one-hot inputs, and camera poses, so direct comparisons are hard.
- Existing tasks test visual generation more than action response, trajectory following, and memory over cyclic paths.

## Approach
- The authors build data from 12 existing datasets plus 18 simulator environments across 4 simulators, then standardize video formats, coordinate systems, and camera parameters.
- They create an Action Generation Framework that maps each action to text commands, one-hot encodings, and intrinsic/extrinsic camera parameters.
- The action space defines 27 translational and 27 rotational IDs, with 729 possible combinations; the evaluation dictionary focuses on 81 common combined actions supported by current models.
- The benchmark defines 6 task types covering action-control difficulty levels 1-4, memory ability, and camera following.
- It scores visual generation, trajectory following, and memory with 9 metrics.

## Results
- The dataset contains 330,000 video clips after filtering 27.8M multi-image samples; 2,100 videos are selected for evaluation.
- The benchmark contains 4,900 test tasks: 1,000 tasks for each of action-control difficulties 1, 2, 3, and 4; 200 memory tasks; and 700 camera-following tasks.
- Coverage includes 4 viewpoints (UGV, UAV, human, robot), 9 outdoor weather types, 5 indoor lighting types, 18 simulator environments, and thousands of scenes.
- The paper evaluates 14 world models: 5 text-controlled models, 2 one-hot-controlled models, and 7 camera-parameter-controlled models.
- The excerpt does not provide per-model leaderboard scores or metric values, so the strongest reported result is the scale and coverage of the benchmark and its cross-modality action mapping.
- In Table 1, iWorld-Bench is the only listed benchmark marked as supporting multiple inputs, interactive tasks, camera control, memory ability, multi-scene, multi-perspective, and all-weather evaluation; its 4,900 examples exceed WorldBench (425), MoveBench (1,018), VMbench (1,050), WorldEval (1,400), EWMBench (2,100), and WorldScore (3,000), while WorldModelBench has more examples (67,000).

## Link
- [https://arxiv.org/abs/2605.03941v2](https://arxiv.org/abs/2605.03941v2)
