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
- data-engine
- self-evolution
- vision-language-action
- multimodal-evaluation
relevance_score: 0.27
run_id: materialize-outputs
language_code: en
---

# Seed2Scale: A Self-Evolving Data Engine for Embodied AI via Small to Large Model Synergy and Multimodal Evaluation

## Summary
This paper proposes Seed2Scale, a self-evolving data engine for embodied intelligence that starts from a small number of seed demonstrations and continuously expands high-quality training data through a collaborative closed loop of "small-model collection + large-model verification + target-model learning." It aims to address the problems of scarce high-quality demonstration data in embodied AI, high noise in automatically generated data, and the risk of self-training collapse.

## Problem
- VLA models for embodied intelligence rely heavily on large amounts of high-quality expert demonstrations, but manual collection is expensive and hard to scale, creating a data bottleneck.
- Existing automatic data generation methods either only perform local perturbations and lack real exploration capability, or suffer from an "embodiment gap," making it difficult to convert video knowledge into executable robot actions.
- Automatically collected trajectories have a low signal-to-noise ratio. Without a reliable filtering mechanism, failed trajectories can contaminate subsequent training and cause performance degradation or even model collapse during iteration.

## Approach
- The core mechanism is simple: first, a small VLA model, **SuperTiny**, starts from only 4 seed demonstrations and performs large-scale action trials in parallel environments to collect candidate trajectories.
- Then a frozen large vision-language model, **Qwen3-VL-32B**, acts as a verifier, taking task instructions, the current rollout video, and a reference success video as input, scoring each trajectory from 0–10, and retaining only high-quality samples above a threshold.
- These filtered "silver" data are continuously added to the training set to form a self-evolving closed loop; the final target model, **SmolVLA**, is trained on this high-quality data rather than directly relying on unfiltered self-generated data.
- SuperTiny uses lightweight visual/language/state encoding, Transformer decoding, and temporally integrated action chunks to achieve stable control and large-scale exploration at low inference cost; SmolVLA uses conditional flow matching to learn more complex action distributions.

## Results
- On 4 Agibot A2 tasks, using only **4 seed demonstrations** per task, the target model's average success rate improved from **22.18%** to **68.57%**, a relative improvement of **209.15%**.
- Per-task results: Kitchen Cleanup **24.63% → 71.43%** (**+190.01%**); Cup-to-Cup Transfer **23.50% → 64.14%** (**+172.94%**); Can Stacking **7.50% → 65.90%** (**+778.67%**); Air Fryer Manipulation **33.08% → 72.82%** (**+120.13%**).
- Compared with MimicGen on GR-1 tasks, average Policy Success was **36.00% vs 79.63%**; average Replay Success was **34.75% vs 77.41%**, with Cylinder Grasp replay success improving from **21.00%** to **86.96%**.
- The paper claims that, relative to MimicGen, downstream policy performance improved by **+77.18%** for Cylinder Grasp and **+168.35%** for Wheel Manipulation, indicating that active exploration + multimodal verification is superior to trajectory augmentation alone.
- In trajectory quality, Seed2Scale is closer to human demonstrations: Total Variation **1.34** (expert **1.32**, MimicGen **3.68**), Mean Absolute Jerk **0.0047** (expert **0.0063**, MimicGen **0.0261**), HF Ratio **0.30%** (expert **0.22%**, MimicGen **2.07%**).
- SuperTiny as a collector is relatively efficient: **48M** parameters, inference time **38.08ms**, control frequency **26.3 Hz**; compared with ACT at **45.67ms / 21.9 Hz** and Diffusion Policy at **135.83ms / 7.4 Hz**.

## Link
- [http://arxiv.org/abs/2603.08260v1](http://arxiv.org/abs/2603.08260v1)
