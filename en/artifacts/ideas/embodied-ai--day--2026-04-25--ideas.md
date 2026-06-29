---
kind: ideas
granularity: day
period_start: '2026-04-25T00:00:00'
period_end: '2026-04-26T00:00:00'
run_id: decf0e23-b7c3-42ba-8013-b6b31563d5d0
status: succeeded
topics:
- robotics
- vision-language-action
- tactile sensing
- low-data post-training
- steerability
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/tactile-sensing
- topic/low-data-post-training
- topic/steerability
language_code: en
pass_output_id: 109
pass_kind: trend_ideas
upstream_pass_output_id: 108
upstream_pass_kind: trend_synthesis
---

# Adaptive Robot Instruction Control

## Summary
Robot adaptation work here points to two concrete changes in practice. Contact-heavy manipulation looks ready for sensor-stream retrofits that add tactile and torque inputs to existing VLAs, with large reported gains and limited latency cost. Low-data post-training also needs explicit instruction-following checks, because narrow demo sets can break steerability even when task execution improves. A small inference-time prompt guidance layer looks plausible as deployment support for adapted policies that need to follow new object and spatial instructions without another data collection cycle.

## Tactile and torque adapter retrofits for contact-heavy VLA tasks
Adding tactile and torque inputs to an existing VLA now looks like a practical upgrade for teams working on contact-heavy manipulation. The clearest target is a retrofit around tasks where camera views miss the deciding event: grasp stability on fragile items, contact onset during board wiping, or misalignment during plug insertion. MoSS keeps the physical signals in separate streams and joins them to the action model with shared attention, which matters because the gain did not come from a generic sensor concatenation story. On four real-robot tasks, the full setup lifted GR00T N1.5 from 20.8% average success to 49.0%, and pi_0 from 26.1% to 45.9%, with reported inference cost rising only to 1.11x for the dual-signal version.

The near-term build is a sensor add-on path for one or two failure-prone skills, not a full policy rewrite. A team already running GR00T, pi_0, or a similar diffusion-style VLA could attach fingertip tactile sensing and joint torque logging, keep those streams separate in the adapter, and test on a narrow set of contact-driven tasks. The cheap check is simple: compare vision-only, tactile-only, torque-only, and dual-signal variants on the same task mix. If the pattern matches the paper, the combined model should beat each single-signal version on the tasks where contact timing and force correction matter most.

### Evidence
- [Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models](../Inbox/2026-04-25--modular-sensory-stream-for-integrating-physical-feedback-in-vision-language-action-models.md): Summary reports average success gains on GR00T N1.5 and pi_0, the contact-rich task set, and the 1.11x inference overhead.
- [Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models](../Inbox/2026-04-25--modular-sensory-stream-for-integrating-physical-feedback-in-vision-language-action-models.md): Introduction explains why tactile and torque cues matter for plug insertion and other contact events that vision alone can miss.

## Instruction lock-in evaluation for low-data VLA post-training
Low-data post-training needs an instruction-following check before teams call an adapted robot policy ready for deployment. DeLock isolates a common failure: the policy learns the demonstrated task but stops obeying new prompts about objects, attributes, or spatial targets. The paper's fix is concrete. It keeps the visual encoder close to its pretrained state during fine-tuning, then applies Contrastive Prompt Guidance at test time to bias action generation toward the new instruction. In the reported eight-task evaluation with 20 trials each, this changed several novel-prompt cases from near-zero baseline performance to usable instruction following, including 19/20 versus 0/20 on T2 and 13/20 versus 1/20 on T8.

The workflow change is to add a small lock-in benchmark to every low-data adaptation run. For each adapted skill, hold back prompt variants that change object identity, attribute, or spatial relation, then compare standard fine-tuning against a visual-drift-regularized model with and without CPG. The paper's ablations give a useful acceptance test: without CPG, spatial-lock tasks collapsed to 0/20 across T5 to T8, while the full method reached 11/20 to 14/20 on T5 to T7 and 13/20 on T8. That makes steerability measurable with a modest trial budget before a team spends more time collecting demonstrations.

### Evidence
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): Summary defines lock-in, describes the visual regularization and CPG method, and gives the novel-prompt and ablation results.
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): Main text describes the low-data post-training setting and the over-specialization problem under narrow instruction coverage.

## Prompt-pair guidance layer for adapted robot policies
There is room for a thin support layer that sits between post-training and deployment: prompt-pair guidance for adapted robot policies. DeLock shows that much of the remaining instruction control can be recovered at inference time by running the policy with a novel prompt and a trained prompt, then combining their denoising fields. That is a usable product boundary because it avoids extra labels, auxiliary objectives, or larger datasets. The first users are teams that already have a policy adapted to a task and need it to obey prompt changes without retraining every time the wording or target relation changes.

A practical first version would expose a small library of trained-prompt anchors for each adapted skill, then evaluate which anchor helps the policy follow unseen prompts for object swaps, side changes, and placement changes. The evidence points to spatial instructions as the highest-value case. DeLock's ablation shows that removing CPG drove T5 to T8 to 0/20, while the full method restored 11/20, 13/20, 14/20, and 13/20. That suggests a deployment tool focused on prompt selection, prompt contrast, and trial logging could improve steerability even when the post-training dataset stays small.

### Evidence
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): Summary explains CPG as a test-time method and reports that removing it wipes out performance on spatial-lock tasks.
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): Abstract states that lock-in appears after low-data post-training and that the method recovers generalization to novel instructions.
