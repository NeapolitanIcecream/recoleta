---
source: arxiv
url: https://arxiv.org/abs/2605.19282v1
published_at: '2026-05-19T03:00:26'
authors:
- Chongyu Fan
- Gaowen Liu
- Mingyi Hong
- Ramana Rao Kompella
- Sijia Liu
topics:
- vla-training
- robot-policy
- optimizer-design
- spectral-optimization
- rlvr
- newton-schulz
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# Rethinking Muon Beyond Pretraining: Spectral Failures and High-Pass Remedies for VLA and RLVR

## Summary
Pion is a Muon-style optimizer for VLA training and RLVR post-training that keeps large singular directions and suppresses small noisy ones. The paper claims better robot-policy training and more stable RLVR than Muon, with the same per-step cost as Muon.

## Problem
- Muon maps all nonzero singular values of the momentum matrix toward 1, which can amplify noisy small singular directions.
- In VLA training, action-module gradients are low-rank because robot actions are low-dimensional, so Muon can corrupt the action update.
- In RLVR, policy gradients have low signal-to-noise ratio, and Muon can collapse training by lifting noisy directions to the same scale as useful directions.

## Approach
- Pion changes Muon’s Newton-Schulz update coefficients while keeping the same optimizer control flow and per-step cost.
- It applies a two-stage high-pass Newton-Schulz iteration: a Promotion stage raises leading singular values, then a Suppression stage pushes small singular values toward 0.
- The Promotion polynomial uses coefficients `(1.875, -1.25, 0.375)` and preserves the order of singular values on `[0,1]`.
- The Suppression stage anchors large singular values near 1 and contracts small ones, giving a soft rank-adaptive update without SVD or sketching.
- For attention layers, Pion can reshape projections by head and apply the same update per head, preserving pretrained head-level differences at no extra cost.

## Results
- On VLA-Adapter with LIBERO Object, Pion reaches `100%` success after `1,500` training steps, compared with `97.0%` for Muon and `32.2%` for AdamW.
- On LIBERO and LIBERO-Plus, Pion beats Muon and AdamW across `l1`-regression VLA-Adapter and flow-matching VLANeXt architectures; the excerpt does not provide full table values.
- On a real Franka Research 3 robot with a `pi_0.5` backbone under the DROID setup, Pion improves three grasp-and-place tasks; the excerpt does not provide numeric success rates.
- In the action-module comparison on LIBERO Object, Low-rank Muon gives the best success among AdamW, Muon, and LRMuon, but costs about `15x` more training time than AdamW and Muon.
- In RLVR post-training with Qwen3-1.7B and Qwen3-4B using GRPO and GMPO, Pion beats AdamW on MATH and GSM8K while Muon collapses to `0`; the excerpt does not provide exact accuracy values.

## Link
- [https://arxiv.org/abs/2605.19282v1](https://arxiv.org/abs/2605.19282v1)
