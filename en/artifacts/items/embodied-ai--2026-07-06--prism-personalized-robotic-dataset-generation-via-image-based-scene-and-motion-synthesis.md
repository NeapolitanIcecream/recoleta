---
source: arxiv
url: https://arxiv.org/abs/2607.04880v1
published_at: '2026-07-06T10:00:47'
authors:
- Dogyu Ko
- Haneul Kim
- Chanyoung Yeo
- Dowoon Lee
- Taeho Park
- Hyoseok Hwang
topics:
- robot-data-generation
- sim2real
- vision-language-action
- imitation-learning
- digital-cousins
- robot-manipulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# PRISM: Personalized Robotic Dataset Generation via Image-based Scene and Motion Synthesis

## Summary
PRISM generates robot training datasets from one target-scene image and a task instruction. It builds matched but varied simulated scenes, plans demonstrations, and uses visual randomization to adapt manipulation policies to the target environment.

## Problem
- Pretrained VLA policies can fail in a user's real scene because their training trajectories do not cover that exact environment.
- Teleoperation gives matched data but costs human time; generic simulation scales but may miss the target scene; digital twins can overfit to one scene instance.
- The paper targets low-cost data generation for personalized robot manipulation, which matters for adapting robot policies without collecting many real demonstrations.

## Approach
- PRISM detects objects from a single RGB-D image, uses Grounded-SAM for masks, and uses depth and camera intrinsics or estimates them with Depth Anything v2 and Perspective Fields when needed.
- It retrieves 3D assets by category with CLIP, ranks rendered asset matches with DINOv2 embeddings, and asks a VLM to select visually similar candidates.
- It builds digital cousin scenes that keep object categories, geometry, and spatial relations close to the target scene while varying asset instances, object poses, lighting, textures, and distractors.
- A VLM converts the natural-language instruction into primitive actions such as pick and place, then TAMP generates collision-free trajectories with grasp poses and joint paths.
- Motion-aware grasp selection prefers grasps aligned with canonical end-effector orientations, and trajectory-preserving visual randomization replays the same successful motion under different visual conditions.

## Results
- In sim-to-sim tests, each method generated 400 trajectories per task. On "Put milk in basket" with pi_0.5, PRISM scored 98.0% on LIBERO versus X-Sim 48.0% and RoboTwin 2.0 14.0%; on LIBERO-Plus it scored 67.6% versus 35.8% and 21.9%.
- On "Put wine bottle on cabinet" with pi_0.5, PRISM scored 98.0% on LIBERO versus X-Sim 82.0% and RoboTwin 2.0 16.0%; on LIBERO-Plus it scored 52.0%, below X-Sim's 54.5% and above RoboTwin 2.0's 3.3%.
- With Diffusion Policy, PRISM reached 95.0% in-domain, 94.0% on LIBERO, and 35.6% on LIBERO-Plus for "Put milk in basket"; X-Sim scored 84.0%, 80.0%, and 2.8%, and RoboTwin 2.0 scored 84.0%, 2.0%, and 33.7%.
- For "Put wine bottle on cabinet" with Diffusion Policy, PRISM scored 100.0% in-domain, 56.0% on LIBERO, and 28.8% on LIBERO-Plus; X-Sim scored 40.0%, 44.0%, and 0.6%, while RoboTwin 2.0 scored 78.0%, 34.0%, and 27.2%.
- In real-to-sim-to-real experiments, PRISM evaluated three real manipulation tasks with 10 trials per task and claims up to 100% success, with higher success than baseline-generated datasets; the excerpt does not provide the per-task numeric values from Figure 4.
- Ablations report PRISM-Cousin at 80.0% on the target environment and 80.0% on variant environments, while PRISM-Twin scored 100.0% on the target and 30.0% on variants. Motion-aware grasp selection improved pi_0.5 from 56.0% to 98.0% and Diffusion Policy from 52.0% to 56.0%.

## Link
- [https://arxiv.org/abs/2607.04880v1](https://arxiv.org/abs/2607.04880v1)
