---
source: arxiv
url: http://arxiv.org/abs/2604.04502v1
published_at: '2026-04-06T07:57:52'
authors:
- Zhongru Zhang
- Chenghan Yang
- Qingzhou Lu
- Yanjiang Guo
- Jianke Zhang
- Yucheng Hu
- Jianyu Chen
topics:
- vision-language-action
- video-models
- dexterous-manipulation
- hierarchical-control
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Veo-Act: How Far Can Frontier Video Models Advance Generalizable Robot Manipulation?

## Summary
Veo-Act tests whether a frontier video generator, Veo-3, can improve robot manipulation without task demonstrations. The paper finds that video prediction alone gives good high-level plans but weak low-level control, and a hierarchical video-planner-plus-VLA system raises success rates on dexterous pick-and-place tasks.

## Problem
- The paper studies generalizable robot manipulation in open-ended scenes, where current vision-language-action policies still fail on object ambiguity, viewpoint changes, and contact-heavy dexterous control.
- Pure video-to-action pipelines can keep the generalization of large video models, but their action recovery is too imprecise for reliable contact-rich manipulation.
- This matters because collecting expert robot data is expensive, and a system that can use web-scale video priors with little or no demonstration data could improve robot generalization at lower data cost.

## Approach
- The authors first test a zero-shot pipeline: Veo-3 generates a future video from the current image and language instruction, and an inverse dynamics model (IDM) converts frame-to-frame changes into robot actions.
- The IDM is trained from random-play data rather than expert demonstrations. It uses a DINOv3 visual encoder and two heads: one predicts actions, the other predicts a gate value for whether the robot is in an interaction phase.
- Veo-Act uses the generated video as a high-level motion plan, turns it into an action chunk, smooths the chunk, and executes it until the gate detector says the robot should switch to a reactive low-level VLA policy.
- During execution, the system can switch back from the VLA policy to the remaining planned action sequence after the interaction phase, pruning the part of the plan that overlaps with the gated interaction window.
- Training data for the IDM includes 300k simulation frame pairs, 100k extra random-motion simulation samples, and 150k real-world samples, with STEM-OB augmentation to reduce the sim-to-real gap.

## Results
- Main headline: the paper reports that Veo-Act improves the average success rate of the strong VLA baseline \(\pi_{0.5}\) from **45% to 80%** across the simulated and real dexterous-hand environments they test.
- In simulation, under the **wrist-camera invisible** experimental setting, overall task success improves from **10/30 = 0.33** for \(\pi_{0.5}\) to **20/30 = 0.67** for Veo-Act. Instruction-following improves from **11/30 = 0.37** to **25/30 = 0.83**.
- In simulation, under **similar-object distractors**, overall success improves from **12/30 = 0.40** to **28/30 = 0.93**. Under **pass-by interaction**, overall success improves from **0/30 = 0.00** to **14/30 = 0.47**.
- In real robot tests, under **similar-object distractors**, overall success improves from **8/16 = 0.50** to **12/16 = 0.75**. Under **pass-by interaction**, it improves from **2/13 = 0.15** to **11/13 = 0.85**.
- In real robot tests with **richer semantics**, overall success improves from **2/19 = 0.11** to **15/19 = 0.79**, and instruction-following improves from **4/19 = 0.21** to **18/19 = 0.95**.
- The zero-shot Veo-3+IDM baseline shows partial capability but weaker control: in simulation, the video-based baseline VPP reaches **15/30 = 0.50** overall in wrist-camera-invisible experimental settings, **6/30 = 0.20** with similar-object distractors, and **1/30 = 0.03** in pass-by interaction. This supports the paper's claim that current video models produce roughly correct task trajectories but lack precise low-level control.

## Link
- [http://arxiv.org/abs/2604.04502v1](http://arxiv.org/abs/2604.04502v1)
