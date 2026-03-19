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
- hierarchical-policy
- cluttered-scene-robotics
- diffusion-policy
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# HSC-VLA: Hierarchical Scene-Clearing for Robust Bimanual Manipulation in Dense Clutter

## Summary
HSC-VLA proposes a hierarchical VLA framework for bimanual manipulation in high-density cluttered scenes by separating “high-level understanding and planning” from “low-level action execution.” The core idea is to first use a vision-language model to remove task-irrelevant scene interference, and then let a diffusion policy act only on filtered visual inputs, thereby significantly improving robustness and long-horizon performance.

## Problem
- Existing end-to-end monolithic VLAs are prone to **instruction-following failures** in high-density cluttered environments, because irrelevant objects and backgrounds distract attention and disrupt target localization and geometric perception.
- In settings such as supermarket shelves, occlusion, reflections, crowded placement, and large numbers of SKUs make bimanual grasping, placing, and coordinated manipulation unstable, while long-horizon tasks accumulate errors over time.
- This matters because real logistics/retail environments require robots to reliably complete picking, organizing, restocking, and similar tasks in complex shelving setups, while existing monolithic policies are not robust enough to visual distribution shifts and complex subtask sequences.

## Approach
- Uses a hierarchical framework: a high-level “Brain” performs task decomposition from language instructions and visual history, determines the current subgoal, and identifies which regions/objects should currently be ignored as distractions.
- The high level outputs **bounding boxes for task-irrelevant regions**, which are then passed to a zero-shot segmentation model to generate pixel-level masks; these are continuously updated through temporal propagation to produce dynamic “scene clearing” results.
- The low-level “Cerebellum” is a **diffusion-based bimanual policy** whose inputs include only mask-filtered images, a 14-dimensional proprioceptive state, and the current subgoal, allowing it to focus on task-relevant geometric structure rather than raw cluttered pixels.
- The method emphasizes **train-test perceptual consistency**: offline data is preprocessed with the same planning + segmentation + mask propagation pipeline, reducing the distribution gap at deployment.
- Execution includes verification and replanning: if a subgoal fails, the system can retry, update mask constraints, or adjust later plans to support failure recovery and long-horizon execution.

## Results
- On real high-density cluttered supermarket shelves, HSC-VLA achieves an **aggregate success rate of 86.7%**, significantly outperforming the best monolithic baseline, **pi0-Full FT at 34.3%**, by **52.4 percentage points**.
- On per-task results in high-density settings, HSC-VLA reaches **85% grasping**, **78% placing**, and **97% bimanual manipulation**; compared with **pi0-Full FT** at **75% / 13% / 15%**, the advantage is especially large for placing and bimanual manipulation.
- In low-density settings, HSC-VLA also achieves **90.7% aggregate success**, with per-task results of **92% grasping / 84% placing / 96% bimanual**, still improving over **pi0-Full FT’s 87.7%**.
- Ablation experiments show that **dynamic clearing** outperforms both no mask and static masks: **98%** in low density, **80%** in high density, and **72%** on long-horizon tasks; in contrast, **base VLA, no mask** achieves **90% / 56% / 40%**, and **static mask** achieves **98% / 69% / 10%**. This indicates that dynamic scene clearing is critical for both heavy clutter and long-horizon tasks.
- The abstract also reports long-horizon task results of **clutter sorting 72%** and **restocking 66%**, and claims stronger robustness and failure recovery.
- On the data side, the authors collected **2,100 complete expert trajectories** on a real bimanual platform through demonstration, covering three skill types: single-arm stable grasping, single-arm placing, and bimanual cooperative grasping. While this is not a direct performance metric, it supports training of the low-level policy.

## Link
- [http://arxiv.org/abs/2603.07484v1](http://arxiv.org/abs/2603.07484v1)
