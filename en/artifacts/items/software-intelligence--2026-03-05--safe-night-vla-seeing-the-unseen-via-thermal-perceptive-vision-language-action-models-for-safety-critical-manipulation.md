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
- robot-safety
- control-barrier-functions
- multimodal-robotics
relevance_score: 0.45
run_id: materialize-outputs
language_code: en
---

# Safe-Night VLA: Seeing the Unseen via Thermal-Perceptive Vision-Language-Action Models for Safety-Critical Manipulation

## Summary
Safe-Night VLA integrates thermal infrared perception and runtime safety constraints into a vision-language-action robot model, enabling robots to use temperature information that RGB cannot see to perform more robust manipulation. It focuses on solving semantic perception and safe execution problems in nighttime, occluded, mirror-deceptive, and out-of-distribution scenarios.

## Problem
- Existing VLA models mainly rely on RGB and cannot directly perceive temperature, buried targets, and other **invisible physical states**, so they are prone to misjudgment in safety-critical manipulation.
- End-to-end generative policies lack **explicit runtime safety guarantees**, and may generate collision-prone actions in out-of-distribution scenarios, around obstacles, or near workspace boundaries.
- This matters because when real robots are deployed in unstructured environments, they must both understand physical semantics such as “pick up the hot bottle” and avoid dangerous execution caused by hallucinations or noise.

## Approach
- Add **LWIR thermal imaging, RGB, and depth** as three-modal inputs on top of a pre-trained GR00T-N1.5-3B/frozen VLM backbone, converting thermal maps and depth maps into pseudo-color images and feeding them directly into the original visual encoder.
- Train only the **action head** (projection layer and DiT policy head), without modifying the frozen vision-language backbone, using a parameter-efficient method to align thermal semantics with the existing foundation model representations.
- Use **asymmetric augmentation** to strongly perturb only RGB, forcing the policy to rely more on thermal/depth cues that are more stable under low light, rather than fragile visible-light textures.
- Add a **QP safety filter based on control barrier functions (CBF)** during execution: convert the end-effector pose increments produced by the VLA into safe joint actions that satisfy collision constraints and joint limits; simply put, the model proposes an action and the safety layer intercepts dangerous parts in real time.
- Design three diagnostic scenarios to evaluate this mechanism: temperature-conditioned manipulation, buried thermal target localization, and specular reflection disambiguation, and validate them on a real Franka manipulator.

## Results
- **Temperature-conditioned manipulation (50 trials)**: under normal lighting and without safety filtering, RGB-T performs best at **78%**, while Safe-Night VLA reaches **72%**, both significantly higher than RGB-Only at **32%** and RGB-D at **24%**; under normal lighting + safety filtering, RGB-T reaches **86%** and Safe-Night VLA **82%**.
- **Temperature-conditioned manipulation (low light/night, 50 trials)**: without safety filtering, Safe-Night VLA reaches **56%**, clearly outperforming RGB-Only at **0%**, RGB-D at **10%**, and RGB-T at **10%**; with safety filtering it rises to **64%**, compared with RGB-Only **0%**, RGB-D **12%**, and RGB-T **22%**.
- **Buried thermal target localization (50 trials)**: under normal lighting + safety filtering, Safe-Night VLA achieves **78%**, higher than RGB-T **66%**, RGB-D **24%**, and RGB-Only **16%**; under low light/night + safety filtering it reaches **72%**, still higher than RGB-T **48%**, RGB-D **2%**, and RGB-Only **0%**.
- **Mirror/reflection disambiguation (single-box success, 20 trials)**: under low light/night + safety filtering, Safe-Night VLA achieves **18/20**, RGB-T **17/20**, while RGB-Only and RGB-D both achieve **9/20**.
- **Mirror rejection success (20 trials)**: under normal lighting + safety filtering, RGB-T is highest at **19/20**, Safe-Night VLA reaches **15/20**, clearly outperforming RGB-Only **12/20** and RGB-D **11/20**; under low light/night + safety filtering, Safe-Night VLA is highest at **17/20**, exceeding RGB-T **15/20**, RGB-Only **13/20**, and RGB-D **11/20**.
- The paper’s core claim is that **thermal perception significantly improves semantic localization ability, the CBF safety layer improves execution reliability, and the combination of the two is most robust under low-light and out-of-distribution conditions**; it also shows that a frozen RGB-pretrained foundation model can effectively leverage non-visible-light modalities.

## Link
- [http://arxiv.org/abs/2603.05754v1](http://arxiv.org/abs/2603.05754v1)
