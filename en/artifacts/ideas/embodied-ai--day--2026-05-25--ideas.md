---
kind: ideas
granularity: day
period_start: '2026-05-25T00:00:00'
period_end: '2026-05-26T00:00:00'
run_id: 1c06e363-c98d-489c-b975-2263ff49b7ab
status: succeeded
topics:
- robot learning
- vision-language-action models
- world models
- reinforcement learning
- robot deployment
- adversarial reliability
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/world-models
- topic/reinforcement-learning
- topic/robot-deployment
- topic/adversarial-reliability
language_code: en
pass_output_id: 231
pass_kind: trend_ideas
upstream_pass_output_id: 230
upstream_pass_kind: trend_synthesis
---

# Factory VLA Execution Checks

## Summary
Manufacturing robot teams can make VLA pilots more concrete with task-specific failure logs, small online fine-tuning trials, and adversarial image checks. The shared practical move is to put pass/fail gates around real execution, action chunks, and visual failure cases.

## Failure-coded rollout logs for factory VLA packaging pilots
Factory VLA pilots need per-episode failure labels tied to production quality checks. The Siemens packaging study gives a useful starting schema for transparent accessory-bag insertion: contents above the product, multiple-bag grasp, incomplete insertion, and poor or failed grasp. The largest reported problem was bag contents left above the product, accounting for 65% of failed unconstrained episodes.

A manufacturing automation team could add these labels to every rollout review, then collect recovery episodes against the largest bucket after each evaluation round. The same review can track constrained and unconstrained trials separately, because the Siemens team first simplified the task and then removed constraints over later rounds. A cheap pilot is one packaging cell, one VLA policy, 30-bin-emptying style evaluations, and a rule that the next data collection round targets the top two failure categories.

### Evidence
- [A Factory-Floor Deployment Case Study of VLA Pipelines for Industrial Packaging Task: Workflow, Failures, and Lessons](../Inbox/2026-05-25--a-factory-floor-deployment-case-study-of-vla-pipelines-for-industrial-packaging-task-workflow-failures-and-lessons.md): Reports the Siemens factory packaging task, 2,535 episodes, iterative fine-tuning workflow, constrained-to-unconstrained rollout plan, and failure breakdown.
- [A Factory-Floor Deployment Case Study of VLA Pipelines for Industrial Packaging Task: Workflow, Failures, and Lessons](../Inbox/2026-05-25--a-factory-floor-deployment-case-study-of-vla-pipelines-for-industrial-packaging-task-workflow-failures-and-lessons.md): Confirms the factory task setup and the repeated loop of data collection, curation, fine-tuning, evaluation, and targeted recovery data collection.

## Operator-corrected replay buffers for action-chunk VLA fine-tuning
Robot teams adapting a pretrained VLA to a new manipulation task can test a small online RL loop that edits action chunks while keeping the base policy intact. EXPO-FT trains a lightweight edit policy over a pretrained π0.5 policy, lets a Q-function choose the base or edited action, and stores human corrections to individual timesteps inside action chunks.

The practical trial is narrow: run the zero-shot policy, add sparse binary rewards and rule-based success detectors, collect online rollouts with operator corrections, then run 30 human-judged evaluation trials. EXPO-FT reports 30/30 final successes on each of 8 real-world manipulation tasks after an average of 19.1 minutes of online robot data. That result is a reason to test an edit-policy loop on precision manipulation jobs where full task data collection would take days.

### Evidence
- [EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models](../Inbox/2026-05-25--expo-ft-sample-efficient-reinforcement-learning-finetuning-for-vision-language-action-models.md): Describes EXPO-FT’s pretrained VLA edit policy, action-chunk RL, operator corrections, sparse rewards, and reported 30/30 success after 19.1 minutes of online data.
- [EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models](../Inbox/2026-05-25--expo-ft-sample-efficient-reinforcement-learning-finetuning-for-vision-language-action-models.md): Confirms the paper’s claim of perfect task performance across evaluated manipulation tasks within an average of 19.1 minutes of online robot data.

## Pre-flight adversarial image tests for VLA robot policies
A VLA deployment checklist should include an image-perturbation test that measures action changes, not only clean-task success. The adversarial reliability paper cites OpenVLA-7B falling from above 95% LIBERO success to under 5% under a 16/255 PGD image attack, and it frames the issue as physical action safety because the model output moves the robot.

A practical audit can run PGD and Square attacks on a held-out set, compare clean and attacked actions across short horizons, and compute the paper’s encoder-specific ceiling or head-agnostic robustness ratio. The paper says these diagnostics can be computed from at most 200 samples and reports zero bound violations across 320 validation cells covering OpenVLA, LIBERO suites, attack types, horizons up to 10, and two action-head designs. This gives robot integrators a small pre-flight test for camera-facing policies before floor trials with people nearby.

### Evidence
- [Capability and Robustness Cannot Both Be Free: An Information-Theoretic Bound for Vision-Language-Action Models](../Inbox/2026-05-25--capability-and-robustness-cannot-both-be-free-an-information-theoretic-bound-for-vision-language-action-models.md): Summarizes the capability and adversarial reliability bound, the OpenVLA PGD drop, the 320-cell validation, and diagnostics computable from at most 200 samples.
- [Capability and Robustness Cannot Both Be Free: An Information-Theoretic Bound for Vision-Language-Action Models](../Inbox/2026-05-25--capability-and-robustness-cannot-both-be-free-an-information-theoretic-bound-for-vision-language-action-models.md): Confirms the paper’s reported zero violations and the proposed pre-flight encoder ceiling, defense-forensics probe, and head-agnostic robustness ratio.
