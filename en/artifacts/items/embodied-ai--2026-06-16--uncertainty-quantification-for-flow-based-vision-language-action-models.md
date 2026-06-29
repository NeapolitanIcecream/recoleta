---
source: arxiv
url: https://arxiv.org/abs/2606.18043v1
published_at: '2026-06-16T15:19:09'
authors:
- "Ralf R\xF6mer"
- Maximilian Seeliger
- Saida Liu
- Ben Sturgis
- Marco Bagatella
- Daniel Marta
- Andreas Krause
- Angela P. Schoellig
topics:
- vision-language-action
- uncertainty-quantification
- flow-matching
- active-fine-tuning
- robot-data-scaling
- failure-detection
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Uncertainty Quantification for Flow-Based Vision-Language-Action Models

## Summary
The paper gives flow-based vision-language-action models a practical confidence signal. It uses ensemble disagreement in the flow velocity field to detect likely failures and to choose which robot demonstrations to collect for fine-tuning.

## Problem
- Flow-based VLAs can act with no reliable warning when a scene, object, or task is outside their training distribution, which matters for real robot deployment and safety.
- Existing VLA fine-tuning often needs many expert demonstrations, and those demonstrations are expensive to collect.
- The key missing signal is epistemic uncertainty: uncertainty that should drop when the model receives the right new data.

## Approach
- The method trains a small ensemble of flow-based VLA action heads and compares their predicted velocity fields during action generation.
- It derives velocity-field disagreement (VFD) as a tractable estimate tied to pairwise KL divergence between flow models, avoiding expensive likelihood computation through ODE divergence terms.
- In simple terms, the model starts generating an action chunk, checks whether ensemble members point in different action directions along the flow path, and treats larger disagreement as higher uncertainty.
- The SAVE active fine-tuning method ranks tasks by mean VFD, selects the most uncertain initial observations, asks an expert for demonstrations, and fine-tunes with new data plus replay data.

## Results
- On the LIBERO benchmark, VFD is reported to give better-calibrated uncertainty estimates that predict downstream task performance better than tested baselines; the excerpt does not provide exact calibration or correlation numbers.
- VFD is reported to perform well for deployment failure detection; the excerpt does not provide AUROC, precision, recall, or threshold numbers.
- SAVE is reported to need at least 22 fewer samples than baselines for multitask adaptation on LIBERO; the excerpt renders the unit as “22” and does not show whether this means 22 demonstrations or 22%.
- The method is evaluated on multitask pools with K tasks and L candidate initial observations per task, using R active-learning rounds and n_e expert queries per round, but the excerpt does not give the concrete K, L, R, or n_e values.

## Link
- [https://arxiv.org/abs/2606.18043v1](https://arxiv.org/abs/2606.18043v1)
