---
source: arxiv
url: https://arxiv.org/abs/2606.31993v1
published_at: '2026-06-30T17:30:05'
authors:
- Arnav Balaji
- Arpit Bahety
- Sriniket Ambatipudi
- Daniel Lam
- Junhong Xu
- "Roberto Mart\xEDn-Mart\xEDn"
topics:
- robot-safety
- manipulation-benchmark
- damage-aware-simulation
- household-manipulation
- sim2real
- vision-language-action
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# OopsieVerse: A Safety Benchmark with Damage-Aware Simulation for Robot Manipulation

## Summary
OopsieVerse adds explicit damage tracking to household robot simulation so policies can be judged on both task completion and physical harm. It pairs DamageSim with OopsieBench, a 32-task benchmark across OmniGibson and RoboCasa.

## Problem
- Household manipulation benchmarks often score goal completion without measuring broken objects, robot damage, heat damage, or liquid damage.
- Real-world training and evaluation can be expensive and unsafe when failures damage the robot or the home.
- Existing safety costs usually need task-specific constraints, which makes cross-task comparison hard.

## Approach
- DamageSim augments a POMDP with per-object and per-link health, initialized on a 0 to 100 scale and reduced when damage evaluators fire.
- Mechanical damage uses simulator contact forces and link acceleration to estimate impulsive and sustained load, then subtracts health when load passes an object-specific threshold.
- Thermal damage subtracts health when object temperature exceeds hot or cold thresholds; the excerpt says this is implemented only in OmniGibson because it needs temperature state.
- Fluid damage subtracts health when liquid contact passes a threshold; the excerpt says this is implemented only in OmniGibson because it needs fluid particles.
- OopsieBench provides household tasks with unsafe shortcuts and safer alternatives, so users can measure success and damage separately.

## Results
- OopsieBench contains 32 task instances, 21 unique task designs, 17 OmniGibson tasks, and 15 RoboCasa tasks.
- DamageSim is implemented in 2 physics stacks: OmniGibson on Nvidia Omniverse and RoboCasa/Robosuite on MuJoCo.
- The damage model covers 3 main damage classes: mechanical, thermal, and fluid; mechanical damage includes impact, compression, and tension examples.
- The excerpt claims live damage feedback makes human teleoperation demonstrations safer, but it gives no exact metric or percentage.
- The excerpt claims damage-conditioned imitation learning, damage-aware reinforcement learning, VLA policy benchmarking, and sim-to-real safety gains, but it provides no quantitative policy results in the supplied text.

## Link
- [https://arxiv.org/abs/2606.31993v1](https://arxiv.org/abs/2606.31993v1)
