---
source: arxiv
url: http://arxiv.org/abs/2604.11302v1
published_at: '2026-04-13T11:01:30'
authors:
- Bronislav Sidik
- Dror Mizrahi
topics:
- world-model-planning
- monte-carlo-tree-search
- robot-scene-memory
- vision-language-action
- embodied-ai
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# 3D-Anchored Lookahead Planning for Persistent Robotic Scene Memory via World-Model-Based MCTS

## Summary
This paper proposes 3D-ALP, a test-time planning method for robot manipulation that keeps a persistent 3D camera pose memory and uses world-model rollouts with MCTS. The main claim is that this persistent 3D anchor fixes the failure of reactive vision-language-action policies on tasks where target objects leave the camera view.

## Problem
- Reactive VLA-style robot policies map the current image to an action, so they lose track of objects once those objects are occluded or out of frame.
- That failure matters in multi-step manipulation, where the robot may need to revisit a location seen earlier or act on objects in a sequence after they are no longer visible.
- The paper argues this is an architectural memory problem, not just a model-capacity problem: without an explicit scene memory state, the policy must guess.

## Approach
- 3D-ALP stores a persistent camera-to-world pose `c2w ∈ SE(3)` and updates it after each real action with forward kinematics, so visited locations remain addressable even after occlusion.
- It uses a 3D-consistent world model, InSpatio-WorldFM, to render predicted views from candidate future `c2w` poses, then runs Monte Carlo Tree Search over these imagined states.
- After each executed action, the MCTS tree is re-rooted instead of discarded, which preserves previously explored spatial states as memory.
- A hybrid scorer combines a semantic image score with a geometric distance penalty so the planner does not trust 2D visual overlap when the gripper is still far away in 3D.
- The method also adds four practical MCTS fixes for robot control: remove the zero-action trap, reset node depths after rerooting, backpropagate max value instead of mean, and set a much smaller UCB exploration constant (`c = 0.02`).

## Results
- On the E3 multi-step coherence task in MuJoCo with a Franka Panda, memory-task success rate is `0.650 ± 0.109` for 3D-ALP versus `0.006 ± 0.008` for the greedy reactive baseline, a `+0.645` gain.
- On the hardest chained-memory step (step 5), greedy gets `0.000` success, MCTS with depth `D=1` gets `0.622`, and 3D-ALP with `D=2` gets `0.822`, so deeper lookahead adds `+0.200` on that step.
- The paper states that on memory-required steps, the reactive baseline drops to about `0.6%` success while 3D-ALP keeps about `65%`; Figure 1 also reports step-5 performance of `82.2%` versus `0.0%` for greedy.
- The ablation says persistent tree memory is the main source of the gain: `D=1` MCTS reaches memory SR `0.539 ± 0.064`, already far above greedy `0.006 ± 0.008`.
- On non-memory steps, greedy is stronger than shallow MCTS in the reported table: greedy `0.748 ± 0.029` versus `0.389 ± 0.024` for `D=1` MCTS, which supports the paper's claim that the benefit is concentrated on occlusion-driven memory steps.
- Component checks report perfect geometric consistency in simulation: `SSIM = 1.000`, `ORB = 1.000` with `391/391` keypoints matched across 5 trajectories, plus kinematic bridge angular error `0.00°`, `100%` pass rate under a `≤5°` threshold, and bridge latency `0.5 ms`.

## Link
- [http://arxiv.org/abs/2604.11302v1](http://arxiv.org/abs/2604.11302v1)
