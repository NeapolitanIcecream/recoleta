---
source: arxiv
url: https://arxiv.org/abs/2605.09586v1
published_at: '2026-05-10T14:55:54'
authors:
- Can Li
- Zhoujian Li
- Ren Li
- Jie Gu
- Lei Lei
- Jingmin Chen
- Lei Sun
topics:
- deformable-object-modeling
- physics-neural-world-model
- robot-interaction
- material-point-method
- gaussian-splatting
- sim2real
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# DeformMaster: An Interactive Physics-Neural World Model for Deformable Objects from Videos

## Summary
DeformMaster learns an interactive world model for deformable objects from real videos. It predicts how ropes, cloths, packages, and soft toys move under new actions and renders the predicted motion from new views.

## Problem
- Deformable objects have high-dimensional motion, contact, self-contact, and spatially varying material behavior, which makes action-conditioned prediction hard from video alone.
- Embodied agents need models that can predict the effect of new interactions, rather than only replay observed motion or produce plausible video.
- Existing physics twins can miss real-world effects, while learned or generative dynamics can drift during long rollouts or lack explicit action control.

## Approach
- DeformMaster represents the object with material particles for dynamics and Gaussian appearance particles for rendering.
- Physics–Neural Particle-Grid Dynamics first rolls the state forward with differentiable MPM, then applies a bounded neural velocity correction to handle effects outside the simulator.
- Distributed Compliant Actuators convert sparse, noisy hand tracks into soft actuator-particle forces spread over local contact neighborhoods.
- A Mixture of Constitutive Experts blends Neo-Hookean, corotated, and StVK material laws with spatially varying weights and learned material fields.
- Predicted material-particle motion drives Gaussian Splatting through linear blend skinning, so new action rollouts can be rendered without re-optimizing the scene.

## Results
- On 20 real PhysTwin sequences captured with 3 RGB-D views at 30 fps, DeformMaster reaches IoU 0.748, Chamfer 0.011, Track error 0.024, PSNR 25.41, SSIM 0.936, and LPIPS 0.061.
- Against PhysTwin, it improves IoU from 0.734 to 0.748 and Chamfer from 0.012 to 0.011, with a slightly worse Track error of 0.024 versus 0.023.
- Against Spring-Gaus, it improves IoU from 0.464 to 0.748, Chamfer from 0.062 to 0.011, Track error from 0.094 to 0.024, and PSNR from 22.49 to 25.41.
- Against GS-Dynamics, it improves IoU from 0.498 to 0.748, Chamfer from 0.041 to 0.011, Track error from 0.070 to 0.024, and PSNR from 22.54 to 25.41.
- By object type, it improves rope IoU from 0.658 to 0.721, Chamfer from 0.007 to 0.005, and Track error from 0.013 to 0.010; on planar objects, Track error is worse than PhysTwin at 0.032 versus 0.028.
- The system supports online interactive rollout at over 15 fps and demonstrates novel action, material-scale, and novel-view queries, including fracture behavior when material fields are scaled to 0.3×.

## Link
- [https://arxiv.org/abs/2605.09586v1](https://arxiv.org/abs/2605.09586v1)
