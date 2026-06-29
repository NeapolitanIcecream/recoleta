---
source: arxiv
url: https://arxiv.org/abs/2605.19365v1
published_at: '2026-05-19T04:55:49'
authors:
- Ravishka Rathnasuriya
- Wei Yang
topics:
- code-intelligence
- input-adaptation
- uncertainty-estimation
- vulnerability-detection
- code-language-models
- inference-time-reliability
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# On-the-Fly Input Adaptation for Reliable Code Intelligence

## Summary
The paper proposes inference-time input adaptation for code language models to reduce wrong predictions without retraining, architecture changes, or extra labels. Preliminary results show accuracy gains on vulnerability detection, while current uncertainty metrics are weak error detectors for code tasks.

## Problem
- Code language models can change their predictions after syntax-preserving edits such as variable renaming, control-flow restructuring, or statement reordering, even when program behavior stays the same.
- Retraining, architecture changes, and prompt tuning add cost, require deployment work, and can fail to transfer across tasks or model families.
- Reliable code intelligence matters because wrong outputs in vulnerability detection, repair, synthesis, and review can create security and production risk.

## Approach
- The method first assigns a validity score to a model output. For classifiers, it uses signals such as sub-model variance and distance to class prototypes. For generators, it uses decoding signals and consistency across prompt variants.
- If the validity score falls below a task threshold, the method rewrites or adjusts the input and runs inference again.
- Input-space adaptation uses meaning-preserving edits, including variable renaming, control-flow restructuring, code simplification, prompt rephrasing, synonym replacement, and constraint reordering.
- Latent-space adaptation nudges the input embedding toward regions linked with higher predicted reliability, with bounds meant to preserve meaning.
- Candidate adaptations are searched and ranked using the validity score; proposed search methods include evolutionary search and constrained decoding.

## Results
- Existing uncertainty metrics were weak at detecting generation errors: ROC-AUC ranged from 0.466 to 0.666 across HumanEval+ and MBPP+ using DeepSeek-Coder-7B and CodeLlama-7B.
- On vulnerability detection classifiers, uncertainty metrics also stayed near chance: ROC-AUC ranged from 0.559 to 0.621 across DeepSeek-Coder-7B and CodeLlama-7B.
- On vulnerability detection with CodeBERT, base accuracy was 63.36%; input transformation reached 71.52% (+8.16 percentage points), and latent transformation reached 76.75% (+13.39 points).
- On vulnerability detection with GraphCodeBERT, base accuracy was 62.99%; input transformation reached 65.26% (+2.27 points), and latent transformation reached 68.32% (+5.33 points).
- Reported overhead was 49.92-59.4 seconds per input for input transformations and 2-3 seconds per input for latent transformations.
- The excerpt reports no full quantitative results for generation adaptation, diffusion guidance, autoregressive revision, or the complete end-to-end method.

## Link
- [https://arxiv.org/abs/2605.19365v1](https://arxiv.org/abs/2605.19365v1)
