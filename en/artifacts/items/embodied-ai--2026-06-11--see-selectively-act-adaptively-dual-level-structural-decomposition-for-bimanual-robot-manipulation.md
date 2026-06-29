---
source: arxiv
url: https://arxiv.org/abs/2606.13279v1
published_at: '2026-06-11T12:33:55'
authors:
- Yoon-Ji Choi
- Young-Chae Son
- Soo-Chul Lim
topics:
- bimanual-manipulation
- vision-language-action
- mixture-of-experts
- visual-routing
- robot-learning
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# See Selectively, Act Adaptively: Dual-Level Structural Decomposition for Bimanual Robot Manipulation

## Summary
The paper tackles bimanual manipulation failures caused by changing visual relevance and changing arm coordination across task stages. It adds explicit routing for what to see and how to act, and reports large gains over a monolithic VLA baseline in simulation and real-world tasks.

## Problem
- Bimanual tasks shift between independent and coordinated arm motion as the task progresses.
- The useful wrist camera view also changes across stages, so a single shared policy can mix irrelevant visual cues with task-critical ones.
- Monolithic Vision-Language-Action policies do not separate view relevance from interaction mode, which hurts robustness and generalization.

## Approach
- Build on a pretrained VLA policy and add two modules.
- Use a View-Selective Visual Router to reweight left and right wrist-view tokens based on the current task context.
- Use an Interaction-Aware Action Mixture-of-Experts to choose between coordinated-action and arm-wise-action experts.
- Train the routers with supervision labels from a KNN-based semi-automatic procedure and optimize the main flow-matching action loss plus router losses.

## Results
- On six RoboTwin 2.0 simulation tasks, the full model reaches 69.6% average success, compared with 41.9% for the monolithic baseline, 54.3% for the variant without IAMoE, and 59.7% for the variant without VSR.
- In simulation, it improves over the monolithic baseline by 27.7 percentage points on average.
- In real-world evaluation on three long-horizon tasks, it improves the overall average success rate over the monolithic baseline by 43.3 percentage points.
- On hard-setting simulation evaluation, it improves over the baseline by 35.7 percentage points on average.
- In real-world hard evaluation, it improves over the baseline by 30%, 40%, and 50% on R1, R2, and R3.
- On the complex simulation tasks S5 and S6, combining both modules gives gains of 13.4% and 6.7% over the two single-module variants in the easy setting, and 17.3% and 13.2% in the hard setting.

## Link
- [https://arxiv.org/abs/2606.13279v1](https://arxiv.org/abs/2606.13279v1)
