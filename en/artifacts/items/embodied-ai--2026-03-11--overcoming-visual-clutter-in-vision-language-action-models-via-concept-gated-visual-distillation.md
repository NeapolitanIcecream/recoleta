---
source: arxiv
url: http://arxiv.org/abs/2603.10340v1
published_at: '2026-03-11T02:21:02'
authors:
- Sangmim Song
- Sarath Kodagoda
- Marc Carmichael
- Karthick Thiyagarajan
topics:
- vision-language-action
- robot-manipulation
- clutter-robustness
- inference-time
- visual-distillation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Overcoming Visual Clutter in Vision Language Action Models via Concept-Gated Visual Distillation

## Summary
This paper proposes CGVD, a training-free, model-agnostic inference-time visual distillation method for vision-language-action (VLA) models, designed to mitigate the “precision-reasoning gap” in cluttered scenes. The core idea is to identify and remove distractors based on language before the action policy sees the image, thereby preserving the target and geometric cues.

## Problem
- Problem addressed: VLA models generalize well in clean scenes under zero-shot settings, but in cluttered manipulation environments, background elements and semantically similar distractors dilute attention, leading to grasping the wrong object, hesitant trajectories, and task failure.
- Why it matters: Real robots often operate in human environments where semantically or visually similar objects are commonly near the target; if the model cannot reliably localize the target in clutter, its generalization ability is hard to realize in practice.
- Existing methods either require expensive retraining/fine-tuning or rely on external APIs and multiple forward probes, and still do not reliably protect the target at inference time.

## Approach
- CGVD is an inference framework wrapped around any VLA: it first parses the instruction into a **safe set** (target objects, anchor objects, robot) and a **distractor set**, and only the safe set must be preserved.
- It uses SAM3 to perform text-prompted segmentation separately on the safe set and distractor set, producing two mask streams; the region to be removed is constructed through set subtraction, structurally avoiding erasing the target as if it were a distractor.
- A two-layer target refinement scheme is proposed: the first layer uses a realism score based on “target confidence - distractor confidence” for cross-validation, explicitly penalizing false targets; the second layer scores connected regions using both realism and confidence, retaining only the most credible target instance.
- For distractor regions, LaMa inpainting based on Fourier convolution is used to generate a “clean background”; then, at each frame, the live image is composited with the cached clean scene, while the robot region is forcibly preserved to avoid damaging visual proprioception.
- The whole method requires no modification or training of VLA parameters; most recomputation is concentrated in the initialization frame, and subsequent frames only require lightweight compositing.

## Results
- In the **Spoon on Towel** task with **18 semantic distractors** and **π0** as the base policy, CGVD improves success rate from **43.0%** to **77.5%**, outperforming the baseline by **34.5 percentage points**.
- Ablation experiments show that removing the **two-layer target refinement** drops success rate from **77.5%** to **65.0%**; replacing LaMa with **mean-color fill** lowers it to **56.5%**; removing **robot mask protection** reduces it to **73.0%**, indicating that each component contributes.
- In the attribute-distractor experiment (**Put spoon with green handle on towel**), under the complex prompt, the baseline drops from **85.0% (0 distractors)** to **57.0% (4 distractors)**; CGVD reaches **73.0%** with **4 distractors**, exceeding the baseline by **16.0 percentage points**. Under the simple prompt, CGVD outperforms the baseline by **14.0/7.0/12.0 percentage points** with **2/3/4 distractors**, respectively.
- The paper states that in high-density semantic clutter, CGVD prevents policy performance collapse, and performs more stably across two VLA types (**π0, GR00T**) and many rollouts; the results in Figure 3 are aggregated over **19,200** episodes.
- In terms of latency, CGVD places heavy recomputation at initialization: **t=0 is 4914 ms**; during execution, the baseline is **317 ms** and CGVD is **421 ms**, i.e., about **104 ms** additional per step, which the authors argue still maintains a control frequency close to the original.
- However, the results are not uniformly better: in tasks like **Carrot on Plate**, which may benefit from environmental context, CGVD sometimes underperforms the baseline, suggesting that aggressive decluttering may hurt performance in scenarios that depend on background cues.

## Link
- [http://arxiv.org/abs/2603.10340v1](http://arxiv.org/abs/2603.10340v1)
