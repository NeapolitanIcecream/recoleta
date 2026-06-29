---
source: arxiv
url: https://arxiv.org/abs/2605.18727v1
published_at: '2026-05-18T17:51:34'
authors:
- Feng Chen
- Tianzhe Chu
- Li Sun
- Pei Zhou
- Zhuxiu Xu
- Shenghua Gao
- Yuexiang Zhai
- Yanchao Yang
- Yi Ma
topics:
- dexterous-manipulation
- robot-benchmark
- vision-language-action
- embodied-agent
- shadowhand
- real-world-robotics
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# DexHoldem: Playing Texas Hold'em with Dexterous Embodied System

## Summary
DexHoldem is a real-world benchmark for testing whether dexterous embodied agents can perceive a Texas Hold'em table, choose legal next actions, and execute card and chip manipulation with a ShadowHand.

## Problem
- Current embodied-agent benchmarks often use simulation, simple grippers, or coarse actions, so they give weak evidence for real multi-finger manipulation.
- Dexterous manipulation benchmarks often test isolated motor skills, while closed-loop tabletop tasks need perception, state tracking, action routing, and scene-preserving execution.
- Texas Hold'em creates a compact real-world testbed because thin cards, chips, changing table state, and legal action choices expose both perception and manipulation failures.

## Approach
- The benchmark provides 1,470 teleoperated demonstrations across 14 Texas Hold'em primitives, with 105 demonstrations per primitive and a fixed 100/5 train-validation split.
- Policies receive three camera views, robot proprioception, and a task condition, then output 30-dimensional joint-position targets for a UR arm and ShadowHand.
- Physical rollouts use a four-level rubric: scene-preserving success, disruptive completion, task failure, and disruptive failure.
- The perception benchmark asks agents to recover structured game state from real tabletop images, including loop stage, turn ownership, blind information, community cards, current bet chips, chip inventories, and showdown outcome.
- Full-system case studies connect perception, routing, primitive dispatch, retries, waiting, recovery, and human-help requests in closed-loop hands.

## Results
- On 80 real-world primitive trials per policy, π0.5 reached the best task completion rate at 61.2% and tied π0 on scene-preserving success rate at 47.5%.
- π0 reached 47.5% scene-preserving success and 57.5% task completion; RDT reached 30.0% and 46.2% on the same metrics.
- The strongest task-specific imitation baseline, DP (DINO), reached 26.2% scene-preserving success and 36.2% task completion, more than 20 percentage points below π0.5 on scene-preserving success.
- Weaker baselines scored much lower: DP-Transformer 13.8% SPSR and 20.0% TCR, ACT 10.0% and 15.0%, BAKU 6.2% and 12.5%, and DP-UNet 1.2% and 1.2%.
- On the 36-problem perception benchmark, Opus 4.7 had the best strict problem-level accuracy at 34.3%, while GPT 5.5 had the best average field-wise accuracy at 66.8%.
- Routing-critical chip fields were weak: current-bet accuracy peaked at 45.8%, and opponent-chip-inventory accuracy peaked at 43.8%.

## Link
- [https://arxiv.org/abs/2605.18727v1](https://arxiv.org/abs/2605.18727v1)
