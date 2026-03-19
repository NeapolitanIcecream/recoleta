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
- temporal-memory
- kv-cache
- long-horizon-manipulation
- training-free
- robotics
relevance_score: 0.56
run_id: materialize-outputs
language_code: en
---

# TempoFit: Plug-and-Play Layer-Wise Temporal KV Memory for Long-Horizon Vision-Language-Action Manipulation

## Summary
TempoFit addresses the problem that vision-language-action (VLA) robotic policies in long-horizon manipulation "only look at the current frame and have no memory" by proposing a training-free, plug-and-play temporal memory mechanism. It directly reuses the attention KV states inside each layer of a frozen model as historical memory, improving long-horizon manipulation stability without increasing the input context length.

## Problem
- Although existing pretrained VLAs are strong at single-step manipulation, their inference is typically **memoryless**, making them prone to repeated actions, missed steps, or failed stage transitions in non-Markovian long-horizon tasks with occlusion, state aliasing, and subtle post-action changes.
- A common approach is to stack historical frames, but this significantly increases the number of visual tokens and the cost of attention computation, while also introducing a large amount of near-duplicate pixels, leading to higher latency and redundant information.
- Another class of methods injects history through additional temporal modules / memory interfaces, but these usually require training or fine-tuning and may disrupt the original single-frame inference graph, making it hard to directly retrofit strong frozen backbone VLAs.

## Approach
- Core idea: treat the **keys/values (K/V)** in Transformer prefix attention as the model's native "addressable runtime state," cache and reuse them across timesteps, instead of storing raw images or learning new memory modules.
- Maintain a layer-wise FIFO KV cache at selected **intermediate layers**, storing only the K/V from the prefix stage and adding no input tokens, thus largely preserving the original model's inference structure and action head.
- Use the current timestep's K to perform **K-to-K retrieval** against historical K, i.e., similarity matching in the model's original key space, to read out relevant historical K/V context; this is a parameter-free, training-free retrieval method.
- Introduce **Frame-Gap Temporal Bias (FGTB)**, which applies a fixed temporal decay bias to older frames so that retrieval remains "present-dominant, history-assisted," reducing interference from stale context.
- Inject the retrieved historical K/V into the current K/V through **pre-attention residual loading**, with **norm-preserving rescaling** to minimize distribution shift and attention instability under frozen weights.

## Results
- On **LIBERO-Long**, TempoFit improves **π0.5** from **92.6%** average success rate to **96.6%**, i.e. **+4.0 percentage points**; in the same table it surpasses **MemoryVLA 93.4%** and is also slightly higher than **HiF-VLA 96.4%**.
- On **LIBERO-Long**, TempoFit improves **QwenGR00T** from **90.8%** to **94.4%**, i.e. **+3.6 percentage points**.
- On the specifically difficult subtask "**Put both pots on stove**," **π0.5** improves from **58.0%** to **84.0%**, a gain of **+26.0 percentage points**, indicating that it is especially effective for cross-stage temporal dependencies.
- On **CALVIN D-D**, the average task length improves from **3.78** to **3.84**; among step-wise metrics, step 5 improves from **59.8** to **62.3**, indicating more stable execution of later instructions.
- On **CALVIN ABC-D**, the average task length improves from **3.83** to **3.87**; step 5 improves from **61.4** to **62.0**.
- The paper also claims the method has **near-real-time / negligible inference overhead** and can transfer to real-robot long-horizon tasks, but the provided excerpt does not include more detailed real-time latency numbers.

## Link
- [http://arxiv.org/abs/2603.07647v1](http://arxiv.org/abs/2603.07647v1)
