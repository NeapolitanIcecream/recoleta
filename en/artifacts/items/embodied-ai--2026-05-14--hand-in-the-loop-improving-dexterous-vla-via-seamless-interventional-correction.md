---
source: arxiv
url: https://arxiv.org/abs/2605.15157v1
published_at: '2026-05-14T17:51:40'
authors:
- Zhuohang Li
- Liqun Huang
- Wei Xu
- Zhengming Zhu
- Nie Lin
- Xiao Ma
- Xinjun Sheng
- Ruoshi Wen
topics:
- vision-language-action
- dexterous-manipulation
- interactive-imitation-learning
- human-in-the-loop
- robot-data-scaling
- bimanual-robotics
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Hand-in-the-Loop: Improving Dexterous VLA via Seamless Interventional Correction

## Summary
HandITL is a human intervention method for dexterous VLA policies that lets an operator correct a robot hand and arm during rollout without causing a sudden hand-pose jump. The paper claims large reductions in takeover discontinuity and better policy fine-tuning from on-policy correction data than from standard teleoperation data.

## Problem
- Dexterous VLA policies can drift during long, contact-heavy tasks; small finger or object-pose errors can compound into drops, failed grasps, or unrecoverable states.
- Interactive imitation learning can collect recovery data during deployment, but direct teleoperation takeover on high-DoF hands creates gesture jumps when the human hand pose does not match the robot hand pose.
- This matters because bimanual anthropomorphic hands need fine finger corrections while keeping existing contacts stable.

## Approach
- HandITL blends human correction with the running VLA policy instead of replacing the policy command with absolute teleoperation at takeover.
- For the hand, it anchors at the intervention time and maps the operator’s relative fingertip motion to the robot hand, so no human motion after takeover means no sudden robot-hand motion.
- The hand retargeting optimization includes fingertip-shape tracking, pinch reinforcement, collision safety, and temporal regularization.
- For the arms, it converts Meta Quest 3 wrist-controller motion into residual velocity twists and adds them to the policy’s arm commands.
- The system records executed on-policy correction rollouts and uses them to fine-tune the base VLA policy.

## Results
- On Bread Clip takeover tests, direct teleoperation switching produced mean command change of about 4.38e-2; HandITL reduced it to about 6.8e-5, a 99.8% reduction and lower than DeltaCmd at about 6.23e-3.
- On Drill takeover tests, direct switching produced mean command change of about 2.75e-2; HandITL reduced it to about 2.65e-4.
- In post-takeover Pick Up and Place the Parts, HandITL completed the task in 42.8 ± 5.0 s versus Teleop at 52.9 ± 14.2 s, Jacobian at 68.0 ± 10.8 s, and DeltaCmd at 56.7 ± 14.5 s.
- In the same parts task, HandITL had 1 retry across 10 trials versus 8 retries for Teleop, reported as an 87.5% grasp-failure reduction.
- In Pick Up the Drill, HandITL had the fastest mean time at 14.4 ± 4.7 s versus Teleop at 15.5 ± 5.7 s, DeltaCmd at 17.3 ± 5.4 s, and Jacobian at 19.4 ± 5.6 s; drill-trigger success was 8/10 for HandITL and 10/10 for Teleop.
- For policy refinement, HandITL correction data outperformed equal-duration standard teleoperation data by 19% on average across three long-horizon dexterous tasks, according to the excerpt.

## Link
- [https://arxiv.org/abs/2605.15157v1](https://arxiv.org/abs/2605.15157v1)
