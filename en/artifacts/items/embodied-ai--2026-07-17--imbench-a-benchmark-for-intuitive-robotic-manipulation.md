---
source: arxiv
url: https://arxiv.org/abs/2607.15641v1
published_at: '2026-07-17T05:34:29'
authors:
- Anurag Maurya
- Sukhvansh Jain
- Prajwal Avhad
- Gautham Balachandran
- Ziyi Zhou
- Atharva Kshirsagar
- Satyam Singh
- Bowen Li. Rishabh Mukund
- Ritul Singh
- Jatin Vira
- Suvonil Chatterjee
- Devesh K. Jha
topics:
- robot-manipulation
- robot-foundation-model
- vision-language-action
- physical-reasoning
- robot-benchmark
- sim2real
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# IMBench: A Benchmark for Intuitive Robotic Manipulation

## Summary
IMBench evaluates whether robotic systems can combine physical reasoning with executable manipulation. Its 35-task suite exposes a large gap between recognizing constraints, proposing valid action sequences, and completing tasks under closed-loop control.

## Problem
- Existing benchmarks usually measure physical reasoning or manipulation execution separately, so they do not test whether a model can turn an inferred constraint into feasible action.
- This gap matters for generalist robot policies because tasks involving contact, tool use, hidden state, timing, and stability can fail even when the robot understands the goal.

## Approach
- IMBench provides 35 robosuite tasks across geometry, dynamics, causal action, tool use, hidden state, reactive replanning, and stability, supported by approximately 14,000 filtered trajectories.
- It formalizes performance as an Understand–Infer–Act loop: identify task constraints, propose an ordered sequence of sub-goals, and execute through closed-loop interaction.
- The benchmark evaluates five vision-language models on constraint understanding and plan correctness, then tests GPT-5.5 and end-to-end policies including Diffusion Policy, π0.5, and GR00T N 1.5.
- Episodes use multi-view RGB, proprioception, gripper state, and wrist force/torque observations with continuous 6-DoF end-effector and gripper actions; policies are also tested under out-of-distribution physical changes.

## Results
- The strongest VLMs achieved about 74% mean constraint-understanding success: Claude Sonnet 4.6 reached 74.5% and GPT-5.5 reached 74.1%; GPT-5.5 achieved 69.5% mean high-level plan correctness.
- Closed-loop GPT-5.5 execution succeeded on only 11.3% of evaluated tasks with vision-only inputs and 18.8% with privileged object-centric information; precise alignment, timing, tool use, hidden-state reasoning, and balancing tasks remained at 0% in both settings.
- Zero-shot vision-language-action policies had mean success of at most 0.02, while task-specific training raised π0.5 to 0.15, GR00T N 1.5 to 0.02, and Diffusion Policy to 0.24.
- Out-of-distribution performance often fell sharply: π0.5 on balance-medium dropped from 0.71 in-distribution to 0.12, and on keyboard-typing from 0.13 to 0.00; contact-tolerant domino-single remained comparatively robust.
- The benchmark is limited to simulation, Franka robots, parallel-jaw and suction grippers, and low-to-mid-horizon tasks, so the reported results do not establish performance on physical robots or dexterous hands.

## Link
- [https://arxiv.org/abs/2607.15641v1](https://arxiv.org/abs/2607.15641v1)
