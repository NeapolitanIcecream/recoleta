---
source: arxiv
url: http://arxiv.org/abs/2604.09294v1
published_at: '2026-04-10T13:04:28'
authors:
- Davide Liconti
- Yuning Zhou
- Yasunori Toshimitsu
- Ronan Hinchet
- Robert K. Katzschmann
topics:
- dexterous-manipulation
- robot-hand-benchmark
- anthropomorphic-hands
- in-hand-manipulation
- grasp-evaluation
- mujoco
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# A Benchmark of Dexterity for Anthropomorphic Robotic Hands

## Summary
POMDAR is a new benchmark for measuring dexterity in anthropomorphic robot hands by how well and how fast they complete a set of grasping and in-hand manipulation tasks. It replaces ad hoc hand evaluation with a taxonomy-based benchmark that runs in both the real world and MuJoCo.

## Problem
- Dexterity for anthropomorphic robot hands has no shared, performance-based definition, so papers often compare hands with different tasks and different metrics.
- Common proxy measures such as degrees of freedom, joint limits, or manipulability capture potential capability, not actual contact-rich manipulation performance.
- Without a standard benchmark, it is hard to compare hand designs, track design progress, or match a hand to a target use case.

## Approach
- The paper introduces **POMDAR**, a benchmark built from established human hand taxonomies: 14 manipulation patterns from Elliott and Connolly plus Ma and Dollar, and 33 grasp types from the GRASP taxonomy.
- These taxonomies are turned into a compact task set with **12 manipulation tasks** and **6 pure grasping tasks**, organized into four configurations: vertical scaffolded tasks, horizontal scaffolded tasks, continuous rotation tasks, and free-space grasping tasks.
- Mechanical scaffolds constrain motion so the benchmark measures the intended hand behavior and reduces compensatory strategies such as palm support, gravity assistance, or excess arm motion.
- Scoring combines task completion quality and speed: **Score = 0.8 × correctness + 0.2 × speed**, where speed is normalized by a human baseline time from a user study. Correctness is continuous for manipulation tasks and discrete for grasping tasks.
- The benchmark is open source, fully 3D printable, and implemented in **MuJoCo** with teleoperation support, so users can test physical hands and simulated hands under the same task logic.

## Results
- The benchmark includes **18 total tasks**: **12 manipulation** and **6 grasping**.
- A human baseline was collected from **6 participants**, each performing **3 trials per task**, for **18 trajectories per task**. Motion capture used **22 hand keypoints at 100 Hz**.
- Robot evaluation used **4 ORCA hand embodiments**: a **2-finger, 5-DoF** version, a **3-finger** version, a **5-finger without abduction** version, and a **full 5-finger, 16-DoF** version, all mounted on a **7-DoF Franka Emika arm**.
- Each robot task was repeated **20 times** per embodiment. The excerpt states these experiments show benchmark comparisons across embodiments, but it does **not provide the actual per-task or aggregate numeric scores** in the available text.
- The user study reports low strategy variability across participants, and PCA plots show task-wise clustering of hand trajectories. The paper uses this as evidence that the scaffolded tasks are intuitive and constrain users toward the intended manipulation patterns.
- The main concrete claim is that POMDAR enables objective, reproducible, throughput-based comparison of anthropomorphic robot hands in both simulation and real hardware; the excerpt does not include stronger quantitative benchmark gains against prior benchmarks.

## Link
- [http://arxiv.org/abs/2604.09294v1](http://arxiv.org/abs/2604.09294v1)
