---
source: arxiv
url: https://arxiv.org/abs/2606.19784v1
published_at: '2026-06-18T04:36:57'
authors:
- Thien-Loc Ha
- Quang-Tan Nguyen
- Trong-Bao Ho
- Long Dinh
- Minh Duc Nguyen
- Gia-Binh Nguyen
- Pham Tri Quang
- Minh N. Vu
- Duy M. H. Nguyen
- An Thai Le
- Ngo Anh Vien
topics:
- vision-language-action
- robot-foundation-model
- equivariant-policy
- robot-manipulation
- data-efficient-robotics
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# EquiVLA: A General Framework for Rotationally Equivariant Vision-Language-Action Models

## Summary
EquiVLA adds SO(2) rotation equivariance to VLA policies built from a frozen vision-language backbone and a flow-matching Diffusion Transformer action head. On GR00T N1.5, it reports higher performance on LIBERO, CALVIN, and Mobile ALOHA real-robot tasks.

## Problem
- Current VLA policies often relearn the same manipulation skill at many object orientations, which raises data needs and hurts use on rotated scenes.
- Data augmentation can expose more rotations, but it does not force the policy to produce a correspondingly rotated action when the observation rotates.
- This matters for generalist robot manipulation because object pose changes are common in tabletop tasks and real deployments.

## Approach
- EquiVLA targets VLA systems that pair a frozen VLM or ViT-style visual backbone with a flow-matching Diffusion Transformer action head.
- EquiPerceptor rotates the input image through a finite rotation group, runs the frozen ViT, moves patch tokens back to aligned grid positions, and averages them to create rotation-aware visual tokens.
- It sends invariant tokens through the frozen VLM with language and wrist-camera inputs, while equivariant tokens stay in a separate stream that preserves rotation structure.
- EquiActor replaces the standard DiT action head with SO(2)-equivariant layers, including equivariant projections, attention, state encoding, and action decoding.
- In simple terms, a rotated scene should lead to the same predicted skill with the action rotated in the matching direction.

## Results
- On LIBERO with relative control, EquiVLA reports 92.6% average success, compared with 78.1% for GR00T N1.5, 91.0% for GR00T N1.5 + EquiActor, 86.0% for pi0, 76.8% for OpenVLA, and 65.6% for SmolVLA.
- On LIBERO with absolute control, EquiVLA reports 76.1% average success, compared with 62.6% for GR00T N1.5 and 73.6% for GR00T N1.5 + EquiActor.
- On CALVIN ABCD→D using single-frame observations, EquiVLA reports an average sequence length of 4.03 out of 5, compared with 3.45 for GR00T N1.5 and 3.89 for GR00T N1.5 + EquiActor.
- On CALVIN task-position success, EquiVLA improves Task 5 from 48.5% to 64.3% over GR00T N1.5, a gain of 15.8 percentage points.
- On five Mobile ALOHA real-robot tasks with 150 demonstrations per task and 20 trials per task, EquiVLA reports 72% average success, compared with 54% for GR00T N1.5.

## Link
- [https://arxiv.org/abs/2606.19784v1](https://arxiv.org/abs/2606.19784v1)
