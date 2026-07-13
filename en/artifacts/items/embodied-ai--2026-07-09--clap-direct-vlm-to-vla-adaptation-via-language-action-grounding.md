---
source: arxiv
url: https://arxiv.org/abs/2607.08974v1
published_at: '2026-07-09T22:34:11'
authors:
- Yuri Ishitoya
- Jeremy Siburian
- Masashi Hamaya
- Kuniaki Saito
- Cristian C. Beltran-Hernandez
- Mai Nishimura
topics:
- vision-language-action
- robot-foundation-model
- language-action-grounding
- robot-data-scaling
- sim-to-real
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# CLAP: Direct VLM-to-VLA Adaptation via Language-Action Grounding

## Summary
CLAP adapts pretrained vision-language models into executable robot policies by placing a natural-language action description before precise numeric action tokens. With one epoch of fine-tuning and no architectural additions, the 2B model reaches 90.8% average success on LIBERO, 14.9 points above a matched VLA-0 baseline.

## Problem
- VLA fine-tuning usually makes a language model emit bare numeric action tokens, creating an output-distribution mismatch with the natural-language data used during pretraining.
- This mismatch can reduce semantic generalization and makes it difficult to measure how much a pretrained VLM contributes to robot control.
- The problem matters for compact VLAs, where limited capacity and short training budgets make capability loss more costly.

## Approach
- CLAP generates a short language description of an action chunk, such as "move forward, tilt right, and close the gripper," before generating the numeric action tokens.
- The model generates both parts in one causal sequence, so each numeric action token conditions on the preceding language description.
- The description comes from a fixed template applied to existing action labels, so the method needs no manual annotations, action expert, vocabulary extension, or architecture change.
- Actions remain directly executable: each 7-DoF action uses 1,000 discretization bins, and the output preserves precise numeric control.
- An optional action-masking augmentation replaces some input action tokens with placeholders, but the default CLAP model does not use masking.

## Results
- On LIBERO after one epoch, 0.8B, 2B, and 4B CLAP models achieve 89.6%, 90.8%, and 84.9% average success, improving over matched VLA-0 baselines by 13.5, 14.9, and 20.7 percentage points.
- The 2B model improves every LIBERO suite over VLA-0: Spatial rises from 77.8% to 93.0%, Object from 86.6% to 97.4%, Goal from 77.0% to 90.8%, and Long from 62.4% to 82.0%.
- On LIBERO-PRO, unmasked CLAP improves average out-of-distribution success over VLA-0 by 5.5, 11.1, and 10.9 points at 0.8B, 2B, and 4B. For 4B models on Spatial tasks with novel visual instances, the gain is 42.6 points; masking raises that gain to 54.4 points.
- Action masking has mixed in-distribution effects: it changes LIBERO averages by -3.9 points at 0.8B, -1.7 points at 2B, and +3.2 points at 4B.
- The reported training cost is about 6.5 hours on 8 GPUs, with open-weight models at 0.8B, 2B, and 4B planned for release.

## Link
- [https://arxiv.org/abs/2607.08974v1](https://arxiv.org/abs/2607.08974v1)
