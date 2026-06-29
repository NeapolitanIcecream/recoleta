---
source: arxiv
url: https://arxiv.org/abs/2606.04825v1
published_at: '2026-06-03T12:48:17'
authors:
- Amirhosein Alian
- Yongqiang Zhao
- Shiyi Gu
- Xuyang Zhang
- Zhuo Chen
- Christopher E. Mower
- Haitham Bou-Ammar
- Shan Luo
topics:
- vision-language-action
- tactile-sensing
- haptic-teleoperation
- robot-manipulation-dataset
- imitation-learning
- contact-rich-manipulation
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning

## Summary
HapTile is a 1,726-demo robot manipulation dataset that pairs language, RGB video, fingertip tactile images, robot state, actions, and operator haptic feedback. It targets contact-rich tasks where vision-only policies miss slip, force, and contact geometry.

## Problem
- VLA datasets often store RGB, language, and actions, while contact-rich manipulation also needs touch signals for slip, force, and occluded contacts.
- Existing tactile datasets often lack task diversity, language used as policy input, action trajectories, or haptic feedback during teleoperation.
- This matters for everyday robot tasks such as wiping, folding, pouring, peg insertion, and bottle turning, where small contact errors can break the task.

## Approach
- The authors collect 1,726 demonstrations across 38 tasks, 9 skills, and 9 human operators on a UR5e with a Robotiq 2F-85 gripper.
- Each episode stores language instructions, third-person RGB, wrist RGB, left and right fingertip tactile images, robot proprioception, 7D end-effector delta actions, timestamps, and haptic feedback state at 15 Hz.
- The fingertip sensors use internal RGB cameras to view deformation in a silicone layer. Lucas-Kanade optical flow tracks marker displacement, and the system converts marker motion into a contact-motion score.
- The teleoperation controller sends discrete vibration feedback to the operator based on tactile marker motion, so the demonstrator can feel contact during data collection.
- The benchmark trains Diffusion Policy and π0 with three input settings: vision-only, vision plus raw tactile images, and vision plus tactile marker features.

## Results
- Dataset scale: 1,726 demonstrations, 38 tasks, 9 skills, 750.33 minutes of interaction, sampled at 15 Hz.
- Task duration examples: peg insertion averages 54.21 s, while moving a golf ball averages 12.42 s.
- On peg insertion with π0, success rises from 0% with vision-only to 90% with vision plus raw tactile images, measured over 10 trials.
- On whiteboard wiping with π0, success rises from 50% with vision-only to 100% with vision plus tactile marker features.
- On turning a bottle upright with Diffusion Policy, the best result is 90% with vision plus tactile marker features, compared with 80% for vision-only.
- Tactile input does not always help: Diffusion Policy drops on pouring from 50% with vision-only to 20% with tactile marker features, and π0 drops on pouring from 30% with vision-only to 0% with tactile marker features.

## Link
- [https://arxiv.org/abs/2606.04825v1](https://arxiv.org/abs/2606.04825v1)
