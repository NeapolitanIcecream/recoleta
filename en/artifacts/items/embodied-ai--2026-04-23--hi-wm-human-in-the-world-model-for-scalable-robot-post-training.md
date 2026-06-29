---
source: arxiv
url: http://arxiv.org/abs/2604.21741v1
published_at: '2026-04-23T14:42:54'
authors:
- Yaxuan Li
- Zhongyi Zhou
- Yefei Chen
- Yanjiang Guo
- Jiaming Liu
- Shanghang Zhang
- Jianyu Chen
- Yichen Zhu
topics:
- world-models
- robot-post-training
- human-in-the-loop
- vision-language-action
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training

## Summary
Hi-WM uses a learned world model as the place where a robot policy is tested, corrected by a human, and then improved with the collected corrections. The paper claims this cuts the cost of post-training generalist robot policies while raising real-world success on manipulation tasks.

## Problem
- Pretrained generalist robot policies still fail on task-specific scenes, contact-heavy manipulation, and long-horizon execution, so they need post-training before deployment.
- Standard human corrective post-training is expensive because every correction needs real robot time, scene setup, resets, and operator supervision in the physical world.
- Prior world-model work mainly uses the model for rollout generation or evaluation, not as an interactive place to collect human corrective data near failure states.

## Approach
- Hi-WM rolls out the current policy in an action-conditioned world model instead of on the real robot, then asks a human to intervene only when the rollout becomes incorrect or likely to fail.
- The world model is trained on a 14D continuous dual-arm action space, with failure cases and edge-case workspace data added so it follows actions closely and stays aligned with real execution.
- The system caches intermediate states, so an operator can roll back to a failure point and branch multiple alternative corrective continuations from the same state.
- These corrective segments are merged with the original real-world dataset and used for post-training the policy; the paper tests this with two backbones, Diffusion Policy (DP) and Pi0.
- The intervention interface is hardware-agnostic: keyboard, robot arm teleop, and VR controllers all map into the same policy action space.

## Results
- Across 3 real-world manipulation tasks and 2 policy backbones, Hi-WM improves average real-world success by **37.9 percentage points** over the base policy and by **19.0 points** over the world-model closed-loop baseline.
- Real-world success rates (%) for **DP**: Base **42.1 / 52.9 / 47.0**, WM-CL **76.3 / 64.7 / 70.6**, Hi-WM **92.1 / 85.3 / 94.1** on **Fold Towel / Push-T / Route Rope**.
- Real-world success rates (%) for **Pi0**: Base **55.3 / 76.5 / 64.7**, WM-CL **78.9 / 79.4 / 82.4**, Hi-WM **97.4 / 97.1 / 100.0** on the same three tasks.
- World-model evaluation tracks real-world performance closely, with **Pearson r = 0.953**, which supports using the model for intervention-time policy assessment.
- Adding edge-case data improves world-model visual fidelity: **PSNR 18.50 -> 22.53**, **SSIM 0.815 -> 0.942**, **LPIPS 0.152 -> 0.055** from base to full augmentation.
- The paper also claims better world-to-real positioning accuracy near workspace boundaries after edge-case augmentation, but the excerpt does not include the full numeric table for that test.

## Link
- [http://arxiv.org/abs/2604.21741v1](http://arxiv.org/abs/2604.21741v1)
