---
source: arxiv
url: https://arxiv.org/abs/2606.23641v1
published_at: '2026-06-22T17:30:29'
authors:
- Haochen Zhang
- Yonatan Bisk
topics:
- vision-language-action
- robot-foundation-model
- instruction-following
- sharpness-aware-minimization
- robot-finetuning
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Flatness Preserves Instruction Following in Vision-Language-Action Models

## Summary
Applying sharpness-aware minimization during VLA finetuning improves instruction following on counterfactual robot tasks using the same finetuning data. The paper claims the gain comes from flatter parameter regions that reduce overfitting to visual shortcuts.

## Problem
- VLA models often lose pretrained vision-language grounding when finetuned on small, biased robot datasets.
- This causes instruction blindness: the robot follows the training-time visual pattern and ignores a changed language instruction, such as picking the seen object instead of the requested one.
- The problem matters because language-conditioned robot policies need to handle new instruction-scene pairings without collecting new demonstrations for every pairing.

## Approach
- The method adds sharpness-aware minimization (SAM) to standard VLA finetuning, with no new data, architecture change, or full retraining.
- At each step, SAM first finds a small weight perturbation in the direction that raises loss, then updates the original weights using the gradient at that perturbed point.
- In simple terms, the model is trained to do well in a small neighborhood around its current weights, which favors flatter solutions and reduces sensitivity to small parameter changes.
- The experiments apply SAM mainly to the π0.5 VLA with AdamW for 30k LIBERO finetuning steps, then test zero-shot on new observation-instruction pairs.
- The paper also tests component-only SAM, sharpness metrics, Hessian maximum eigenvalue, and inference-time guidance combined with SAM.

## Results
- The paper reports relative instruction-following gains of 60.2% on LIBERO-PRO Task, 70.2% on LangGap, and 217% on LIBERO-CF over the default finetuned π0.5 model.
- On LIBERO-PRO Task, π0.5_SAM reaches 42.6% average success, compared with 26.6% for π0.5, 30.2% for π0.5_cfg, 6.75% for π0.5_LORA, and 1.4% for OpenVLA-OFT.
- On LangGap, π0.5_SAM reaches 41.7% average success, compared with 24.5% for π0.5, 29.4% for π0.5_cfg, 24.8% for π0.5_LangGap, and 0.2% for π0.5_LORA.
- On LIBERO-CF, π0.5_SAM reaches 47.8% average success, compared with 13.2% for π0.5, 36.3% for π0.5_cfg, 21.7% for π0.5 CAG, 11.3% for OpenVLA-OFT CAG, and 5.7% for π0.5_LORA.
- The sharpness metric drops from 0.012 for π0.5 to 0.005 for π0.5_SAM, and the Hessian maximum eigenvalue drops from 0.93 to 0.52.
- In real-world DROID-style pick-and-place tests, SAM raises average task success from 13.8% to 36.3%, a 163% relative improvement.

## Link
- [https://arxiv.org/abs/2606.23641v1](https://arxiv.org/abs/2606.23641v1)
