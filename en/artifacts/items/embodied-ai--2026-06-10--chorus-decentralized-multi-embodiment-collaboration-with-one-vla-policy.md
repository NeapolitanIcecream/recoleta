---
source: arxiv
url: https://arxiv.org/abs/2606.12352v1
published_at: '2026-06-10T17:26:08'
authors:
- Ria Doshi
- Tian Gao
- Annie Chen
- Chelsea Finn
- Jeannette Bohg
topics:
- vision-language-action
- multi-robot-collaboration
- decentralized-control
- robot-foundation-model
- multi-embodiment
- mobile-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# CHORUS: Decentralized Multi-Embodiment Collaboration with One VLA Policy

## Summary
CHORUS fine-tunes one pretrained VLA policy to run independently on each robot in a heterogeneous team. Each robot uses only its own observations and an identity prompt, yet the shared policy coordinates real mobile manipulators without runtime communication.

## Problem
- Multi-robot manipulation needs robots to respond to teammates while acting under partial observability.
- Centralized policies require team-wide observations and actions, so context length and communication needs grow with team size.
- Decentralized per-robot policies can require shared cameras, teammate proprioception, online alignment, or one trained policy per robot, which makes deployment and scaling harder.

## Approach
- CHORUS starts from the pretrained $\pi_{0.5}$ vision-language-action backbone and fine-tunes it with LoRA on multi-robot demonstrations.
- The training data is split into single-robot tuples $(o_r^t, A_r^t, c_r)$, so the model sees one robot's local observation, action chunk, and identity prompt at a time.
- A robot-identifying prompt names the embodiment and role, allowing one shared policy to choose actions for different robots.
- Padded 32-dimensional action vectors and variable image tokens let the same policy handle different robots, sensors, and action spaces.
- At inference, each robot runs its own copy of CHORUS using only local observations; no inter-robot messages, shared cameras, or shared proprioceptive state are used.

## Results
- In real-world tests on basket lifting, tape measurement, book handover, and 3-robot transport, the paper reports 25-45 demonstrations per task and 10-18 evaluation rollouts per task.
- CHORUS improves mean task success by 64 percentage points over decentralized diffusion policies trained from scratch.
- In a teammate-perturbation handover test, CHORUS succeeds in 17/20 trials versus 9/20 for the same VLA backbone trained as separate per-robot policies, a 40 percentage point gain.
- The perturbation split is 8/10 versus 3/10 for left perturbations and 9/10 versus 6/10 for right perturbations.
- CHORUS matches or exceeds a centralized VLA baseline across the three 2-robot tasks, although the centralized baseline conditions on both robots' observations.
- On a 3-robot transport task with Kinova and YAM mobile manipulators, one unchanged CHORUS policy reaches 90% success.

## Link
- [https://arxiv.org/abs/2606.12352v1](https://arxiv.org/abs/2606.12352v1)
