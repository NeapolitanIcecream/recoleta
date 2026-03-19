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
- token-routing
- perceptual-loss
- low-cost-training
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# PRX Part 3 – Training a Text-to-Image Model in 24h

## Summary
This article presents a text-to-image diffusion training recipe that combines multiple previously validated techniques, making it possible to train a "usable" 512/1024-resolution model within a budget of **24 hours, 32 H200s, and about $1500**. The core contribution is not proposing a single brand-new algorithm, but demonstrating that through careful engineering integration, low-cost and rapid training of high-quality diffusion models has become feasible.

## Problem
- The problem the paper aims to solve is: **under strict compute and cost constraints, how can a competitive text-to-image model be trained quickly from scratch**.
- This matters because early diffusion model training often required extremely high cost; if that cost can be reduced to the **single-day, thousand-dollar scale**, the barrier to research and product iteration drops substantially.
- The authors also want to verify whether using the previously tested tricks together can achieve a practically useful balance between **throughput, convergence speed, and final image quality**.

## Approach
- Use **pixel-space x-prediction**, training directly in pixel space **without using a VAE**; control token count via patch size 32 and a 256-dimensional initial bottleneck, then train at **512px before fine-tuning to 1024px**.
- In addition to the standard diffusion/flow matching objective, add two lightweight **perceptual losses**: **LPIPS (weight 0.1)** and **DINOv2 perceptual loss (weight 0.01)**, applying supervision at **all noise levels** based on **full-image pooled features** to improve visual quality and convergence.
- Use **TREAD token routing** to reduce computation: let **50% of tokens** bypass from the 2nd block to the penultimate block, then reinject them; also use **self-guidance** to mitigate the quality drop of sparsely routed models under CFG.
- Use **REPA + DINOv3** for representation alignment, applying one alignment loss at the **8th transformer block** with weight **0.5**, and compute it only on **non-routed tokens** to keep supervision consistent.
- The optimizer uses **Muon** (for 2D parameters) + **Adam** (for the remaining parameters); the training data consists of about **8.7M** public synthetic image-text samples, with a schedule of **512px 100k steps, batch 1024**, then **1024px 20k steps, batch 512**, and **EMA=0.999** for sampling and evaluation.

## Results
- The clearest result is cost and speed: the authors completed training in **24 hours** on **32×H200**, with a total cost of about **$1500 (at $2/hour/GPU)**.
- In terms of data scale, training used about **8.7M** samples: **1.7M Flux generated + 6M FLUX-Reason-6M + 1M midjourney-v6-llava**.
- The resolution training strategy is **100k steps at 512px** followed by **20k steps at 1024px**; the authors claim the 1024 stage mainly serves to **improve detail sharpness without damaging composition**.
- The article **does not provide specific quantitative metrics** (such as FID/CLIP score/GenEval or clearly readable baseline comparison values from curves), so it is not possible to report strict numerical SOTA or percentage improvements.
- The strongest qualitative conclusion is that after only one day of training, the model is already "**clearly usable**," showing **strong prompt following** and **consistent aesthetic quality**, though it still has issues such as **texture artifacts, occasional human anatomy errors, and insufficient stability on difficult prompts**.
- The authors' core claim is that the remaining shortcomings look more like **insufficient training and limited data diversity** rather than a fundamentally structural problem with the training recipe; therefore, with **more compute and broader data coverage**, this approach should continue to improve steadily.

## Link
- [https://huggingface.co/blog/Photoroom/prx-part3](https://huggingface.co/blog/Photoroom/prx-part3)
