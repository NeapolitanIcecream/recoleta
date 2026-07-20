---
source: arxiv
url: https://arxiv.org/abs/2607.15714v1
published_at: '2026-07-17T07:51:03'
authors:
- Xiaojiang Peng
- Kai Peng
- Jie Lu
- Zheng Lian
- Zitong YU
- Xiaobo Wang
topics:
- vision-language-action
- robot-foundation-model
- compositional-generalization
- out-of-distribution
- robot-manipulation
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# AC-VLA: Robust Out-of-Distribution Action Execution via Compositional Learning

## Summary
AC-VLA improves compositional out-of-distribution execution in vision-language-action models by combining sub-task supervision with state-conditioned masking of wrist-camera inputs. On LIBERO, it raises π₀.₅ success on Spatial-OOD and Goal-OOD to 64.2% and 73.3% while keeping in-distribution success at 96.7% in the ablation and 98.0–98.4% across standard suites.

## Problem
- VLA models often memorize complete task trajectories and wrist-view visual shortcuts, so they fail when familiar pick-and-place sub-skills are recombined in new object-target or spatial configurations.
- This matters because standard in-distribution success can conceal poor compositional generalization: π₀.₅ reaches 98.8% on LIBERO-Spatial but only 35.5% on Spatial-OOD.

## Approach
- An LLM decomposes each instruction into ordered sub-tasks, while a proprioceptive aligner segments the trajectory using gripper-state transitions and low end-effector displacement, producing dense offline sub-task supervision without manual labels.
- Mixed training combines complete demonstrations with decomposed sub-task segments, preserving long-horizon coherence while teaching the policy to recombine reusable actions.
- During closed-gripper phases, the method masks wrist-camera inputs and retains third-person views, encouraging global spatial grounding during placement while preserving wrist feedback during approach and grasping.
- The components are architecture-agnostic and are evaluated with the π₀.₅ and GR00T-N1 VLA backbones without modifying their architectures or inference procedures.

## Results
- On LIBERO-OOD, AC-VLA with π₀.₅ achieves 64.2% on Spatial-OOD and 73.3% on Goal-OOD, improving over vanilla π₀.₅ by 28.7 and 26.7 percentage points and reaching an overall average of 87.3% versus 78.6%.
- AC-VLA with GR00T-N1 reaches 36.4% and 44.0% on Spatial-OOD and Goal-OOD, gains of 18.5 and 19.9 points over the backbone, while standard-suite success remains 92.3–99.1%.
- The ablation shows that mixed raw-task and sub-task training obtains 51.6%/67.5% OOD success versus 35.5%/46.6% for raw-task training, while retaining 96.6% in-distribution success; adding masking raises OOD success further to 64.2%/73.3% with 96.7% in-distribution success.
- In a real-world evaluation with a 6-DoF PIPER arm, AC-VLA improves OOD success from 35.0% to 82.5% and overall performance from 64.4% to 85.6%, while in-distribution success changes from 93.7% to 88.7%.
- The excerpt reports results on LIBERO, LIBERO-OOD, and four real-world in-distribution tasks plus two OOD variants; broader evidence beyond these evaluations is not provided.

## Link
- [https://arxiv.org/abs/2607.15714v1](https://arxiv.org/abs/2607.15714v1)
