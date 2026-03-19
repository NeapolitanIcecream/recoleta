---
source: arxiv
url: http://arxiv.org/abs/2603.03818v1
published_at: '2026-03-04T08:03:13'
authors:
- Huihan Liu
- Changyeon Kim
- Bo Liu
- Minghuan Liu
- Yuke Zhu
topics:
- vision-language-action
- continual-learning
- experience-replay
- catastrophic-forgetting
- robot-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Pretrained Vision-Language-Action Models are Surprisingly Resistant to Forgetting in Continual Learning

## Summary
This paper studies forgetting in large-scale pretrained Vision-Language-Action (VLA) models for robot continual learning, finding that they are much less prone to catastrophic forgetting than smaller models trained from scratch. The core conclusion is: for VLAs, simple experience replay is often sufficient, and pretraining significantly changes the dynamics of continual learning.

## Problem
- Robot policies need to continually learn new tasks over time, but they often **catastrophically forget** old tasks, making sequential finetuning nearly unusable.
- Previous conclusions mainly come from **small behavior cloning models trained from scratch**; whether these conclusions apply to modern **pretrained VLAs** remains unclear.
- This matters because if VLAs are naturally more resistant to forgetting, robot skill libraries could be expanded continuously with simpler methods, without relying on very large replay buffers or complex regularization.

## Approach
- On four continual learning benchmarks, **LIBERO-Spatial / Object / Goal / 10**, the paper compares two pretrained VLAs (**Pi0, GR00T N1.5**) with several smaller non-pretrained models (such as **BC-Transformer, BC-ViT, BC-Diffusion Policy**).
- It uses the simplest **Experience Replay (ER)**: when learning a new task, mix current-task data with a small number of replay samples from old tasks; forgetting is evaluated using **average success rate (SR)** and **Negative Backward Transfer (NBT, lower is better)**.
- Controlled ablations are conducted to isolate the **role of pretraining**: three initializations of the same Pi0 architecture are compared — **VL+Action pretraining, VL-only pretraining, and training from scratch** — while scanning different replay buffer sizes (0.2%, 2%, 20%).
- It further analyzes whether “apparent forgetting” equals “complete loss of knowledge” through **module swapping and recovery-via-refinetuning experiments**, distinguishing knowledge retention in the VL backbone versus the action head.

## Results
- At **sample size=1000 (about 20% data per task)**, pretrained VLA + ER significantly outperforms small models: **GR00T** achieves average **SR=0.919±0.011, NBT=0.027±0.021** across the four LIBERO suites; **Pi0** averages **SR=0.768±0.017, NBT=-0.016±0.022**. By comparison, **BC-Transformer** averages **SR=0.585±0.066, NBT=0.245±0.080**, and **BC-ViT** averages **SR=0.508±0.142, NBT=0.193±0.082**. This indicates that VLA forgetting is close to zero, and even shows **positive backward transfer** (negative NBT).
- On more specific tasks, **GR00T** reaches **SR=0.975±0.004, NBT=0.019±0.013** on **LIBERO-Object**, and **SR=0.820±0.017, NBT=0.059±0.035** on **LIBERO-10**; meanwhile **BC-Transformer** achieves only **0.595±0.112 / 0.132±0.120** and **0.376±0.034 / 0.192±0.019** on those same two benchmarks.
- Compared with non-ER baselines, **ER is especially effective for VLAs**. For example, on **GR00T, LIBERO-Object**: **Sequential** has **NBT=0.752**, **EWC=0.766**, while **ER=0.004**; on **Pi0, LIBERO-10**: **Sequential=0.562**, **EWC=0.543**, while **ER=-0.070**. This shows that a small amount of explicit replay is far better than relying only on sequential training or parameter regularization.
- Even with a **small replay buffer**, VLAs are still clearly more resistant to forgetting: when buffer size is **2% (100 samples per task)**, the paper states that **Pi0/GR00T have NBT around 0.1–0.2**, while non-pretrained baselines are around **0.4–0.5**, meaning the latter forget about **2–4×** more; small models typically require **>20%** replay data to approach VLA performance.
- Pretraining itself is the key factor. In the controlled Pi0 comparison, **Pi0 from VL+Action** averages **SR=0.863, NBT=-0.0322**; **Pi0 from VL** averages **SR=0.899, NBT=0.0159**; **Pi0 from scratch** averages **SR=0.655, NBT=-0.0393**; **BC-Transformer** averages **SR=0.678, NBT=0.191**. Based on this, the authors argue that pretraining not only reduces forgetting, but also preserves stronger **forward learning capability**; when training from scratch, low forgetting can sometimes simply reflect that the new tasks were not learned well either.
- The paper also claims that even when old-task performance declines during continual learning, **relevant knowledge is still retained inside the VLA**, because old-task performance can be rapidly recovered with only **a small number of finetuning steps**; the excerpt does not provide specific numbers for this recovery experiment, but this is its strongest concrete claim supporting the idea that “apparent forgetting does not equal knowledge loss.”

## Link
- [http://arxiv.org/abs/2603.03818v1](http://arxiv.org/abs/2603.03818v1)
