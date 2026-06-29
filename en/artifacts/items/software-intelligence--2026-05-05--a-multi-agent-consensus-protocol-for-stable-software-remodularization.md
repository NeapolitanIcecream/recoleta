---
source: arxiv
url: https://arxiv.org/abs/2605.04188v1
published_at: '2026-05-05T18:27:02'
authors:
- Ahmed F. Ibrahim
topics:
- software-remodularization
- multi-agent-negotiation
- code-intelligence
- architecture-recovery
- software-clustering
- stability-constraints
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# A Multi-Agent Consensus Protocol for Stable Software Remodularization

## Summary
AMCP treats software remodularization as negotiation between cohesion and stability agents. It improves a code partition only when the change stays within an architect-set stability budget.

## Problem
- Existing software clustering tools often optimize a single structural metric such as TurboMQ, so they can recommend layouts that change too much between releases.
- Large layout changes make developers relearn the system structure, which raises maintenance cost even when cohesion improves.
- Weighted-sum multi-objective methods need hand-set coefficients and do not enforce a hard stability floor.

## Approach
- The paper models a software system as a directed dependency graph and a decomposition as a partition of classes into clusters.
- A Cohesion Agent scores each partition with TurboMQ divided by the number of clusters. A Stability Agent scores it as 1 - MoJo(D, D_prev) / n_common.
- AMCP starts from the previous accepted decomposition and enumerates all single-class reassignments at each step.
- It keeps only moves that improve cohesion and satisfy U_sta >= τ_sta, then chooses the move with the smallest stability loss per cohesion gain.
- The paper claims formal proofs for finite termination, Zeuthen-style bounded concession under closed-instance conditions, and local Pareto-satisfactoriness within the single-move neighborhood.

## Results
- On Xwork 1.0 to 1.1, the experiment uses 113 common classes, 10 packages in version 1.0, and 156 classes in version 1.1.
- With τ_sta from 0.60 to 0.90 and τ_coh fixed at 0.5, AMCP reaches U_coh = 0.5980, U_sta = 0.9167, social welfare = 1.5146, and 6 negotiation steps.
- Bunch on the same Xwork graph reports U_coh = 0.5979 and U_sta = 0.9167, so AMCP matches the main cohesion result when the stability budget is loose.
- CC/G reports U_coh = 0.5885, U_sta = 0.9167, and social welfare = 1.5052, below AMCP's 1.5146 in the loose-budget runs.
- With a strict τ_sta = 0.95, AMCP stops after 3 steps with U_coh = 0.5919, U_sta = 0.9583, and social welfare = 1.5502, showing the claimed stability-budget enforcement.
- Runtime claims are 1.24 seconds per step for the 113-class Xwork system and 1.02 seconds per step for a 120-module Apache Ant subset. The ten-system extended evaluation and NSGA-II comparison are deferred to a later paper, so the excerpt gives no numbers for those claims.

## Link
- [https://arxiv.org/abs/2605.04188v1](https://arxiv.org/abs/2605.04188v1)
