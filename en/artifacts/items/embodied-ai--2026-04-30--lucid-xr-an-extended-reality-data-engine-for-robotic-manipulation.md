---
source: arxiv
url: https://arxiv.org/abs/2605.00244v1
published_at: '2026-04-30T21:25:20'
authors:
- Yajvan Ravan
- Adam Rashid
- Alan Yu
- Kai McClennen
- Gio Huh
- Kevin Yang
- Zhutian Yang
- Qinxi Yu
- Xiaolong Wang
- Phillip Isola
- Ge Yang
topics:
- robot-data-scaling
- sim2real
- dexterous-manipulation
- synthetic-data
- xr-teleoperation
- vision-language-action
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Lucid-XR: An Extended-Reality Data Engine for Robotic Manipulation

## Summary
Lucid-XR is an XR-based synthetic data system for robot manipulation that collects human demonstrations in browser-based MuJoCo simulation, then turns them into realistic multi-view training images. The paper claims policies trained only on this data can transfer to real robot pick-and-place settings and handle visual changes better than policies trained on real teleoperation data.

## Problem
- Robot manipulation policies need diverse contact-rich data, but real teleoperation is slow because each trial needs manual reset, safety checks, and physical setup.
- Browser or cloud VR setups can add latency, which hurts dexterous tasks with deformable objects, particles, tight contact, or fast motion.
- Synthetic demonstrations in plain 3D scenes do not train vision policies well unless the visual data covers clutter, lighting, camera pose, and object appearance.

## Approach
- Lucid-XR runs MuJoCo inside the XR headset browser through WebAssembly, with rendering through WebGL and web-XR input for hands and controllers.
- Users collect demonstrations in virtual scenes; the system records SE(3) mocap poses at 25 Hz and can reset scenes with one button.
- Human hand or controller motion is retargeted to robot grippers or dexterous hands using MuJoCo inverse kinematics and user-defined bindings between mocap sites and robot parts.
- A generative image pipeline uses simulation masks, depth, camera poses, and text prompts to convert simple virtual demonstrations into realistic multi-view images.
- Extra data comes from changing camera views after collection and warping trajectories to move objects, robots, and initial states.

## Results
- The browser-based simulator runs at 90 fps on Apple Vision Pro, records data at 25 fps, and reports under 12 ms per simulation step in the tested setup.
- In 30-minute collection sessions across 3 tasks, participants gathered about 2x more demonstrations in Lucid-XR than with real-world teleoperation.
- With augmentation, the effective Lucid-XR dataset size reached about 5x the real-world teleoperation baseline.
- On a kitchen clearing evaluation with unseen real-life meshes, ACT scored 100% in the base environment, 0% in low clutter, and 0% in high clutter plus noise; ACT + LucidSim scored 100%, 90%, and 25% on the same settings.
- Sim-to-real tests used 10, 20, and 30 minutes of Lucid-XR data versus matched real teleoperation data; the paper reports comparable real-robot pick-and-place performance, but the excerpt does not give the exact success rates from Figure 11.
- The paper reports zero-shot transfer to unseen, cluttered, and poorly lit evaluation environments after training only on Lucid-XR synthetic data, with examples covering block stacking, pouring particles, ball sorting, knot tying, kitchen clearing, and mug-tree placement.

## Link
- [https://arxiv.org/abs/2605.00244v1](https://arxiv.org/abs/2605.00244v1)
