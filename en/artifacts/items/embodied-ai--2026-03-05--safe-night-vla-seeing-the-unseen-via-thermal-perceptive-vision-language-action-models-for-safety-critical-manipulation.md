---
source: arxiv
url: http://arxiv.org/abs/2603.05754v1
published_at: '2026-03-05T23:26:44'
authors:
- Dian Yu
- Qingchuan Zhou
- Bingkun Huang
- Majid Khadiv
- Zewen Yang
topics:
- vision-language-action
- thermal-perception
- safe-robotics
- multimodal-manipulation
- control-barrier-functions
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Safe-Night VLA: Seeing the Unseen via Thermal-Perceptive Vision-Language-Action Models for Safety-Critical Manipulation

## Summary
This paper proposes Safe-Night VLA, which integrates thermal infrared perception into a pre-trained vision-language-action model and adds a control barrier function safety filter during execution for safety-critical manipulation tasks. Its core value is enabling robots to use "unseen" thermal information for more robust and constrained manipulation under low light, occlusion, mirror deception, and out-of-distribution scenarios.

## Problem
- Existing VLA models mainly rely on RGB and cannot directly perceive **invisible physical states** such as temperature and buried targets, so they are prone to failure in thermal-related or occluded tasks.
- End-to-end generative policies lack **runtime safety constraints**, and may output dangerous actions in OOD scenarios, near obstacles, or close to workspace boundaries.
- This matters because real-world robot deployment often occurs in **low-light, unstructured environments with optical illusions and unknown disturbances**, where robots must both understand the task and avoid collisions.

## Approach
- The framework is built on **GR00T-N1.5-3B**, using **RGB, LWIR thermal, and depth** as three separate image-token inputs to a frozen vision-language backbone; both thermal and depth maps are converted into 3-channel pseudocolor so the RGB pre-trained encoder can be reused.
- It adopts **parameter-efficient adaptation**: the vision encoder and language model are frozen, and only the action head (VLM projector + 16-layer DiT) is trained, allowing the model to learn thermal-aware manipulation while preserving its original semantic capabilities.
- **Asymmetric data augmentation** is used to reduce dependence on RGB: during training, only RGB receives stronger brightness, color jitter, noise, and cropping perturbations, encouraging the policy to rely more on more robust modalities such as thermal and depth.
- At the execution layer, high-level action intent is decoupled from low-level safety: the VLA first outputs 6DoF end-effector pose increments and gripper commands, then a **CBF-QP safety filter** solves in joint space for the safest action closest to the desired one while satisfying collision constraints and joint limits.
- The method is validated through three physical evaluation scenarios: **temperature-conditioned manipulation**, **buried thermal target localization**, and **mirror reflection disambiguation**, while also testing normal lighting vs. dim/night conditions and whether the safety filter is enabled.

## Results
- Data and setup: the authors collected **600** demonstrations on a **Franka Panda**, each with about **200** state-action pairs; training ran for **5,000 steps**; they compared four independently trained models: **RGB-Only / RGB-D / RGB-T / Ours(RGB-T-D)**.
- **Temperature-conditioned manipulation (50 trials)**: under normal light without safety filtering, RGB-Only achieved **32%**, RGB-D **24%**, RGB-T **78%**, and Ours **72%**; under normal light with filtering, RGB-T reached **86%** and Ours **82%**. Under **dim/night + safety**, Ours reached **64%**, outperforming RGB-T at **22%**, RGB-D at **12%**, and RGB-Only at **0%**.
- **Buried thermal target localization (50 trials)**: under normal light with filtering, Ours achieved **78%**, higher than RGB-T at **66%**, RGB-D at **24%**, and RGB-Only at **16%**; under **dim/night + safety**, Ours achieved **72%**, above RGB-T at **48%**, while RGB-D and RGB-Only almost completely failed (**2%** / **0%**).
- **Mirror reflection disambiguation (20 trials per subtask)**: under normal light with filtering, Mirror Rejection Success was RGB-Only **12/20**, RGB-D **11/20**, RGB-T **19/20**, and Ours **15/20**; under **dim/night + safety**, Ours reached **17/20**, above RGB-T at **15/20**, RGB-Only at **13/20**, and RGB-D at **11/20**.
- In the **single-box subtask** under **dim/night + safety**, Ours achieved **18/20**, slightly above RGB-T at **17/20**, and clearly above RGB-Only / RGB-D at **9/20 / 9/20**, indicating that depth provides additional geometric stability under low light.
- Overall claim: the thermal modality is critical for "hot/cold discrimination" and "buried target localization," and the CBF safety filter can further reduce execution-level failures; based on this, the authors argue that foundation models can effectively leverage **non-visible physical modalities** for more robust safety-critical manipulation.

## Link
- [http://arxiv.org/abs/2603.05754v1](http://arxiv.org/abs/2603.05754v1)
