---
source: arxiv
url: https://arxiv.org/abs/2606.13497v1
published_at: '2026-06-11T15:46:28'
authors:
- Nils Blank
- Paul Mattes
- Maximilian Xiling Li
- Jakub Suliga
- Thomas Roth
- Moritz Reuss
- Pankhuri Vanjani
- Rudolf Lioutikov
topics:
- robot-learning
- spatial-annotation
- reliability-scoring
- embodied-vlm
- data-filtering
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale

## Summary
SPARC solves reliable auto-labeling of robot demonstrations with spatial annotations, so robot learning can use more data without letting noisy labels dominate. It matters because grounded policies and embodied models need object locations, trajectories, and phase labels, but detector confidence alone often picks the wrong object in cluttered scenes.

## Problem
- Robot demos need structured labels such as object boxes, trajectories, and manipulation phases, but human labeling is expensive.
- Existing auto-labeling pipelines use detector confidence as the main quality signal, and that signal does not track whether the detected object is the one the robot actually manipulates.
- In clutter, occlusion, and bimanual scenes, these pipelines face a quality-coverage tradeoff: keep noisy labels or throw away useful data.

## Approach
- SPARC splits a demo into object-centric interaction segments using gripper phase detection and language parsing.
- For each candidate object, it proposes regions with LLMDet, masks them with SAM2, tracks them with AllTracker, and lifts tracks to 3D with MoGe-2.
- It scores each candidate with interaction evidence: motion during the grasp phase, 3D proximity to the gripper, and a penalty for overlap with the robot body.
- The top-scoring candidate becomes the annotation, and a single reliability threshold controls how strict the filter is.
- The paper also introduces IA-Bench, a benchmark with hand-labeled interacted-object start and target boxes across 1,748 demonstrations from 12 embodiments.

## Results
- On IA-Bench, SPARC reaches 80.2% interacted-object localization accuracy, versus 58.1% for a detection-confidence baseline.
- It keeps 77.6% coverage at the 90% precision operating point, while the strongest trajectory-filtering baseline gets 33.1% coverage and detector confidence gets 0.2% coverage.
- Its selective-prediction scores are the best reported: AURC 0.056 and E-AURC 0.035.
- At a 95% precision target, SPARC retains 58% of samples, compared with 20% for the strongest trajectory filter.
- Training Qwen3.5-4B on about 511K SPARC-generated VQA pairs gives 79.1 on IA Bench, 71.0 on Where2Place, 65.7 on VA Bench-P, and 69.6 average across the pointing benchmarks, beating the human-annotated EO-1.5M mix on the reported spatial-grounding average (69.6 vs 62.6).
- In real-world cluttered manipulation scenes, policies trained on SPARC annotations outperform baselines trained on detector-annotated data, but the excerpt does not give the exact policy numbers.

## Link
- [https://arxiv.org/abs/2606.13497v1](https://arxiv.org/abs/2606.13497v1)
