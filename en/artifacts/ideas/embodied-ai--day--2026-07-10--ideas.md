---
kind: ideas
granularity: day
period_start: '2026-07-10T00:00:00'
period_end: '2026-07-11T00:00:00'
run_id: 881de7fd-6d0b-4152-832f-0775438ef513
status: succeeded
topics:
- robot learning
- sample efficiency
- action representations
- tactile manipulation
- active perception
tags:
- recoleta/ideas
- topic/robot-learning
- topic/sample-efficiency
- topic/action-representations
- topic/tactile-manipulation
- topic/active-perception
language_code: en
pass_output_id: 347
pass_kind: trend_ideas
upstream_pass_output_id: 346
upstream_pass_kind: trend_synthesis
---

# Robot Policy Training and Deployment Diagnostics

## Summary
Robot teams can recover training signal from failed rollouts, test execution speed against force and controller limits, and audit latent actions for visual confounders before spending on robot-action adaptation. Each change fits into an existing VLA, action-chunking, or world-model pipeline and can be checked on a small offline batch or bounded robot trial.

## Hindsight relabeling for failed VLA rollouts
VLA teams with low early success rates should add a relabeling stage to RL post-training. A VLM reviews a failed rollout, writes an instruction for the behavior the robot completed, and scores the rollout against that instruction; the policy then trains on both the original task signal and the relabeled example. Learning from Hindsight kept 70%–80% of rollout groups usable, reached standard GRPO’s final LIBERO-PRO performance in about five training steps versus nearly 30, and achieved 56% success with 160 physical-robot rollouts compared with 22% for GRPO.

A low-cost check can run on stored failures before collecting more robot data. Relabel a few hundred trajectories, manually inspect a stratified sample for instruction and reward accuracy, then compare usable-group rate and held-out task success with the current reward pipeline. Deployment should keep relabeling focused on coherent completed behavior and reject ambiguous clips, since incorrect hindsight instructions would train the policy on mislabeled actions.

### Evidence
- [Learning More from Less: Reinforcement Learning from Hindsight](../Inbox/2026-07-10--learning-more-from-less-reinforcement-learning-from-hindsight.md): Documents the relabeling method, usable-group rates, sample-efficiency result, backbone coverage, and physical Franka comparison.
- [Learning More from Less: Reinforcement Learning from Hindsight](../Inbox/2026-07-10--learning-more-from-less-reinforcement-learning-from-hindsight.md): Describes the operational workflow in which one VLM proposes hindsight instructions, scores rollout groups, and supplies joint training signal.

## Speed and force acceptance tests for action-chunking policies
Manipulation teams should evaluate action policies across a speed-and-contact envelope before choosing an execution rate. B-spline Policy provides continuous action curves that can be resampled at higher control frequencies and retimed without retraining. PAC-ACT supplies a complementary post-training method for contact tasks by optimizing eight-step action chunks with PPO and constraining updates near the pretrained ACT policy.

The acceptance test should report completion time, success, tracking error, peak force, and the share of force samples above a task-specific threshold at each speed setting. B-spline Policy cut table-cleaning time from 23.57 to 11.80 seconds while success moved from 13/20 to 14/20, yet its Speed Stacking result fell to 0/20 at 4× speed because of controller tracking limits. PAC-ACT reduced force readings above 60 N by 46 times on a precision-contact task. A bounded trial at 1×, 2×, and 4× speed can identify the usable operating range before a longer deployment run.

### Evidence
- [B-spline Policy: Accelerating Manipulation Policies via B-spline Action Representations](../Inbox/2026-07-10--b-spline-policy-accelerating-manipulation-policies-via-b-spline-action-representations.md): Provides real-robot timing and success results, integration details, and the failure at aggressive speedup.
- [PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers](../Inbox/2026-07-10--pac-act-post-training-actor-critic-for-action-chunking-transformers.md): Provides the chunk-level RL design and reported reduction in force readings above 60 N.
- [PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers](../Inbox/2026-07-10--pac-act-post-training-actor-critic-for-action-chunking-transformers.md): Explains why pose and contact distribution shifts create force-safety failures in behavior-cloned action-chunking policies.

## Visual-confounder audits for latent action models
World-model teams using unlabeled video should test whether latent actions encode camera motion, static backgrounds, or untouched objects before robot-action adaptation. A compact audit can include duplicated frames as a zero-transition control, horizontal and vertical camera shifts, background swaps, and object changes outside the interaction region. The model should produce a near-zero action for duplicated frames and remain stable under visual changes that do not alter the embodied action.

CD-LAM shows that this audit can guide a targeted fine-tuning stage using embodiment-weighted reconstruction, action-centric contrastive learning, and latent-space calibration. Its camera-shift response fell from 0.555 to 0.156 horizontally and from 0.545 to 0.110 vertically; the 14B model matched the DreamDojo reference with more than 12 times fewer robot-action adaptation updates. Teams can first run these perturbations on a few hundred held-out clips, then proceed to expensive action-labeled training only when latent responses track robot and object interaction consistently.

### Evidence
- [Causally Debiased Latent Action Model for Embodied Action Conditioned World Models](../Inbox/2026-07-10--causally-debiased-latent-action-model-for-embodied-action-conditioned-world-models.md): Reports the confounder audit metrics, debiasing objectives, and robot-action adaptation efficiency.
- [Causally Debiased Latent Action Model for Embodied Action Conditioned World Models](../Inbox/2026-07-10--causally-debiased-latent-action-model-for-embodied-action-conditioned-world-models.md): Explains how reconstruction-only latent action training admits backgrounds and non-interacted objects into action codes.
- [Causally Debiased Latent Action Model for Embodied Action Conditioned World Models](../Inbox/2026-07-10--causally-debiased-latent-action-model-for-embodied-action-conditioned-world-models.md): Details the staged fine-tuning pipeline used before adaptation to executable robot actions.
