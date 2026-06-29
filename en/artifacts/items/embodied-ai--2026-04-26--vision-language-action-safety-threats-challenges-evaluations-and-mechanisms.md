---
source: arxiv
url: http://arxiv.org/abs/2604.23775v1
published_at: '2026-04-26T15:58:19'
authors:
- Qi Li
- Bo Yin
- Weiqi Huang
- Ruhao Liu
- Bojun Zou
- Runpeng Yu
- Jingwen Ye
- Weihao Yu
- Xinchao Wang
topics:
- vision-language-action
- robot-safety
- adversarial-robustness
- survey-paper
- embodied-ai
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms

## Summary
This paper is a survey of safety risks, defenses, evaluation methods, and deployment issues for vision-language-action (VLA) models in robotics. Its main contribution is a unified map of the field organized by when attacks happen and when defenses are applied.

## Problem
- VLA models connect perception, language, and robot control in one policy, so failures can cause physical harm rather than only bad text output.
- Their attack surface spans images, language prompts, proprioceptive state, training data, and long action sequences, which makes safety work harder than in text-only models or classical modular robotics.
- Prior work is split across adversarial ML, robot learning, alignment, and autonomous systems, with no single overview that ties threats, defenses, benchmarks, and deployment risks together.

## Approach
- The paper defines VLA safety as a distinct topic from LLM safety and classical robot safety, then reviews the standard VLA setup: visual encoder, language backbone, action decoder, imitation-learning training, and deployment-time inference.
- It organizes the literature along two timing axes: **attack timing** (training-time vs inference-time) and **defense timing** (training-time vs inference-time).
- Under that taxonomy, it surveys training-time threats such as data poisoning and backdoors, and inference-time threats such as adversarial patches, cross-modal perturbations, jailbreaks, and freezing attacks.
- It also reviews defenses, safety benchmarks and metrics, and deployment issues across six application domains, then lists open problems such as certified robustness for trajectories, physically realizable defenses, safety-aware training, runtime safety architectures, and standard evaluation.

## Results
- This is a survey paper, so the excerpt does not report new experimental benchmark numbers or a new model accuracy result.
- It claims to be the **first comprehensive survey** focused on VLA safety across attacks, defenses, evaluation, and deployment.
- It introduces a **2-axis taxonomy**: attack timing has **2 categories** (training-time, inference-time) and defense timing has **2 categories** (training-time, inference-time).
- It states that deployment analysis covers **6 major domains**.
- The background section summarizes the scale of representative VLA systems that motivate the safety review: **RT-1** trained on **130,000+** real robot demonstrations from **13 robots** over **17 months**; **Open X-Embodiment** contains about **1 million** demonstrations across **22 embodiments** from **21 institutions**; **Octo** uses about **800,000** trajectories; **OpenVLA** is a **7B** model fine-tuned on **970k** episodes; **RT-2** builds on a **55B** vision-language model.

## Link
- [http://arxiv.org/abs/2604.23775v1](http://arxiv.org/abs/2604.23775v1)
