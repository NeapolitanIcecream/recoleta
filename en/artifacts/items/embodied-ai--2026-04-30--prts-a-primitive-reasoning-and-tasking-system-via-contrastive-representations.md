---
source: arxiv
url: https://arxiv.org/abs/2604.27472v1
published_at: '2026-04-30T06:14:02'
authors:
- Yang Zhang
- Jiangyuan Zhao
- Chenyou Fan
- Fangzheng Yan
- Tian Li
- Haitong Tang
- Sen Fu
- Xuan'er Wu
- Qizhen Weng
- Weinan Zhang
- Xiu Li
- Chi Zhang
- Chenjia Bai
- Xuelong Li
topics:
- vision-language-action
- robot-foundation-model
- goal-conditioned-rl
- contrastive-learning
- long-horizon-manipulation
- offline-robot-data
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# PRTS: A Primitive Reasoning and Tasking System via Contrastive Representations

## Summary
PRTS is a 4B vision-language-action robot model that adds goal-reachability learning to behavior-cloning pretraining. It trains the VLM to score how likely a state-action pair is to reach a language goal, using only offline trajectories.

## Problem
- Existing VLA pretraining mainly uses behavior cloning, so the model learns action prediction without an explicit estimate of task progress toward the language goal.
- This matters for long-horizon and contact-rich robot tasks, where a policy needs to tell whether the current state-action is moving closer to success.
- Prior value-augmented VLA methods cited in the excerpt need reward labels, progress labels, separate value networks, or multi-stage training.

## Approach
- PRTS treats each language instruction as a goal and applies contrastive reinforcement learning to offline robot demonstrations.
- It learns two embeddings: a state-action embedding phi(s,a) and a goal embedding psi(l). Their inner product approximates log discounted goal reachability, or log Q_l(s,a).
- Since the language goal is shared across a trajectory, the method weights positives by temporal distance to completion using gamma^(T-t), giving higher weight to states closer to task success.
- It uses bidirectional InfoNCE losses: state-action to language for task discrimination, and language to state-action for temporal progress ordering.
- The architecture adds <CRL_action> and <CRL_goal> token blocks to Qwen3-VL-4B-Instruct, with a role-aware causal mask that produces action logits and both contrastive embeddings in one forward pass.

## Results
- The excerpt gives no quantitative benchmark success rates, so the main performance claims cannot be checked numerically from the provided text.
- PRTS is pretrained on 167B tokens of manipulation and embodied-reasoning data.
- Training uses 64 H100 GPUs for 1 week, with a custom CuTe-FlashAttention kernel and sequence packing.
- The paper claims state-of-the-art performance on 4 simulation benchmark families: LIBERO, LIBERO-Pro, LIBERO-Plus, and SimplerEnv.
- The paper also evaluates on a real-world suite with 14 complex manipulation tasks across dual-arm RealMan and single-arm Flexiv platforms.
- Claimed gains are strongest for long-horizon execution, contact-rich tasks, zero-shot novel-instruction generalization, and recovery under human interventions, but the excerpt does not provide the success-rate deltas.

## Link
- [https://arxiv.org/abs/2604.27472v1](https://arxiv.org/abs/2604.27472v1)
