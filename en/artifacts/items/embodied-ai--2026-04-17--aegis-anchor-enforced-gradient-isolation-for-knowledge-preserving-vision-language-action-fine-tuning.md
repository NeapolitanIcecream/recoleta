---
source: arxiv
url: http://arxiv.org/abs/2604.16067v1
published_at: '2026-04-17T13:49:57'
authors:
- Guransh Singh
topics:
- vision-language-action
- catastrophic-forgetting
- gradient-projection
- robot-fine-tuning
- knowledge-preservation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# AEGIS: Anchor-Enforced Gradient Isolation for Knowledge-Preserving Vision-Language-Action Fine-Tuning

## Summary
AEGIS is a fine-tuning method for vision-language-action models that keeps a pre-trained vision-language model's visual reasoning ability while still letting continuous action gradients update the backbone. It does this by detecting, layer by layer, when action-training gradients would push the model away from its pre-trained activation patterns and removing only that conflicting component.

## Problem
- Vision-language models are pre-trained with cross-entropy gradients spread across many semantic directions, while robot action fine-tuning injects high-magnitude MSE gradients concentrated in a narrow control subspace.
- This mismatch causes catastrophic forgetting: the paper reports that naive direct MSE fine-tuning causes VQA holdout loss to degrade steadily within **1,500 training steps**.
- Existing defenses have clear costs: **stop-gradient** preserves VQA by blocking action gradients, **LoRA** slows but does not stop VQA erosion, and mixed-batch VQA co-training can use up to **50%** VQA data during robot training, adding compute and data overhead.

## Approach
- AEGIS pre-computes a static activation anchor from masked VQA forward passes over all **26 transformer layers**, storing per-layer Gaussian mean and variance statistics.
- During robot fine-tuning, it measures how current layer activations drift from that anchor with a per-layer **Wasserstein-2** distance using mean shift and standard-deviation mismatch.
- It runs two backward passes on the same graph: one for the action loss and one for the anchor-restoration objective, producing a task gradient and an anchor gradient.
- For each transformer layer, it checks whether the action gradient conflicts with the anchor-restoration direction. If the dot product is negative, it projects out the conflicting component with a Gram-Schmidt step; if not, it leaves the gradient unchanged.
- The method changes only the backward pass. The paper says the forward pass, architecture, and task losses stay unchanged, and training needs no replay buffer, no co-training batches, and no discrete action tokens.

## Results
- The paper claims naive direct MSE fine-tuning causes a **significant, steady** increase in VQA holdout loss within **1,500 steps**.
- The stop-gradient baseline keeps VQA loss **roughly constant**, according to the text, but blocks continuous supervision from the action expert.
- The LoRA baseline uses **rank 16** and **alpha 32** on LLM layers and still shows a **steady increase** in VQA loss, though slower than naive fine-tuning.
- AEGIS builds its anchor in about **5 minutes on a single GPU** using **3,000 VQAv2 samples**.
- The projection removes less than **1% of gradient energy on average**, according to the abstract.
- The excerpt does **not provide full benchmark tables or end-task robot success numbers**, so there is no quantitative comparison here for manipulation performance, dataset-wide VQA scores, or baselines beyond the concrete claims above.

## Link
- [http://arxiv.org/abs/2604.16067v1](http://arxiv.org/abs/2604.16067v1)
