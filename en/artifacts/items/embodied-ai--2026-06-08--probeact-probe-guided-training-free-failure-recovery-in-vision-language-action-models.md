---
source: arxiv
url: https://arxiv.org/abs/2606.09740v1
published_at: '2026-06-08T17:04:24'
authors:
- Fan Zhang
- Seongbin Park
- Baharan Mirzasoleiman
- Shariar Talebi
- Nader Sehatbakhsh
topics:
- vision-language-action
- failure-recovery
- control-barrier-functions
- hidden-state-probing
- robot-manipulation
- libero-plus
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models

## Summary
ProbeAct is a runtime recovery system for frozen vision-language-action robot policies. It raises OpenVLA-OFT success on LIBERO-plus from 69.6% to 74.1% by detecting failed grasps and steering actions away from repeated failure locations.

## Problem
- VLA robot policies often fail under camera, lighting, layout, and robot-start perturbations even when their internal visual features still contain useful object-location information.
- The failure matters because a robot can recognize the target yet execute a memorized grasp path that misses the object, causing empty grasps, drops, or bad placements.
- Prior runtime fixes often need external vision modules, extra symbols, 3D reprojection, new sensing, or policy retraining.

## Approach
- ProbeAct keeps the VLA weights fixed and adds a small multi-target MLP probe trained on 50,000 hidden-state/object-position pairs. The probe reads layer-8 spatial tokens and predicts 3D positions for task objects.
- Hungarian matching handles multiple objects during probe training, and online Hungarian matching keeps object identities stable during rollout.
- A kinematic state machine detects grasp, transport, and placement failures using gripper width, end-effector motion, and probe-tracked object motion.
- After an initial failure, the system lets the policy retry. After repeated failure in the same region, it adds a Control Barrier Function zone and projects the VLA action to avoid that zone while changing the action as little as possible.
- Multi-step tasks reset object tracking and barrier zones after each completed placement.

## Results
- On LIBERO-plus, ProbeAct improves OpenVLA-OFT total success from 69.6% to 74.1%, a gain of 4.5 percentage points.
- Category gains over OpenVLA-OFT are 56.4% to 63.8% on Camera, 31.9% to 40.3% on Robot Initial States, 79.5% to 82.0% on Language, 88.7% to 93.6% on Light, 93.3% to 93.5% on Background, 75.8% to 76.8% on Noise, and 74.2% to 80.9% on Layout.
- On a fine-tuned OpenVLA-OFT-mixdata checkpoint for Robot Initial States, ProbeAct improves average success from 28.0% to 32.2%, with suite gains of +2.0, +6.8, +4.9, and +3.1 points.
- In a 300-episode Objects Layout drift study, the probe has 6.9 cm mean target error while the action endpoint has 23.6 cm error. On failed episodes, the probe error is 10.4 cm and the endpoint error is 34.9 cm.
- Probe quality peaks at layer 8 with image-spatial pooling, reaching R² = 0.968; other layer-8 pooling results are 0.926 for image mean, 0.815 for last token, and 0.869 for language mean.
- Step analysis reports 151 rescued tasks, with ProbeAct finishing rescued cases in 197 steps versus the baseline timeout at 600 steps. Across 2,591 tasks, average steps fall from 275 to 255.

## Link
- [https://arxiv.org/abs/2606.09740v1](https://arxiv.org/abs/2606.09740v1)
