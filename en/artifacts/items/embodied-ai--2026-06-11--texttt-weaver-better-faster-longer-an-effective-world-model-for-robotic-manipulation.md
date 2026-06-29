---
source: arxiv
url: https://arxiv.org/abs/2606.13672v1
published_at: '2026-06-11T17:59:15'
authors:
- Arnav Kumar Jain
- Yilin Wu
- Jesse Farebrother
- Gokul Swamy
- Andrea Bajcsy
topics:
- world-model
- robot-manipulation
- multiview-vision
- latent-dynamics
- test-time-planning
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# $\texttt{WEAVER}$, Better, Faster, Longer: An Effective World Model for Robotic Manipulation

## Summary
WEAVER is a robot world model for manipulation that predicts future latent states, rewards, and decoded observations from multiview inputs and action chunks. It targets three uses: policy evaluation, policy improvement, and test-time planning.

## Problem
- Robot world models need to be accurate, stay coherent over long horizons, and run fast enough for planning.
- Manipulation adds multiview occlusions, contact-rich motion, and the need to judge arbitrary visuomotor policies from predicted rollouts.
- Prior models trade off fidelity, consistency, and speed, so they do not support all three downstream uses at once.

## Approach
- Encode multiview images and proprioception into latents with a pretrained encoder.
- Predict future latent trajectories with a flow-matching objective, plus diffusion forcing for long-horizon consistency.
- Use sparse memory and short-term history so the model tracks both recent motion and longer context.
- Add latent reward and critic heads so the model can score imagined rollouts without decoding images into an external judge.
- Distill the model with rectified flow and use KV caching and token dropping to cut inference cost.

## Results
- On DROID validation, WEAVER gets FID 10.20 and FVD 27.83 at 16 NFE on the exterior view, versus Ctrl-World’s FID 26.09 and FVD 78.73; on the wrist view it gets FID 21.50 and FVD 90.72 versus 33.83 and 195.37.
- On the out-of-distribution task set, WEAVER gets FID 23.95 and FVD 88.27 at 16 NFE on the exterior view, versus Ctrl-World’s 36.16 and 139.54.
- Reported inference time for a 10 s rollout is 4.78 s at 16 NFE for WEAVER versus 14.65 s for Ctrl-World; at 50 NFE it is 14.25 s versus 42.33 s.
- For policy evaluation on five real manipulation tasks, WEAVER reports correlation rho = 0.870 with real-world success rate.
- For policy improvement, it raises the real-world success rate of the pi_0.5 robot foundation model by 38% without real-world interaction.
- For test-time planning, it improves real-world success rate by 14% and runs 5-10x faster than Ctrl-World.

## Link
- [https://arxiv.org/abs/2606.13672v1](https://arxiv.org/abs/2606.13672v1)
