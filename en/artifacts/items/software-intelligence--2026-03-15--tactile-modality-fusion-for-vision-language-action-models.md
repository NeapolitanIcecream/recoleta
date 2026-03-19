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
- robotics
- vision-language-action
- tactile-sensing
- multimodal-fusion
- film-conditioning
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# Tactile Modality Fusion for Vision-Language-Action Models

## Summary
This paper proposes **TacFiLM**, a lightweight method for injecting tactile information into vision-language-action (VLA) robot foundation models to improve contact-rich manipulation. Through post-training fine-tuning rather than large-scale retraining, it significantly improves success rate, direct insertion rate, speed, and force stability on real-robot insertion tasks.

## Problem
- Existing VLA robot policies rely mainly on vision, but vision cannot reliably perceive contact dynamics such as contact force, friction, compliance, and shear, making failures common in fine manipulation tasks such as insertion and plug-in operations.
- Existing tactile fusion methods often use token concatenation or additional multimodal pretraining, which increases sequence length, computational cost, and training complexity, making efficient adaptation of large models more difficult.
- This problem matters because contact-rich manipulation is a core bottleneck for real-world robotics; without a low-cost way to incorporate touch, general-purpose robot foundation models will struggle to operate robustly in real physical interaction.

## Approach
- The authors propose **TacFiLM**: instead of appending tactile signals as extra tokens to the input, they first use a pretrained tactile encoder to extract tactile embeddings, then apply **FiLM** to modulate intermediate visual backbone features with channel-wise scaling and shifting.
- The core idea can be understood as: **using touch to “lightly rewrite” visual features rather than expanding the context length**, thereby preserving existing vision-language priors while reducing computational burden.
- Concretely, the method is built on OpenVLA-OFT; tactile images are encoded by pretrained models (such as **T3** and **Sparsh**), which generate per-layer amma/beta parameters for FiLM modulation inside ViT blocks.
- Training mainly uses **LoRA post-training fine-tuning**, freezing most of the original model and updating only a small number of parameters plus the fusion module, making it parameter-efficient and avoiding additional large-scale multimodal pretraining.
- The method claims to be relatively agnostic to the choice of tactile encoder (encoder-agnostic), and can complete visual-tactile fusion without increasing token sequence length.

## Results
- Experiments are based on **700+ rollouts** on real robots, including **270** in-distribution evaluations, **225** out-of-distribution evaluations, and **210** ablation experiments.
- In-distribution **Circle-Peg (3mm)**: TacFiLM achieves a **100.00%** success rate, outperforming OpenVLA-OFT at **86.67%** and TactileConcat at **96.67%**; direct insertion rate is **36.67%**, higher than **3.33% / 16.67%**; average maximum force is **7.64N**, lower than **14.94N / 9.19N**; average completion time is **52.03s**, lower than **92.24s / 75.11s**.
- In-distribution **Circle-Peg (2mm)**: TacFiLM has **86.67%** success rate, compared with OpenVLA-OFT at **66.67%** and TactileConcat at **73.33%**; average maximum force is **7.22N**, lower than **15.09N / 8.72N**; average time is **87.11s**, better than **110.44s / 114.80s**.
- In-distribution **USB-Cable-Plug**: TacFiLM has **73.33%** success rate, clearly higher than OpenVLA-OFT at **33.33%** and TactileConcat at **43.33%**; direct insertion rate is **33.33%**, higher than **0.00% / 6.67%**; average time is **99.71s**, better than **164.52s / 135.11s**.
- Average in-distribution performance: TacFiLM achieves **86.67%** success rate, compared with OpenVLA-OFT at **62.22%** and TactileConcat at **71.11%**; direct insertion rate is **31.11%**, far above **8.89% / 7.78%**; average maximum force is **8.34N**, lower than **15.01N / 10.29N**; average time is **79.62s**, better than **122.40s / 108.34s**.
- Out-of-distribution **Square-Peg (3mm)**: TacFiLM achieves **100.00%** success rate, higher than the **93.33%** of OpenVLA-OFT and TactileConcat; direct insertion rate is **46.67%**, higher than **0.00% / 13.33%**; average maximum force is **5.37N**, significantly lower than **18.31N / 9.34N**.
- The paper also explicitly claims that, on selected tasks, TacFiLM can deliver up to **30%** success-rate improvement over the next-best baseline; on the out-of-distribution **HDMI** insertion task, success rate improves by **50%**; and on some tasks, the required applied force is about **1/3** of the baseline.

## Link
- [http://arxiv.org/abs/2603.14604v1](http://arxiv.org/abs/2603.14604v1)
