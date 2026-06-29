---
source: arxiv
url: https://arxiv.org/abs/2606.05960v1
published_at: '2026-06-04T09:58:55'
authors:
- Anlan Yu
- Zaishu Chen
- Zhiqing Hong
- Daqing Zhang
topics:
- world-models
- robot-data-scaling
- imitation-learning
- industrial-logistics
- synthetic-recovery-data
- embodied-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Towards a Data Flywheel for Embodied Intelligence in Logistics

## Summary
The paper proposes a logistics data flywheel that turns daily warehouse operations, robot logs, demonstrations, and failure cases into training data for embodied policies. Its concrete result is WM-DAgger, which uses an action-conditioned World Model to generate recovery trajectories for imitation learning.

## Problem
- Logistics robots face long-tail parcel manipulation cases under throughput and reliability constraints, and lab demonstrations do not cover enough failures or recovery behaviors.
- Human-in-the-loop DAgger-style recovery labeling is costly at industrial scale.
- Existing operational data is heterogeneous, so it must be aligned into observation-action-outcome sequences before it can train World Models or policies.

## Approach
- Train an action-conditioned World Model from limited expert demonstrations plus about 5 minutes of play data.
- Generate candidate video-action recovery trajectories by predicting future eye-in-hand observations for robot actions.
- Use Corrective Action Synthesis to perturb expert trajectories toward nearby out-of-distribution states and guide actions back toward expert behavior.
- Use Consistency-Guided Filtering to reject generated rollouts whose terminal frames disagree with matched real demonstration frames.
- Aggregate filtered synthetic recovery data with real demonstrations to train imitation policies; future work adds unlabeled operational videos, automation logs, and deployment feedback.

## Results
- Soft Bag Pushing (5-shot): 5 real demonstrations plus 1,500 generated trajectories reached 93.3% success, versus 26.7% for standard BC and 40.0% for DMD.
- Soft Bag Pushing (20-shot): 96.7% with WM-DAgger, versus 30.0% BC and 56.7% DMD, using 20 real demonstrations and 1,500 generated trajectories.
- Pick-and-Place (Seen): 84.4% with WM-DAgger, versus 11.1% BC and 32.2% DMD.
- Pick-and-Place (Unseen): 70.0% with WM-DAgger, versus 5.0% BC and 11.8% DMD.
- Ballot Insertion and Towel Folding reached 73.3% and 46.7% success with WM-DAgger, compared with 13.3% and 0.0% for BC.
- The broader logistics flywheel beyond WM-DAgger is proposed work; the excerpt reports no production-scale deployment metric.

## Link
- [https://arxiv.org/abs/2606.05960v1](https://arxiv.org/abs/2606.05960v1)
