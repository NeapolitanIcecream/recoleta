---
source: arxiv
url: https://arxiv.org/abs/2605.19986v1
published_at: '2026-05-19T15:25:13'
authors:
- He-Yang Xu
- Pengyuan Zhang
- Zongyuan Ge
- Xiaoshuai Hao
- Serge Belongie
- Xin Geng
- Yuxin Peng
- Xiu-Shen Wei
topics:
- vision-language-action
- robot-evaluation
- fine-grained-manipulation
- dexterous-manipulation
- spatial-perception
- sim2real
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Beyond Binary Success: A Diagnostic Meta-Evaluation Framework for Fine-Grained Manipulation

## Summary
MetaFine is an evaluation system for fine-grained robot manipulation that separates language understanding, spatial perception, and motor behavior. It shows that binary success rates can overstate VLA manipulation ability and hide the source of failure.

## Problem
- Fine-grained tasks such as part grasping, slot insertion, and constrained rotation need correct local language grounding, precise spatial perception, and controlled motion.
- Standard embodied AI benchmarks often report a single pass/fail score, so they can count coarse object movement as success even when the part, contact, direction, or sequence is wrong.
- This matters because VLA models can look competent on headline metrics while failing the local constraints needed for real robot dexterity.

## Approach
- MetaFine rebuilds tasks as graphs of atomic skills such as grasp-part, align, insert, press-part, toggle-part, rotate-along, and slide-along.
- It tests understanding by changing attribute-level instructions while keeping the scene fixed, such as switching the target from a bottle cap to a bottle body.
- It tests perception with geometric and lighting perturbations at 3 severity levels and reports success rates plus area under the success curve.
- It tests behavior by splitting long tasks into stages and measuring stage success and trajectory smoothness.
- It absorbs tasks from RoboTwin, CALVIN, and LIBERO, scales to 431 objects and 4,312 grasp poses, and uses paired real-sim rollouts with prediction-powered inference for calibrated physical estimates.

## Results
- Conventional evaluation can inflate fine-grained capability by up to 70%. Object-level grasping is often above 95%, but the best policy reaches only 80% on Grasp Part, 85% on Toggle Part, 68% on Press Part, and 12% on Rotate Along under part-level constraints.
- Under severe lighting perturbation, the top Grasp Part policy drops from 80% to 15%; under viewpoint perturbation it keeps 55%. On Toggle Part, two models with similar nominal success, 85% and 79%, split under L3 lighting, with 83% versus 11% retained success.
- In semantic substitution tests, all 5 evaluated VLAs score 0% on the modified instruction. Original-task behavior also drops: pi_0.5 by 31.2%, pi_0 by 34%, OpenVLA-OFT by 10%, OpenVLA by 6%, and Octo by 8%.
- On peg-in-hole, all 5 VLAs have near-zero overall success, 0% to 3%. Stage metrics separate failures: OpenVLA-OFT grasps in 47% of trials and aligns in 19%, while pi_0.5 grasps in 39% and aligns in 0%.
- Replacing pi_0.5's SigLIP encoder with a multi-scale cross-attention encoder, while freezing the VLM backbone and action head, raises grasp success from 39% to 67% and alignment from 0% to 32%.
- Hybrid real-sim calibration reduces estimate variance. For pi_0.5, standard deviation drops from 11.5% to 2.6%; for pi_0, it drops from 5.8% to 2.9%. A 55% hardware-only estimate for pi_0.5 is corrected to 66%, close to the 65.0% large-sample real reference.

## Link
- [https://arxiv.org/abs/2605.19986v1](https://arxiv.org/abs/2605.19986v1)
