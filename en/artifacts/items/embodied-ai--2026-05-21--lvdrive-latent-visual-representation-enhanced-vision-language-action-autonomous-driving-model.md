---
source: arxiv
url: https://arxiv.org/abs/2605.22089v1
published_at: '2026-05-21T07:31:49'
authors:
- Xiaodong Mei
- Diankun Zhang
- Hongwei Xie
- Guang Chen
- Hangjun Ye
- Dan Xu
topics:
- vision-language-action
- autonomous-driving
- latent-world-model
- trajectory-planning
- closed-loop-evaluation
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# LVDrive: Latent Visual Representation Enhanced Vision-Language-Action Autonomous Driving Model

## Summary
LVDrive is a VLA autonomous driving model that predicts future scene features in latent space and uses them to refine the planned trajectory. On Bench2Drive, it reports the best Driving Score and Success Rate among the listed camera-only driving methods.

## Problem
- Existing VLA driving models mainly learn from sparse action labels, so they get limited supervision for scene dynamics and future hazards.
- Image-reconstruction world models add dense supervision, but pixel generation can spend model capacity on texture instead of planning-relevant semantics.
- Autoregressive future-frame or action-token generation adds inference cost, which matters for closed-loop driving.

## Approach
- LVDrive adds a future scene prediction task to the VLA model, using latent visual features as supervision instead of reconstructed RGB frames.
- A frozen pretrained vision model supplies target future visual embeddings; the model predicts 6 future timesteps, with 256 latent tokens per future frame.
- Future scene tokens and the planning token are produced in one forward pass in a shared continuous embedding space.
- The planner first decodes a coarse trajectory from the planning embedding, then a transformer refiner uses cross-attention over predicted future scene embeddings to produce the final trajectory.
- Training uses visual latent prediction loss, coarse and refined trajectory losses, structured-view feature loss, and cross-entropy for the placeholder token sequence.

## Results
- On Bench2Drive closed-loop evaluation, LVDrive reports 80.71 Driving Score and 58.26% Success Rate.
- Against the strongest listed image-reconstruction world-model baseline, UniDrive-WM-AR+Diff, LVDrive improves Driving Score from 79.31 to 80.71 and Success Rate from 56.42% to 58.26%.
- Against ORION, the VLA baseline it builds on, LVDrive improves Driving Score from 77.74 to 80.71 and Success Rate from 54.62% to 58.26%.
- Against the strongest listed traditional end-to-end method, Raw2Drive, LVDrive improves Driving Score from 71.36 to 80.71 and Success Rate from 50.24% to 58.26%.
- Open-loop Avg. L2 is 0.63, matching UniDrive-WM-AR+Diff at 0.63 and better than ORION at 0.68; DriveMoE has a lower listed Avg. L2 at 0.38.
- LVDrive uses imitation learning with camera input only; it reports Efficiency 155.77 and Comfortness 14.34 on Bench2Drive.

## Link
- [https://arxiv.org/abs/2605.22089v1](https://arxiv.org/abs/2605.22089v1)
