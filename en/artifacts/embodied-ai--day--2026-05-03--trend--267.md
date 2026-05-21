---
kind: trend
trend_doc_id: 267
granularity: day
period_start: '2026-05-03T00:00:00'
period_end: '2026-05-04T00:00:00'
topics:
- robot learning
- VLA
- sim-to-real
- teleoperation
- world models
- planning security
run_id: materialize-outputs
aliases:
- recoleta-trend-267
tags:
- recoleta/trend
- topic/robot-learning
- topic/vla
- topic/sim-to-real
- topic/teleoperation
- topic/world-models
- topic/planning-security
language_code: en
pass_output_id: 128
pass_kind: trend_synthesis
---

# Robot learning papers put deployment details under test

## Overview
Robot learning work this day centers on deployable systems. Vision-Language-Action (VLA) policies are tested with real hands, long-horizon subgoals, cheap data capture, and low-cost hardware. DexSim2Real, Anticipation-VLA, and Phone2Act give the clearest signal: success claims now depend on hardware trials, latency, data format, and failure checks.

## Clusters

### Dexterous sim-to-real transfer
DexSim2Real targets contact-rich hand manipulation without real demonstrations for the sim-to-real methods. It uses GPT-4V as a visual realism critic, then optimizes simulation randomization over lighting, texture, friction, mass, and camera noise. The policy also combines RGB, tactile readings, and proprioception through cross-attention during contact.

The reported hardware result is strong for this corpus: 78.2% average success over six real-world tasks on a Franka Panda with an Allegro Hand. The paper also reports an 8.3% average sim-to-real gap, compared with 28.5% for vanilla domain randomization and 19.2% for active domain randomization. The largest value is the mechanism, since the visual critic gives randomization a measurable target instead of relying only on hand-set ranges.

#### Evidence
- [DexSim2Real: Foundation Model-Guided Sim-to-Real Transfer for Generalizable Dexterous Manipulation](../Inbox/2026-05-03--dexsim2real-foundation-model-guided-sim-to-real-transfer-for-generalizable-dexterous-manipulation.md): Summary gives the FM-DR, tactile-visual policy, progressive curriculum, and six-task real-world success metrics.

### Adaptive subgoals for long-horizon VLA tasks
Anticipation-VLA addresses long tasks by keeping a stack of active goals and reachable subgoals. A high-level model proposes text and image subgoals. A value model then checks whether the task is achieved, improving, or stalled, and that status controls whether the system continues, refines the subgoal, or pops a completed goal.

The paper reports 63.2 success on Libero-Long, ahead of 54.6 for the underlying pi_0.5-style policy and 53.2 for a VLM-assisted version. In real-world Arx-X5 tests, the excerpt gives relative gains rather than exact success rates: +60% in seen configurations and +107% in unseen configurations. The useful lesson is operational. Long-horizon VLA execution needs state-dependent subgoals and progress checks, not a fixed recipe set before the rollout starts.

#### Evidence
- [Anticipation-VLA: Solving Long-Horizon Embodied Tasks via Anticipation-based Subgoal Generation](../Inbox/2026-05-03--anticipation-vla-solving-long-horizon-embodied-tasks-via-anticipation-based-subgoal-generation.md): Summary describes the goal stack, text-and-image subgoal generation, value model, Libero-Long result, and real-world relative gains.

### Low-cost data and hardware for real VLA deployment
Two papers treat data collection and robot cost as core research constraints. Phone2Act turns an Android phone into a 6-DoF teleoperator, sends pose events through ROS 2, and records synchronized robot data directly in LeRobot format. Fine-tuning GR00T-N1.5-3B on 130 collected episodes produced 9 successes in 10 Dobot CR5 ball-to-basket trials, with 350–440 ms end-to-end latency.

VILAS builds a roughly $8,000 manipulation setup using a Fairino FR5 arm, dual RealSense cameras, teleoperation, and a kirigami soft gripper extension for fragile objects. On grape grasping, pi_0.5 reached 84% single-grasp success, while GR00T N1.6 reached 58% multi-grasp success and the lowest mean inference latency among the tested models. These results make cost, logging format, and gripper mechanics part of the VLA performance claim.

#### Evidence
- [Phone2Act: A Low-Cost, Hardware-Agnostic Teleoperation System for Scalable VLA Data Collection](../Inbox/2026-05-03--phone2act-a-low-cost-hardware-agnostic-teleoperation-system-for-scalable-vla-data-collection.md): Summary gives Phone2Act architecture, LeRobot export, data rate, latency, and 90% real-world fine-tuning result.
- [VILAS: A VLA-Integrated Low-cost Architecture with Soft Grasping for Robotic Manipulation](../Inbox/2026-05-03--vilas-a-vla-integrated-low-cost-architecture-with-soft-grasping-for-robotic-manipulation.md): Summary gives VILAS hardware cost, soft gripper design, tested VLA models, grasp success rates, and latency.

### World-model planning needs sufficiency tests and attack tests
The world-model papers focus on what planning states preserve and how planners fail under triggers. Latent State Design proposes judging a world model by the function its latent state must support: prediction, control, planning, memory, grounding, or counterfactual reasoning. It offers a six-role taxonomy and a seven-axis evaluation matrix, but reports no new benchmark score.

TRAP gives the security counterpart. It attacks world-model planners by changing the ranking of imagined trajectories with a deployment-time visual patch. On DreamerV3 Crafter, it reports 98.1% attack success rate and a 63.2% mean return drop. On several DreamerV3 Atari and TD-MPC2 DMControl tasks, it reports 100% attack success. Together, the papers point to a concrete requirement for planned-control agents: evaluate the latent state for the task, then test whether the planner’s trajectory ranking can be manipulated.

#### Evidence
- [Latent State Design for World Models under Sufficiency Constraints](../Inbox/2026-05-03--latent-state-design-for-world-models-under-sufficiency-constraints.md): Summary gives the latent-state roles, sufficiency relationships, and seven-axis evaluation matrix.
- [TRAP: Tail-aware Ranking Attack for World-Model Planning](../Inbox/2026-05-03--trap-tail-aware-ranking-attack-for-world-model-planning.md): Summary gives TRAP’s tail-aware ranking attack method and reported attack success and return-drop metrics.
