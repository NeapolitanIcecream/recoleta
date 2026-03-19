---
source: arxiv
url: http://arxiv.org/abs/2603.08260v1
published_at: '2026-03-09T11:30:45'
authors:
- Cong Tai
- Zhaoyu Zheng
- Haixu Long
- Hansheng Wu
- Zhengbin Long
- Haodong Xiang
- Rong Shi
- Zhuo Cui
- Shizhuang Zhang
- Gang Qiu
- He Wang
- Ruifeng Li
- Biao Liu
- Zhenzhe Sun
- Tao Shen
topics:
- embodied-ai
- vision-language-action
- data-scaling
- self-evolving-data
- robot-manipulation
- multimodal-evaluation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Seed2Scale: A Self-Evolving Data Engine for Embodied AI via Small to Large Model Synergy and Multimodal Evaluation

## Summary
This paper proposes Seed2Scale, a self-evolving data engine for embodied intelligence that uses very few human demonstrations to bootstrap automatic collection, automatic verification, and target policy learning. The core idea is to let a small model handle efficient exploration, a large model handle quality evaluation, and then use the filtered data to train the target VLA policy, thereby alleviating the robot data scarcity problem.

## Problem
- Embodied AI / VLA models depend heavily on large-scale, high-quality expert demonstrations, but manual collection is expensive, creating a data bottleneck that limits the scaling of generalist robot policies.
- Existing automatic data generation methods either only perform local augmentation without active exploration, or are affected by the "embodiment gap," making it difficult to convert video knowledge into executable robot actions.
- More importantly, the signal-to-noise ratio of automatic sampling is low; if failed trajectories are mixed into training, errors will accumulate during self-iteration and lead to model collapse, so reliable automatic quality evaluation is needed.

## Approach
- The paper proposes a heterogeneous collaborative framework: **small-model collection, large-model evaluation, target-model learning**. Put simply, a small and fast VLA tries many actions, a frozen VLM judges whether those attempts are good, and then the high-scoring data is used to train the final policy.
- It designs a lightweight collector, **SuperTiny**: ResNet-18 processes vision, T5-Small processes language, an MLP processes robot state, and then a lightweight Transformer decodes action chunks; time-weighted averaging makes control smoother and more stable, facilitating parallel rollout.
- It uses the pretrained **Qwen3-VL-32B** as the verifier, taking as input the task instruction, the current rollout video, and a reference successful video, and outputting a 0–10 quality score; only trajectories above a threshold are kept in the silver-label dataset, reducing contamination from failed data.
- Starting from only **4** seed demonstrations, it self-iteratively executes the closed loop of "train collector → generate trajectories in parallel → VLM scoring and filtering → expand dataset → train target model."
- The target model is **SmolVLA**, which learns a more robust action distribution from the filtered high-quality trajectories via conditional flow matching.

## Results
- On 4 Agibot A2 manipulation tasks, using only **4** seed demonstrations per task, the average success rate increases from **22.18%** to **68.57%**, a relative improvement of **209.15%**.
- Per-task results: Kitchen Cleanup **24.63% → 71.43%** (**+190.01%**); Cup-to-Cup Transfer **23.50% → 64.14%** (**+172.94%**); Can Stacking **7.50% → 65.90%** (**+778.67%**); Air Fryer Manipulation **33.08% → 72.82%** (**+120.13%**).
- Self-evolution scalability: on the hardest **Can Stacking** task, the target model's success rate shows a sustained upward trend across **8** self-evolution iterations; the paper emphasizes the stability of the trend, but the excerpt does not provide the specific value for each iteration.
- Compared with MimicGen on GR-1 tasks, Seed2Scale achieves an average policy success rate of **79.63% vs 36.00%**; specifically, Cylinder Grasp **66.00% vs 37.25%**, and Wheel Manipulation **93.25% vs 34.75%**.
- For replay success rate, Seed2Scale averages **77.41% vs 34.75%**; specifically, Cylinder Grasp **86.96% vs 21.00%**, and Wheel Manipulation **67.86% vs 48.50%**, indicating higher generated data quality.
- In trajectory quality, Seed2Scale approaches or even surpasses human demonstrations: Total Variation **1.34** (expert **1.32**, MimicGen **3.68**), Mean Absolute Jerk **0.0047** (expert **0.0063**, MimicGen **0.0261**), HF Ratio **0.30%** (expert **0.22%**, MimicGen **2.07%**). In addition, SuperTiny has only **48M** parameters, with inference at **38.08ms / 26.3 Hz**, faster than ACT (**45.67ms / 21.9 Hz**) and Diffusion Policy (**135.83ms / 7.4 Hz**).

## Link
- [http://arxiv.org/abs/2603.08260v1](http://arxiv.org/abs/2603.08260v1)
