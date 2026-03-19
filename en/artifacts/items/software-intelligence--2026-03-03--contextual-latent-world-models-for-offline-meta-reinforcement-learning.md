---
source: arxiv
url: http://arxiv.org/abs/2603.02935v1
published_at: '2026-03-03T12:45:20'
authors:
- Mohammadreza Nakheai
- Aidan Scannell
- Kevin Luck
- Joni Pajarinen
topics:
- offline-meta-rl
- world-models
- representation-learning
- task-conditioning
- reinforcement-learning
relevance_score: 0.34
run_id: materialize-outputs
language_code: en
---

# Contextual Latent World Models for Offline Meta Reinforcement Learning

## Summary
This paper proposes SPC (Self-Predictive Contextual Offline Meta-RL), which jointly trains task context encoding and a task-conditioned latent world model to improve generalization in offline meta-reinforcement learning to unseen tasks. The core idea is to use a temporal consistency signal of "predicting future latent states and rewards," rather than only distinguishing tasks through contrastive learning.

## Problem
- Offline meta-reinforcement learning must learn, from only fixed offline data, a policy that can generalize to unseen but related tasks, which is important for real-world settings where repeated online interaction is not possible.
- Existing methods based on a context encoder usually rely mainly on contrastive learning. They may only "distinguish tasks," without necessarily learning the task-relevant dynamics and reward structure that truly determine control performance.
- One-step reconstruction or observation reconstruction signals are often insufficient to capture long-horizon, task-related dynamic changes, thus limiting few-shot / zero-shot generalization.

## Approach
- A context encoder aggregates a task representation `z` from a short sequence of transitions \b(s,a,r,s'), and uses it as an implicit task identifier for the world model, value function, and policy.
- An observation encoder maps states to a discrete latent code `c`, then a **task-conditioned** latent dynamics model `D(c,a,z)` predicts future latent states, and a reward model `R(c,a,z)` predicts rewards.
- Training uses a multi-step temporal consistency objective: cross-entropy loss for future latent codes and squared error for rewards. This forces the task representation to contain task information that can explain future evolution and rewards.
- To avoid representation collapse and improve task separability, an InfoNCE contrastive loss is additionally applied to the context encoder; the final context encoder is jointly optimized with "temporal consistency + contrastive learning."
- The downstream policy learning stage uses IQL to perform offline policy optimization over the discrete latent state `c` and task representation `z`, reducing the distribution shift problem in offline RL.

## Results
- The paper claims that on three benchmark families—**MuJoCo, Contextual-DeepMind Control, and Meta-World**—SPC significantly outperforms existing SOTA offline meta-reinforcement learning methods in **few-shot and zero-shot generalization** to unseen tasks.
- The abstract and provided excerpt do not include specific numeric tables, means/variances, percentage improvements, or per-baseline comparison numbers, so **quantitative results cannot be extracted from the provided text**.
- The strongest concrete claim is that, compared with using only contrastive learning or reconstruction-based representation learning, the task representations learned by SPC better capture **task-relevant dynamics**, rather than merely separating different tasks.
- The paper also claims that a discrete codebook latent space + task-conditioned dynamics is more expressive for learning **stochastic / multimodal transition dynamics** and has a clear impact on performance, but the excerpt does not provide the magnitude quantitatively.

## Link
- [http://arxiv.org/abs/2603.02935v1](http://arxiv.org/abs/2603.02935v1)
