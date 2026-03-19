---
source: hn
url: https://huggingface.co/blog/Photoroom/prx-part3
published_at: '2026-03-09T23:17:50'
authors:
- gsky
topics:
- text-to-image
- diffusion-models
- pixel-space-training
- efficient-training
- perceptual-loss
- token-routing
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# PRX Part 3 – Training a Text-to-Image Model in 24h

## Summary
This article presents a practical diffusion model training recipe: combine multiple engineering techniques that have been validated to work, and train a usable text-to-image model under a budget of **24 hours, 32 H200s, and about $1,500**. The core contribution is not proposing a single entirely new algorithm, but demonstrating that under low-cost, short-cycle constraints, pixel-space training can work together reliably with multiple acceleration and quality-improvement methods.

## Problem
- The problem to solve is: **how to quickly train a text-to-image diffusion model with acceptable quality and practical usability under strict compute and budget constraints**.
- This matters because early high-quality diffusion model training usually required extremely high costs; if the cost can be reduced to roughly one day and about $1,500, it would significantly lower the barrier to research and productization.
- The practical difficulty is that training cost must be reduced without causing obvious degradation in image quality, prompt following, or high-resolution detail.

## Approach
- **Train directly in pixel space**: use x-prediction and no longer use a VAE; control token count through patch size 32 and a 256-dimensional bottleneck, making it possible to start at 512px and then fine-tune to 1024px.
- **Add perceptual losses**: beyond the main diffusion/flow matching objective, add **LPIPS (weight 0.1)** and **DINOv2 perceptual loss (weight 0.01)** to directly constrain the predicted image and target image to be close in perceptual feature space, improving convergence speed and visual quality.
- **Use TREAD for token routing**: let **50% tokens** jump from block 2 to the second-to-last block to reduce computation; at the same time, use self-guidance based on dense vs. routed conditional prediction to mitigate the degradation in visual quality that routed models show under vanilla CFG.
- **Use REPA for representation alignment**: use **DINOv3** as the teacher, apply an alignment loss at **transformer block 8** with weight **0.5**; compute it only on non-routed tokens to keep the signal consistent.
- **Optimizer and training recipe**: use **Muon** for 2D parameters and Adam for the rest; the dataset consists of three public synthetic datasets totaling **1.7M + 6M + 1M**; the training schedule is **512px for 100k steps (batch 1024)**, then **1024px for 20k steps (batch 512, without REPA)**, with **EMA=0.999**.

## Results
- The most central result is that the authors claim to have trained a **"clearly usable"** text-to-image model under a budget of **32×H200, 24 hours, and about $1,500**, showing that low-cost rapid training is now feasible.
- In terms of quantitative training configuration, the model uses about **8.7M** training samples (**1.7M + 6M + 1M**), for a total of **120k steps**, including **100k steps@512px** and **20k steps@1024px**.
- In terms of quality, the authors explicitly claim the model has **strong prompt following**, a **consistent overall aesthetic style**, and that the **1024px stage mainly improves detail sharpness without damaging composition**.
- The authors also clearly point out limitations: there are still **texture artifacts, occasional human anatomy abnormalities, and instability on complex prompts**; they attribute these to **insufficient training and limited data diversity**, rather than structural flaws in the recipe itself.
- The article **does not provide explicit standard benchmark numbers** (such as FID, CLIP score, GenEval, or DrawBench scores) or quantitative comparisons against specific baselines; the strongest empirical claim is that this combined recipe can produce a “usable” 1024-resolution text-to-image model under a very limited budget, and can serve as the foundation for future large-scale training recipes.

## Link
- [https://huggingface.co/blog/Photoroom/prx-part3](https://huggingface.co/blog/Photoroom/prx-part3)
