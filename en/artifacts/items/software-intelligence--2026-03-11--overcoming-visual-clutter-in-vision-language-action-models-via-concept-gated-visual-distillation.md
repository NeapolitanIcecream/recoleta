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
- visual-distillation
- clutter-robustness
- inference-time
- instance-segmentation
relevance_score: 0.36
run_id: materialize-outputs
language_code: en
---

# Overcoming Visual Clutter in Vision Language Action Models via Concept-Gated Visual Distillation

## Summary
This paper proposes CGVD, a training-free, model-agnostic inference-time visual purification framework to mitigate the "precision-reasoning gap" of vision-language-action models in cluttered scenes. The core idea is to identify and remove distractors based on the instruction before the policy sees the image, allowing the robot to grasp and place targets more reliably.

## Problem
- Although VLA models have strong zero-shot generalization, in cluttered environments they often attend to the wrong location due to interference from backgrounds and similar objects, leading to manipulation failures.
- This issue is most severe when distractors are semantically or visually similar to the target, for example confusing a spoon with a spatula or fork.
- This matters because if robots are to operate in real human environments, they must maintain precise geometric grounding and manipulation success under open-vocabulary instructions.

## Approach
- The method is called **Concept-Gated Visual Distillation (CGVD)**: it first decomposes the language instruction into a "safe set" that must be preserved (target object, anchor object, robot) and a removable "distractor set."
- A text-prompted segmentation model is used to segment the safe set and distractor set separately, and final removal regions are constructed through set subtraction to ensure the target is not accidentally deleted.
- To avoid mistaking similar distractors for the target, the authors design a two-layer target refinement process: first, "cross-validation" compares the confidence gap between target prompts and distractor prompts; then, "spatial disambiguation" keeps only the most trustworthy connected target region.
- Distractor regions are processed with LaMa inpainting based on Fourier convolutions to generate a "clean scene." Then, at each frame, the live image is fused with the cached clean background, while the robot arm region is explicitly protected to preserve visual proprioception.
- The entire framework is an inference-time external wrapper: it does not modify VLA parameters, requires no fine-tuning, and performs heavy recomputation only on the initial frame, with later frames consisting mainly of lightweight compositing.

## Results
- On **Spoon on Towel, 18 semantic distractors, π₀ policy**, the baseline success rate is **43.0%**, while full CGVD reaches **77.5%**, an improvement of **34.5 percentage points**.
- Ablation experiments show that removing **LaMa inpainting** drops performance to **56.5%**; removing the **two-layer target refinement** drops it to **65.0%**; removing **robot mask protection** drops it to **73.0%**, indicating that all of these modules are effective.
- In attribute-distractor tests, under the complex prompt *"Put spoon with green handle on towel"*, the baseline drops from **85.0% (0 distractors)** to **57.0% (4 distractors)**; CGVD reaches **73.0%** with **4 distractors**, **16.0** percentage points higher than the baseline.
- Under the simpler prompt *"Put green spoon on towel"*, with **4 attribute distractors** the baseline is **75.0%** and CGVD is **87.0%**, an improvement of **12.0** percentage points; with **2 distractors**, performance improves from **73.0%** to **87.0%**.
- In terms of latency, CGVD concentrates the main overhead at initialization: **t=0 is 4914 ms**; during execution it is **421 ms**, a moderate increase relative to the base π₀'s **317 ms**, which the authors say preserves the original control frequency.
- The results also show that the method does not always provide monotonic gains: in tasks like **Carrot on Plate**, which may benefit from contextual clutter, CGVD can sometimes underperform the baseline, suggesting that aggressive decluttering may remove useful environmental cues.

## Link
- [http://arxiv.org/abs/2603.10340v1](http://arxiv.org/abs/2603.10340v1)
