---
source: arxiv
url: https://arxiv.org/abs/2606.30456v1
published_at: '2026-06-29T15:23:34'
authors:
- Mathilde Hochedel
- Marc Lalonde
topics:
- vision-language-action
- openvla
- real-robot-deployment
- ur5e
- robot-data-pipeline
- imitation-learning
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform

## Summary
This paper is a real-robot case study of OpenVLA and OpenVLA-OFT on a UR5e manipulator. Its main finding is that closed-loop VLA deployment fails or becomes unstable when action semantics, timing, preprocessing, frames, and data coverage are misaligned.

## Problem
- The paper asks whether open VLA models can move from benchmark settings to a local UR5e robot with reproducible data collection, fine-tuning, and deployment.
- This matters because VLA policies depend on the full perception-action loop; small mismatches in images, action units, coordinate frames, or timing can change the robot's physical behavior.
- The excerpt reports limited guidance for adapting open VLA models to new robot setups, especially collaborative industrial arms.

## Approach
- The authors build a UR5e setup with a Robotiq 2F-140 gripper, an Intel RealSense D435 third-person camera, and a wrist-mounted Logitech webcam.
- They collect real-robot demonstrations, convert the data into an RLDS-compatible format, and prepare fine-tuning and inference paths for OpenVLA and OpenVLA-OFT.
- OpenVLA maps images and language instructions to discretized robot action tokens; each action dimension is quantized into 256 bins and decoded through the language-model token path.
- OpenVLA-OFT is studied as a follow-on model with continuous action regression, parallel action decoding, action chunking, and optional wrist-camera and robot-state inputs.
- The deployment uses a client-server setup: the robot client sends camera inputs to a GPU server, receives predicted actions, and executes them through UR RTDE.

## Results
- The excerpt gives no quantitative task success rate, no rollout count, and no benchmark table for the authors' UR5e trials.
- Original OpenVLA inference ran at about 3 Hz on an NVIDIA A100 in their setup, making model inference the main speed limit rather than network transfer.
- Fine-tuning used 4 NVIDIA A100 GPUs; local development and simulation used an RTX 5080 with 16 GB of VRAM on Ubuntu 22.04.
- The authors report a consistent gap between offline indicators and unstable closed-loop behavior on the physical UR5e system.
- The strongest concrete result is the delivered engineering pipeline: real-robot data acquisition, RLDS conversion, VLA fine-tuning, inference deployment, and action/control validation on the UR5e platform.
- As background for model choice, the paper cites OpenVLA-OFT results from its source work, including speedups up to 26x from parallel decoding and action chunking; this is not presented as a new UR5e result from this project.

## Link
- [https://arxiv.org/abs/2606.30456v1](https://arxiv.org/abs/2606.30456v1)
