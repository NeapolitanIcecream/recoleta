---
source: arxiv
url: https://arxiv.org/abs/2606.17598v1
published_at: '2026-06-16T07:04:13'
authors:
- Xingyuming Liu
- Ruichun Ma
- Heyu Guo
- Qixiu Li
- Qingwen Yang
- Lin Luo
- Shiqi Jiang
- Chenren Xu
- Jiaolong Yang
- Baining Guo
topics:
- vision-language-action
- multimodal-sensing
- dexterous-manipulation
- robot-data-scaling
- sensor-selection
- simulated-sensor-data
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# MuseVLA: An Adaptive Multimodal Sensing Vision-Language-Action Model for Robotic Manipulation

## Summary
MuseVLA is a VLA model for dexterous manipulation that selects thermal, audio, mmWave, or RGB sensing from the task and scene. It turns the selected sensor reading into an RGB-like grounded sensor image so one vision encoder can combine it with language and robot state.

## Problem
- RGB-only VLA policies miss physical cues such as temperature, sound source location, and radar response, which are needed for tasks like picking the hot drink or finding an object hidden in a box.
- Multi-sensor robot data is costly: the paper collects 720 real teleoperated episodes, while its synthesis pipeline adds 9.6K episodes and 1.05M frames from RGB-only datasets.
- Fixed sensor fusion processes sensors that may be irrelevant and ties the policy to a fixed sensor set.

## Approach
- The model first reads the instruction and RGB image, then generates a sensor token such as <Thermal>, <Acoustic>, <mmWave>, or <None>, plus a target description such as the mugs.
- A segmentation model, SAM3, masks the described object, and the selected sensor heatmap is overlaid on that mask to create a grounded sensor image.
- The grounded sensor image is fed back into a PaliGemma-2/VITRA-based VLM with a diffusion transformer action expert to predict action chunks.
- Training combines cross-entropy losses for sensor and target generation with a diffusion MSE action loss; the action loss weight is 1e-2.
- The synthesis pipeline injects sensor-related words into RGB robot episodes, uses GPT-5.2 for target descriptions, segments the target, and overlays color-coded masks to imitate sensor cues.

## Results
- On real dexterous-hand tasks using thermal, acoustic, and mmWave sensing, MuseVLA with synthesized pretraining reaches 80.6% average success on seen tasks: 87.5% thermal, 70.8% acoustic, and 83.3% mmWave.
- In the direct task comparison table without synthesized pretraining, MuseVLA reaches 76.4% average success versus 20.8% for π0-RGB, 19.4% for π0.5-RGB, 27.8% for π0-Raw, and 33.3% for MuseVLA-Raw.
- MuseVLA reports 95.8% sensing-stage success, 77.8% manipulation-stage success, and a 0.868 task score in Table 1.
- Synthesized pretraining raises unseen-task success to 66.7% average, compared with 27.1% for MuseVLA without pretraining and 25.0% for MuseVLA-Raw.
- Adaptive sensor selection reaches 100% sensor-token accuracy and 82.0% target-description accuracy on unseen tasks after pretraining; PaliGemma-2 alone scores 0% and 9.5% on the same metrics.
- The real training set contains 720 demonstrations across 10 sub-task instructions, 7 objects, and 3 sensing modalities; the synthesized set contains 9.6K episodes, 1.05M frames, and over 1000 objects.

## Link
- [https://arxiv.org/abs/2606.17598v1](https://arxiv.org/abs/2606.17598v1)
