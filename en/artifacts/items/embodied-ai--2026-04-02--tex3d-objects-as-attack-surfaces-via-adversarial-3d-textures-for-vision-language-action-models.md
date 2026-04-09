---
source: arxiv
url: http://arxiv.org/abs/2604.01618v1
published_at: '2026-04-02T04:55:34'
authors:
- Jiawei Chen
- Simin Huang
- Jiawei Du
- Shuaihang Chen
- Yu Tian
- Mingjie Wei
- Chao Yu
- Zhaoxia Yin
topics:
- vision-language-action
- adversarial-robustness
- robot-manipulation
- 3d-texture-attacks
- sim2real
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Tex3D: Objects as Attack Surfaces via Adversarial 3D Textures for Vision-Language-Action Models

## Summary
Tex3D attacks vision-language-action models by optimizing adversarial 3D textures on object surfaces inside the simulator. The paper claims this is the first end-to-end method for physically grounded 3D texture attacks on VLA systems and shows large failure-rate increases in simulation and real-robot tests.

## Problem
- VLA models for robotic manipulation can fail under adversarial inputs, but prior attacks mainly use text perturbations or 2D image patches.
- Those attack surfaces are weak fits for real deployment: language attacks depend on the instruction channel, and 2D patches are view-dependent and visually obvious.
- 3D object textures are a stronger physical attack surface for robots, but standard simulators such as MuJoCo do not let gradients flow from the VLA loss back to object appearance, and long-horizon manipulation makes single-frame attacks unstable.

## Approach
- Tex3D builds a differentiable attack path with **Foreground-Background Decoupling (FBD)**: MuJoCo renders the full scene background, Nvdiffrast renders the target object with a learnable texture, and the two are composited into the observation used by the frozen VLA policy.
- FBD aligns object pose, camera matrices, and lighting across MuJoCo and Nvdiffrast so the inserted object matches the simulator view while still allowing gradients to update the texture.
- Tex3D adds **Trajectory-Aware Adversarial Optimization (TAAO)** to keep attacks effective over long episodes by giving more weight to behaviorally critical frames, estimated from latent velocity and acceleration in a pretrained visual encoder.
- TAAO also uses per-vertex color parameterization to keep the optimized texture smoother and reduce overfitting to a narrow set of views or frames.
- The framework supports both untargeted attacks, which push actions away from clean behavior, and targeted attacks, which push the policy toward attacker-chosen behavior; it also uses expectation over transformations for stronger physical transfer.

## Results
- The strongest claim is a **task failure rate up to 96.7%** under Tex3D.
- On **OpenVLA**, average failure rate rises from **24.1%** with no attack to **88.1%** with Tex3D for untargeted attacks, and to **90.5%** for targeted attacks. Gaussian noise reaches **31.1%**, and the strongest ablation before full Tex3D reaches **82.9%** untargeted and **86.6%** targeted.
- On **OpenVLA-OFT**, average failure rate rises from **4.7%** to **76.0%** under untargeted Tex3D and **79.3%** under targeted Tex3D. Gaussian noise reaches **6.5%**.
- On **pi0**, average failure rate rises from **4.6%** to **71.8%** under untargeted Tex3D and **73.3%** under targeted Tex3D. Gaussian noise reaches **10.7%**.
- For **OpenVLA spatial tasks**, failure reaches **95.8%** untargeted and **96.7%** targeted, compared with **15.6%** under no attack.
- The excerpt states experiments were run across multiple manipulation task suites in both simulation and real-robot settings, but the real-robot numbers are not included in the provided text.

## Link
- [http://arxiv.org/abs/2604.01618v1](http://arxiv.org/abs/2604.01618v1)
