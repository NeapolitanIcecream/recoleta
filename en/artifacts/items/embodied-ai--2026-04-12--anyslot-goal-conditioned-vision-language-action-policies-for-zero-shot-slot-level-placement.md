---
source: arxiv
url: http://arxiv.org/abs/2604.10432v2
published_at: '2026-04-12T03:09:44'
authors:
- Zhaofeng Hu
- Sifan Zhou
- Qinbo Zhang
- Rongtao Xu
- Qi Su
- Ci-Jyun Liang
topics:
- vision-language-action
- goal-conditioned-policy
- zero-shot-manipulation
- slot-level-placement
- spatial-reasoning
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement

## Summary
AnySlot targets slot-level robotic placement from natural language, where the robot must choose the exact slot and place with sub-centimeter precision in unseen layouts. It does this by converting the instruction into an explicit visual goal marker and then using a goal-conditioned VLA policy to execute the placement.

## Problem
- The paper studies zero-shot slot-level placement: given a compositional language instruction, the robot must identify the correct slot among dense candidates and place the object accurately enough for physical success.
- This matters for tasks such as precision assembly and factory automation, where choosing the wrong compartment or missing alignment by a small margin causes failure.
- Existing flat VLA policies mix language reasoning and motor control in one model, while prior modular systems often reduce the target to a single coordinate, which loses slot shape and boundary information needed for precise execution.

## Approach
- AnySlot uses a two-stage pipeline. A high-level grounding module takes the initial scene image and the language instruction, then edits the image by placing a colored sphere marker on the target slot.
- The system extracts the marker center, lifts it into 3D with the depth map and camera calibration, and re-projects it into all camera views as a consistent overlay. This overlay is the visual goal.
- A goal-conditioned VLA policy, built on π0.5 with a PaliGemma-3B backbone and a flow-matching action expert, receives the multi-view observations plus the overlaid marker and outputs continuous robot actions.
- The low-level instruction is fixed to a simple template such as moving the object into the slot with blue-sphere guidance. Language-based slot reasoning stays in the high-level module; the low-level policy focuses on execution.
- The paper also introduces SlotBench, a SAPIEN simulation benchmark with 9 task categories for slot-level reasoning: ordinal, size, height, distance, compositional relations, negation, vague language, affordance, and world knowledge.

## Results
- The paper claims AnySlot achieves nearly **90% average success rate** on SlotBench across the 9 zero-shot slot-placement task categories.
- SlotBench uses tight geometry: slot size is about **0.03 m**, object length about **0.15 m**, and instruction accuracy counts a prediction as correct only if it is within **0.02 m** of the ground-truth slot center.
- The low-level policy is trained on a synthetic simulator dataset with object pose randomization up to **0.05 m** translation noise, then evaluated zero-shot on unseen layouts and instructions.
- In the visible table excerpt, a flat Diffusion Policy baseline reaches only **16% success** on ordinal reasoning and **0%** on the other shown categories, which is consistent with the paper's claim that flat baselines fail on most SlotBench tasks.
- The excerpt does not include the full quantitative table for all baselines and AnySlot, so exact per-category gains, baseline averages, and comparison margins are not fully recoverable from the provided text.

## Link
- [http://arxiv.org/abs/2604.10432v2](http://arxiv.org/abs/2604.10432v2)
