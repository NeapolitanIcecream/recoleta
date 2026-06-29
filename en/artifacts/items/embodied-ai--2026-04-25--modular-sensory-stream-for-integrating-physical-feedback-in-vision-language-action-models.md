---
source: arxiv
url: http://arxiv.org/abs/2604.23272v1
published_at: '2026-04-25T12:28:47'
authors:
- Jimin Lee
- Huiwon Jang
- Myungkyu Koo
- Jungwoo Park
- Jinwoo Shin
topics:
- vision-language-action
- multimodal-robot-learning
- tactile-sensing
- torque-feedback
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models

## Summary
MoSS adds tactile and torque feedback to pretrained vision-language-action models through separate modality streams that talk to the action model with shared attention. On real contact-rich robot tasks, it improves success rates over vision-only VLAs and over single-modality physical-feedback baselines.

## Problem
- Standard VLAs act from vision and language, which leaves them weak on contact-rich manipulation where grasp force, contact detection, and alignment depend on physical feedback.
- Prior work usually adds one physical modality at a time, such as tactile or torque, and does not handle multiple heterogeneous signals well.
- This matters for real robot tasks like cup unstacking, fragile object handling, board erasing, and plug insertion, where visual input alone can be ambiguous or miss contact events.

## Approach
- MoSS attaches a separate sensory stream for each physical modality, such as tactile and torque, to a pretrained diffusion-based VLA action expert.
- The action stream and sensory streams stay structurally separate, but exchange information through joint cross-modal self-attention, so the model can use physical signals for action prediction without fully mixing all parameters.
- Training uses two stages: first freeze the pretrained VLA and train only the new sensory streams to align them with the existing policy representation; then unfreeze and fine-tune the full model together.
- An auxiliary loss asks each sensory stream to predict future physical signals over the action horizon, which is meant to help the model learn contact dynamics and use feedback more effectively.

## Results
- On four real-world contact-rich tasks, base GR00T N1.5 scores **20.8% avg** success and base pi_0 scores **26.1% avg**. MoSS with both tactile and torque reaches **49.0% avg** on GR00T N1.5 and **45.9% avg** on pi_0.
- For **GR00T N1.5**, MoSS with tactile only gets **42.7% avg**, better than **Tactile-VLA 30.2%** and **ForceVLA 34.4%**. MoSS with torque only gets **37.5% avg**, better than **TA-VLA 33.3%**. With both tactile and torque it reaches **49.0% avg**.
- For **pi_0**, MoSS with torque only gets **41.7% avg** versus **TA-VLA 34.4%**. With both tactile and torque it reaches **45.9% avg**, above the base **26.1% avg**.
- Per-task best numbers reported for **GR00T N1.5 + MoSS (tactile+torque)** are **54.2%** on Unstack Cup, **66.7%** on PnP Egg, **50.0%** on Board Erase, and **25.0%** on Plug Insertion.
- Ablations on GR00T N1.5 show full MoSS at **54.2%** on Unstack Cup and **66.7%** on PnP Egg. Removing decoupled streams drops results to **33.3% / 50.0%**, removing two-stage training to **37.5% / 58.3%**, and removing future prediction to **45.8% / 58.3%**.
- Inference overhead is small in the reported setup: GR00T N1.5 runs at **21.0 ms** per action chunk, while MoSS adds tactile only to **22.4 ms (1.06x)**, torque only to **21.9 ms (1.04x)**, and both to **23.4 ms (1.11x)**.

## Link
- [http://arxiv.org/abs/2604.23272v1](http://arxiv.org/abs/2604.23272v1)
