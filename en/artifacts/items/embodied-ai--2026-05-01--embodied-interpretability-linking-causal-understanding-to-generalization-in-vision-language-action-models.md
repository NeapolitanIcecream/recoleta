---
source: arxiv
url: https://arxiv.org/abs/2605.00321v1
published_at: '2026-05-01T01:00:00'
authors:
- Hanxin Zhang
- Mingshuo Xu
- Abdulqader Dhafer
- Shigang Yue
- Hongbiao Dong
- Zhou Daniel Hao
topics:
- vision-language-action
- embodied-interpretability
- robot-policy
- causal-attribution
- ood-generalization
- manipulation
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Embodied Interpretability: Linking Causal Understanding to Generalization in Vision-Language-Action Models

## Summary
This paper proposes ISS and NMR, two diagnostics for checking whether a Vision-Language-Action policy bases actions on task-relevant image regions or nuisance regions. It claims that high nuisance attribution predicts worse out-of-distribution manipulation performance.

## Problem
- VLA policies can fail under distribution shift when they rely on background, texture, shadows, or other spurious visual cues instead of the robot, objects, and supports needed for the task.
- Attention maps and hidden-state probes can show where information appears, but they do not prove that a region changes the policy's action.
- The problem matters because a robot policy that depends on nuisance cues may pass seen-task tests and then fail when the scene changes.

## Approach
- The paper treats visual-action attribution as an intervention problem: mask or blur image tokens, rerun the VLA policy, and measure how much the predicted action changes.
- Interventional Significance Score (ISS) assigns high saliency to visual regions whose removal causes a large action change. The implementation uses randomized binary masks, blurred replacements, and action MSE as a proxy for KL divergence under a fixed isotropic Gaussian policy.
- Nuisance Mass Ratio (NMR) measures how much of the top-k ISS saliency falls inside task-irrelevant regions such as backgrounds, wall colors, reflections, and distractor objects.
- The paper partitions visual tokens into action-critical regions, environmental support regions, and nuisance regions, then treats nuisance attribution as evidence that the policy learned a spurious dependency.

## Results
- On AGNOSTOS with RLBench evaluation, the VLA policy was fine-tuned on 3,600 seen-task episodes and evaluated with 575 unseen-task episodes.
- The unseen set was split into U1 with 13 partially overlapping tasks and U2 with 10 tasks using novel objects or actions.
- Across 41 tasks, 5 random seeds, and 25 trials per task, NMR@10 had a Pearson correlation of -0.77 with task success rate, meaning higher nuisance attribution tracked lower success.
- In a noise test on 200 selected episodes with Gaussian noise standard deviation 0.25 applied to nuisance regions, ISS reached action MSE 0.002 and saliency cosine similarity 0.995.
- In the same test, attention saliency reached action MSE 0.002 and cosine similarity 0.959, while token-norm saliency reached action MSE 0.011 and cosine similarity 0.999.
- The paper also claims that ISS has an unbiased estimator and that action prediction error is a valid proxy for causal influence under stated Gaussian-policy assumptions.

## Link
- [https://arxiv.org/abs/2605.00321v1](https://arxiv.org/abs/2605.00321v1)
