---
source: arxiv
url: https://arxiv.org/abs/2607.00666v1
published_at: '2026-07-01T09:13:40'
authors:
- Taewook Kang
- Taeheon Kim
- Donghyun Shin
- Jonghyun Choi
topics:
- vision-language-action
- one-shot-adaptation
- robot-foundation-models
- weight-arithmetic
- domain-adaptation
- embodiment-transfer
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Domain Arithmetic: One-Shot VLA Adaptation under Environmental Shifts

## Summary
DART adapts a Vision-Language-Action policy to a changed environment using one target-domain demonstration for one task. It extracts a domain-shift vector from fine-tuned weights and adds it to the base policy so other learned tasks can run in the target domain.

## Problem
- VLA policies can fail when camera pose, lighting, sensor calibration, or robot embodiment changes, even when the task itself stays the same.
- Existing adaptation often needs demonstrations for each task in the target domain, which is expensive for real robot deployment.
- One-shot fine-tuning on a single target task tends to improve that task while failing on held-out tasks, so it does not preserve the base policy’s multi-task behavior.

## Approach
- Fine-tune the base VLA model on one source-domain demonstration and one target-domain demonstration of the same task, producing two weight update vectors.
- Subtract the source update from the target update to cancel the shared task direction and isolate a domain vector for the environmental shift.
- Run SVD on layer updates and keep source singular directions that align with the target update subspace before subtraction, reducing source-domain artifacts.
- Scale each layer’s domain vector by its source-target subspace alignment score, then add the scaled vector to the base model with a coefficient α.
- The method changes weights only, so it does not require a new policy architecture.

## Results
- The excerpt gives no task-success percentages, standard errors, or baseline margins, so the main performance claim cannot be checked numerically from the provided text.
- It claims one-shot adaptation with 1 target-domain demonstration for 1 task, plus a matching source-domain demonstration, then evaluation across all tasks in the source task set.
- On LIBERO with π0.5 under a Medium camera-viewpoint shift, one-shot fine-tuning keeps higher performance on the adaptation task than on held-out tasks; no success rates are provided.
- The weight analysis uses 16 update vectors from 4 tasks × 4 domains; the composed task-plus-domain estimate has the highest subspace alignment with target updates, but the excerpt gives no alignment values.
- The paper reports experiments with π0.5 and π0-FAST in simulation and on real robots across visual and embodiment shifts, and claims DART beats existing one-shot VLA adaptation baselines without numeric margins in the excerpt.

## Link
- [https://arxiv.org/abs/2607.00666v1](https://arxiv.org/abs/2607.00666v1)
