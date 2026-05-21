---
source: arxiv
url: https://arxiv.org/abs/2605.05714v1
published_at: '2026-05-07T05:57:49'
authors:
- Hanyu Zhou
- Chuanhao Ma
- Gim Hee Lee
topics:
- vision-language-action
- robot-manipulation
- relational-reasoning
- generalist-robot-policy
- robot-data-scaling
- sim2real
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# TriRelVLA: Triadic Relational Structure for Generalizable Embodied Manipulation

## Summary
TriRelVLA is a vision-language-action model that routes action prediction through explicit object-hand-task relations. It targets better robot manipulation transfer across unseen scenes, objects, and task compositions.

## Problem
- Existing VLA policies can bind actions to object appearance, background texture, and scene layout, which hurts transfer to new visual conditions.
- Structured VLA methods often encode objects or scene semantics, while the paper argues that manipulation needs relations among the target object, robot hand, and task constraints.

## Approach
- It builds object tokens from multi-view visual features, a hand token from visual features anchored by proprioception, and 4 task tokens for action, role, constraint, and stage.
- It fuses SigLIP semantic features with VGGT 3D geometric features to form a 3D visual latent for wrist and third-person views.
- It constructs a task-grounded graph with object, hand, and task nodes and 4 relation types: task-object, task-hand, object-hand, and object-object.
- A relation-aware graph transformer injects edge features into attention, then a bottleneck compresses relation-enhanced nodes into tokens passed to a Qwen3-4B LLM action head.
- Training uses 3 stages across OXE, DROID, LIBERO, and the new CSOT-Bench dataset, with action loss plus object and hand attention-mask losses.

## Results
- The provided excerpt does not include quantitative success rates, benchmark tables, or ablation numbers.
- It claims state-of-the-art performance across generalizable robotic tasks, but the excerpt gives no metric, dataset split, or baseline margin for that claim.
- It claims gains in 3 generalization settings: cross-scene, cross-object, and cross-task manipulation.
- CSOT-Bench is presented as a real-world dataset with 3 evaluation suites: scene reasoning, object understanding, and task goal.
- The model uses 4 task cue tokens and 4 edge relation types, which are the main concrete mechanism counts available in the excerpt.

## Link
- [https://arxiv.org/abs/2605.05714v1](https://arxiv.org/abs/2605.05714v1)
