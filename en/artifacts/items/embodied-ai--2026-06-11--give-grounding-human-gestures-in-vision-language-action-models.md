---
source: arxiv
url: https://arxiv.org/abs/2606.13435v1
published_at: '2026-06-11T14:59:38'
authors:
- Pengfei Liu
- Gen Li
- Junqiao Fan
- Boyu Ma
- Jindou Jia
- Yang Xiao
- Jianfei Yang
topics:
- vision-language-action
- human-robot-interaction
- gesture-grounding
- robot-manipulation
- foundation-model-adaptation
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# GIVE: Grounding Human Gestures in Vision-Language-Action Models

## Summary
GIVE adds human gesture understanding to pre-trained vision-language-action policies for robot handover tasks. It matters because text-only instruction following misses pointing and open-palm cues, which leads to wrong target selection and failed interaction.

## Problem
- Existing VLA policies usually treat manipulation as a text-driven task.
- In human-robot interaction, gestures often carry the target object and task state.
- Ambiguous or underspecified language causes intent grounding errors and execution failures.

## Approach
- GIVE injects gesture information without changing the base policy architecture.
- It uses a visual path that overlays hand skeletons and, for pointing, a fingertip ray on the robot’s camera image.
- It uses a semantic path that calls a pretrained VLM to turn stable gestures into a short text tuple for gesture type and execution instruction.
- The semantic output is cached per phase, and object names are kept generic so the visual path handles target grounding.
- The augmented image and text are fed into a pre-trained c0_0.5 VLA policy trained with a flow-matching action objective.

## Results
- On real-world grasp-then-handover trials with a Galaxea R1-Lite dual-arm robot, GIVE reaches 86.7% Identify SR, 80.0% Grasp SR, 80.0% React SR, and 80.0% Handover SR.
- The baseline c0_0.5 gets 46.7% Identify SR, 6.7% Grasp SR, 3.3% React SR, and 0.0% Handover SR.
- The paper reports a 40% gain in target object recognition accuracy and an 80% gain in overall task success rate over the baseline.
- In the visual-semantic ablation, keypoints alone give 56.7% Identify SR, keypoints plus ray give 70.0%, and the full visual-plus-semantic system gives 86.7% Identify SR.
- For semantic parsing, visual overlay raises target grounding accuracy from 40.0% to 90.0% over 20 trials.
- On unseen participants, GIVE gets 8/10, 8/10, and 6/10 Identify SR for the seen participant, unseen participant A, and unseen participant B, while the baseline gets 4/10, 1/10, and 0/10.

## Link
- [https://arxiv.org/abs/2606.13435v1](https://arxiv.org/abs/2606.13435v1)
