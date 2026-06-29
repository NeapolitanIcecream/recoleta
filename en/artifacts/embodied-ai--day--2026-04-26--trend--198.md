---
kind: trend
trend_doc_id: 198
granularity: day
period_start: '2026-04-26T00:00:00'
period_end: '2026-04-27T00:00:00'
topics:
- robotics
- vision-language-action
- manipulation
- tactile sensing
- safety
run_id: materialize-outputs
aliases:
- recoleta-trend-198
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/manipulation
- topic/tactile-sensing
- topic/safety
language_code: en
pass_output_id: 110
pass_kind: trend_synthesis
---

# Contact-time control and VLA safety define the day’s robotics papers

## Overview
This day is strongest on embodied control that must work at contact time. Two papers focus on better execution in manipulation: Move-Then-Operate separates approach and contact phases, while Tube Diffusion Policy adds step-wise visual-tactile correction inside an action horizon. A third paper widens the frame with a survey of safety risks and defenses for vision-language-action, or VLA, systems, showing that deployment concerns are now part of the core research agenda.

## Clusters

### Behavioral phasing for precise manipulation
Move-Then-Operate argues that high-precision manipulation improves when the policy treats approach motion and contact work as separate behaviors. Its dual-expert design uses one expert for moving and one for operating, with a router selecting the phase per action chunk. On 8 RoboTwin2 tasks with 50 demonstrations per task, it reports 68.88% average success, above pi_0 at 44.75%, RDT at 35.63%, and ACT at 31.63%. The gains are large on contact-heavy tasks such as Click Bell at 99% versus 44% for pi_0 and Place Cans Plasticbox at 79% versus 34%. The paper also claims peak performance in 40% fewer training steps.

#### Evidence
- [Move-Then-Operate: Behavioral Phasing for Human-Like Robotic Manipulation](../Inbox/2026-04-26--move-then-operate-behavioral-phasing-for-human-like-robotic-manipulation.md): Summary and benchmark results for phased manipulation policy.

### Reactive visual-tactile control
Tube Diffusion Policy focuses on contact-rich control under uncertainty. It keeps diffusion for chunk-start action generation, then adds a learned streaming feedback flow so the robot can correct actions at each step from fresh visual and tactile input. The paper reports consistent gains over prior imitation-learning baselines on Push-T and three additional visual-tactile tasks, plus two real-world experiments with stronger reactivity under disturbances. The excerpt does not include exact success rates, so the main grounded takeaway is architectural: reactive within-chunk correction is being treated as a core control requirement for tactile manipulation.

#### Evidence
- [Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation](../Inbox/2026-04-26--tube-diffusion-policy-reactive-visual-tactile-policy-learning-for-contact-rich-manipulation.md): Summary of action-tube method and reported empirical scope.

### VLA safety taxonomy and evaluation scope
Safety is getting treated as a first-class research problem for vision-language-action models, not a side note attached to model scale. The VLA safety survey lays out a concrete threat map across training-time and inference-time attacks, and across training-time and runtime defenses. It covers threats such as data poisoning, backdoors, adversarial patches, cross-modal perturbations, jailbreaks, and freezing attacks, then ties them to evaluation and deployment issues across six domains. The paper is a survey rather than a new benchmark report, but it is useful as a sign of where the field now needs shared evaluation and runtime protection.

#### Evidence
- [Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms](../Inbox/2026-04-26--vision-language-action-safety-threats-challenges-evaluations-and-mechanisms.md): Survey summary with taxonomy, threat classes, and deployment scope.
