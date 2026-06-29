---
kind: ideas
granularity: week
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-27T00:00:00'
run_id: decf0e23-b7c3-42ba-8013-b6b31563d5d0
status: succeeded
topics:
- robotics
- vision-language-action
- contact-rich manipulation
- world models
- evaluation
- safety
- adaptation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/contact-rich-manipulation
- topic/world-models
- topic/evaluation
- topic/safety
- topic/adaptation
language_code: en
pass_output_id: 113
pass_kind: trend_ideas
upstream_pass_output_id: 112
upstream_pass_kind: trend_synthesis
---

# Embodied task reliability

## Summary
This week supports three concrete moves: add physical feedback where contact failures dominate, screen generated robot rollouts for executability before using them in training or planning, and expand VLA evaluation with intervention tests that expose state-tracking and composition failures. The common thread is execution under real task pressure: contact, recovery, and task completion are becoming the useful unit of measurement.

## Physical-feedback adapters for pretrained VLAs on contact-heavy skills
Adding a physical-feedback adapter to an existing VLA now looks like a practical build for teams stuck on plug insertion, fragile picks, wiping, or other contact-heavy steps. The best evidence this week comes from MoSS: a modular add-on that keeps tactile and torque streams separate, aligns them with a pretrained VLA in two stages, and then fine-tunes jointly. On four real robot tasks, average success rose from 20.8% to 49.0% on GR00T N1.5 and from 26.1% to 45.9% on pi_0, with only modest inference overhead. The useful product shape is narrow and concrete: a drop-in sensory sidecar for a small set of failure-prone skills, not a full retrain of the policy stack.

The first customer is a robotics team that already has a vision-language-action policy working on approach and gross motion, but loses reliability at first contact. A cheap validation pass is to instrument one or two recurring failure modes and compare three versions on the same robot: vision only, single physical modality, and dual-stream tactile plus torque. The MoSS ablations give a clear design constraint for that test. Decoupled streams, staged training, and a future-signal objective all mattered, so a quick prototype should preserve those choices instead of collapsing everything into one fused encoder. If the gains show up on a small contact suite with less than 1.1x latency cost, this becomes an easy support layer to justify for production manipulation.

### Evidence
- [Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models](../Inbox/2026-04-25--modular-sensory-stream-for-integrating-physical-feedback-in-vision-language-action-models.md): Real-robot results show large average success gains from adding tactile and torque streams to pretrained VLAs, with concrete task examples and low inference overhead.
- [Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models](../Inbox/2026-04-25--modular-sensory-stream-for-integrating-physical-feedback-in-vision-language-action-models.md): The paper explains why plug insertion and similar tasks need both tactile and torque cues at contact time.

## Executability screening for generated robot rollouts
Robot teams using world models need an executability gate before they trust generated rollouts for policy training or planner selection. RoboWM-Bench gives a direct template for that gate: generate a future manipulation video, convert it into robot actions, execute it in a controlled simulator, and score both intermediate steps such as contact or lift and final task completion. The reason to build this now is simple: visually strong generated videos still fall apart when executed. In the reported results, early contact often succeeds while the rest of the task fails. On robot evaluation, even the better models stay low on task success and often collapse after the first step in harder sequences such as putting an object into a drawer.

This is a workflow change more than a research benchmark. Any team collecting synthetic robot videos, using imagined futures for planning, or fine-tuning from generated traces can insert an executability screen before data enters training. The first version does not need a full new simulator stack. It needs a small task set with step checks, a video-to-action retargeting path for the embodiment in use, and pass-fail thresholds that reject visually plausible but mechanically wrong samples. A cheap pilot is to take the current top 100 generated rollouts for two tasks and measure the drop from contact to completion. If that gap is large, the team has a data quality problem that image-level evaluation is hiding.

### Evidence
- [RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation](../Inbox/2026-04-21--robowm-bench-a-benchmark-for-evaluating-world-models-in-robotic-manipulation.md): The benchmark is built around converting generated manipulation videos into executable actions and shows the gap between visual realism and task completion.
- [RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation](../Inbox/2026-04-21--robowm-bench-a-benchmark-for-evaluating-world-models-in-robotic-manipulation.md): The paper names common failure modes such as unstable contact prediction and non-physical deformations, which fit a pre-training executability gate.

## Controlled intervention test suites for VLA deployment checks
Evaluation for VLA models needs controlled intervention tests before teams claim instruction grounding or long-horizon competence. BeTTER gives a concrete pattern: keep the base manipulation tasks, then expand them with layout shifts, primitive recomposition, distractor perturbations, and temporal changes that force the model to track state and compose subgoals. This matters because standard benchmark scores can stay high while the same model collapses on small changes that a deployment environment will produce.

The most immediate build is an internal stress-test pack for the tasks a team already runs in simulation or on a workcell. The reported failures show where to focus. Instruction grounding can polarize around attribute words, and unseen subgoal compositions can drop success close to zero even when the component skills were seen separately. A cheap check is to duplicate five existing benchmark tasks, add one controlled intervention for each, and compare the delta in success rather than the absolute score. If the drop is severe, the team has an adoption blocker for any setting where layouts, object identities, or step order vary across shifts.

### Evidence
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md): BeTTER defines controlled interventions for instruction grounding, layout shifts, recomposition, and temporal extrapolation, with concrete failure rates.
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md): The authors argue these tests isolate reasoning failures from low-level control limits and report collapse under dynamic scenarios.
