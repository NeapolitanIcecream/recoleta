---
source: arxiv
url: https://arxiv.org/abs/2606.09258v1
published_at: '2026-06-08T09:30:38'
authors:
- Suyeon Shin
- Juwon Kim
- Hyeonbin Park
- Hyunseo Kim
- Hyundo Lee
- Hyung-Sin Kim
- Byoung-Tak Zhang
topics:
- vision-language-action
- failure-recovery
- robot-manipulation
- future-image-goals
- milestone-selection
- libero
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Back to the Familiar Future: Failure Recovery for VLA Policies via Pre-Imagined Milestone Selection

## Summary
B2FF improves failure recovery for frozen foresight-driven vision-language-action policies by selecting a pre-generated future image as the recovery goal. On failure-injected LIBERO, it raises UD-VLA average success from 56.3% to 74.0% with perturbation-aligned recovery timing.

## Problem
- VLA robot policies can drift away from demonstration-like states during manipulation because of action errors, contact changes, or external perturbations.
- Once the robot is off-trajectory, direct re-planning from the current image can produce unstable actions even when the task is still feasible.
- This matters for robot deployment because small recoverable mistakes, such as gripper shifts or object displacement, can otherwise cause full task failure.

## Approach
- Before execution, B2FF asks the frozen VLA to generate a bank of 12 future-image milestones from the clean initial observation. No actions are executed during this imagination step.
- At recovery time, it builds a local candidate set from the milestone bank using offsets {-1, 0, +1, +2, +4} around the recovery index.
- A learned selector scores each candidate milestone using the failure observation, recent observation history, and candidate images.
- The chosen milestone is fixed as the future-image goal, and the frozen VLA generates only the action chunk toward that image.
- The selector is trained offline with counterfactual rollouts that label whether each candidate milestone leads to task success, then refined with a one-step actor-critic-style objective.

## Results
- On failure-injected LIBERO, B2FF improves UD-VLA average success from 56.3% to 74.0%, a +17.7 percentage-point gain.
- On the same benchmark, B2FF scores 69.3% on Object, 66.0% on Spatial, 73.3% on Goal, and 87.3% on Long.
- The online-trigger variant reaches 64.5% average success on failure-injected LIBERO, compared with 56.3% for UD-VLA.
- On standard LIBERO without injected failures, B2FF raises UD-VLA average success from 91.3% to 93.7%.
- Selector ablations on failure-injected LIBERO-Object show full B2FF at 69.3% success, compared with 63.3% for scratch supervised training and 50.8% for observation-only scoring.
- In real-world tests across 90 recovery trials, B2FF reaches 61.1% overall success after selector tuning on 35 real-world recovery groups; the excerpt states it beats UD-VLA and fixed-anchor baselines but does not give their exact scores.

## Link
- [https://arxiv.org/abs/2606.09258v1](https://arxiv.org/abs/2606.09258v1)
