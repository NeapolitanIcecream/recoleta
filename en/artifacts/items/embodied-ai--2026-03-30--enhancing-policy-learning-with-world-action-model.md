---
source: arxiv
url: http://arxiv.org/abs/2603.28955v1
published_at: '2026-03-30T19:56:05'
authors:
- Yuci Han
- Alper Yilmaz
topics:
- world-model
- robot-policy-learning
- inverse-dynamics
- calvin-benchmark
- diffusion-policy
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Enhancing Policy Learning with World-Action Model

## Summary
WAM adds action prediction to a DreamerV2 world model so its latent states keep information that matters for control, not only image reconstruction. On CALVIN manipulation tasks, this change improves both imitation learning and PPO fine-tuning inside the learned model.

## Problem
- Standard world models in robotics are trained to predict future observations, so their latent states may miss the action-relevant details that a policy needs.
- In pipelines such as DiWA, the policy learns from those latent states directly. If the representation is good for pixels but weak for control, downstream policy learning suffers.
- This matters because better latent dynamics can improve policy success and reduce real or simulated training effort for robot manipulation.

## Approach
- The paper builds WAM on DreamerV2's RSSM world model and adds an inverse dynamics head that predicts the action between two consecutive encoder embeddings.
- Training uses a joint loss: KL regularization for the latent dynamics, image reconstruction loss for future observation prediction, and L1 action prediction loss for the inverse dynamics head.
- The action head operates on encoder embeddings rather than RSSM features so action prediction is not trivial from already-conditioned latent dynamics.
- After world-model training, the model is frozen and used to extract latent features for a diffusion policy trained with behavioral cloning on 50 expert episodes per task.
- The BC policy is then fine-tuned with model-based PPO inside the frozen world model, using imagined latent rollouts and a reward classifier retrained on WAM features.

## Results
- On CALVIN world-model evaluation, WAM beats DreamerV2 on all reported video prediction metrics after 230K training steps versus 2M for DreamerV2: PSNR 22.10 vs 21.66, SSIM 0.814 vs 0.807, LPIPS 0.144 vs 0.149, and FVD 10.82 vs 12.13.
- For behavioral cloning on 8 CALVIN tasks, WAM reaches 61.7% average success versus 45.8% for DiWA in Table III. The abstract also reports 71.2% vs 59.4%, so the excerpt contains two different averages.
- WAM beats DiWA on 7 of 8 BC tasks in Table III, including close_drawer 89.7% vs 58.6%, open_drawer 73.3% vs 53.3%, and move_slider_right 82.8% vs 51.7%.
- After 800 iterations of model-based PPO fine-tuning, WAM reaches 92.8% average success versus 79.8% for DiWA, a gain of 13.0 percentage points.
- Two PPO-tuned tasks reach 100.0% success with WAM: turn_on_lightbulb and turn_off_led. Other reported gains include open_drawer 96.7% vs 74.4% and turn_on_led 96.6% vs 86.2%.
- The paper claims these gains come with 8.7x fewer world-model training steps than the DreamerV2 baseline, and reward classifiers trained on WAM features achieve at least 0.97 precision and 1.00 recall on training data.

## Link
- [http://arxiv.org/abs/2603.28955v1](http://arxiv.org/abs/2603.28955v1)
