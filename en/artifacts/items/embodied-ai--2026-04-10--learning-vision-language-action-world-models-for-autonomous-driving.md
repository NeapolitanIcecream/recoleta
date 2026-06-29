---
source: arxiv
url: http://arxiv.org/abs/2604.09059v1
published_at: '2026-04-10T07:38:05'
authors:
- Guoqing Wang
- Pin Tang
- Xiangxuan Ren
- Guodongfang Zhao
- Bailan Feng
- Chao Ma
topics:
- autonomous-driving
- vision-language-action
- world-models
- future-frame-generation
- trajectory-planning
relevance_score: 0.73
run_id: materialize-outputs
language_code: en
---

# Learning Vision-Language-Action World Models for Autonomous Driving

## Summary
VLA-World combines a vision-language-action driving policy with a world model that generates a short-term future image and then reasons over that imagined frame before refining the driving plan. The paper targets safer and more interpretable end-to-end autonomous driving by adding explicit foresight and self-checking to action generation.

## Problem
- Current VLA driving models can map observations to actions, but they do not model scene dynamics and other agents well enough for strong foresight in complex traffic.
- Current driving world models can generate plausible future scenes, but they usually do not evaluate whether those imagined futures imply risk, safety issues, or a better action.
- This matters because autonomous driving needs both prediction of how the scene will change and a way to revise decisions when the predicted future looks unsafe.

## Approach
- VLA-World first predicts a short-term ego trajectory, then uses that trajectory plus multi-view observations to generate the next-frame driving image 0.5 seconds ahead.
- The model feeds this self-generated future image back into a reflective reasoning module, which checks agents, motion cues, and possible risks, then refines the final 3-second trajectory and action.
- Training uses three stages: visual pretraining for future-frame generation, supervised fine-tuning on mixed driving tasks, and GRPO reinforcement learning with rule-based rewards for output format, short-term prediction, visual token validity, action quality, and trajectory quality.
- The paper also introduces **nuScenes-GR-20K**, a dataset derived from nuScenes for future generation and reasoning conditioned on imagined futures.

## Results
- The paper claims VLA-World consistently beats prior VLA and world-model baselines on both planning and future-generation benchmarks.
- Quantitative planning results shown in the excerpt use **ST-P3** and **UniAD** metrics with **L2 trajectory error** and **collision rate**, but the row for **VLA-World** is not visible in the provided text, so its exact numbers cannot be extracted here.
- The strongest concrete claim from the visible text is that VLA-World achieves the **lowest collision rate and FID score** among compared methods, according to Figure 1, but the excerpt does not include the exact FID value.
- Baselines visible in the table include **FeD*** on UniAD with **0.58 avg L2** and **0.19 avg collision (%)**, **UniAD*** with **0.46 avg L2** and **0.37 avg collision (%)**, and **BEV-Planner*** on ST-P3 with **0.35 avg L2** and **0.34 avg collision (%)**. The authors state VLA-World surpasses such state-of-the-art baselines.

## Link
- [http://arxiv.org/abs/2604.09059v1](http://arxiv.org/abs/2604.09059v1)
