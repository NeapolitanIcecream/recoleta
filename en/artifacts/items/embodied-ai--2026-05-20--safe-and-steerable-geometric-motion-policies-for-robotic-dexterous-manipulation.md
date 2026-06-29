---
source: arxiv
url: https://arxiv.org/abs/2605.21811v1
published_at: '2026-05-20T23:16:01'
authors:
- Albert Wu
- Riccardo Bonalli
- Thomas Lew
- C. Karen Liu
topics:
- dexterous-manipulation
- control-barrier-functions
- geometric-control
- motion-policy
- in-hand-reorientation
- robot-safety
relevance_score: 0.56
run_id: materialize-outputs
language_code: en
---

# Safe and Steerable Geometric Motion Policies for Robotic Dexterous Manipulation

## Summary
SafePBDS generates dexterous robot motions by combining task-space goals and hard safety constraints defined on different manifolds. It targets real-time grasping and in-hand reorientation for multi-finger hands, with high-level actions able to steer the motion while safety constraints stay active.

## Problem
- Dexterous manipulation mixes goals and constraints in joint space, end-effector pose space, contact geometry, distance margins, and force-closure conditions. A controller must reconcile these at control rate.
- Prior PBDS methods compose manifold tasks with geometric consistency, but safety enters as soft costs and can be violated under competing objectives.
- Learned dexterous policies often need large task-specific datasets and can fail outside their training distribution, so explicit online safety matters for hardware hands.

## Approach
- SafePBDS maps task-manifold objectives and safety conditions back to the robot configuration manifold through smooth task maps, then solves quadratic programs for one configuration-space acceleration command.
- Pullback control barrier functions convert safety functions on arbitrary task manifolds into linear constraints on configuration acceleration.
- The paper derives two higher-order CBF forms for this setting: exponential CBFs and backstepping CBFs.
- Autonomous PBDS behavior stays in a weighted least-squares objective, while safety constraints are enforced as hard constraints in the QP.
- A task-manifold action interface lets a high-level policy add low-dimensional residual commands; zero input recovers the autonomous behavior, and arbitrary inputs remain filtered by the same safety constraints.

## Results
- On hardware dexterous grasping with a 23-DOF Franka Panda plus Allegro Hand, SafePBDS reports 92.5% success across 20 household objects and 120 trials, equal to 111 successful trials.
- With the action interface, the system can exclude any one of four fingers during grasping using a 1-dimensional action.
- In the 3-finger grasp test, it reports 94.4% success across 3 objects and 36 trials, equal to 34 successful trials.
- For in-hand reorientation, the method reports more than 360° yaw rotation in both directions with a fully actuated palm-down Allegro Hand setup under varying object weight and wrist motion.
- The excerpt claims simulation tests on an S² double integrator and a 7-DOF arm validate chart invariance, metric effects, unsafe-state recovery, and the action interface, but it does not provide numeric simulation metrics in the shown text.

## Link
- [https://arxiv.org/abs/2605.21811v1](https://arxiv.org/abs/2605.21811v1)
