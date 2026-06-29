---
source: arxiv
url: http://arxiv.org/abs/2604.03191v1
published_at: '2026-04-03T17:06:31'
authors:
- Takuya Shiba
topics:
- vision-language-action
- robot-policy-scaling
- discrete-action-tokenization
- diffusion-policy
- information-bottleneck
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# The Compression Gap: Why Discrete Tokenization Limits Vision-Language-Action Model Scaling

## Summary
This paper argues that scaling a vision encoder does not reliably improve robot manipulation when actions are compressed into discrete tokens. It names this failure mode the **Compression Gap**: the tightest information bottleneck in the policy pipeline determines whether better visual features can reach the action output.

## Problem
- Vision-language-action work often assumes that a stronger vision encoder should improve downstream control, as it does in vision-language modeling.
- The paper tests whether that assumption still holds when the policy predicts **discrete action tokens** instead of continuous actions.
- This matters for robot foundation models because many scaling plans focus on larger encoders and more pretraining, but those gains may be blocked by the action representation.

## Approach
- The paper compares two policy families on **LIBERO-10** under matched training and backbone settings: **Diffusion Policy (continuous actions)** and **OAT (discrete ordered action tokenization)**.
- It frames the pipeline with an information bottleneck view: in a chain from observation to representation to action, end-to-end information flow is capped by the narrowest stage.
- For OAT, the discrete tokenizer imposes a hard cap: with vocabulary size **1000** and latent horizon **8**, the action channel is bounded at about **80 bits per action chunk**.
- It runs three tests: a factorial comparison of encoder upgrades (**ResNet-18 → SigLIP**) across two model sizes, an encoder-quality sweep across **ResNet-18 / SigLIP / SigLIP 2 / DINOv2**, and a codebook-size ablation that changes OAT capacity.

## Results
- On **LIBERO-10**, upgrading the encoder from **ResNet-18 to SigLIP** improves **Diffusion Policy** from **36.4% → 57.6%** at size **M** (**+21.2 points**) and **44.0% → 70.0%** at size **L** (**+26.0 points**).
- Under the same encoder upgrade, **OAT** improves much less: **53.8% → 57.4%** at size **M** (**+3.6 points**) and **48.0% → 58.4%** at size **L** (**+10.4 points**).
- In the encoder sweep at size **M**, **Diffusion Policy** rises with encoder quality: **36.4% (ResNet-18)**, **57.6% (SigLIP)**, **62.8% (SigLIP 2)**, **63.8% (DINOv2 ViT-L/14)**. **OAT** does not show the same pattern: **53.8%**, **57.4%**, **44.2%**, **51.0%**.
- The relative ranking flips across encoder quality: with **ResNet-18**, **OAT beats DP by 17.4 points**; with **DINOv2**, **DP beats OAT by 12.8 points**, a reversal of about **30.2 points**.
- In the OAT codebook experiment, increasing capacity from **1000 (~80 bits)** to **1920 (~87 bits)** changes encoder sensitivity from **+3.6** to **+15.2 points** because **ResNet-18 drops to 42.6%** while **SigLIP stays near 57.8%**. At **4375 (~97 bits)**, OAT reaches **54.6% (ResNet-18)** and **58.6% (SigLIP)** with **+4.0 points**.
- The paper’s main claim is that discrete tokenization can block scaling gains from better perception. For VLA systems, the limiting factor may be the action tokenizer rather than the vision encoder or policy size.

## Link
- [http://arxiv.org/abs/2604.03191v1](http://arxiv.org/abs/2604.03191v1)
