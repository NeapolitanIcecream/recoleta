---
source: arxiv
url: http://arxiv.org/abs/2604.17706v2
published_at: '2026-04-20T01:36:58'
authors:
- Haoxiang Jie
- Yaoyuan Yan
- Xiangyu Wei
- Kailin Wang
- Hongjie Yan
- Zhiyou Heng
- Daocheng Chen
topics:
- vision-language-action
- robot-foundation-model
- spatial-understanding
- online-reinforcement-learning
- flow-matching
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# OmniVLA-RL: A Vision-Language-Action Model with Spatial Understanding and Online RL

## Summary
OmniVLA-RL is a vision-language-action model that adds explicit 3D spatial modeling and online reinforcement learning to robotic manipulation. The paper claims this combination improves action precision, training stability, and benchmark success rates on LIBERO and LIBERO-Plus.

## Problem
- Existing VLA models often understand language and image semantics well but miss fine 3D spatial details needed for grasping, placement, and obstacle-aware manipulation.
- Common spatial fusion designs add 3D features only before or after the core model, which limits joint reasoning over language, vision, spatial cues, and actions.
- RL fine-tuning for VLA models is hard to stabilize: PPO is heavy because it needs a value model, and the paper argues GRPO can become unstable when applied at token level.

## Approach
- The model uses a **Mixture-of-Transformers (MoT)** backbone with three experts inside shared Transformer layers: a Reasoning Expert for vision-language understanding, a Spatial Expert for 3D scene features, and an Action Expert for control generation.
- The Reasoning Expert uses **SigLIP** to encode multi-view RGB observations and language tokens. The Spatial Expert uses **VGGT** to extract fine-grained spatial features and adds an auxiliary spatial decoder during training.
- A **Block-wise Causal Attention** mask treats reasoning and spatial tokens as a fully visible prefix, while action tokens form a causal suffix. This lets action generation read scene context without letting action noise corrupt scene understanding.
- Actions are generated with **Conditional Flow Matching** over action chunks, conditioned on spatial, semantic, and language features.
- For online RL, the paper introduces **Flow-GSPO**: it converts the flow-matching action sampler from a deterministic ODE into a stochastic SDE, then applies **GSPO** at the action-block level so exploration stays stochastic and optimization matches sequence actions better.

## Results
- On **LIBERO**, the paper claims an average success rate of **97.6%**.
- The abstract and introduction say the method **surpasses mainstream existing methods** on **LIBERO** and **LIBERO-Plus**.
- The paper claims better **convergence speed** and **final performance** than **PPO** and **GRPO** baselines on **LIBERO-Plus**.
- The provided excerpt does **not** include full result tables, per-task scores, or exact PPO/GRPO comparison numbers beyond the **97.6% average success rate on LIBERO**.

## Link
- [http://arxiv.org/abs/2604.17706v2](http://arxiv.org/abs/2604.17706v2)
