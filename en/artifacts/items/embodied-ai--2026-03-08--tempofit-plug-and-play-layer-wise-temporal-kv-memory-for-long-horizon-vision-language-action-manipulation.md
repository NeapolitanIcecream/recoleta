---
source: arxiv
url: http://arxiv.org/abs/2603.07647v1
published_at: '2026-03-08T14:17:25'
authors:
- Jun Sun
- Boyu Yang
- Jiahao Zhang
- Ning Ma
- Chencheng Wu
- Siqing Zhang
- Yiou Huang
- Qiufeng Wang
- Shan Liang
- Yaran Chen
topics:
- vision-language-action
- long-horizon-manipulation
- temporal-memory
- kv-cache
- training-free
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# TempoFit: Plug-and-Play Layer-Wise Temporal KV Memory for Long-Horizon Vision-Language-Action Manipulation

## Summary
TempoFit is a **training-free** temporal memory plug-in for pretrained Vision-Language-Action (VLA) policies, designed to transform originally "single-frame decision-making" models into long-horizon manipulation policies that can leverage historical information. It directly reuses the model's internal layer-wise attention K/V cache, rather than stacking historical images or training additional temporal modules, making it easier to plug in while maintaining near-real-time inference.

## Problem
- Many existing VLAs are essentially **memoryless** at inference time: each step only looks at the current observation, which makes them prone to repeated actions, missed steps, and failed phase transitions in **non-Markovian** long-horizon tasks involving occlusion, state aliasing, and subtle post-action changes.
- Directly stacking historical frames can introduce temporal information, but it increases visual tokens and inference latency, while bringing in many near-duplicate pixels, making it inefficient.
- Training additional memory/fusion modules usually requires retraining or fine-tuning, and also changes the original single-frame inference graph, making true plug-and-play upgrades for strong pretrained VLAs difficult.

## Approach
- Core idea: treat the **K/V** in Transformer prefix attention as the model's native "state memory." TempoFit caches prefix K/V from past timesteps at several **intermediate layers**, instead of storing raw images or adding new tokens.
- The retrieval method is **K-to-K retrieval**: it uses the current timestep's key to perform similarity matching against historical keys, and then reads out the corresponding historical K/V; the entire process has **no additional parameters and no new training**, while remaining consistent with the original attention geometry of the frozen backbone.
- To prevent old information from interfering with current decisions, it introduces **FGTB (Frame-Gap Temporal Bias)**: a fixed decay bias is added to more distant history so that retrieval favors content that is "recent and relevant."
- The retrieved historical context is added back into the current K/V via a **residual** pathway, rather than by concatenating virtual tokens; then **norm-preserving rescaling** is applied to avoid distribution shift as much as possible under frozen weights.
- The method is **plug-and-play**: it does not modify model parameters, does not change input context length, does not depend on the structure of the action head, and is compatible with different VLA backbones.

## Results
- **LIBERO-Long**: on the **\(\pi_{0.5}\)** baseline, the average success rate improves from **92.6% to 96.6%**, i.e. **+4.0 percentage points**; on **QwenGR00T**, it improves from **90.8% to 94.4%**, i.e. **+3.6 percentage points**.
- Compared with trained temporal methods, TempoFit matches or exceeds representative methods on LIBERO-Long: **MemoryVLA 93.4%**, **HiF-VLA 96.4%**; among them, **TempoFit+\(\pi_{0.5}\)** reaches **96.6%**.
- On the difficult subtask **"Put both pots on stove"**, **\(\pi_{0.5}\)** improves from **58.0% to 84.0%**, indicating that it is particularly effective for cross-stage temporal association.
- **CALVIN D-D**: the average successful task length improves from **3.78 to 3.84** (QwenGR00T → TempoFit); step-wise success rates improve more noticeably on later instructions, e.g. the 5th task improves from **59.8 to 62.3**.
- **CALVIN ABC-D**: the average successful task length improves from **3.83 to 3.87** (\(\pi_{0.5}\) → TempoFit); the 5th task improves from **61.4 to 62.0**.
- The paper also claims that the method incurs **negligible inference overhead** and maintains near-real-time control, but no more detailed latency numbers are provided in the given excerpt.

## Link
- [http://arxiv.org/abs/2603.07647v1](http://arxiv.org/abs/2603.07647v1)
