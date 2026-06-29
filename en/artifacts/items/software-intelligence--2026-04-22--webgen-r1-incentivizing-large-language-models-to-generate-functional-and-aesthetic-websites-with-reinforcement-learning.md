---
source: arxiv
url: http://arxiv.org/abs/2604.20398v1
published_at: '2026-04-22T10:04:46'
authors:
- Juyong Jiang
- Chenglin Cai
- Chansung Park
- Jiasi Shen
- Sunghun Kim
- Jianguo Li
- Yue Wang
topics:
- website-generation
- reinforcement-learning
- code-generation
- multimodal-reward
- small-language-model
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# WebGen-R1: Incentivizing Large Language Models to Generate Functional and Aesthetic Websites with Reinforcement Learning

## Summary
WebGen-R1 trains a 7B open model with reinforcement learning to generate multi-page websites that both run and look good. The paper claims this closes much of the gap between small open models and much larger frontier models on project-level web generation.

## Problem
- LLMs do well on function-level coding, but multi-page website generation adds routing, multi-file dependencies, runtime behavior, and visual design.
- Existing website generators often stop at single-page static sites, or use multi-agent pipelines that raise token cost, latency, and integration failures.
- RL for this task is hard because reward is not easy to verify: a site can look good but fail at runtime, and full GUI-agent testing is too expensive for training.

## Approach
- WebGen-R1 keeps the model inside a fixed, pre-validated React scaffold, so the model only writes the variable parts of the project instead of the whole app from scratch.
- It runs a two-stage check before expensive reward scoring: static compliance checks first, then dependency install, build, local serving, and browser rendering.
- The reward is cascaded and multimodal: invalid structure gets zero, build failures get zero, and successful renders get a combined score from visual quality, runtime error-free execution, and a required planning-format signal.
- Visual quality comes from a VLM score on rendered screenshots and the user prompt; functional integrity is a binary score based on runtime and console errors.
- The policy is optimized with GRPO to handle high reward variance across candidate websites for the same prompt.

## Results
- Training uses WebGen-Instruct with 6,667 tasks; main evaluation uses WebGen-Bench with 101 tasks; out-of-distribution evaluation uses 119 filtered tasks from WebDev-Arena.
- On the paper's main before/after comparison for the 7B base model, valid render ratio rises from **30.56%** to **95.89%**.
- The paper reports a **44.32%** improvement in aesthetic scoring.
- Functional quality improves from **1.59%** to **29.21%** on the reported metric.
- The authors claim WebGen-R1 beats open-source models up to **72B** and is competitive with **DeepSeek-R1 671B** on functional success, while scoring higher on valid rendering and aesthetic alignment.
- The excerpt does not include the full Table 1 values for each baseline, so exact per-model comparison numbers are not available here.

## Link
- [http://arxiv.org/abs/2604.20398v1](http://arxiv.org/abs/2604.20398v1)
