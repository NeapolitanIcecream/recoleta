---
kind: ideas
granularity: week
period_start: '2026-05-25T00:00:00'
period_end: '2026-06-01T00:00:00'
run_id: 1c06e363-c98d-489c-b975-2263ff49b7ab
status: succeeded
topics:
- robot learning
- vision-language-action models
- real-robot evaluation
- dexterous manipulation
- tactile control
- continual learning
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/real-robot-evaluation
- topic/dexterous-manipulation
- topic/tactile-control
- topic/continual-learning
language_code: en
pass_output_id: 245
pass_kind: trend_ideas
upstream_pass_output_id: 244
upstream_pass_kind: trend_synthesis
---

# Robot Manipulation Deployment Checks

## Summary
Robot VLA work now gives teams concrete control checks for deployment: short online fine-tuning runs with regression tests, explicit SE(3) action geometry, and contact-force metrics for tasks where task success can hide unsafe handling.

## Online VLA fine-tuning station with old-task regression checks
Robot teams trialing pretrained VLA policies can build a small post-training station around online rollouts, human correction, sparse reward detectors, replay, and a fixed action-normalization setting. The target user is the operator who sees a policy reach a new task after fine-tuning, then finds that earlier skills have degraded.

EXPO-FT gives the practical template: keep the pretrained policy as the base, train a lightweight edit policy for action-chunk corrections, let a Q-function choose between base and edited chunks, and store human corrections from online rollouts in replay. The reported real-robot result is 30/30 success on eight manipulation tasks after an average of 19.1 minutes of online data, with final success judged by a human observer.

The regression side matters because sequential VLA fine-tuning can erase prior tasks. In a real-world continual-learning study, plain fine-tuning dropped Stack Bowl from 100.0 to 15.0 and Hang Cup from 97.5 to 25.0, while replay with a 0.2 buffer ratio, 0.2 replay frequency, and fixed action normalization reached a 93.5 final average score across four tasks. A useful adoption check is to run the new task and all previously accepted tasks after each fine-tuning stage, using the same action scaling across the deployment line.

### Sources
- [EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models](../Inbox/2026-05-25--expo-ft-sample-efficient-reinforcement-learning-finetuning-for-vision-language-action-models.md): EXPO-FT describes online off-policy RL fine-tuning for VLA action chunks, human corrections, sparse rewards, and 30/30 real-task success after 19.1 minutes of online data on average.
- [Can VLA Models Learn from Real-World Data Continually without Forgetting?](../Inbox/2026-05-26--can-vla-models-learn-from-real-world-data-continually-without-forgetting.md): The continual-learning study shows severe forgetting under plain sequential fine-tuning and strong retention from replay with fixed action normalization.

## SE(3) trajectory traces for VLA manipulation policies
Manipulation evaluations should ask VLA policies to expose the future end-effector poses they are using to produce action chunks. This is a cheap interface change for labs comparing policies across Franka, Kinova, ALOHA, or mobile manipulation setups: log the predicted pose trajectory, the executed action chunk, gripper commands, robot state, and the robot description used at inference.

OASIS shows why this trace is useful. It predicts an 8-step camera-frame SE(3) end-effector trajectory before decoding 6-DoF relative actions and gripper commands. Its ablation attributes the largest gain to the SE(3) trajectory predictor, with LIBERO-Long rising from 89.5% to 95.2% and LIBERO-Spatial from 91.6% to 99.0%. It also reports 89.2% average success in real-world tests on Franka Research 3 and Kinova Gen3 robots.

Qwen-VLA points to the cross-embodiment version of the same logging need. It uses embodiment-aware prompts that specify the robot tag, arm setup, control frequency, and prediction horizon, then trains actions and trajectories in a shared padded tensor format with masks. A simple evaluation harness can compare pose-trace stability under changed camera viewpoint, background, object layout, and robot prompt before giving weight to benchmark-only success rates.

### Sources
- [OASIS: Observation-Action Space Alignment via SE(3) Trajectory Prediction for Robotic Manipulation](../Inbox/2026-05-25--oasis-observation-action-space-alignment-via-se-3-trajectory-prediction-for-robotic-manipulation.md): OASIS uses an SE(3) trajectory predictor before action decoding and reports gains on LIBERO, real robots, and out-of-distribution perturbations.
- [Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments](../Inbox/2026-05-28--qwen-vla-unifying-vision-language-action-modeling-across-tasks-environments-and-robot-embodiments.md): Qwen-VLA uses embodiment-aware prompts and a shared action-and-trajectory tensor format across manipulation, navigation, and robot embodiments.

## Contact-force reporting for gentle and dexterous manipulation tasks
Robot manipulation tests should record contact quality alongside task completion when objects can be squeezed, struck, jammed, or damaged. The concrete build is an evaluation harness that logs average and peak grip force, average and peak applied force, tactile contact location, and task success for the same rollout.

Tabero gives a VLA-style version of this harness. It generates synchronized vision, touch, force, proprioception, action, and language data in Isaac Lab, encodes tactile marker motion or tactile images as tokens, and sends pose and force targets to a hybrid controller. Its benchmark reports four force metrics and claims more than 70% lower average grip force under gentle instructions while maintaining high task success.

CoP gives the dexterous-hand version. It compresses tactile taxel readings into a 3D contact force and 3D contact position for each tactile sensing region, then trains policies in simulation with sensor delay and domain randomization. On real peg-in-hole insertion across six shapes, CoP reached 0.78 success, ahead of binary contact at 0.53 and raw taxels at 0.48. Teams working with tactile grippers or dexterous hands can start with one blind insertion or fragile-object pick task and publish success together with force and contact-location traces.

### Sources
- [Tabero: Learning Gentle Manipulation with Closed-Loop Force Feedback from Vision, Touch, and Language](../Inbox/2026-05-27--tabero-learning-gentle-manipulation-with-closed-loop-force-feedback-from-vision-touch-and-language.md): Tabero adds tactile tokens and closed-loop force control, evaluates grip and applied force, and reports over 70% lower average grip force under gentle instructions.
- [Beyond Binary: Sim-to-Real Dexterous Manipulation with Physics-Grounded Contact Representation](../Inbox/2026-05-27--beyond-binary-sim-to-real-dexterous-manipulation-with-physics-grounded-contact-representation.md): CoP maps dense tactile readings to contact force and contact location and reports stronger real peg-in-hole success than binary contact and raw-taxel baselines.
