---
kind: trend
trend_doc_id: 87
granularity: day
period_start: '2026-04-09T00:00:00'
period_end: '2026-04-10T00:00:00'
topics:
- embodied-ai
- world-models
- humanoid-control
- navigation
- dexterous-manipulation
- articulation
run_id: materialize-outputs
aliases:
- recoleta-trend-87
tags:
- recoleta/trend
- topic/embodied-ai
- topic/world-models
- topic/humanoid-control
- topic/navigation
- topic/dexterous-manipulation
- topic/articulation
language_code: en
pass_output_id: 44
pass_kind: trend_synthesis
---

# Embodied research is getting more explicit about body, future state, and object structure

## Overview
April 9 centers on embodied models that make structure explicit. The clearest pattern is morphology, future state, and object kinematics being written into the learning problem itself. WorldMAP provides the strongest hard numbers. HEX, QWM, ViVa, BLaDA, and DailyArt add breadth across humanoids, quadrupeds, navigation, dexterous grasping, and articulated objects.

## Clusters

### Embodiment-aware models
Work on control now puts body structure into the model, not just into the hardware description. QWM conditions a quadruped world model on explicit morphology features from the robot's USD file, with claims of zero-shot deployment on unseen quadrupeds inside the trained family. HEX does something similar for humanoids at the policy level: it maps different robots into shared body-part slots and predicts short-horizon future proprioception before acting. Both papers target cross-embodiment transfer by making morphology a first-class input. The evidence is promising, but neither excerpt includes the full numeric gains needed to judge how far the transfer holds under harder body changes.

#### Evidence
- [Toward Hardware-Agnostic Quadrupedal World Models via Morphology Conditioning](../Inbox/2026-04-09--toward-hardware-agnostic-quadrupedal-world-models-via-morphology-conditioning.md): Summary states morphology-conditioned quadrupedal world model, zero-shot deployment claims, and distribution-bounded limitation.
- [HEX: Humanoid-Aligned Experts for Cross-Embodiment Whole-Body Manipulation](../Inbox/2026-04-09--hex-humanoid-aligned-experts-for-cross-embodiment-whole-body-manipulation.md): Summary describes shared humanoid body-part state representation and future proprioception prediction for cross-embodiment manipulation.

### Generative models as supervision and value estimators
Generated futures are being used as training signals and value signals, not only as rollout media. WorldMAP uses a teacher built on generated future views to create pseudo-labeled navigation paths, then trains a smaller student that runs alone at inference time. The numbers are concrete: on Target-Bench it reports ADE 42.06 and FDE 38.87, beating Gemini-3-Pro on both. ViVa applies the same broad idea to reinforcement learning. It uses a video diffusion model to predict future proprioception and a scalar value, and the paper reports smoother task-progress tracking plus better real-world box assembly inside RECAP. This is a stronger evidence block than most of the day because WorldMAP includes benchmark numbers, while ViVa adds task-level qualitative behavior.

#### Evidence
- [WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models](../Inbox/2026-04-09--worldmap-bootstrapping-vision-language-navigation-trajectory-prediction-with-generative-world-models.md): Summary gives teacher-student design and Target-Bench metrics versus Gemini-3-Pro, Qwen3-VL-8B, and MindJourney.
- [ViVa: A Video-Generative Value Model for Robot Reinforcement Learning](../Inbox/2026-04-09--viva-a-video-generative-value-model-for-robot-reinforcement-learning.md): Summary explains video-generative value estimation and qualitative gains on box assembly, shirt folding, and toilet paper organization.

### Structured scene and object understanding for manipulation
Manipulation papers are spelling out intent in more executable forms. BLaDA parses open-vocabulary instructions into a structured sextuple, localizes functional contact regions in a 3D Gaussian Splatting scene, and maps them into wrist pose, finger commands, and force settings. DailyArt addresses a related perception bottleneck for articulated objects. It synthesizes an opened state from a single image, then estimates joints, axes, pivots, and motion ranges from the gap between closed and opened views. The common thread is explicit intermediate structure: contact constraints for dexterous action and kinematic structure for object interaction. Both excerpts claim strong results, but neither gives the final benchmark table in the available text.

#### Evidence
- [BLaDA: Bridging Language to Functional Dexterous Actions within 3DGS Fields](../Inbox/2026-04-09--blada-bridging-language-to-functional-dexterous-actions-within-3dgs-fields.md): Summary details language-to-constraint parsing, 3D functional localization, and finger-level execution.
- [DailyArt: Discovering Articulation from Single Static Images via Latent Dynamics](../Inbox/2026-04-09--dailyart-discovering-articulation-from-single-static-images-via-latent-dynamics.md): Summary describes synthesis-mediated articulation inference from a single image and joint estimation outputs.
