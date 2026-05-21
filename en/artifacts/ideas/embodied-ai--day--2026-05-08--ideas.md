---
kind: ideas
granularity: day
period_start: '2026-05-08T00:00:00'
period_end: '2026-05-09T00:00:00'
run_id: 26352eda-dc39-49a0-8486-b73bb90d90e1
status: succeeded
topics:
- robotics
- vision-language-action
- world models
- tactile control
- federated learning
- policy adaptation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/tactile-control
- topic/federated-learning
- topic/policy-adaptation
language_code: en
pass_output_id: 139
pass_kind: trend_ideas
upstream_pass_output_id: 138
upstream_pass_kind: trend_synthesis
---

# Deployment Signals for Robot Control Loops

## Summary
Robot teams can test compact latent planning, gated tactile correction, and private-log training with concrete protocols from recent VLA papers. The common adoption blocker is no longer only model size or benchmark score; it is whether the control loop has the right deployment signal at the point of failure: reachable future state, contact feedback, or task labels for logs that cannot be pooled.

## Reachability checks for latent world-model planning
Teams adding a world model to a VLA should test whether latent rollouts are usable by the planner before trusting prediction loss. OneWM-VLA gives a practical build path: keep most of π0 frozen, compress each camera view and frame into one semantic latent token, then generate future latent tokens and action chunks with one flow-matching model. The reported gains are large enough to justify a small prototype, including 98.1% average success on LIBERO and 71.7% average real Piper-arm success under clean conditions.

The missing check is plannability. RC-aux shows why: short-horizon latent prediction can still create latent shortcuts where a goal looks close but cannot be reached within the action budget. A cheap evaluation is to add finite-budget reachability labels and temporal hard negatives to the world-model test suite, then compare action success against terminal latent distance on obstacle or long-horizon tasks. On Wall, RC-aux raises success from 50.4 ± 6.5 for the LeWM control to 83.6 ± 3.6, with planner ablations showing that the reachability-aware planner adds value beyond training alone.

### Evidence
- [One Token Per Frame: Reconsidering Visual Bandwidth in World Models for VLA Policy](../Inbox/2026-05-08--one-token-per-frame-reconsidering-visual-bandwidth-in-world-models-for-vla-policy.md): OneWM-VLA compresses each view and frame into one semantic token, jointly generates latent tokens and action chunks, and reports LIBERO and real Piper-arm gains.
- [Predictive but Not Plannable: RC-aux for Latent World Models](../Inbox/2026-05-08--predictive-but-not-plannable-rc-aux-for-latent-world-models.md): RC-aux identifies latent shortcuts as a planning failure mode and reports large gains from finite-budget reachability supervision.

## Gated tactile correction loops for contact-rich VLA tasks
Contact-heavy robot tasks need a fast correction path outside the normal VLA inference cadence. AT-VLA is a concrete retrofit: add a lightweight tactile encoder for 3D normal and tangential force, train a contact gate, and run a dual-stream loop where vision-language reasoning stays slow while tactile action correction runs at higher frequency. The gate protects pre-contact visual grounding by activating tactile input only after contact is detected.

This is most relevant for teams working on unzipping, wiping, stamping, lid rotation, insertion, and other tasks where vision alone misses force state. A practical test is to collect 30 to 50 demonstrations for one contact-rich operation, label contact states for the gate, and compare success with tactile input disabled at inference. AT-VLA reports closed-loop tactile reaction within 0.04 s and improves real-robot Wipe Vase success to 0.67 versus 0.07 for GO-1 and 0.33 for π0.5; Unzip Bag rises to 0.33 versus 0.20 and 0.00.

### Evidence
- [AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models](../Inbox/2026-05-08--at-vla-adaptive-tactile-injection-for-enhanced-feedback-reaction-in-vision-language-action-models.md): AT-VLA adds gated tactile feedback, a dual-rate tactile correction stream, and reports real-robot gains on contact-rich tasks.

## Federated pseudo-instruction training for private robot logs
Operators with vision-action robot logs can turn private fleet data into VLA training data without centralizing raw video or asking staff to write language annotations. ForgeVLA shows the workflow: train an embodied instruction classifier on a small public VLA dataset, run it locally on each client’s vision-action pairs to assign pseudo instructions, train client policies with an action loss plus contrastive planning loss, and aggregate updates on the server while keeping a global task representation bank.

The first deployment check is narrow: pick a fixed instruction set for one robot family, run local pseudo-labeling on held-out logs, and inspect whether task embeddings remain separated across clients. The paper names feature collapse under non-i.i.d. robot data as a failure mode, so embedding separation should be part of the acceptance test before longer federated runs. On LIBERO-Goal, ForgeVLA reaches 55.2% success and 100% Pass@50, compared with 28.8% and 80% for FedAvg, using 10 clients, 20 communication rounds, and 5 local epochs per round.

### Evidence
- [ForgeVLA: Federated Vision-Language-Action Learning without Language Annotations](../Inbox/2026-05-08--forgevla-federated-vision-language-action-learning-without-language-annotations.md): ForgeVLA trains from distributed vision-action logs with on-device pseudo instructions, contrastive planning loss, and adaptive server aggregation, with measured gains over FedAvg.
