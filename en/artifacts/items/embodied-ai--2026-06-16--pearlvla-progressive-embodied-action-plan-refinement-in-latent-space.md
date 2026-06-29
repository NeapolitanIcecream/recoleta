---
source: arxiv
url: https://arxiv.org/abs/2606.17924v1
published_at: '2026-06-16T13:38:03'
authors:
- Bochen Yang
- Lianlei Shan
topics:
- vision-language-action
- robot-foundation-model
- world-model
- latent-planning
- long-horizon-manipulation
- generalist-robot-policy
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# PearlVLA: Progressive Embodied Action-Plan Refinement in Latent Space

## Summary
PearlVLA adds latent planning rounds to an OpenVLA-style policy before decoding robot actions. It claims 98.7% average success on LIBERO, above the VLA baselines listed in the excerpt.

## Problem
- Direct VLA action decoding is fast, but it gives the policy little chance to revise a plan before acting.
- Text chains, pixel subgoals, and action-candidate search can improve planning, but they add latency or create a mismatch with continuous robot control.
- The problem matters for long-horizon manipulation because small early errors in grasping, motion direction, or task interpretation can cause later task failure.

## Approach
- The model starts with OpenVLA-7B and splits final meta-query tokens into fixed visual grounding tokens and writable latent plan tokens.
- Each refinement round maps the current latent plan into a world-query vector, asks a frozen UWM latent world model for an action-free future observation latent, and feeds that future back into the plan.
- A Future-Guided RefineNet writes a residual correction to the plan tokens. Larger early updates handle coarse task direction; smaller later updates tune the plan.
- After K refinement rounds, a lightweight action head decodes the final latent plan into an H-step continuous action chunk in parallel.
- A second training stage, CRG-PRL, samples M=8 residual edits from the same refinement state, scores their post-edit imagined futures with Robometer-4B, standardizes rewards within the group, and updates RefineNet with a PPO-style objective while keeping the deployed inference path deterministic.

## Results
- PearlVLA reports 98.7% average success on LIBERO across Spatial, Object, Goal, and Long suites.
- The excerpt lists strong LIBERO baselines: π0.5 at 97.5% average, VLANeXt at 97.4%, FLOWER at 96.9%, and UniVLA at 95.2%.
- The same table lists older regression or classification VLA baselines below that range: OpenVLA at 76.5%, WorldVLA at 79.1%, CoT-VLA at 83.9%, and NORA at 87.9% average success.
- LIBERO uses 4 suites with 10 tasks each and 500 expert demonstrations per suite; the reported metric is task success rate.
- The frozen latent world model is UWM post-trained for 50K steps on LIBERO-90 action-free video, disjoint from the 4 evaluation suites.
- The excerpt states K=4 refinement rounds for the main LIBERO model and M=8 branches per state for CRG-PRL reward grouping.

## Link
- [https://arxiv.org/abs/2606.17924v1](https://arxiv.org/abs/2606.17924v1)
