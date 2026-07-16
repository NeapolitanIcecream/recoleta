---
kind: ideas
granularity: week
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-29T00:00:00'
run_id: b0ab954b-e654-4caf-86de-008a63ee7d2b
status: succeeded
topics:
- robotics
- vision-language-action
- robot manipulation
- deployment adaptation
- robot safety
- world models
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/robot-manipulation
- topic/deployment-adaptation
- topic/robot-safety
- topic/world-models
language_code: en
pass_output_id: 321
pass_kind: trend_ideas
upstream_pass_output_id: 320
upstream_pass_kind: trend_synthesis
---

# Robot-Side VLA Release Checks

## Summary
Robot VLA teams can test reliability with short robot-side procedures: online rollout fine-tuning after imitation training, safe pre-task calibration clips for changed setups, and trajectory-level safety scoring that separates clean completion from risky completion.

## Short online rollout fine-tuning before releasing a VLA manipulation policy
A manipulation team that already has an imitation-trained VLA can add a bounded online fine-tuning stage on the target robot before release. The useful build is a rollout runner that keeps the demonstration buffer, collects on-policy attempts, warms up the critic on mixed offline and rollout data, and filters candidate actions by value before updating the policy.

FORCE gives a concrete test case for this workflow. On six real-world Franka tasks, its reported average success rose from 45.0% under behavior cloning to 98.3% after online fine-tuning, with average execution steps falling from 112.8 to 38.9. The reported online stage used no human intervention. A practical first check would run the procedure on one high-value station task and compare behavior cloning, critic warm-up without actor updates, and full value-filtered updates under the same rollout budget.

### Sources
- [FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation](../Inbox/2026-06-24--force-efficient-vla-reinforcement-fine-tuning-via-value-calibrated-warm-up-and-self-distillation.md): FORCE reports the offline-to-online RL recipe, the critic warm-up mechanism, the value-guided action filtering, and the real-world Franka success and execution-step changes.
- [FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation](../Inbox/2026-06-24--force-efficient-vla-reinforcement-fine-tuning-via-value-calibrated-warm-up-and-self-distillation.md): The abstract states the sample-efficiency problem, value-calibrated warm-up, Q-based filtering, and no-human-intervention claim.

## Safe pre-task calibration clips for changed cameras and robot setups
VLA deployments with moved cameras, calibration drift, or changed end effectors need a small setup-identification step in the runbook. The build is direct: before the task, execute a few safe target poses, record the start image, action, and resulting image, then pass those clips as cached context for the task policy. The same log format can store action-consequence triplets during execution, so the policy can keep seeing how its own commands change the scene in the current setup.

ICWM reports gains under unseen camera viewpoints using task-agnostic probing clips, with no test-time weight updates or task demonstrations. Reflective VLA reports that full observation-action-consequence triplets beat observation-only and action-only context under camera and robot-calibration shifts. G3VLA adds a complementary engineering route for multi-camera cells: inject intrinsics and extrinsics into visual tokens through ray embeddings, PRoPE, and cross-view fusion while keeping the action pathway unchanged.

### Sources
- [In-Context World Modeling for Robotic Control](../Inbox/2026-06-24--in-context-world-modeling-for-robotic-control.md): ICWM describes safe random probing before task execution, cached context, and gains on seen and unseen LIBERO viewpoints.
- [Reflective VLA: In-Context Action Consequences Make VLAs Generalize](../Inbox/2026-06-23--reflective-vla-in-context-action-consequences-make-vlas-generalize.md): Reflective VLA reports rolling observation-action-consequence triplets and ablations showing that full triplets improve generalization under camera and calibration shifts.
- [G$^3$VLA: Geometric inductive bias for Vision-Language-Action Models](../Inbox/2026-06-23--g-3-vla-geometric-inductive-bias-for-vision-language-action-models.md): G3VLA describes adding camera intrinsics and extrinsics to visual tokens and reports gains on spatial and camera-sensitive manipulation tasks.

## Trajectory-level safety scoring for VLA manipulation tests
VLA test suites should log whether each completed rollout stayed safe through the whole motion. The concrete tool is a safety ledger for every episode: safe success, unsafe success, safe failure, unsafe failure, cumulative safety cost, and risk exposure time. This matters for release decisions because a robot can finish the instruction after brushing a hazard, entering a restricted zone, or colliding with a nearby object.

ForesightSafety-VLA shows the shape of the measurement. Across completed baselines, unsafe success appears even for the strongest listed policy: OpenVLA-oft reports unsafe success rate 0.06 and cumulative safety cost 0.18, while weaker baselines show higher unsafe shares among successful episodes. LIBERO-Safety adds a practical source of test cases: 75 tasks across physical and semantic safety suites, plus 19,664 screened collision-free demonstrations generated with keyposes and CuRobo collision checks. A small deployment version can start with the hazards already present in the workcell and add safety predicates to the rollout logger before expanding the task set.

### Sources
- [ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models](../Inbox/2026-06-25--foresightsafety-vla-a-unified-diagnostic-safety-benchmark-for-vision-language-action-models.md): ForesightSafety-VLA defines safe and unsafe rollout outcomes plus cumulative safety cost, risk exposure time, and safety-adjusted success rate, with baseline unsafe-success results.
- [ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models](../Inbox/2026-06-25--foresightsafety-vla-a-unified-diagnostic-safety-benchmark-for-vision-language-action-models.md): The benchmark abstract states process-level risk measurement and the four-quadrant safe/unsafe success and failure decomposition.
- [LIBERO-Safety: A Comprehensive Benchmark for Physical and Semantic Safety in Vision-Language-Action Models](../Inbox/2026-06-22--libero-safety-a-comprehensive-benchmark-for-physical-and-semantic-safety-in-vision-language-action-models.md): LIBERO-Safety provides the safety task structure, generated collision-free demonstrations, and evidence that current VLA policies still drop on hard safety levels.
