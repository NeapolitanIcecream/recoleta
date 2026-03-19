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
- robotics-safety
- attention-recalibration
- ood-robustness
- linguistic-grounding
relevance_score: 0.42
run_id: materialize-outputs
language_code: en
---

# Restoring Linguistic Grounding in VLA Models via Train-Free Attention Recalibration

## Summary
This paper reveals the problem of "linguistic blindness" in Vision-Language-Action (VLA) robotic policies: even when the instruction contradicts the scene, the model still continues executing visually plausible actions based on visual priors. The authors propose IGAR, a training-free inference-time method, and construct ICBench to diagnose and mitigate this issue.

## Problem
- The paper addresses the problem that **VLA models still incorrectly execute actions under contradictory or out-of-distribution language instructions**, indicating that the models do not truly use language constraints in action generation.
- This is important because robots differ from pure dialogue systems; ignoring language constraints can directly cause incorrect real-world manipulation, safety risks, and physical damage.
- Existing evaluations typically only look at task success rates under normal instructions, and cannot distinguish whether a model is "truly understanding language" or merely "completing tasks using visual heuristics alone."

## Approach
- The authors propose **ICBench**: while keeping the visual scene unchanged, they systematically modify LIBERO task instructions into semantically contradictory versions to test in isolation whether genuine language-action coupling exists.
- ICBench defines 4 types of contradictions: manipulation object attribute substitution (V1), target attribute augmentation (V2), dual-attribute perturbation (V3), and spatial relation substitution (V4). If a model truly relies on language, it should fail or refuse to execute under these contradictory instructions.
- The authors propose **IGAR (Instruction-Guided Attention Recalibration)**: a **training-free, inference-time, plug-and-play** attention recalibration mechanism that neither changes the model architecture nor updates parameters.
- The core mechanism of IGAR is simple: it first identifies sink tokens that "absorb most of the attention," then locates attention heads with cross-modal imbalance, and reallocates part of the attention from sink tokens to language instruction tokens, so that action generation refers more to textual constraints.
- The paper also defines **LGS (Linguistic Grounding Score)** to measure the success-rate gap between normal instructions and contradictory instructions; the larger the gap, the stronger the influence of language on behavior.

## Results
- Across 30 LIBERO tasks and 3 representative VLA models ($\pi_0$, $\pi_{0.5}$, OpenVLA-OFT), baseline models often still achieve high success rates under contradictory instructions, directly proving "linguistic blindness." For example, in the Spatial suite, $\pi_{0.5}$ achieves SR of **96.2/97.8/96.4/97.6** under V1/V2/V3/V4 respectively, with corresponding LGS of only **1.2/-0.4/1.0/-0.2**; OpenVLA-OFT achieves SR **97.8** and LGS **-0.2** on Spatial V1.
- In the Goal suite, OpenVLA-OFT still completes tasks almost as usual under contradictory instructions: SR for V1/V2/V3 is **97.8/98.2/98.4**, with LGS only **0.2/-0.2/-0.4**; this shows that language has almost no effect on actions.
- $\pi_0$ is relatively more sensitive to language, but the problem remains obvious: for example, under Goal-V4, normal SR is **95.8**, contradictory-instruction SR is still **76.4**, and LGS is **19.4**; under Object-V3, contradictory SR is **98.2**, with LGS only **0.6**.
- After applying IGAR, the paper claims that erroneous execution under contradictory instructions is significantly reduced across all suites, and LGS is substantially improved. One representative figure given is that under the **V4 spatial contradiction** in the **Goal** suite, the success rate can be reduced to as low as **36.4%**, while **LGS increases to 59.4**.
- The authors also claim that while improving sensitivity to language constraints, IGAR **preserves baseline task performance under normal instructions**; and validation on a real **Franka** robotic arm shows that IGAR can effectively prevent incorrect manipulation when contradictory instructions appear.
- The abstract and excerpted main text do not provide a complete full results table for IGAR or precise comparative numbers for the real robot, but the strongest quantitative conclusion is: baseline SR often remains **>90%** in many contradictory scenarios, while IGAR can reduce contradictory-execution SR in some scenarios to **36.4%** and raise LGS to **59.4**.

## Link
- [http://arxiv.org/abs/2603.06001v1](http://arxiv.org/abs/2603.06001v1)
