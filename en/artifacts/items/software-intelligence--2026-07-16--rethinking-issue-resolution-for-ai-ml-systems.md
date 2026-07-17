---
source: arxiv
url: https://arxiv.org/abs/2607.14657v1
published_at: '2026-07-16T07:22:57'
authors:
- Ahmed Adnan
- Mushfiqur Rahman
- Antu Saha
- Oscar Chaparro
topics:
- ai-ml-maintenance
- issue-resolution
- software-engineering-for-ml
- reproducibility
- artifact-provenance
- human-ai-collaboration
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Rethinking Issue Resolution for AI/ML Systems

## Summary
The paper argues that AI/ML issue resolution needs workflows that model experimentation, nondeterminism, and artifacts beyond source code. A qualitative study of 100 issues across TensorFlow, scikit-learn, MLflow, and AutoGPT provides preliminary evidence for an iterative, artifact-aware framework.

## Problem
- Traditional issue-resolution frameworks assume mostly deterministic behavior, code-centric debugging, and pass/fail verification, which do not fully fit AI/ML systems.
- Resolving AI/ML issues can require changes to datasets, prompts, models, hyperparameters, dependencies, and infrastructure, making reproducibility and traceability difficult.

## Approach
- The authors qualitatively analyzed 100 randomly sampled closed issues and associated pull requests from 2020–2025, with 25 issues each from TensorFlow, scikit-learn, MLflow, and AutoGPT.
- Two authors independently open-coded 988 snippets, reconciled disagreements through consensus, and expanded an existing issue-resolution codebook with AI/ML-specific activities, challenges, and mitigation strategies.
- The analysis compared traditional resolution stages with AI/ML activities such as model performance monitoring, parameter tuning and training, data modification, and model functionality analysis.
- Based on the findings, the paper proposes future frameworks supporting iterative cross-stage workflows, reproducibility-aware verification, artifact provenance, heterogeneous-artifact coordination, and human-AI collaboration.

## Results
- The study identified 947 traditional issue-resolution activities and 41 AI/ML-specific activities across the 100 issues; 64 issues were classified as AI/ML, 18 as hybrid, and 18 as non-AI/ML.
- AI/ML-specific activities occurred at these rates: model performance monitoring in 27% of issues, parameter tuning and training in 11%, data modification in 7%, and model functionality analysis in 5%.
- Among the 64 AI/ML issues, 28 (45%) required changes outside production code, including prompts, datasets, hyperparameters, dependencies, CI, Docker, or runtime configuration. The corresponding figures were 83% code-only resolution for non-AI/ML issues and 77% for hybrid issues.
- Traditional stages were also common: issue analysis appeared in 65% of issues, solution design in 62%, implementation in 54%, verification in 53%, reproduction in 42%, and code review in 34%.
- Reported challenges included scaling fixes to larger datasets or distributed training in 9 issues, understanding model architectures in 6, nondeterministic solution verification in 4, and issue reproduction in 4. Developers used repeated executions, statistical tests, containerized environments, documentation, and distributed validation as mitigations.
- The evidence is preliminary: it covers four open-source projects and uses qualitative consensus coding without inter-coder agreement metrics, so the patterns may not generalize to other AI/ML systems.

## Link
- [https://arxiv.org/abs/2607.14657v1](https://arxiv.org/abs/2607.14657v1)
