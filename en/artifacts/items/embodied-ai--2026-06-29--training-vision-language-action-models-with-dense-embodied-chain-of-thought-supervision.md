---
source: arxiv
url: https://arxiv.org/abs/2606.30552v1
published_at: '2026-06-29T16:48:48'
authors:
- Haoyang Li
- Guanlin Li
- Youhe Feng
- Chen Zhao
- Zhuoran Wang
- Yang Li
- Qizhe Wei
- Shifeng Bao
- Haitao Shen
- Yihan Zhao
- Tong Yang
- Jing Zhang
topics:
- vision-language-action
- embodied-chain-of-thought
- cross-embodiment-transfer
- robot-data-scaling
- diffusion-policy
- generalist-robot-policy
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision

## Summary
ZR-0 is a 2.6B-parameter vision-language-action model for cross-embodiment robot manipulation. It trains a VLM with dense embodied chain-of-thought labels, then skips that text generation at inference while a diffusion action expert outputs continuous action chunks.

## Problem
- Cross-embodiment VLA training is hard because robot arms, bimanual systems, and humanoids use different state vectors, action spaces, joints, sensors, and control interfaces.
- Padding, normalization, and shared action formats allow mixed training, but they leave the model to learn hardware-specific patterns instead of shared manipulation concepts.
- The problem matters because a useful generalist robot policy needs shared scene understanding, object grounding, task progress tracking, and subtask planning while still producing robot-specific controls.

## Approach
- ZR-0 combines a 2.1B-parameter Qwen3-VL-2B-Instruct VLM with a 500M-parameter Diffusion Transformer action expert.
- The VLM is trained to produce dense ECoT labels for each frame: scene description, progress assessment, future plan, to-do actions, target-object boxes, and discrete action tokens.
- The action expert receives VLM features, robot state, noisy action chunks, and a flow-matching timestep, then predicts continuous action chunks.
- A cross-attention mask lets the action expert read only task-and-image prompt features, so ECoT text generation is skipped at inference.
- Pre-training uses ProcCorpus-60M, which aggregates robot data from sources including Open X-Embodiment, DROID, RH20T, Bridge, and Fractal, plus general vision-language data from CapsFusion and Pixmo for VLM retention.

## Results
- ProcCorpus-60M has about 60M frames, about 1,000 hours, more than 400K trajectories, and ECoT annotations for 96.8% of frames.
- On LIBERO, ZR-0 reports 97.8% average success rate, compared with MolmoAct2 at 97.2%, GR00T-N1.7 at 97.0%, π0.5 at 96.9%, π0 at 94.2%, CoT-VLA at 83.9%, and OpenVLA at 76.5%.
- LIBERO suite scores for ZR-0 are 97.4% on Spatial, 99.4% on Object, 98.0% on Goal, and 96.4% on LIBERO-10.
- LIBERO-10 is the clearest reported gain: ZR-0 reaches 96.4%, compared with DeepThinkVLA at 96.2%, GR00T-N1.7 at 94.4%, π0.5 at 92.4%, π0 at 85.2%, and OpenVLA at 53.7%.
- The excerpt states evaluation across 40 LIBERO tasks, 50 RoboTwin 2.0 tasks, 24 RoboCasa GR-1 Tabletop tasks, and real xArm tests with more than 2,000 trajectories across 4 tasks and 50+ objects, but it does not include full quantitative tables for RoboTwin, RoboCasa, or real-world results.
- Inference generates an action chunk in about 90 ms on one NVIDIA A6000 GPU with bfloat16 precision, and the paper claims no performance loss from skipping ECoT generation at inference.

## Link
- [https://arxiv.org/abs/2606.30552v1](https://arxiv.org/abs/2606.30552v1)
