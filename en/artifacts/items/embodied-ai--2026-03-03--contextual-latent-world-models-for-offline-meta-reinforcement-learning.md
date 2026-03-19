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
- world-model
- task-representation
- self-supervised-rl
- temporal-consistency
relevance_score: 0.34
run_id: materialize-outputs
language_code: en
---

# Contextual Latent World Models for Offline Meta Reinforcement Learning

## Summary
This paper proposes SPC (Self-Predictive Contextual Offline Meta-RL), which jointly trains task context encoding and a conditional latent world model, using temporal consistency to learn more useful task representations. The core idea is that task representations should not only distinguish tasks, but also genuinely help predict future latent states and rewards under that task, thereby enabling better generalization to unseen tasks.

## Problem
- Offline meta-reinforcement learning aims to learn generalization across related tasks from fixed data, but without online interaction, **how to infer the task from limited context** becomes especially critical.
- Existing context-based methods mostly rely on **contrastive learning** to learn task representations, which typically can only “separate different tasks,” but **do not enforce that the representations contain long-term task-relevant dynamics and reward information**.
- This limits few-shot / zero-shot generalization to unseen tasks, which is one of the most important goals of offline meta-RL.

## Approach
- The authors propose **SPC**: first, a context encoder maps a set of transitions \((s,a,r,s')\) to a task representation \(z\), then the world model is made to **explicitly condition on this task representation** when predicting the future.
- Observations are first encoded into latent states, then discretized into discrete codes using **FSQ discrete quantization**; afterward, a task-conditioned dynamics model predicts the next discrete code based on the current code, action, and task representation, while a reward model predicts the reward.
- Training uses a **multi-step temporal consistency loss**: the model continuously predicts future states and rewards over multiple steps in latent space, rather than reconstructing raw observations; this forces the task representation to carry key information needed to explain task dynamics/rewards.
- To prevent the representation from learning only prediction while becoming less useful for distinguishing tasks, the method also adds an **InfoNCE contrastive loss** to the context encoder, making representations from the same task closer and those from different tasks farther apart.
- After learning the representation, the policy, Q-function, and value function are all conditioned on the **discrete latent state + task representation**, and **IQL** is used for offline policy optimization to mitigate distribution shift.

## Results
- The paper claims that on three benchmark families—**MuJoCo, Contextual-DeepMind Control, and Meta-World**—SPC significantly outperforms existing offline meta-RL methods in **generalization to unseen tasks**, covering both **few-shot and zero-shot** settings.
- The strongest conclusion in the abstract is that a jointly trained **task-conditioned latent world model** can learn **more expressive task representations** than methods relying only on contrastive learning or one-step reconstruction objectives, thereby significantly improving generalization performance.
- Key methodological findings include: **multi-step latent temporal consistency** outperforms **reconstruction-based objectives**; and **discrete codebooks / categorical dynamics** are important for modeling stochastic, multimodal transitions.
- The provided excerpt **does not include specific numerical results**, so it is not possible to accurately list metrics, dataset scores, relative improvement percentages, or precise gaps versus each baseline.

## Link
- [http://arxiv.org/abs/2603.02935v1](http://arxiv.org/abs/2603.02935v1)
