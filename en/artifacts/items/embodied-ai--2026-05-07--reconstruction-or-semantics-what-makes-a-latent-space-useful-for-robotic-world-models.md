---
source: arxiv
url: https://arxiv.org/abs/2605.06388v1
published_at: '2026-05-07T15:05:26'
authors:
- Nilaksh
- Saurav Jha
- Artem Zholus
- Sarath Chandar
topics:
- robot-world-models
- latent-diffusion
- semantic-latents
- policy-evaluation
- robot-planning
- bridgev2
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models

## Summary
The paper finds that semantic latents from V-JEPA 2.1, Web-DINO, and SigLIP 2 make better robot diffusion world models than pixel-reconstruction latents for planning and policy evaluation. Reconstruction VAEs can render strong pixels, but the useful signal for control is action- and task-relevant structure in the latent space.

## Problem
- Robot world models are used to test action sequences and policies before running them on real hardware, so their predictions need to preserve object state, contact, geometry, and task progress.
- Latent diffusion world models often use VAE-style latents trained for image reconstruction, which may score well on pixel metrics while losing signals needed for control.
- The paper asks which latent space works best for action-conditioned latent diffusion world models on real robot manipulation data.

## Approach
- The authors train action-conditioned DiT latent diffusion world models on BridgeV2, which has about 60K WidowX 250 demonstrations across 13 task families with RGB observations, 7-DoF actions, and language instructions.
- They keep the dataset, transition model, optimizer, history length, and action conditioning fixed, then vary only the encoder, optional adapter, and decoder path.
- They compare reconstruction encoders SD3 VAE (D=16), VA-VAE (D=32), and Cosmos (D=16) against semantic encoders V-JEPA 2.1 (D=1024), Web-DINO (D=1024), and SigLIP 2 (D=1152).
- For semantic encoders, they test native high-dimensional latents and S-VAE compressed latents with d=96, using a wide DDT head and dimension-dependent noise schedule shift where needed.
- Evaluation covers visual fidelity, CEM planning error, OpenVLA-7B rollouts inside the world model, OOD object and instruction tests, inverse-dynamics action recovery, and SOAR success classification.

## Results
- On DiT-S policy rollouts, V-JEPA 2.1_96 reaches the best consensus success rate at 0.362 ± 0.038, compared with VAE at 0.169 ± 0.030, VA-VAE at 0.175 ± 0.030, and Cosmos at 0.244 ± 0.034.
- SigLIP 2_96 has the best reported in-distribution success rate in the OOD subset at 0.625 ± 0.054 and the best distractor OOD success rate at 0.588 ± 0.055; VAE gets 0.375 ± 0.054 and 0.287 ± 0.051 on the same metrics.
- CEM action recovery favors semantic latents: SigLIP 2 has the lowest k=1 error at 0.082 ± 0.006, and V-JEPA 2.1 has the lowest k=4 error at 0.424 ± 0.014; VAE reports 0.111 ± 0.009 and 0.612 ± 0.023.
- In inverse-dynamics action recovery on encoder latents, V-JEPA 2.1 reaches Pearson r=0.829 at k=1 and r=0.865 at k=4, while VAE reaches r=0.507 and r=0.478.
- On generated world-model latents, V-JEPA 2.1 keeps the highest IDM correlations among listed DiT-S encoders at r=0.781 for k=1 and r=0.840 for k=4; VAE reports r=0.476 and r=0.464.
- On SOAR whole-video success classification, SigLIP 2 has the best world-model latent accuracy at 0.823, ahead of V-JEPA 2.1 at 0.789, Web-DINO at 0.788, VA-VAE at 0.744, Cosmos at 0.723, and VAE at 0.716.

## Link
- [https://arxiv.org/abs/2605.06388v1](https://arxiv.org/abs/2605.06388v1)
