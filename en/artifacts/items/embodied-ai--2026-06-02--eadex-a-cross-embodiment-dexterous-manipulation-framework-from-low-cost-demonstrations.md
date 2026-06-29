---
source: arxiv
url: https://arxiv.org/abs/2606.03268v1
published_at: '2026-06-02T07:35:18'
authors:
- Qian Zhao
- Xin Tong
- Chengdong Wu
- Yang Yang
- Yingtian Li
topics:
- dexterous-manipulation
- low-cost-demonstrations
- cross-embodiment
- reinforcement-learning
- motion-retargeting
- contact-rewards
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# EaDex: A Cross-Embodiment Dexterous Manipulation Framework from Low-Cost Demonstrations

## Summary
EaDex trains bimanual dexterous manipulation policies from single RGB-D human demonstrations and retargets them across several robot hand embodiments. Its main gain comes from reducing dependence on noisy demonstrations once the policy has learned stable contact.

## Problem
- Dexterous manipulation has a large control space, so pure reinforcement learning needs heavy exploration and often fails to converge.
- Imitation learning can reduce exploration, but high-quality dexterous hand demonstrations often need motion capture, teleoperation hardware, or careful calibration.
- The paper targets low-cost demonstrations that still give useful contact and motion cues for articulated object opening tasks.

## Approach
- EaDex records bimanual human hand motion with one Intel RealSense D435i RGB-D camera.
- It detects hand keypoints with MediaPipe, fits MANO hand pose parameters, smooths trajectories with a Gaussian filter, and stores data in ARCTIC format.
- The same human demonstrations are retargeted to three dexterous hands: Inspire Hand, Allegro Hand, and XHand.
- Policies are trained in Genesis with PPO using task reward, imitation reward, behavior cloning reward, and contact reward.
- A contact-reward-based annealing rule lowers the imitation and behavior cloning weights only after contact reward and episode length pass fixed stability thresholds.

## Results
- On a custom low-cost dataset, EaDex evaluates 3 hands × 3 articulated objects, giving 9 cross-embodiment manipulation settings.
- Average success rate rises from 23.5% without annealing to 36.5% with annealing, a 55.3% relative improvement.
- The best custom-dataset task reaches 93.3% success.
- Evaluation tasks include box, waffle iron, and mixer opening, with success defined by keeping the object on a 0.2 m × 0.2 m × 0.1 m platform and reaching a final articulation angle above 45°.
- On ARCTIC Ability Hand tasks using ADD-AUC3, annealing improves Ketchup from 9.0 ± 0.6 to 57.91 ± 28.12, Waffleiron from 9.1 ± 0.7 to 23.01 ± 0.65, and Mixer from 28.1 ± 7.4 to 35.14 ± 4.02.
- The authors report that some full pipelines from demonstration collection to a trained policy finish in about 1 hour on one RTX 3090 GPU.

## Link
- [https://arxiv.org/abs/2606.03268v1](https://arxiv.org/abs/2606.03268v1)
