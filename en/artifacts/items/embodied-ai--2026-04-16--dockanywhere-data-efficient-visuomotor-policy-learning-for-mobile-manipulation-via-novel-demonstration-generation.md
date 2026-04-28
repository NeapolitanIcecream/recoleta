---
source: arxiv
url: http://arxiv.org/abs/2604.15023v1
published_at: '2026-04-16T13:53:01'
authors:
- Ziyu Shan
- Yuheng Zhou
- Gaoyuan Wu
- Ziheng Ji
- Zhenyu Wu
- Ziwei Wang
topics:
- mobile-manipulation
- imitation-learning
- data-augmentation
- point-clouds
- sim2real
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# DockAnywhere: Data-Efficient Visuomotor Policy Learning for Mobile Manipulation via Novel Demonstration Generation

## Summary
DockAnywhere is a data augmentation method for mobile manipulation that turns a small set of demonstrations at one docking pose into many consistent demonstrations at new docking poses. It targets failures caused by navigation errors that shift the robot's base and change the view seen by the manipulation policy.

## Problem
- Two-stage mobile manipulation systems often navigate to a docking pose and then run a fixed-base manipulation policy, but small docking errors change the robot's viewpoint and can break the policy.
- Collecting demonstrations for many docking poses is expensive, and prior augmentation methods for static manipulation do not handle base relocation well.
- This matters in homes and factories because real navigation is noisy, so manipulation policies need to keep working when the robot stops at unseen positions.

## Approach
- The method switches policy input from egocentric views to a fixed third-person RGB-D view, so docking shifts become a geometry problem over base pose instead of a large appearance change.
- It parses one demonstration into two parts: free-space motion segments and contact-rich skill segments. Motion segments are low-precision approach moves; skill segments are object interaction phases that should stay the same.
- For a new feasible docking point, it keeps the skill segments, replans only the motion segments with task-and-motion planning under visibility, reachability, and collision-free constraints, and reuses gripper commands.
- It then synthesizes new observations directly in 3D point-cloud space by editing robot and object points with the same spatial transforms used for the actions, keeping observation-action pairs aligned.
- The generated demonstrations train a behavior-cloned visuomotor policy, using DP3 as the policy head in the reported experiments.

## Results
- In ManiSkill with 5 docking points, DockAnywhere reaches **78.9%** overall success rate, compared with **74.2%** for **DP3+DemoGen**, **17.8%** for **DP3**, and **15.8%** for **DP**.
- Task-level ManiSkill results with 5 docking points: **Pick Banana 97.0%**, **Pick Mug 89.4%**, **Place Can 87.2%**, **Cabinet Door 60.2%**, **Cabinet Drawer 60.6%**. Against **DP3+DemoGen**, gains are **+0.8**, **+3.0**, **+12.0**, and **+8.6** points on the last four tasks except Pick Banana, where it is **-1.0** point.
- With only 1 docking point, plain DP3 gets **88.6%** overall success in ManiSkill, but with 5 docking points and no mobile-specific augmentation it drops to **17.8%**, which shows the docking-shift problem the paper targets.
- In the ablation on augmentation count, testing on an unseen docking point, overall success rises from **35.5%** with **1** dock to **48.5%** with **2**, **61.9%** with **4 (ours)**, and **63.9%** with **6**. This suggests most of the gain appears by 4 augmented docking points.
- The paper reports real-world deployment on a mobile manipulator with a single third-person camera and claims an average success rate of **43.3%** with a limited number of source demonstrations, plus about **0.1 s** augmentation cost per source trajectory.
- The excerpt does not provide a full real-world table, so detailed task-by-task real-world baseline comparisons are not available here.

## Link
- [http://arxiv.org/abs/2604.15023v1](http://arxiv.org/abs/2604.15023v1)
