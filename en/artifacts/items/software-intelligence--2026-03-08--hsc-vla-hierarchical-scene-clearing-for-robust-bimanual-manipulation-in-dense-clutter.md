---
source: arxiv
url: http://arxiv.org/abs/2603.07484v1
published_at: '2026-03-08T05:58:36'
authors:
- Zhen Liu
- Xinyu Ning
- Zhe Hu
- XinXin Xie
- Yitong Liu
- Zhongzhu Pu
topics:
- vision-language-action
- bimanual-manipulation
- hierarchical-control
- cluttered-robotics
- diffusion-policy
relevance_score: 0.46
run_id: materialize-outputs
language_code: en
---

# HSC-VLA: Hierarchical Scene-Clearing for Robust Bimanual Manipulation in Dense Clutter

## Summary
HSC-VLA proposes a hierarchical VLA framework for bimanual manipulation in densely cluttered scenes by separating “high-level semantic planning” from “low-level action execution.” The core idea is to first use a vision-language model to identify task-irrelevant distractors and clear the scene, then let a diffusion policy execute actions based only on filtered visual input and proprioception.

## Problem
- Problem addressed: Existing end-to-end VLAs are easily distracted by irrelevant objects in high-density cluttered environments, leading to failures in instruction following, target localization, grasping, and placement.
- Why it matters: Real-world supermarket shelf scenarios involve occlusion, reflections, complex arrangements, and long-horizon tasks, where errors can accumulate over time and reduce the practicality of robots in logistics and retail.
- Limitations of existing methods: Monolithic models compress planning, memory, perception, and control into a single representation, making it difficult to robustly handle long-horizon tasks, multiple subtasks, failure recovery, and visual distribution shifts.

## Approach
- Uses a hierarchical architecture: the high-level “Brain” takes language instructions and observation history, decomposes them into subgoals, and predicts bounding boxes for task-irrelevant regions that should be ignored.
- Applies segmentation and masking for “scene clearing”: it first performs zero-shot segmentation on those irrelevant regions, then updates masks through temporal propagation, removing distractors from the original image while retaining only the geometry relevant to the current subtask.
- The low-level “Cerebellum” is a diffusion-based bimanual manipulation policy that only sees mask-filtered images, a 14-dimensional proprioceptive state, and the current subgoal, and generates action chunks rather than single-step actions to improve smoothness and stability.
- Consistent training and deployment: offline data is processed with the same planning-segmentation-masking pipeline, reducing distribution mismatch caused by inconsistent visual preprocessing between training and testing.
- Adds verification and replanning: after each action chunk, it checks whether the subgoal has been completed, and if not, allows retries, mask-constraint updates, or adjustments to the subsequent plan.

## Results
- On real densely cluttered supermarket shelves, HSC-VLA achieves an overall success rate of **86.7%**, improving by **52.4 percentage points** over the best monolithic baseline, **π0-Full FT at 34.3%**.
- Under high-density settings, success rates for individual atomic skills are **85%** for grasping, **78%** for placing, and **97%** for bimanual manipulation; π0-Full FT achieves **75% / 13% / 15%**, respectively.
- In low-density scenes, HSC-VLA reaches an overall success rate of **90.7%**, higher than **87.7%** for π0-Full FT; the category-wise results are **92%** for grasping, **84%** for placing, and **96%** for bimanual tasks.
- The scene simplification ablation shows that under high density, performance is **56%** with **no mask**, **69%** with a **static mask**, and **80%** with **dynamic clearing**; for long-horizon tasks, the corresponding numbers are **40% / 10% / 72%**, indicating that dynamic clearing is especially important for long sequences.
- The paper abstract also reports long-horizon task results: **clutter sorting 72%** and **restocking 66%**, and claims stronger robustness and failure recovery.
- In terms of data and setup, the authors collected **2,100** expert trajectories on a real bimanual platform and compared against methods including ACT, DP, DP3, RDT, π0-LoRA, and π0-Full FT under a unified training configuration.

## Link
- [http://arxiv.org/abs/2603.07484v1](http://arxiv.org/abs/2603.07484v1)
