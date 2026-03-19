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
- continual-learning
- vision-language-action
- robot-learning
- experience-replay
- catastrophic-forgetting
relevance_score: 0.16
run_id: materialize-outputs
language_code: en
---

# Pretrained Vision-Language-Action Models are Surprisingly Resistant to Forgetting in Continual Learning

## Summary
This paper investigates whether large pretrained Vision-Language-Action (VLA) models in robot continual learning suffer severe forgetting like traditional small models. The authors find that pretrained VLAs, combined with very simple experience replay, can significantly suppress forgetting, and even achieve near-zero forgetting with a small replay buffer.

## Problem
- Robot continual learning requires learning new tasks sequentially, but common policy models experience **catastrophic forgetting** of old tasks when learning new ones.
- Existing conclusions mostly come from **small behavior cloning models trained from scratch**; for modern **large-scale pretrained VLAs**, their continual learning behavior lacks systematic study.
- This problem matters because if large models are inherently more resistant to forgetting, robots could continuously accumulate skills with simpler methods, without relying on complex regularization or huge replay buffers.

## Approach
- On four robot continual learning benchmarks, **LIBERO-Spatial / Object / Goal / 10**, the paper compares two pretrained VLA families (**Pi0, GR00T N1.5**) with several non-pretrained small models (such as **BC-Transformer, BC-ViT, BC-DP**).
- It uses the simplest **Experience Replay (ER)**: during sequential task training, only a small subset of samples from each previous task is retained and mixed with current-task data for training.
- **Success Rate (SR)** is used to measure overall task success, and **Negative Backward Transfer (NBT)** is used to measure forgetting; the closer NBT is to 0, the better, while negative values indicate positive transfer back to old tasks.
- To analyze the role of pretraining, the authors fix the Pi0 architecture and compare three initializations: **VL+Action pretraining**, **VL-only pretraining**, and **training from scratch**, while varying replay buffer size (e.g. 10 / 100 / 1000 samples).
- They further analyze the phenomenon of “apparent forgetting despite retained knowledge” through **component swapping and recovery experiments**: specifically checking whether the vision-language backbone and action head still preserve old-task knowledge after continued learning.

## Results
- Under the **20% data/task (sample size=1000)** setting, pretrained VLAs clearly outperform non-pretrained models:
  - **GR00T** average **SR=0.919±0.011**, **NBT=0.027±0.021**;
  - **Pi0** average **SR=0.768±0.017**, **NBT=-0.016±0.022**;
  - Compared with **BC-DP** at **SR=0.696±0.068, NBT=0.127±0.071** and **BC-T** at **SR=0.585±0.066, NBT=0.245±0.080**, this shows that VLAs forget less and achieve higher success rates.
- On **LIBERO-Object** and **LIBERO-10**, ER is far better than methods without replay:
  - **Pi0 + ER**: Object **SR=0.898, NBT=-0.007**; 10 **SR=0.586, NBT=-0.070**.
  - **Pi0 Sequential**: Object **NBT=0.696**; 10 **NBT=0.562**.
  - **GR00T + ER**: Object **SR=0.962, NBT=0.004**; while **Sequential** on Object has **NBT=0.752**, and **EWC** is **0.766**.
- The pretraining advantage is even more pronounced with small buffers: the authors state that with **2% replay data (100 samples/task)**, pretrained VLAs have **NBT around 0.1–0.2**, while non-pretrained baselines are around **0.4–0.5**, meaning the latter forget about **2–4×** more; in some cases VLAs can achieve **zero forgetting** under this setting.
- Pretraining itself is the key factor. Under the same Pi0 architecture (**sample size=1000**):
  - **Pi0 from VL+Action**: average **SR=0.863, NBT=-0.0322**;
  - **Pi0 from VL**: average **SR=0.899, NBT=0.0159**;
  - **Pi0 from scratch**: average **SR=0.655, NBT=-0.0393**;
  - **BC-Transformer**: average **SR=0.678, NBT=0.191**.
  This indicates that low forgetting cannot be judged from NBT alone; pretraining improves both **forward learning ability** and the ability to retain old knowledge.
- The paper also claims that even when performance on some old tasks declines, relevant knowledge is still retained inside the VLA, allowing old skills to be rapidly recovered with **a small amount of finetuning steps**; the excerpt does not provide explicit numbers for this recovery experiment, but this is a core conclusion behind the authors’ claim that “apparent forgetting does not equal complete knowledge loss.”

## Link
- [http://arxiv.org/abs/2603.03818v1](http://arxiv.org/abs/2603.03818v1)
