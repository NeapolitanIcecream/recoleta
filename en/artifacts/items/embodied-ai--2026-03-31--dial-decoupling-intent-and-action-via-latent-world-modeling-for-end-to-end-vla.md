---
source: arxiv
url: http://arxiv.org/abs/2603.29844v1
published_at: '2026-03-31T15:02:27'
authors:
- Yi Chen
- Yuying Ge
- Hui Zhou
- Mingyu Ding
- Yixiao Ge
- Xihui Liu
topics:
- vision-language-action
- latent-world-model
- robot-foundation-model
- sim2real
- generalist-robot-policy
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# DIAL: Decoupling Intent and Action via Latent World Modeling for End-to-End VLA

## Summary
DIAL is an end-to-end vision-language-action model that separates high-level intent from low-level control with a latent world model. It uses a VLM to predict future visual features as an intent signal, then a policy converts that signal and the current observation into robot actions.

## Problem
- Existing end-to-end VLAs often map vision-language features straight to low-level actions, which can make training unstable and damage the VLM's pretrained semantic features.
- Hierarchical robot systems keep high-level planning and low-level control separate, but the interface is often non-differentiable, which blocks action feedback from improving the planner.
- World-model objectives have been added before, but in many prior methods the predicted future is only an auxiliary signal, so the policy can still ignore it and learn shortcuts.

## Approach
- DIAL builds a two-part policy: **System-2** is a pretrained VLM that predicts a latent representation of the future observation at horizon **H = 16**, and **System-1** is an action policy that uses this predicted future plus the current state to output an action chunk.
- The key mechanism is a **latent intent bottleneck**: instead of sending text plans or pixels to the controller, the VLM predicts future visual features in the same ViT feature space used for perception. This future feature tensor is the model's intent.
- System-2 uses learnable query tokens on top of a VLM such as **Qwen2.5-VL-3B** and is trained with an **MSE world-model loss** to match the ViT features of the future frame \(o_{t+H}\).
- System-1 is a latent inverse-dynamics policy with a **4-layer self-attention fusion module** and a **16-layer DiT** trained with **flow matching** to generate the next **16-step** action chunk.
- Training has two stages: a decoupled warmup where System-2 predicts future latents and System-1 learns control from ground-truth future features, then joint end-to-end training with both the world-model loss and action loss so action gradients can refine the VLM without fully collapsing its representations.

## Results
- On the **RoboCasa GR1 Tabletop** benchmark, the paper claims a **new state of the art** over prior methods.
- The main quantitative efficiency claim is **10× fewer robot demonstrations** than prior methods while still outperforming them; the excerpt states a few-shot regime of **2,400 trajectories** versus a full-data regime of **24,000 trajectories**.
- Evaluation in simulation covers **24 tasks**, each tested over **50 episodes**, including **18** pick-and-place tasks and **6** articulated tasks.
- For cross-embodiment learning, DIAL uses **27,419** EgoDex human pick-and-place trajectories and is reported to improve zero-shot generalization on three OOD settings: unseen appearance (**18 tasks**), unseen combinations (**14 tasks**), and unseen object types (**32 tasks**).
- In real-world experiments on the **IRON-R01-1.11** humanoid, training uses **120 robot trajectories per task**, plus a mixed pretraining set of **32k** robot trajectories and **30k** EgoDex trajectories. The paper claims reliable execution and zero-shot transfer to novel objects and configurations.
- The excerpt does **not provide exact success-rate numbers, baseline margins, or per-method tables**, so the strongest concrete claims are SOTA on RoboCasa, 10× higher data efficiency, and robust zero-shot transfer in simulation and real-world tests.

## Link
- [http://arxiv.org/abs/2603.29844v1](http://arxiv.org/abs/2603.29844v1)
