---
source: arxiv
url: https://arxiv.org/abs/2606.18960v1
published_at: '2026-06-17T11:42:00'
authors:
- Zirui Zheng
- Jiaqian Yu
- Xiongfeng Peng
- jun shi
- Mingyi Li
- Chao Zhang
- Weiming Li
- Dong Wang
- Huchuan Lu
- Xu Jia
topics:
- robot-world-model
- action-conditioned-video
- memory-retrieval
- persistent-manipulation
- sim2real
- policy-evaluation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Mem-World: Memory-Augmented Action-Conditioned World Models for Persistent Robot Manipulation

## Summary
Mem-World is a multi-view action-conditioned robot world model that uses geometric memory to keep object details consistent during long manipulation rollouts. It targets wrist-camera occlusion and rapid egocentric motion, which cause prior models to forget or hallucinate scene content.

## Problem
- Robot manipulation world models often lose object identity and scene layout when the wrist camera is blocked by the gripper or moves away and returns.
- Fixed-stride history retrieval, used by Ctrl-World, uses joint-pose similarity as an indirect signal and can miss frames that show the relevant object or surface.
- This matters because long-horizon policy evaluation and synthetic policy training need rollouts that preserve task objects, targets, and contact-relevant details.

## Approach
- Mem-World builds on Ctrl-World and predicts future multi-view observations from the current observation, a future action chunk, and retrieved history frames.
- Its main mechanism is W-VMem, a wrist-view-centered surfel memory. A surfel is a small surface element tied to past visual observations and stored with time, view geometry, depth, and a manipulated-object flag.
- The model initializes memory from the first three camera views, then updates memory during rollout using predicted wrist-view frames so timestamps track what the moving wrist camera has seen.
- For each future action chunk, it estimates the future wrist-camera pose with forward kinematics, renders historical surfels from that pose, scores past timesteps by visibility, task relevance, and recency, then retrieves top-K non-redundant history frames.
- Retrieved frames give the video model concrete visual evidence for objects that may be hidden or out of view in the current wrist frame.

## Results
- On 34 memory-stress DROID replay trajectories, third-view results improve over Ctrl-World: PSNR 25.30 vs 23.17, SSIM 0.878 vs 0.828, LPIPS 0.054 vs 0.076, object consistency 0.619 vs 0.573. Cosmos Predict 2.5 scores 22.80 PSNR, 0.819 SSIM, 0.089 LPIPS, and 0.579 object consistency.
- On wrist-view prediction, Mem-World beats Ctrl-World: PSNR 19.21 vs 17.34, SSIM 0.691 vs 0.623, LPIPS 0.236 vs 0.281, object consistency 0.524 vs 0.476.
- In memory ablations, W-VMem outperforms short-term and stride retrieval. Third-view PSNR is 24.78 for W-VMem, 22.58 for stride, and 21.25 for short-term; wrist-view PSNR is 18.97, 17.06, and 15.04.
- For policy evaluation across five tasks, Mem-World's simulated success rates correlate with real-world success at r=0.97, p<0.001. Ctrl-World reaches r=0.85, p<0.01; the paper reports a 14.5% Pearson correlation gain.
- For policy improvement, the authors generate 200 synthetic trajectories per task, keep 20–30 human-labeled successful trajectories, and fine-tune π0.5. Average real-world success on three long-horizon tasks rises from 58% to 72%.

## Link
- [https://arxiv.org/abs/2606.18960v1](https://arxiv.org/abs/2606.18960v1)
