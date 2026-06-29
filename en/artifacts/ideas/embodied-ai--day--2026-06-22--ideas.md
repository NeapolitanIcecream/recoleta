---
kind: ideas
granularity: day
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-23T00:00:00'
run_id: f49899cd-dd3b-4d29-9ec3-992c8e857877
status: succeeded
topics:
- robotics
- vision-language-action models
- reinforcement learning
- robot safety
- world models
- human demonstrations
- shared autonomy
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/reinforcement-learning
- topic/robot-safety
- topic/world-models
- topic/human-demonstrations
- topic/shared-autonomy
language_code: en
pass_output_id: 307
pass_kind: trend_ideas
upstream_pass_output_id: 306
upstream_pass_kind: trend_synthesis
---

# Closed-Loop VLA Deployment Controls

## Summary
Robot VLA teams now have clearer near-term work to do before broader deployment: add safety-specific rollouts to release testing, route fine contact steps through shared autonomy, and collect recovery demonstrations at the states where a deployed policy is uncertain. The common pressure is closed-loop behavior after the model leaves offline imitation training.

## Safety-specific release tests for VLA manipulation policies
VLA manipulation teams should add a safety test stage that measures unsafe contact and unsafe instruction following separately from task completion. LIBERO-Safety gives a usable template: 75 tasks across affordance-aware grasping, human-robot interaction, tabletop spatial avoidance, free-space hand-object avoidance, and semantic safety reasoning, with difficulty levels L0-L2. The benchmark also includes 19,664 human-screened collision-free demonstrations generated from sparse keyposes and CuRobo collision checks.

The operational reason is simple: a policy can finish easy manipulation tasks and still fail around clutter, human hands, or held objects. In LIBERO-Safety, OpenVLA-OFT drops to 1.3% success on hard affordance-aware grasping, and π0.5 reaches only 35.3% on the same level. A practical release gate would run the same policy on standard task suites and on safety suites, log success, collision, refusal, and recovery behavior, and block deployment on tasks where L2 safety cases fail repeatedly.

### Evidence
- [LIBERO-Safety: A Comprehensive Benchmark for Physical and Semantic Safety in Vision-Language-Action Models](../Inbox/2026-06-22--libero-safety-a-comprehensive-benchmark-for-physical-and-semantic-safety-in-vision-language-action-models.md): LIBERO-Safety defines the safety suites, dataset size, data-generation method, and baseline failures under hard physical safety settings.
- [LIBERO-Safety: A Comprehensive Benchmark for Physical and Semantic Safety in Vision-Language-Action Models](../Inbox/2026-06-22--libero-safety-a-comprehensive-benchmark-for-physical-and-semantic-safety-in-vision-language-action-models.md): The paper abstract describes the parametric safety benchmark and the 19,664 collision-free demonstrations.

## Joystick handoff at grasping and release steps for assistive VLA robots
Assistive robot teams can test a frozen VLA with a contact-aware shared-control layer before collecting a large fine-tuning set. Assistron shows the shape of this workflow: the VLA handles language-conditioned macro movement, a wrist-camera detector watches for contact-heavy phases and predicted gripper-state changes, and the user gives joystick input during grasping, insertion, or release. The joystick command is blended into the VLA flow-matching denoising process, then control returns to autonomy.

This is a concrete fix for a common failure mode in home manipulation. Frozen VLAs can interpret broad intent but lose reliability at precise contact points. In a novice-user scene-recovery benchmark, Assistron reached 91.3% partial success, while the autonomous VLA reached 13.7% and timed out. The system still required active user input for 56.5% of the run, so the first adoption test should focus on whether the handoff reduces workload for weaker joystick users without creating new trust problems.

### Evidence
- [Assistron: Bayesian Shared Autonomy with Off-the-shelf Vision-Language-Action Models](../Inbox/2026-06-22--assistron-bayesian-shared-autonomy-with-off-the-shelf-vision-language-action-models.md): Assistron keeps the VLA frozen, triggers user intervention near contact-rich steps, and reports partial success, autonomy time, workload, and user-study results.
- [Assistron: Bayesian Shared Autonomy with Off-the-shelf Vision-Language-Action Models](../Inbox/2026-06-22--assistron-bayesian-shared-autonomy-with-off-the-shelf-vision-language-action-models.md): The paper motivates direct use of VLAs in assistive settings and describes the zero-shot reliability problem.

## Uncertainty-triggered recovery demonstrations with replay during VLA fine-tuning
Robot learning teams can shorten post-deployment adaptation by logging high-uncertainty states during rollouts and asking for recovery demonstrations from those states. RECALL uses INSIGHT to flag uncertain token-level decisions, collects recovery examples online, and then fine-tunes with replay data to preserve earlier skills.

The useful workflow change is to stop treating every failed task as a request for a full start-state demonstration. Demonstrators can spend time on the substeps where the policy is unsure, then replay older tasks during training. In RECALL, strong INSIGHT online recovery with full replay reaches 72.4% overall LIBERO-10 success, compared with 60.2% for matched passive collection. Training only on the new recovery data collapses retained behavior, with the best new-only setting at 28.4% overall success and 0.4% collected-task success, so the replay mix is part of the workflow, not an optional cleanup step.

### Evidence
- [RECALL: Recovery Experience Collection for Active Lifelong Learning in Vision-Language-Action Models](../Inbox/2026-06-22--recall-recovery-experience-collection-for-active-lifelong-learning-in-vision-language-action-models.md): RECALL reports uncertainty-guided recovery collection, the active-versus-passive comparison, and the failure of new-only fine-tuning without replay.
- [RECALL: Recovery Experience Collection for Active Lifelong Learning in Vision-Language-Action Models](../Inbox/2026-06-22--recall-recovery-experience-collection-for-active-lifelong-learning-in-vision-language-action-models.md): The paper explains why passive start-state demonstrations waste effort and why uncertain intermediate states are useful targets for new supervision.
