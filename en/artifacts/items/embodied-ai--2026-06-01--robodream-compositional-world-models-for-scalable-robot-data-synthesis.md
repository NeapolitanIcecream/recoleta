---
source: arxiv
url: https://arxiv.org/abs/2606.02577v1
published_at: '2026-06-01T17:59:38'
authors:
- Junjie Ye
- Rong Xue
- Basile Van Hoorick
- Runhao Li
- Harshitha Rajaprakash
- Pavel Tokmakov
- Muhammad Zubair Irshad
- Vitor Guizilini
- Yue Wang
topics:
- robot-world-model
- synthetic-robot-data
- video-diffusion
- sim2real
- robot-data-scaling
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# RoboDream: Compositional World Models for Scalable Robot Data Synthesis

## Summary
RoboDream generates robot training videos by fixing the robot motion first, then adding target objects and scenes with a video diffusion model. The paper claims this synthetic data improves real robot policy success while cutting teleoperation time.

## Problem
- Robot imitation learning needs many demonstrations, and real teleoperation is slow because each trial needs object setup, resets, and human operation.
- Existing video generation methods can change appearance, but full generated robot videos may contain wrong robot shapes or infeasible motion, which can hurt policies on hardware.
- Prior motion-anchored generation such as AnchorDream still needs task- or environment-specific fine-tuning, which limits use on new objects, scenes, and camera views.

## Approach
- RoboDream conditions a video diffusion transformer on a rendered robot-only trajectory, a scene prior image, an object prior image, the language instruction, and the global robot trajectory.
- The rendered robot video gives a pixel-level motion anchor, so the generated demo keeps the robot kinematics tied to a feasible trajectory.
- The scene prior is encoded with the video latent input, while object-prior tokens enter self-attention so the model can place task objects into the generated video.
- Training priors are built automatically from DROID episodes: a vision-language model identifies task objects, Grounded-SAM segments them, and OmniPaint removes them to create clean scene backgrounds.
- Deployment has two modes: retrieval and rebirth reuses similar DROID trajectories in new contexts; prop-free teleoperation records motions without physical objects and adds objects afterward.

## Results
- The model is fine-tuned from Cosmos-Predict2 2B on about 40k DROID episodes with camera calibration, using 2 nodes of 8 NVIDIA A100 GPUs for one week.
- In real-world evaluation over 4 manipulation tasks with 20 rollouts per policy, Gen-Mix reached 62.5% average success, compared with 36.3% for Real-50, 45.0% for Orig-Mix, 15.0% for Gen-100, and 0% for Orig-100.
- Task-level Gen-Mix success rates were 65% for Put Cube into Cup, 55% for Put Marker into Bowl, 35% for Remove Marker from Bowl, and 95% for Wipe Table with Towel.
- Prop-free collection took 55 minutes for 50 trajectories, compared with about 2 hours for 50 real teleoperation episodes, about 2.2x faster; its policy success was 32.5% average versus 36.3% for Real-50.
- Scaling generated data mixed with Real-50 improved average success from 36.3% to 62.5% with Mix-100, 72.5% with Mix-200, and 73.75% with Mix-300 and Mix-400.
- The paper reports zero-shot generation with unseen objects, unseen scenes, and new viewpoints, controlled by changing object priors, scene priors, and rendered camera views.

## Link
- [https://arxiv.org/abs/2606.02577v1](https://arxiv.org/abs/2606.02577v1)
