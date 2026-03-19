---
source: arxiv
url: http://arxiv.org/abs/2603.06001v1
published_at: '2026-03-06T08:01:36'
authors:
- Ninghao Zhang
- Bin Zhu
- Shijie Zhou
- Jingjing Chen
topics:
- vision-language-action
- linguistic-grounding
- attention-recalibration
- ood-robustness
- robot-safety
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Restoring Linguistic Grounding in VLA Models via Train-Free Attention Recalibration

## Summary
This paper reveals the problem of "linguistic blindness" in Vision-Language-Action (VLA) models: when instructions contradict the scene, the robot still executes seemingly reasonable actions. The authors propose IGAR, a train-free inference-time method that strengthens the constraint of language on action generation through attention recalibration, and use ICBench to systematically evaluate this issue.

## Problem
- The paper addresses the problem that **VLA models ignore linguistic semantics and rely too heavily on visual priors under OOD contradictory instructions**.
- This matters because if robots ignore user language constraints in real-world environments, it may lead to incorrect manipulation, object damage, or safety incidents.
- Existing evaluations mostly check only whether the model succeeds under "normal instructions," and cannot distinguish whether the model truly understands language or merely completes tasks using visual heuristics.

## Approach
- The authors propose **ICBench**: a diagnostic benchmark built on LIBERO that injects controlled contradictions into instructions while **keeping the visual scene unchanged**, in order to measure whether language truly influences action generation.
- ICBench includes 4 types of contradictions: manipulated object attribute substitution (V1), target attribute intensified contradiction (V2), dual-attribute contradiction (V3), and spatial relation substitution (V4). If a model still completes tasks with a high success rate, that indicates weak language grounding.
- The authors propose **IGAR (Instruction-Guided Attention Recalibration)**: a **train-free, inference-time** attention recalibration mechanism that neither changes the model architecture nor updates parameters.
- Its core mechanism can be understood in three steps: **identify attention "black hole" tokens** (visually dominant sinks), **identify attention heads related to cross-modal grounding**, and **reallocate part of the attention from sink tokens to instruction tokens** so that action prediction better "follows the instruction."
- The paper also defines **LGS (Linguistic Grounding Score)**, namely the success rate under normal instructions minus the success rate under contradictory instructions; the higher the LGS, the stronger the constraint of language on actions.

## Results
- On **30 LIBERO tasks** with **50 rollouts per task variant**, the authors evaluate three representative VLAs: **\(\pi_0\), \(\pi_{0.5}\), and OpenVLA-OFT**.
- Baseline results show clear "linguistic blindness": for example, in the **Spatial** suite, **OpenVLA-OFT** still achieves **97.8% SR (V1)**, **96.4% SR (V2)**, and **96.2% SR (V3)** under contradictory instructions; the corresponding **LGS values are only -0.2, 1.2, and 1.4**, indicating that it is barely affected by language.
- **\(\pi_{0.5}\)** is similarly severe: under **Spatial-V4**, it has **SR 97.6%** and **LGS -0.2**; under **Object-V1/V3**, it achieves **96.2% / 96.4% SR** respectively, showing that contradictory language hardly changes its actions.
- **\(\pi_0\)** performs relatively better, but still often succeeds at high rates under contradictions: for example, **Spatial-V2 96.2% SR, LGS 0.6**; **Object-V3 98.2% SR, LGS 0.6**.
- After adding **IGAR**, the paper claims that erroneous execution under contradictory instructions drops significantly and LGS rises substantially; a representative number given in the paper is that in **the spatial contradiction V4 of the Goal suite**, **SR drops as low as 36.4%**, and **LGS increases to 59.4**, indicating that the model is more likely to refuse actions that do not match the semantics.
- The paper also claims that **IGAR largely preserves baseline performance under normal instructions**, and validates the approach on a **real Franka robotic arm**: when the instruction is inconsistent with the scene, IGAR can effectively prevent erroneous operations. However, the provided excerpt does not include a more complete quantitative comparison table for the real-robot experiments.

## Link
- [http://arxiv.org/abs/2603.06001v1](http://arxiv.org/abs/2603.06001v1)
