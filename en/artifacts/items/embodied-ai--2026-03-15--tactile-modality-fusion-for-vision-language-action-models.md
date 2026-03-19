---
source: arxiv
url: http://arxiv.org/abs/2603.14604v1
published_at: '2026-03-15T20:57:51'
authors:
- Charlotte Morissette
- Amin Abyaneh
- Wei-Di Chang
- Anas Houssaini
- David Meger
- Hsiu-Chin Lin
- Jonathan Tremblay
- Gregory Dudek
topics:
- vision-language-action
- tactile-fusion
- contact-rich-manipulation
- robot-policy-finetuning
- film-conditioning
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Tactile Modality Fusion for Vision-Language-Action Models

## Summary
This paper proposes TacFiLM, a post-training fusion method for lightweight injection of tactile information into vision-language-action models, aimed at improving contact-rich robotic manipulation. The core idea is to avoid adding input tokens; instead, pretrained tactile representations modulate intermediate visual features, enhancing contact awareness while preserving the original VLA priors.

## Problem
- Existing VLA models mostly rely on vision, but in contact-rich tasks such as insertion and cable plugging, vision cannot reliably perceive contact forces, friction, compliance, shear, and subtle pose errors under occlusion.
- Existing methods for incorporating tactile sensing into VLA often rely on token concatenation or additional large-scale multimodal pretraining, leading to longer context, higher compute cost, and more complex training pipelines.
- Training/finetuning robot behavior models is already expensive, so there is a need for a **post-training, parameter-efficient, computationally lightweight** tactile fusion mechanism.

## Approach
- Built on OpenVLA-OFT, the authors propose **TacFiLM**: first, a pretrained tactile encoder (such as T3 or Sparsh) encodes DIGIT tactile images into embeddings, and then these embeddings generate FiLM scaling and shifting parameters.
- These FiLM parameters are inserted into intermediate ViT blocks of the visual backbone to perform channel-wise affine modulation of visual features: letting “tactile information influence visual representations” rather than directly concatenating tactile inputs as extra tokens.
- Intuitively, tactile sensing acts like a global conditioning signal that tells visual features “what the current contact state is,” helping the action model make finer and more stable adjustments at the moment of contact.
- This method does not increase the input sequence length of the language model, does not require retraining the large backbone, and uses only LoRA-style parameter-efficient finetuning, preserving the original vision-language priors as much as possible.
- The authors also verify compatibility with different pretrained tactile representations, suggesting that the fusion framework is relatively flexible with respect to the choice of tactile encoder.

## Results
- Experiments cover **700+ real-robot rollouts**; among them, **270** for ID evaluation, **225** for OOD evaluation, and **210** for ablations.
- **ID: Circle-Peg 3mm**: TacFiLM achieves a success rate of **100.00%**, outperforming **86.67%** for OpenVLA-OFT and **96.67%** for TactileConcat; direct insertion rate is **36.67%**, higher than **3.33%/16.67%**; average maximum force is **7.64 N**, lower than **14.94/9.19 N**; average time is **52.03 s**, lower than **92.24/75.11 s**.
- **ID: Circle-Peg 2mm**: TacFiLM achieves a success rate of **86.67%**, higher than **66.67%** for OpenVLA-OFT and **73.33%** for TactileConcat; average maximum force is **7.22 N**, lower than **15.09/8.72 N**; average time is **87.11 s**, lower than **110.44/114.80 s**.
- **ID: USB-Cable-Plug**: TacFiLM achieves a success rate of **73.33%**, compared with **33.33%** for OpenVLA-OFT and **43.33%** for TactileConcat; direct insertion rate is **33.33%**, compared with **0.00%/6.67%**; time is **99.71 s**, better than **164.52/135.11 s**.
- **ID average**: TacFiLM achieves a success rate of **86.67%**, which is **15.56 percentage points** higher than **71.11%** for the runner-up baseline TactileConcat; direct insertion rate is **31.11%**, significantly higher than **8.89%** and **7.78%**; average maximum force is **8.34 N**, lower than **15.01/10.29 N**; average time is **79.62 s**, lower than **122.40/108.34 s**.
- The paper also claims that under **OOD** settings, TacFiLM maintains a **100% success rate** on **3mm peg insertion** and improves **HDMI cable plugging** success rate by **50%**; in some tasks it requires only about **1/3 of the force** used by baseline methods. Given that the OOD table in the excerpt is incomplete, it is not possible to verify every value item by item, but these are the strongest results explicitly claimed by the authors.

## Link
- [http://arxiv.org/abs/2603.14604v1](http://arxiv.org/abs/2603.14604v1)
