---
kind: ideas
granularity: day
period_start: '2026-05-03T00:00:00'
period_end: '2026-05-04T00:00:00'
run_id: b8ba9f5b-127f-47cc-b94f-0b755ace37a5
status: succeeded
topics:
- robot learning
- VLA
- sim-to-real
- teleoperation
- world models
- planning security
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vla
- topic/sim-to-real
- topic/teleoperation
- topic/world-models
- topic/planning-security
language_code: en
pass_output_id: 129
pass_kind: trend_ideas
upstream_pass_output_id: 128
upstream_pass_kind: trend_synthesis
---

# Robot Learning Deployment Checks

## Summary
Recent robot learning papers give concrete tests for deployment work: collect VLA demonstrations with cheap teleoperation and training-ready logs, tune simulation randomization against real images before dexterous hand transfer, and wrap long-horizon policies with subgoal progress checks during rollout.

## Phone-based teleoperation with LeRobot-format recording for VLA fine-tuning
Small robotics labs can treat the teleoperation interface and data format as part of the model test. Phone2Act shows a practical pattern: an Android phone publishes 6-DoF pose and button events through ARCore at 50 Hz, ROS 2 maps those events into robot target poses, and robot-specific bridge nodes handle the final API calls. The recorder writes synchronized RGB frames, joint states, end-effector poses, and gripper state at 20 Hz into LeRobot-format MP4 and Parquet files.

A useful adoption check is to build one bridge node for the local arm, collect roughly 100 to 150 episodes on a single manipulation task, measure phone-to-actuation latency with high-speed video, and fine-tune an existing VLA checkpoint. Phone2Act reports 130 collected episodes, GR00T-N1.5-3B fine-tuning, and 9 successes in 10 Dobot CR5 ball-to-basket trials, with 350–440 ms end-to-end latency. VILAS points in the same operational direction for low-cost manipulation setups: it uses an $8,000 arm, gripper, dual RealSense cameras, teleoperation, and a soft gripper extension, then compares pi_0, pi_0.5, and GR00T N1.6 on real grape grasping with latency and sequential-grasp results.

### Evidence
- [Phone2Act: A Low-Cost, Hardware-Agnostic Teleoperation System for Scalable VLA Data Collection](../Inbox/2026-05-03--phone2act-a-low-cost-hardware-agnostic-teleoperation-system-for-scalable-vla-data-collection.md): Phone2Act details the phone teleoperation stack, ROS 2 bridge pattern, LeRobot-format recording, latency, data volume, and Dobot success result.
- [VILAS: A VLA-Integrated Low-cost Architecture with Soft Grasping for Robotic Manipulation](../Inbox/2026-05-03--vilas-a-vla-integrated-low-cost-architecture-with-soft-grasping-for-robotic-manipulation.md): VILAS supports the low-cost hardware angle with an $8,000 VLA manipulation setup, teleoperation data, soft gripper hardware, and real grasping metrics.

## VLM-scored simulation randomization for dexterous hand transfer
Dexterous manipulation teams can add a scoring loop before training policies in simulation: render candidate randomized scenes, compare them with real reference images using a VLM realism score, and optimize the randomization distribution over lighting, texture, mass, friction, camera pose, and sensor noise. DexSim2Real implements this with GPT-4V as a visual realism critic and CMA-ES over the simulation parameters.

The concrete test is a small calibration run per task: capture real reference images, run 200–300 VLM queries, check whether the realism score rises, then train the same policy with the tuned randomization and a baseline randomization. DexSim2Real reports a rise in VLM realism score from 4.2/10 to 7.8/10, a friction mean error drop from 0.35 to 0.08, and about 2 GPU-hours of added overhead. On six Franka Panda and Allegro Hand tasks, it reports 78.2% average real-world success and an 8.3% average sim-to-real gap, compared with 28.5% for vanilla domain randomization and 19.2% for active domain randomization.

### Evidence
- [DexSim2Real: Foundation Model-Guided Sim-to-Real Transfer for Generalizable Dexterous Manipulation](../Inbox/2026-05-03--dexsim2real-foundation-model-guided-sim-to-real-transfer-for-generalizable-dexterous-manipulation.md): The summary gives the FM-DR method, optimized simulation parameters, query and overhead costs, real-world success rate, and sim-to-real gap comparisons.
- [DexSim2Real: Foundation Model-Guided Sim-to-Real Transfer for Generalizable Dexterous Manipulation](../Inbox/2026-05-03--dexsim2real-foundation-model-guided-sim-to-real-transfer-for-generalizable-dexterous-manipulation.md): The paper text states the 78.2% real-world success rate and 8.3% sim-to-real gap claim for dexterous manipulation transfer.

## Progress-gated subgoal supervision for long-horizon VLA rollouts
Teams testing long-horizon VLA policies can wrap the policy with a supervisor that maintains active goals, proposes reachable text and image subgoals, and checks rollout progress after execution steps. Anticipation-VLA gives a concrete design: a high-level model generates the next subgoal, an inverse dynamics check rejects mismatched text-image subgoals, and a value model classifies the rollout as achieved, improving, or stalled. That status controls whether the system continues, refines the subgoal, or pops a completed goal.

A cheap validation path is to run the same base policy with and without the supervisor on Libero-Long or a local multi-stage task, then log where stalls occur and whether recursive subgoal refinement recovers them. Anticipation-VLA reports 63.2 success on Libero-Long, above 54.6 for the underlying pi_0.5-style policy and 53.2 for a VLM-assisted version. In Arx-X5 real-world tests, the paper reports gains over baselines in both seen and unseen configurations, with the larger gain in unseen settings.

### Evidence
- [Anticipation-VLA: Solving Long-Horizon Embodied Tasks via Anticipation-based Subgoal Generation](../Inbox/2026-05-03--anticipation-vla-solving-long-horizon-embodied-tasks-via-anticipation-based-subgoal-generation.md): The summary specifies the goal stack, subgoal generation, inverse dynamics check, progress value model, Libero-Long score, and real-world gains.
- [Anticipation-VLA: Solving Long-Horizon Embodied Tasks via Anticipation-based Subgoal Generation](../Inbox/2026-05-03--anticipation-vla-solving-long-horizon-embodied-tasks-via-anticipation-based-subgoal-generation.md): The paper abstract states the long-horizon compounding-error problem and adaptive recursive subgoal generation approach.
