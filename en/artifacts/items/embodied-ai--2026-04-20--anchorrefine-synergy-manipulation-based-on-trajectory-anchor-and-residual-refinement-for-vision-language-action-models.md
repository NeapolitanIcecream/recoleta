---
source: arxiv
url: http://arxiv.org/abs/2604.17787v1
published_at: '2026-04-20T04:25:24'
authors:
- Tingzheng Jia
- Kan Guo
- Lanping Qian
- Yongli Hu
- Daxin Tian
- Guixian Qu
- Chunmian Lin
- Baocai Yin
- Jiapu Wang
topics:
- vision-language-action
- robot-manipulation
- hierarchical-policy
- residual-refinement
- gripper-control
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# AnchorRefine: Synergy-Manipulation Based on Trajectory Anchor and Residual Refinement for Vision-Language-Action Models

## Summary
AnchorRefine splits robot action prediction into a coarse trajectory anchor and a small correction step. The paper targets precision failures in vision-language-action policies and reports consistent gains on LIBERO, CALVIN, and real-robot tests.

## Problem
- Standard VLA policies predict full action chunks in one space, so large arm motions dominate training and small correction signals get weak supervision.
- This hurts precision-critical manipulation such as final pose alignment, contact timing, and gripper closing, where small errors can flip success to failure.
- The paper points to gripper control as a major failure source: over 88% of LIBERO failures in their analysis involve gripper-related errors.

## Approach
- AnchorRefine uses a two-stage action model: an anchor planner predicts a coarse action trajectory, then a refinement module predicts the residual error between that anchor and the ground-truth action.
- For arm motion, the final action is `anchor + residual`, so the second module only learns the small correction that remains after the coarse plan.
- Training is sequential: first train the anchor planner on the original action target, then freeze it and train the residual branch on anchor-relative residuals.
- For gripper control, the paper adds a decision-aware refinement head that corrects the anchor gripper prediction based on how close it is to the open/close decision boundary.
- The method is designed to plug into both regression-based and diffusion-based VLA backbones, shown here with GR-1 and X-VLA.

## Results
- On **LIBERO-LONG**, **AnchorRefine (GR-1)** improves success rate from **74.5% to 82.3%**, a **+7.8** point gain.
- On **LIBERO-LONG**, **AnchorRefine (X-VLA)** improves success rate from **95.8% to 97.4%**, a **+1.6** point gain.
- On **CALVIN ABC→D**, **AnchorRefine (GR-1)** improves 5-task chain success from **52.0% to 55.3%** (**+3.3**), 3-task success from **68.5% to 71.9%** (**+3.4**), and average sequence length from **3.51 to 3.64** (**+0.13**).
- On **CALVIN ABC→D**, **AnchorRefine (X-VLA)** improves 5-task chain success from **74.6% to 76.5%** (**+1.9**), 4-task success from **81.3% to 83.7%** (**+2.4**), 3-task success from **86.9% to 89.1%** (**+2.2**), and average sequence length from **4.31 to 4.40** (**+0.09**).
- The abstract claims gains of up to **7.8%** in simulation success rate and **18%** in real-world success rate.
- Among the listed LIBERO results, **AnchorRefine (X-VLA)** reaches **97.4%**, higher than the reported **95.8%** X-VLA baseline and **95.2%** AtomicVLA result in the table.

## Link
- [http://arxiv.org/abs/2604.17787v1](http://arxiv.org/abs/2604.17787v1)
