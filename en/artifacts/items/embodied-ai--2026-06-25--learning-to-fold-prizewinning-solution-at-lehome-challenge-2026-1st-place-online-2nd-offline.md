---
source: arxiv
url: https://arxiv.org/abs/2606.27163v1
published_at: '2026-06-25T15:31:23'
authors:
- Ilia Larchenko
topics:
- vision-language-action
- robot-folding
- sim2real
- reinforcement-learning
- bimanual-manipulation
- deformable-objects
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Learning to Fold: prizewinning solution at LeHome Challenge 2026 (1st place online, 2nd offline)

## Summary
This paper reports a competition-winning bimanual garment-folding system built around a flow-matching VLA policy improved with reinforcement learning, replay, human corrections, and sim-to-real tuning.

## Problem
- It targets deformable-object manipulation: folding shirts, tops, pants, and shorts with two 6-DOF robot arms from RGB cameras.
- The task matters because cloth folding is hard for behavior cloning alone: cloth state changes fast, rewards are sparse, and the policy must generalize to unseen garments.
- The real-world phase adds a transfer problem: the author trained without access to the final evaluation robot.

## Approach
- The base policy is a SigLIP + Gemma VLA derived from pi_0.5, with a Gemma-300M action expert that outputs 30-step, 12-dimensional joint-action chunks by flow matching.
- The same network predicts actions and value-like signals: success probability, completion, garment type, keypoint distances, future keypoint distances, and an action-conditional success residual.
- Training combines AWR-style advantage-weighted sampling with RECAP-style advantage conditioning, so high-advantage frames are sampled more and the policy can be guided at inference time.
- Data collection runs asynchronously through HuggingFace Hub: one trainer, multiple Isaac Sim rollout workers, and a manual DAgger station for correcting hard states.
- Sim-to-real uses camera-alignment tooling, heavy image and environment augmentation, velocity alignment, and human-in-the-loop real-robot data.

## Results
- Online simulation round: 1st place out of 62 teams in the LeHome Challenge 2026.
- Online score: 79.63% overall success, 6.1 percentage points ahead of 2nd place.
- Online evaluation covered 4 garment types, with 20 instances per type: 10 seen and 10 unseen, including private unseen garments.
- Real-world final: 2nd place among the top 8 simulation teams at ICRA 2026.
- Real evaluation used 4 garment types with 5 garments per type, including 3 seen and 2 unseen garments per type.
- The paper gives little formal ablation evidence; it describes the shipped system and states that the components were not tested in a controlled way.

## Link
- [https://arxiv.org/abs/2606.27163v1](https://arxiv.org/abs/2606.27163v1)
