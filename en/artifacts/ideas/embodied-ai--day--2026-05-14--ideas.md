---
kind: ideas
granularity: day
period_start: '2026-05-14T00:00:00'
period_end: '2026-05-15T00:00:00'
run_id: 794c680a-5c69-4f90-8e0d-c508fe185027
status: succeeded
topics:
- embodied AI
- robotics
- VLA
- world models
- long-horizon planning
- video evaluation
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/robotics
- topic/vla
- topic/world-models
- topic/long-horizon-planning
- topic/video-evaluation
language_code: en
pass_output_id: 155
pass_kind: trend_ideas
upstream_pass_output_id: 154
upstream_pass_kind: trend_synthesis
---

# Targeted Reliability Fixes for Long-Running Robot Workflows

## Summary
Robot teams can act on narrow changes that target failures during extended execution: relative intervention for dexterous rollouts, household-planner tests that score goal progress and full completion separately, and RGB-derived depth features for placement-heavy VLA tasks.

## Relative correction mode for dexterous VLA rollouts
Dexterous robot labs should add a correction mode where the operator changes the hand and arm command relative to the current policy state while the VLA policy keeps running. The operational pain is the takeover jump: a human hand pose rarely matches the robot hand pose at the intervention moment, and an absolute teleoperation switch can break a stable grasp.

HandITL gives a concrete pattern to copy. It anchors the hand at intervention time, maps the operator’s relative fingertip motion to the robot hand, and adds wrist-controller residual velocity twists to the policy’s arm commands. The system also records the executed correction rollouts for later fine-tuning. A small adoption test is to instrument takeover command change, object drops or retries, and post-fine-tuning task success on two or three contact-heavy tasks before changing the base policy architecture.

### Evidence
- [Hand-in-the-Loop: Improving Dexterous VLA via Seamless Interventional Correction](../Inbox/2026-05-14--hand-in-the-loop-improving-dexterous-vla-via-seamless-interventional-correction.md): Summarizes HandITL’s relative correction method, takeover discontinuity results, task retry reductions, and fine-tuning gains from correction data.
- [Hand-in-the-Loop: Improving Dexterous VLA via Seamless Interventional Correction](../Inbox/2026-05-14--hand-in-the-loop-improving-dexterous-vla-via-seamless-interventional-correction.md): Describes the gesture-jump problem at the takeover boundary and the proposed relative intervention design.

## Long-horizon household planner tests with separate progress and completion scores
Teams evaluating household robot agents should run free-form multi-goal chores in simulation and report goal progress separately from full task completion. LongAct shows why this matters: a planner can complete many subgoals and still fail the whole chore after losing dependencies, forgetting object state, or failing to recover across rooms.

A practical test harness can use chores such as desk setup, kitchen reset, and cleaning sequences, with a step cap, object-state logging, and scoring for Success Rate, Goal-Condition Success, step count, and Improvement Rate. The agent should expose its dependency graph, spatial memory updates, and Critic decisions so failures can be traced to planning, memory, or execution recovery. LongAct’s reported gap is large enough to justify this evaluation work: pure Qwen3-VL-32B reaches 6.14% Goal-Condition Success and 0% Success Rate, while HoloMind with Qwen3-VL-32B reaches 51.2% Goal-Condition Success and 15.0% Success Rate.

### Evidence
- [When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution](../Inbox/2026-05-14--when-robots-do-the-chores-a-benchmark-and-agent-for-long-horizon-household-task-execution.md): Provides LongAct’s benchmark setup, metrics, HoloMind components, and reported Goal-Condition Success and Success Rate numbers.
- [When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution](../Inbox/2026-05-14--when-robots-do-the-chores-a-benchmark-and-agent-for-long-horizon-household-task-execution.md): Explains that LongAct tests instruction interpretation, state maintenance, dependency handling, and plan adaptation over thousands of steps.

## RGB-derived depth modulation for spatially precise VLA manipulation
Robot teams using multi-view RGB cameras can test a compact depth-feature module before adding depth hardware or large 3D models. The target workflows are grasping, placement, and object-object interaction tasks where 2D visual tokens lose relative position and depth cues.

Evo-Depth offers a concrete implementation path: extract compact latent depth features from multi-view RGB with IDEM, turn them into FiLM-style scale and shift terms with SEM, and modulate the vision-language tokens used by the action expert. A low-cost trial should compare the current VLA policy against a depth-modulated variant on placement-heavy tasks, while recording success rate, GPU memory, and inference frequency. The paper reports 90% average real-world success across three tasks, 3.2 GB GPU memory use, and 12.3 Hz inference for a 0.9B-parameter model.

### Evidence
- [Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model](../Inbox/2026-05-14--evo-depth-a-lightweight-depth-enhanced-vision-language-action-model.md): Summarizes Evo-Depth’s RGB-derived depth features, compact model size, benchmark results, and real-world deployment numbers.
- [Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model](../Inbox/2026-05-14--evo-depth-a-lightweight-depth-enhanced-vision-language-action-model.md): Describes the spatial weakness of 2D-only VLA policies on localization, placement, and spatially consistent manipulation.
