---
source: arxiv
url: https://arxiv.org/abs/2605.28231v1
published_at: '2026-05-27T09:44:46'
authors:
- Seungsu Kim
- Jinyoung Choi
- Seungmin Baek
- Jean-Michel Renders
topics:
- vision-language-action
- robot-manipulation
- progress-estimation
- token-compression
- flow-matching
- long-horizon-control
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# ProgVLA: Progress-Aware Robot Manipulation Skill Learning

## Summary
ProgVLA is a 0.1B-parameter vision-language-action policy for long-horizon robot manipulation under limited compute and memory. It compresses visual, language, and proprioceptive inputs into a small token set and trains auxiliary progress heads that reweight flow-matching imitation learning.

## Problem
- Large VLA robot policies often use multi-billion-parameter backbones and large robot pretraining datasets, which raises training and deployment cost.
- Small VLA policies can run on modest hardware, but the paper says they still struggle on long-horizon tasks where the robot must track how far it has progressed.
- The target problem matters because many manipulation tasks need reliable multi-step execution with limited robot data and local compute.

## Approach
- ProgVLA uses DUNE ViT-Small for vision, a frozen T5 text encoder for instructions, and an MLP for proprioception.
- Two Perceiver resampling stages compress variable-length inputs: one stage resamples each modality, a Transformer fuses the tokens, and a second resampler produces a fixed set of control tokens.
- A SmolVLA-style flow-matching action expert generates action chunks from the compressed context, using 10 Heun steps at inference.
- Progress heads predict normalized remaining-horizon progress, a state-action value, and a near-completion success signal from the same context tokens.
- The predicted advantage and success probability are detached and used as per-sample weights on the imitation loss, so training favors demonstrations and time steps linked to later task progress.

## Results
- On LIBERO, ProgVLA reaches 91.1% average success with 0.1B parameters, compared with 88.75% for SmolVLA 2.25B, 82.75% for SmolVLA 0.24B, 76.5% for OpenVLA 7B, and 86.0% for pi0 3.3B. The paper notes that baseline scores are imported from prior work, so this is a published-number comparison.
- On LIBERO Long, ProgVLA scores 88.6%, compared with 77% for SmolVLA 2.25B, 63% for SmolVLA 0.24B, 53.7% for OpenVLA 7B, and 73% for pi0 3.3B.
- On Meta-World MT50 LeRobot, ProgVLA reaches 78.5% average success across 49 tasks, compared with 68.24% for SmolVLA 2.25B, 56.95% for SmolVLA 0.24B, 50.5% for pi0 Paligemma-3B, and 47.9% for pi0 3.3B.
- Ablations on LIBERO show the post-fusion context resampler has the largest effect: removing it drops average success from 91.1% to 75.1% and Long success from 88.6% to 51.2%.
- Freezing DUNE drops LIBERO average success from 91.1% to 77.6%, replacing DUNE with DINOv3 drops it to 88.7%, and removing progress objectives drops it to 88.8%.
- In real-world in-distribution tests on a 6-DOF PiPER arm, trained from 50 demonstrations per task across 10 tasks, ProgVLA reaches 68% success over 100 trials; failures include 10 clutter obstructions, 8 gripper-opening timeouts, and 4 wrong-object grasps.

## Link
- [https://arxiv.org/abs/2605.28231v1](https://arxiv.org/abs/2605.28231v1)
