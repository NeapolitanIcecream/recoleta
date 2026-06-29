---
source: arxiv
url: https://arxiv.org/abs/2605.17556v1
published_at: '2026-05-17T17:37:34'
authors:
- Peter Schaldenbrand
- Jean Oh
topics:
- robotic-sculpting
- deformable-manipulation
- visual-planning
- dynamics-modeling
- long-horizon-planning
- sim2real
relevance_score: 0.56
run_id: materialize-outputs
language_code: en
---

# Visual Sculpting: Visually-Aligned Planning Representations for Long-Horizon Robot Clay Sculpting

## Summary
Visual Sculpting is a robot clay-sculpting method that plans over dense depth maps and spatial depth gradients, so the robot can target both 3D shape and visible surface detail. It learns a depth-change dynamics model from robot-generated pushes and uses MPC to execute long action sequences.

## Problem
- Prior deformable object methods often retrain a policy for each goal or plan over sparse point clouds of about 300 points, which miss surface texture and shading cues that affect how a sculpture looks.
- Clay relief sculpting needs many controlled actions, material movement across a large surface, and fine local detail; gripper pinches used in earlier dough work can make long-horizon sculpting messy.
- The problem matters because a robot that matches only coarse 3D shape can still miss the visual features that people use to judge the sculpture.

## Approach
- The state is a dense 512×512 depth map. The visual planning signal is the spatial gradient of that depth map, which captures local surface changes tied to lighting and texture.
- Each robot action is a linear push with parameters x, y, direction θ, travel length l, and depth z. The main system uses a single end-effector and compares it with a gripper pinch baseline.
- A neural dynamics model, param2deform, predicts the depth change caused by an action from the current depth map, its gradient, and the push shape parameters l and z.
- The model predicts deformations in a fixed pose, then differentiable perspective warps translate and rotate the prediction to the requested x, y, and θ. This reduces the amount of robot data needed.
- Planning uses MPC: greedy action initialization, gradient descent or CEM optimization, execution of a small action batch, rescanning, and replanning against 3D and visual losses.

## Results
- On held-out deformation prediction, adding the visual loss improved foam metrics: L3D went from 0.138 to 0.130, Lviz from 0.025 to 0.024, Chamfer Distance from 0.26 to 0.22, and EMD from 0.16 to 0.15. Lower is better for all listed metrics.
- On dough, adding the visual loss improved L3D from 0.190 to 0.187, Lviz from 0.029 to 0.028, Chamfer Distance from 0.45 to 0.41, and EMD from 0.31 to 0.30.
- On sand, the visual loss helped only Lviz, from 0.012 to 0.011; L3D worsened from 0.043 to 0.047, and Chamfer Distance and EMD stayed at 0.40 and 0.22.
- Single-end-effector pushes were easier to model than gripper pinches on foam: push results with L3D+Lviz were L3D 0.130, Lviz 0.024, CD 0.22, EMD 0.15, compared with pinch results of L3D 0.624, Lviz 0.043, CD 0.50, EMD 0.30.
- The dynamics model learned useful transitions with roughly 100 robot actions, with better performance as more samples were added.
- The system produced long-horizon sculptures with more than 100 actions, including an alphabet sequence from A through F without resetting the clay and a 50-action X sculpture where both 3D and visual losses decreased during execution. The excerpt does not give final numeric loss values for those planning runs.

## Link
- [https://arxiv.org/abs/2605.17556v1](https://arxiv.org/abs/2605.17556v1)
