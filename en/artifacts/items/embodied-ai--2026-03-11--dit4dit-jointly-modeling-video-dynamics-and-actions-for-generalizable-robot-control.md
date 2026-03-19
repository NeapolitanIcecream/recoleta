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
- vision-language-action
- video-diffusion
- robot-control
- generalist-robot-policy
- world-model
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# DiT4DiT: Jointly Modeling Video Dynamics and Actions for Generalizable Robot Control

## Summary
DiT4DiT proposes end-to-end joint training of a video generation model and an action generation model, using intermediate spatiotemporal features from the video diffusion process to guide robot action prediction. The core idea is that learning video dynamics of "how the future will change" is more suitable as a foundation for general robot control than relying only on static visual semantics.

## Problem
- Existing VLA/robot foundation models mostly inherit representations from static vision-language pretraining and lack native modeling of **temporal change and physical dynamics**, so their control capability depends heavily on expensive action-labeled data.
- Previous methods that use video models for robot control often follow a **multi-stage** pipeline: first video/representation learning, then separate training of the action model, which makes information transfer indirect and training non-unified.
- The paper aims to solve: **how to truly make video generation the core backbone of robot policy learning**, and to show why it can improve generalization, data efficiency, and real-world deployment performance.

## Approach
- Uses a unified **dual-DiT architecture**: one Video Diffusion Transformer predicts future video dynamics, and one Action Diffusion Transformer predicts action trajectories.
- The key mechanism is not to use the final reconstructed future frames, but to extract features from the **intermediate hidden states in the video denoising process**, using these temporally grounded representations as conditional inputs to the action model.
- Proposes a **dual flow-matching** joint objective to train video generation and action generation simultaneously; both share a unified framework, but each has independent noise and flow timesteps.
- Adopts a **tri-timestep / decoupled timestep** design: the video module uses uniformly sampled timesteps to learn the full denoising trajectory; feature extraction uses fixed timesteps to ensure stable conditioning; the action module uses Beta-distributed timesteps to emphasize key control stages.
- For initialization, the video backbone comes from Cosmos-Predict2.5-2B, the action head is based on the GR00T-series Action DiT, and the text encoder and VAE are frozen, with only the two DiT modules jointly fine-tuned.

## Results
- On the **LIBERO** simulation benchmark, DiT4DiT achieves a **98.6% average success rate**, which the paper describes as a new SOTA, and it reports outperforming strong VLA baselines such as **π0.5** and **CogVLA** on long-horizon tasks.
- On **RoboCasa GR1** across 24 tabletop tasks, it reaches a **50.8% average success rate**, which the paper says significantly exceeds pretrained policy series such as **GR00T**.
- As validation for the claim that "video generation is a better scaling proxy task," on RoboCasa GR1 it improves **sample efficiency by over 10×** and **convergence speed by up to 7×** relative to Grounding and FLARE-style semantic-centric baselines.
- On the real-world **Unitree G1** robot, the paper claims it outperforms the pretrained baseline **GR00T-N1.5** and a parameter-matched baseline, and can complete high-precision tasks using only a **single first-person camera**; however, the excerpt **does not provide specific real-world numerical metrics**.
- The paper also claims strong **zero-shot generalization**, adapting to unseen objects, category changes, and quantity changes across both simulation and real environments; the excerpt likewise **does not provide quantified generalization scores**.

## Link
- [http://arxiv.org/abs/2603.10448v1](http://arxiv.org/abs/2603.10448v1)
