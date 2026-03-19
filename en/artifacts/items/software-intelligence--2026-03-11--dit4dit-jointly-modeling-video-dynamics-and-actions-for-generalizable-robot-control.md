---
source: arxiv
url: http://arxiv.org/abs/2603.10448v1
published_at: '2026-03-11T06:03:53'
authors:
- Teli Ma
- Jia Zheng
- Zifan Wang
- Chuili Jiang
- Andy Cui
- Junwei Liang
- Shuo Yang
topics:
- robot-control
- video-diffusion
- vision-language-action
- flow-matching
- embodied-ai
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# DiT4DiT: Jointly Modeling Video Dynamics and Actions for Generalizable Robot Control

## Summary
This paper proposes DiT4DiT, which jointly trains a video generation model and an action generation model end-to-end, using intermediate features from the video diffusion process to guide robot control. The central claim is that video generation can serve as a stronger robot policy learning “scaling proxy” than static visual semantics, thereby delivering better generalization, sample efficiency, and control performance.

## Problem
- Existing VLA robot models are mostly inherited from static image-text pretraining and lack priors over **temporal variation and physical dynamics**, causing control capability to rely mainly on expensive action-labeled data to fill the gap.
- Prior uses of video models in robotics are often **multi-stage** pipelines, such as first generating video or extracting features and then separately training an action model, making the control pipeline indirect and the optimization inconsistent.
- This problem matters because generalized robot control requires understanding both “how the future will move” and “what I should do,” while static semantics alone is often insufficient for learning complex manipulation efficiently.

## Approach
- Proposes a unified **dual-DiT** architecture: a Video Diffusion Transformer predicts future video dynamics, and an Action Diffusion Transformer predicts action trajectories.
- The key mechanism is not to use reconstructed future frames themselves, but to extract features from the **intermediate hidden states of the video denoising process** and use them as temporal conditions for the action model; intuitively, this lets the action model “peek at” the video model’s internal representation of future dynamics rather than only the final frames.
- Uses a **dual flow-matching** joint objective to train video generation and action generation simultaneously, avoiding the mismatch caused by traditional staged training.
- Designs a **tri-timestep** decoupling scheme: the video module uses uniformly sampled timesteps to learn the full denoising trajectory; feature extraction uses fixed timesteps to ensure stable conditioning; the action module samples timesteps from a Beta distribution to focus training on more critical control phases.
- For initialization, the video backbone comes from Cosmos-Predict2.5-2B, the action head is adapted from GR00T-N1, and the text encoder and VAE are frozen while only the two DiT modules are jointly fine-tuned.

## Results
- Achieves an average success rate of **98.6%** on the **LIBERO** simulation benchmark, which the paper describes as a new **state-of-the-art**; it also explicitly states that it outperforms recent strong VLA models such as **π0.5** and **CogVLA**.
- Reaches an average success rate of **50.8%** on the 24 tabletop tasks of **RoboCasa GR1**, also claimed as **SOTA**; it further says it leads strong pretrained policies such as the **GR00T** series by “substantial margins,” though the excerpt does not provide per-method comparison numbers.
- As a training proxy task, compared with grounding and FLARE-style latent modeling, video generation improves **sample efficiency by more than 10×** and **convergence speed by up to 7×**; these conclusions come from experiments on the 24 RoboCasa-GR1 tasks.
- The paper emphasizes that it achieves the above performance with **less training data**, suggesting that the video generation objective can serve as a scalable policy learning signal, though the excerpt does not give precise data-scale configurations.
- On the real **Unitree G1** robot, the authors claim it outperforms the pretrained baseline **GR00T-N1.5** and a parameter-matched baseline, and shows strong **zero-shot generalization**, adapting to unseen objects, category changes, and quantity changes; however, the excerpt does not provide concrete real-world success-rate numbers.

## Link
- [http://arxiv.org/abs/2603.10448v1](http://arxiv.org/abs/2603.10448v1)
