---
kind: ideas
granularity: day
period_start: '2026-04-14T00:00:00'
period_end: '2026-04-15T00:00:00'
run_id: 006dd63e-d43e-4c5c-97bc-f01a25413d82
status: succeeded
topics:
- robotics
- vla-safety
- humanoid-manipulation
- tactile-sensing
- 3d-geometry
tags:
- recoleta/ideas
- topic/robotics
- topic/vla-safety
- topic/humanoid-manipulation
- topic/tactile-sensing
- topic/3d-geometry
language_code: en
pass_output_id: 71
pass_kind: trend_ideas
upstream_pass_output_id: 70
upstream_pass_kind: trend_synthesis
---

# Embodied manipulation control

## Summary
Robotics work in this window points to three concrete workflow changes: evaluate VLA safety with stage-wise hazard progression and a refusal gate, add future tactile latent prediction to humanoid behavior cloning on contact-heavy tasks, and treat 3D geometry backbones as the default candidate for multi-view manipulation policies where viewpoint shift and placement precision matter.

## Stage-wise semantic safety checks for VLA action execution
A practical safety gate for VLA deployment is now straightforward to test: score every risky task with attempt, commit, and final success, then add a small refusal layer before action execution. HazardArena gives a clean way to do it because the safe and unsafe versions keep the same motion demands and change only the semantic condition that makes the action allowed or dangerous. That matters for teams that currently rely on task completion and think a low unsafe success rate means the policy is safe.

The paper shows why that workflow misses risk. On unsafe `insert outlet`, pi_0 reaches attempt 0.93 and commit 0.80 before final success 0.44. A robot can get most of the way into a dangerous action even when it does not finish. The same benchmark also shows that fine-tuning on safe demonstrations can raise safe success and unsafe success together. For a team shipping household or service manipulation, the near-term build is a semantic pre-execution check tied to a refusal action, plus stage-wise logging in evaluation. A cheap validation pass is to replay a small set of safe and unsafe twin tasks and look for policies whose unsafe commit rate rises as general task skill improves.

### Evidence
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md): HazardArena defines safe/unsafe twin tasks, stage-wise metrics, and the reported coupling between safe-task gains and unsafe behavior.
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md): The paper introduces the training-free Safety Option Layer as an inference-time guard for blocking unsafe actions.

## Future tactile latent prediction in humanoid behavior cloning
Humanoid manipulation teams have a concrete training change to try on contact-heavy tasks: predict future tactile latents during behavior cloning and keep touch in the policy input at runtime. HTD gives a direct case for this on real hardware. The gains are attached to jobs where visual state is incomplete at the moment of contact, including insertion, towel folding, scooping, and tea serving.

The evidence is specific enough to guide an implementation plan. HTD takes multi-view RGB, proprioception, hand-joint force, and tactile input, then adds future-touch prediction as an auxiliary target. Across five real-world tasks, it reports a 90.9% relative improvement in average success over ACT, and its latent tactile prediction beats raw tactile prediction by 30% in ablations. The system also handles 3.5 mm insertion clearance and runs the learned policy at 30 Hz. For labs already collecting teleoperation demonstrations, the missing support layer is often tactile logging and a latent prediction head, not a larger policy backbone. A cheap check is to add the auxiliary tactile target on one insertion or deformable-object task and compare contact failure modes, not just endpoint success.

### Evidence
- [Learning Versatile Humanoid Manipulation with Touch Dreaming](../Inbox/2026-04-14--learning-versatile-humanoid-manipulation-with-touch-dreaming.md): The summary gives the task set, the 90.9% relative gain over ACT, the 30% ablation gain for latent tactile prediction, and deployment details.
- [Learning Versatile Humanoid Manipulation with Touch Dreaming](../Inbox/2026-04-14--learning-versatile-humanoid-manipulation-with-touch-dreaming.md): The abstract states that HTD models touch as a core modality alongside multi-view vision and proprioception in a real humanoid system.

## 3D geometry backbones for multi-view manipulation policies
A strong near-term model choice for manipulation stacks with multi-view cameras is a 3D geometry backbone that learns control and scene reconstruction together. VGA makes that case with benchmark numbers that are high enough to affect model selection, especially for teams still using vision-language or video backbones for precise placement and viewpoint robustness.

The setup is concrete. VGA uses a pretrained 3D world model, feeds in multi-view RGB, language, and proprioception, and trains the shared backbone to predict actions together with camera parameters and depth maps. On LIBERO it reports 98.1% average, ahead of pi_0.5 at 96.9%, OpenVLA-oft at 97.1%, VLA-Thinker at 97.5%, GeoAwareVLA at 96.8%, and GeoVLA at 97.7%. The real-robot result in the excerpt is qualitative, but it points to better zero-shot transfer to unseen camera viewpoints. For a team choosing between backbone upgrades, a focused test is to freeze the downstream training recipe and swap only the representation stack on tasks where camera pose changes or object orientation precision drive failures.

### Evidence
- [Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models](../Inbox/2026-04-14--robotic-manipulation-is-vision-to-geometry-mapping-f-v-rightarrow-g-vision-geometry-backbones-over-language-and-video-models.md): The summary provides VGA's architecture, joint training setup, LIBERO scores, and comparisons with major baselines.
- [Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models](../Inbox/2026-04-14--robotic-manipulation-is-vision-to-geometry-mapping-f-v-rightarrow-g-vision-geometry-backbones-over-language-and-video-models.md): The abstract excerpt states better zero-shot generalization to unseen viewpoints in real-world deployments.
