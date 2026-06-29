---
kind: ideas
granularity: day
period_start: '2026-04-26T00:00:00'
period_end: '2026-04-27T00:00:00'
run_id: decf0e23-b7c3-42ba-8013-b6b31563d5d0
status: succeeded
topics:
- robotics
- vision-language-action
- manipulation
- tactile sensing
- safety
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/manipulation
- topic/tactile-sensing
- topic/safety
language_code: en
pass_output_id: 111
pass_kind: trend_ideas
upstream_pass_output_id: 110
upstream_pass_kind: trend_synthesis
---

# Layered Contact Control

## Summary
Contact-stage manipulation is getting carved into more explicit control layers. One paper shows that separating approach motion from contact work can improve success with modest demonstration budgets. Another argues that tactile tasks need step-wise correction inside an action horizon, not only better chunk initialization. The safety survey adds a deployment requirement around VLA systems: threat-based evaluation and runtime checks belong in the operating workflow, not only in model training.

## Phase-labeled fine-tuning for contact-heavy manipulation
A two-phase manipulation policy is now a concrete build target for teams training on small robot-demonstration sets. Move-Then-Operate splits coarse approach motion from contact work, trains a separate expert for each phase, and routes each action chunk through the matching expert. In the reported RoboTwin2 setup, that lifted average success to 68.88% with 50 demonstrations per task, versus 44.75% for pi_0, with large gains on contact-heavy tasks such as Click Bell at 99% versus 44% and Place Cans Plasticbox at 79% versus 34%.

The practical workflow change is straightforward: label demonstration segments as approach or contact, then stop asking one action head to learn both behaviors from the same gradients. The paper’s own labeling pipeline uses video, language, subtask decomposition, and end-effector velocity cues, which makes this test cheap enough for an existing imitation-learning stack. A first check is to replay your current logs, split trajectories at contact onset, fine-tune two small adapters or heads, and measure whether final-stage failures drop on press, click, insert, and placement tasks. This looks most useful for labs and robotics teams that already have a base VLA policy but keep losing reliability at the last centimeter of motion.

### Evidence
- [Move-Then-Operate: Behavioral Phasing for Human-Like Robotic Manipulation](../Inbox/2026-04-26--move-then-operate-behavioral-phasing-for-human-like-robotic-manipulation.md): Summary gives the two-phase design, the dual-expert router, the 50-demo setup, and benchmark gains including the average success rate.
- [Move-Then-Operate: Behavioral Phasing for Human-Like Robotic Manipulation](../Inbox/2026-04-26--move-then-operate-behavioral-phasing-for-human-like-robotic-manipulation.md): Abstract confirms explicit decoupling into move and operate phases with a dual-expert policy and automatic phase labeling.

## Within-chunk action correction for visual-tactile manipulation
Visual-tactile policies need a within-chunk correction layer when contact conditions change faster than diffusion inference can replan. Tube Diffusion Policy gives a concrete pattern: keep diffusion for chunk-start action generation, then update the remaining actions at each step with a learned feedback flow driven by fresh visual and tactile observations. The paper reports consistent gains over imitation-learning baselines on Push-T and three additional visual-tactile manipulation tasks, plus two real-world experiments under disturbances.

That points to a buildable support layer for anyone already using chunked action policies on tactile tasks. The job is not a full new policy stack; it is an execution module that rewrites the rest of the current horizon after each observation. The cheap validation is to add disturbances during insertion, pushing, or deformable-object handling and compare open-loop chunk execution against step-wise corrected execution on recovery rate, contact loss, and overshoot. The missing evidence here is exact benchmark margins, so the immediate claim is about control architecture and test design, not a fixed expected gain.

### Evidence
- [Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation](../Inbox/2026-04-26--tube-diffusion-policy-reactive-visual-tactile-policy-learning-for-contact-rich-manipulation.md): Summary describes the action-tube design, the learned streaming feedback flow, and the reported qualitative performance scope.
- [Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation](../Inbox/2026-04-26--tube-diffusion-policy-reactive-visual-tactile-policy-learning-for-contact-rich-manipulation.md): Content states consistent outperformance on Push-T and three additional tasks, real-world disturbance experiments, and reduced denoising needs for real-time control.
- [Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation](../Inbox/2026-04-26--tube-diffusion-policy-reactive-visual-tactile-policy-learning-for-contact-rich-manipulation.md): Introduction explains why high-frequency tactile sensing and slow per-step diffusion inference create a reactivity gap in contact-rich manipulation.

## Runtime safety gating for VLA deployment
VLA deployment now needs a runtime safety gate and a threat-based evaluation checklist before field use. The safety survey maps attacks by timing and modality: training-time poisoning and backdoors, plus inference-time adversarial patches, cross-modal perturbations, jailbreaks, and freezing attacks. It also points to runtime defenses and standardized evaluation as open needs, which is useful guidance for teams moving a research VLA model into a real robot workflow.

A concrete adoption change follows from that map. Before deployment, teams can run a fixed preflight suite that perturbs camera input, language instructions, and state streams, then record action deviations, refusal behavior, stop latency, and recovery on longer trajectories. During operation, the same threat model supports a small runtime monitor that checks for prompt anomalies, observation inconsistency, and unsafe action sequences before execution continues. This is less a new model than a missing safety layer around existing VLA stacks. The survey does not provide a benchmark to adopt directly, so the near-term value is in turning its taxonomy into a local red-team and gating process.

### Evidence
- [Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms](../Inbox/2026-04-26--vision-language-action-safety-threats-challenges-evaluations-and-mechanisms.md): Summary provides the two-axis taxonomy, the main threat classes, and the call for runtime safety architectures and standard evaluation.
- [Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms](../Inbox/2026-04-26--vision-language-action-safety-threats-challenges-evaluations-and-mechanisms.md): Content lists the threat types and connects them to training-time and inference-time defenses, evaluation, and deployment.
- [Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms](../Inbox/2026-04-26--vision-language-action-safety-threats-challenges-evaluations-and-mechanisms.md): Abstract explains the embodied safety risks, multimodal attack surface, latency constraints, and trajectory-level error propagation that motivate deployment gating.
