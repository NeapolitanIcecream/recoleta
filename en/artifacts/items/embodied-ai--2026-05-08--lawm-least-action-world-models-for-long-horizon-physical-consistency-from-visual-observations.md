---
source: arxiv
url: https://arxiv.org/abs/2605.08279v1
published_at: '2026-05-08T07:03:13'
authors:
- Qixin Xiao
- Maani Ghaffari
topics:
- world-model
- visual-prediction
- embodied-ai
- robot-interaction
- physics-informed-learning
- variational-integrator
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# LaWM: Least Action World Models for Long-Horizon Physical Consistency from Visual Observations

## Summary
LaWM is a visual latent world model whose next-state update comes from a learned least-action objective. It targets long-horizon video and robot-scene prediction where unconstrained latent transitions can drift away from physical dynamics.

## Problem
- It addresses compounding error, energy drift, unstable acceleration, and geometry errors in long-horizon visual rollouts.
- This matters for embodied AI, model-based reinforcement learning, and robot planning because a planner needs futures that remain dynamically coherent, beyond plausible-looking frames.

## Approach
- Each observation is encoded as a latent coordinate q_t; decoded latents produce predicted frames or states.
- The model learns a discrete Lagrangian L_d(q_k, q_{k+1}; h, eta) with a learned positive diagonal mass matrix and potential network. Here, action means the Lagrangian action, not a robot command.
- It forms a discrete action over latent states and derives a discrete Euler-Lagrange residual.
- The next latent state is found by an unrolled local solver that reduces that residual, initialized with constant-velocity extrapolation; the paper reports N=4 solver steps as enough for stable PIS and energy behavior in an ablation.
- Training combines rollout prediction losses, a DEL residual loss, and regularization, while inference uses the same DEL-defined transition recursively.

## Results
- On NewtonGen-style uniform motion, LaWM reports PIS-v_x 0.9938±0.0045 versus NewtonGen 0.9830±0.005, Veo3 0.9784±0.006, Sora 0.6548±0.022, CogVideoX-5B 0.5392±0.007, Wan2.2 0.6395±0.029, and PhyT2V 0.5349±0.014; the reference is 0.9972.
- On uniform-motion background consistency, LaWM reports BC 0.9930±0.0021 versus NewtonGen 0.9694±0.020 and Sora 0.9573±0.003, with reference 1.
- On uniform-motion motion smoothness, LaWM reports MS 0.9993±0.0001 versus NewtonGen 0.9962±0.003, Veo3 0.9953±0.001, and Sora 0.9926±0.003, with reference 1.
- On acceleration, LaWM reports PIS-a_x 0.8964±0.0275 versus NewtonGen 0.6568±0.013, Veo3 0.6187±0.308, Sora 0.3437±0.355, CogVideoX-5B 0.5458±0.038, Wan2.2 0.3077±0.261, and PhyT2V 0.5033±0.011; the reference is 0.8489.
- The excerpt also claims gains on embodied robot interaction metrics, including LPIPS, PSNR, AbsRel, δ1, δ2, and APSNR, but the provided text does not include those numeric values.

## Link
- [https://arxiv.org/abs/2605.08279v1](https://arxiv.org/abs/2605.08279v1)
