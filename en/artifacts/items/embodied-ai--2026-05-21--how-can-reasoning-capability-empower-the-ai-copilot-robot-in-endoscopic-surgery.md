---
source: arxiv
url: https://arxiv.org/abs/2605.22322v1
published_at: '2026-05-21T11:08:59'
authors:
- Guankun Wang
- Long Bai
- Hongliang Ren
topics:
- vision-language-action
- surgical-robotics
- endoscopic-surgery
- robot-copilot
- uncertainty-fusion
- deformable-tissue
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# How can reasoning capability empower the AI copilot robot in endoscopic surgery

## Summary
This paper argues that reasoning-enabled vision-language-action models can make endoscopic surgical copilot robots safer and more useful under surgeon supervision. It is a concept paper, with architecture proposals and clinical use cases rather than new experiments.

## Problem
- Endoscopic surgery has restricted tool motion, unstable or limited visual views, deformable tissue, bleeding, smoke, and large patient-to-patient variation.
- Current robotic assistants can help with dexterity and camera stability, but they still struggle with tissue state estimation, multi-instrument coordination, and safe action choice during uncertain events.
- The problem matters because a surgical copilot at LoA 2-3 must support precise subtasks such as traction, dissection, and hemostasis without taking task-level authority away from the surgeon.

## Approach
- The paper defines the AI copilot as a Level of Autonomy 2-3 system: it can generate options, monitor the scene, and execute bounded low-level maneuvers, while the surgeon keeps task-level selection, override, and final authority.
- The proposed mechanism uses a reasoning VLA model to read surgical video and language intent, then output low-level motion goals and grounding information for tools and tissue.
- A second VLA-style motion policy maps those goals, plus multimodal signals, into kinematic changes such as position, orientation, and velocity.
- The copilot fuses endoscopic video with CT/MRI priors, EUS, OCT, shape sensing, EM tracking, and force proxies, then weights these inputs by uncertainty.
- Chain-of-thought-style reasoning is proposed for anticipating tissue deformation, choosing safer action constraints, coordinating multiple instruments, and deciding when deeper inference is needed.

## Results
- The paper reports no new quantitative experiments, benchmarks, success rates, latency measurements, or clinical trial outcomes.
- Its main concrete claim is an LoA 2-3 surgical copilot design tied to 4 Degree-of-Autonomy functions: Generate, Execute, Monitor, and Select.
- It claims reasoning can improve specific subtasks, including countertraction-dissection coordination, bleeding point localization, hemostasis, and response to smoke or blood occlusion.
- It proposes a latency target of sub-second response for real surgical use, but gives no measured runtime.
- It calls for future benchmarks that connect fusion quality, uncertainty calibration, and safety-critical outcomes, with per-case time, resource, and energy reporting.

## Link
- [https://arxiv.org/abs/2605.22322v1](https://arxiv.org/abs/2605.22322v1)
