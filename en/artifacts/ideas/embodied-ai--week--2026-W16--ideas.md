---
kind: ideas
granularity: week
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-20T00:00:00'
run_id: 006dd63e-d43e-4c5c-97bc-f01a25413d82
status: succeeded
topics:
- robotics
- embodied-ai
- vla
- evaluation
- long-horizon-control
- memory
- safety
- geometry
tags:
- recoleta/ideas
- topic/robotics
- topic/embodied-ai
- topic/vla
- topic/evaluation
- topic/long-horizon-control
- topic/memory
- topic/safety
- topic/geometry
language_code: en
pass_output_id: 83
pass_kind: trend_ideas
upstream_pass_output_id: 82
upstream_pass_kind: trend_synthesis
---

# State-Aware Robot Execution

## Summary
The week points to concrete changes in how robot systems should be built and tested. Evaluation is getting more diagnostic, with stage-wise progress and hazardous precondition metrics exposing failure modes that aggregate success hides. Control stacks are also moving toward explicit planner state, where subtask, grounding, memory, and verification are passed through the loop as operational data. In lab automation, progress-based subtask switching now has enough evidence to treat it as a practical runtime component for multi-step protocols.

## Stage-wise long-horizon evaluation with hazardous commit tracking
Benchmarks for long-horizon manipulation need a failure log, not just a success number. LongBench gives a concrete template: split tasks by failure mechanism, score progress stage by stage, and keep fully observable tasks separate from tasks that require memory of earlier context. The practical build is an evaluation harness for robot teams already running tabletop or lab manipulation. It should tag episodes with mechanism labels such as phase dependence, error accumulation, temporal windows, and ambiguity classes, then report where the policy stalled or drifted. That is more useful for model selection than a single task-completion rate, because LongBench shows large gaps on specific mechanisms even when all models use the same 16-step open-loop interface. The same scoring style also fits safety review. HazardArena shows why endpoint success hides risk: a policy can reach a hazardous precondition, or nearly complete an unsafe action, without finishing it. A deployment-facing test rig should therefore add action-level `attempt`, `commit`, and `success` counters for unsafe twins of common tasks. Teams shipping VLA systems into homes, labs, or warehouses can build this with their existing teleoperation and replay stack before adding new model complexity. A cheap first check is to re-score one current benchmark or internal task set with stage-wise and pre-hazard metrics and see whether the ranking of candidate policies changes.

### Evidence
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): LongBench defines mechanism-aware long-horizon evaluation, stage-wise scoring, and shows large performance differences tied to execution robustness and temporal difficulty.
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md): HazardArena adds safe/unsafe twin tasks and `attempt`, `commit`, `success` metrics that expose hazardous progress hidden by endpoint success.

## Planner-state logging and controller interfaces for long-horizon manipulation
A planner state record is becoming a concrete control interface, not just an interpretability extra. HiVLA and Goal2Skill both improve manipulation by making intermediate control state explicit: subtask instruction, target object, localized visual grounding, memory of prior outcomes, post-condition checks, and recovery decisions. A useful build for robotics teams is a planner-state schema that every rollout writes and every controller reads. The schema can stay narrow: current subtask, target region, expected post-condition, timeout, error code, and next action if verification fails. That gives operators something they can inspect when a multi-step task goes off course, and it gives the low-level policy better inputs than a raw instruction plus recent frames. Goal2Skill reports a jump to 32.4% average success on five RMBench tasks versus 9.8% for the strongest baseline, with larger gains on memory-intensive tasks. HiVLA reports 83.3% average success on RoboTwin 2.0 and a clear lead on hard cluttered tasks by routing a grounded plan and target crop into a separate action expert. The immediate adoption path is a logging and control-layer change, not a full new foundation model. A cheap test is to add this state record to one existing long-horizon task and measure whether failure review becomes specific enough to separate planning errors from motor errors.

### Evidence
- [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](../Inbox/2026-04-15--goal2skill-long-horizon-manipulation-with-adaptive-planning-and-reflection.md): Goal2Skill uses structured memory, post-condition verification, and reflection to improve long-horizon task success, especially on memory-intensive tasks.
- [HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System](../Inbox/2026-04-15--hivla-a-visual-grounded-centric-hierarchical-embodied-manipulation-system.md): HiVLA exposes structured subtask plans and grounded target boxes, then feeds them into a separate controller with strong gains on cluttered and long-horizon manipulation.

## Progress-based subtask handoff for multi-step lab automation
A progress head for subtask switching looks ready for applied lab automation where tasks have clear stage boundaries and high restart cost. ChemBot uses a progress-aware Skill-VLA that predicts subtask completion on a 0 to 1 scale, then hands control back to the planner when the threshold is crossed. It pairs that with short-term scene memory, long-term retrieval of successful trajectories, and a structured scene description for the planner. The direct product is a lab robot runtime that ends a skill because the task state says the step is done, not because a fixed action horizon elapsed. That matters in chemical workflows where stirring, pouring, heating, and transfer steps vary in duration and failures compound across a protocol. The paper reports better real-world task success than full-trajectory baselines on three multi-step UR3 experiments, and its ablations show the scene description and subtask chain carry much of the decomposition gain while memory cuts context load. A first user is a research lab automating repetitive wet-lab procedures with a limited skill library. A cheap check is to retrofit one existing scripted or VLA-driven procedure with a scalar progress estimator and compare unnecessary extra motions, premature handoffs, and restart frequency across repeated runs.

### Evidence
- [Long-Term Memory for VLA-based Agents in Open-World Task Execution](../Inbox/2026-04-17--long-term-memory-for-vla-based-agents-in-open-world-task-execution.md): ChemBot combines progress-aware subtask switching, structured scene description, and dual-layer memory, with reported gains on multi-step real-world chemical tasks.
