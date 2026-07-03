---
source: arxiv
url: https://arxiv.org/abs/2607.01366v1
published_at: '2026-07-01T18:28:09'
authors:
- Holger R. Roth
- Ziyue Xu
- Chester Chen
- Daguang Xu
- Peter Cnudde
- Andrew Feng
topics:
- federated-learning
- coding-agents
- automated-research
- fl-optimization
- nvflare
- benchmark-evaluation
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Auto-FL-Research: Agentic Search for Federated Learning Algorithms

## Summary
Auto-FL-Research is a constrained coding-agent workflow that searches for federated learning training recipes while keeping data, budget, communication, and scoring fixed. It treats agent edits as logged candidates, then reruns selected winners across seeds to separate repeated gains from search artifacts.

## Problem
- Federated learning performance depends on many linked choices: local optimizers, server aggregation, schedules, regularization, client updates, and model architecture.
- Manual search is expensive, and unconstrained coding agents can change the metric, data split, evaluation route, or compute budget, which makes benchmark wins invalid.
- The problem matters for cross-silo healthcare FL because sites cannot pool raw data, and small training-protocol changes can change final model quality.

## Approach
- AFR uses NVFlare task profiles to lock the dataset, metric, client setup, rounds, model budget, allowed edit files, and final global-model evaluation path.
- The agent proposes and implements candidates inside that edit surface, including aggregation rules, client schedules, local losses, optimizers, regularization, and registered model variants.
- Static checks and smoke tests verify the FL contract: strict model loading, DIFF-typed client updates, local-step metadata, and the same final global server model for scoring.
- Each campaign logs 100 candidates with score, runtime, status, edited files, artifacts, crashes, and literature events.
- Selected candidates are rerun with five seeds and compared with matched baselines and same-budget scalar HPO controls.

## Results
- On FLamby, AFR showed repeated gains on 4 of 5 healthcare tasks: Heart Disease accuracy 0.721±0.001 to 0.794±0.005 (+0.074), IXI Dice 0.7914±0.0005 to 0.9895±0.0000 (+0.1981), ISIC2019 balanced accuracy 0.494±0.032 to 0.640±0.023 (+0.146), and Camelyon16 ROC AUC 0.5861±0.0310 to 0.7494±0.0182 (+0.1634).
- TCGA-BRCA did not show a meaningful repeated gain: C-index 0.807±0.009 to 0.808±0.025 (+0.001), so the paper treats that campaign win as seed-sensitive.
- IXI exceeded the selected FedCompass calibration target by +0.0015 Dice, and Camelyon16 exceeded the selected FENS calibration target by +0.0344 ROC AUC; ISIC2019 stayed 0.110 below its selected external target.
- On grouped-client LEAF profiles, the excerpt reports repeated gains on 5 of 6 tasks. Visible table values include FEMNIST accuracy 0.834±0.002 to 0.873±0.004 (+0.038), Shakespeare next-character accuracy 0.462±0.004 to 0.575±0.001 (+0.113), and Synthetic accuracy 0.955±0.001 to 0.989±0.001 (+0.033).
- CelebA is a reported failure case: the campaign winner did not beat the repeated baseline mean, and a follow-up top-k check found only a small alternate gain with uncertainty crossing zero.
- Campaign cost was explicit: every main search used a 100-candidate cap; reported wall time ranged from 1.5 hours for FLamby TCGA to 71.3 hours for FLamby IXI, with 0 to 3 crashes per task.

## Link
- [https://arxiv.org/abs/2607.01366v1](https://arxiv.org/abs/2607.01366v1)
