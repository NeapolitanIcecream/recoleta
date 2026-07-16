---
kind: ideas
granularity: week
period_start: '2026-06-29T00:00:00'
period_end: '2026-07-06T00:00:00'
run_id: 9b886b15-3493-446f-a1b3-e5a9e5c56589
status: succeeded
topics:
- robot learning
- vision-language-action models
- world models
- robot manipulation
- deployment systems
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/world-models
- topic/robot-manipulation
- topic/deployment-systems
language_code: en
pass_output_id: 337
pass_kind: trend_ideas
upstream_pass_output_id: 336
upstream_pass_kind: trend_synthesis
---

# Robot VLA Execution Reliability

## Summary
Robot VLA work is moving into the parts of execution that break first: model-serving delays across fleets, long rollout drift, and policies that lose track of the scene change caused by contact. The practical work is to add scheduling, progress signals, and action-relevant future-change targets to existing robot pipelines, then test them against task completion rather than request latency or single-step prediction alone.

## SLO-qualified model-serving scheduler for multi-robot factory tasks
Factory robot teams running VLA, planner, safety, and monitor models should test a shared GPU serving pool with task-level SLOs before buying one accelerator path per robot. ROSA shows the concrete shape of the workflow: a declarative task file records the robot fleet, model components, prompts, call rates, retry rules, and fallback actions such as stop, resend, replan, or call a human. The scheduler then chooses model placement, request routing, batching, and per-task action rates against SLO-qualified action throughput.

A cheap validation is to replay logged robot observations through the current serving setup and a shared Ray Serve-style pool, then count only actions that arrive inside the task SLO and allow the robot to keep working safely. ROSA reports up to 12.06x higher SLO-qualified factory productivity than dedicated serving baselines on 8 NVIDIA H200 GPUs with up to 64 virtual robots, and up to 2.44x higher qualified factory action throughput than shared-server baselines without its scheduler. The adoption blocker is concrete: lower model latency is useful only when it changes safe task progress, and factory workloads include idle time during physical motion that dedicated GPU allocations waste.

### Sources
- [ROSA: A Robotics Foundation Model Serving System for Robot Factories](../Inbox/2026-07-01--rosa-a-robotics-foundation-model-serving-system-for-robot-factories.md): Describes ROSA’s shared GPU pool, declarative task file, scheduler inputs, and reported SLO-qualified throughput gains.
- [ROSA: A Robotics Foundation Model Serving System for Robot Factories](../Inbox/2026-07-01--rosa-a-robotics-foundation-model-serving-system-for-robot-factories.md): The paper abstract frames the system around shared GPU-pool serving, multi-model pipelines, failure handling, and factory productivity.

## Continuous progress heads for long-horizon bimanual assembly policies
Teams building long-horizon manipulation demos should add a continuous progress output to the policy and use it to trigger subtask transitions. FurnitureVLA gives a direct implementation pattern for bimanual assembly: decompose the job into language-conditioned subtasks such as grasping, alignment, insertion, lifting, rotation, and retreat; train the VLA to predict 14-dimensional dual-arm actions plus a scalar progress value; switch subtasks when progress crosses a threshold.

The key test is a full-task rollout, not a short subtask score. FurnitureVLA covers real-scale furniture assembly with 4 to 7 subtasks and 650 to 1,550 control steps. Its average simulated success rises from 0.48 for monolithic finetuning to 0.80 across three IKEA-style tasks. The ablations also give practical checks for deployment planning: removing the rear-camera setup drops average success to 0.50, and discrete progress prediction fails all three simulated furniture tasks. Progress supervision is most useful where early millimeter-scale errors push later steps into states missing from the demonstrations.

### Sources
- [FurnitureVLA: Learning Long-Horizon Bimanual Furniture Assembly with Vision-Language-Action Model](../Inbox/2026-07-01--furniturevla-learning-long-horizon-bimanual-furniture-assembly-with-vision-language-action-model.md): Summarizes FurnitureVLA’s continuous progress output, subtask triggering, long-horizon task setup, and success-rate gains.
- [FurnitureVLA: Learning Long-Horizon Bimanual Furniture Assembly with Vision-Language-Action Model](../Inbox/2026-07-01--furniturevla-learning-long-horizon-bimanual-furniture-assembly-with-vision-language-action-model.md): The abstract states the up-to-7-subtask, 1,550-control-step setting and the progress-enhanced VLA design.

## Cached future-change targets for manipulation policies under visual shifts
Manipulation policy teams can add a training pass that labels each demonstration with the intended scene outcome, the pixels likely to change, and local motion direction. Bridge-WA trains a future-change teacher on real robot trajectories, caches future tokens, change maps, and motion-flow maps, then trains a lightweight predictor so the deployed policy can run without the 5B teacher or dense future-image generation.

This is a practical fit for pick, push, pour, and insert tasks where the robot must act on the region that will change after contact while ignoring lighting, background, and distractors. The first experiment should compare the existing VLA against the future-change-conditioned policy on the same manipulation tasks with distractors, lighting shifts, and tablecloth changes. Bridge-WA reports 52.8% average success on VLABench versus 43.1% for the strongest listed success-rate baseline, and on Dobot hard-track averages it reports 62.8% with distractors, 74.0% under lighting shifts, and 70.4% under tablecloth shifts, compared with X-VLA at 53.2%, 65.2%, and 55.6%.

### Sources
- [Bridge-WA: Predicting Where and How the World Changes for Robotic Action](../Inbox/2026-07-02--bridge-wa-predicting-where-and-how-the-world-changes-for-robotic-action.md): Describes the future-change teacher, cached targets, lightweight predictor, inference setup, and benchmark results.
- [Bridge-WA: Predicting Where and How the World Changes for Robotic Action](../Inbox/2026-07-02--bridge-wa-predicting-where-and-how-the-world-changes-for-robotic-action.md): The abstract states the three compact priors and the deployment-time removal of dense future-image generation.
