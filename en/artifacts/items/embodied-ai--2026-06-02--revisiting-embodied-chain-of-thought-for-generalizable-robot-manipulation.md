---
source: arxiv
url: https://arxiv.org/abs/2606.03784v1
published_at: '2026-06-02T15:37:59'
authors:
- Nan Sun
- Yuan Zhang
- Yongkun Yang
- Wentao Zhao
- Peiyan Li
- Jun Guo
- Wenxuan Song
- Pengxiang Ding
- Runze Suo
- Yifei Su
- Xin Xiao
- Xinghang Li
- Huaping Liu
topics:
- vision-language-action
- embodied-cot
- robot-manipulation
- diffusion-policy
- robot-data-scaling
- generalist-robot-policy
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation

## Summary
ERVLA treats embodied chain-of-thought as training supervision for robot action representations instead of a required test-time prefix. It reports state-of-the-art success rates on LIBERO-Plus and VLABench using a large auto-labeled embodied CoT corpus.

## Problem
- VLA robot policies can understand images and language but often fail when tasks need semantic disambiguation, spatial grounding, or long action sequences.
- Prior embodied CoT methods often make the policy generate reasoning before actions, which adds latency and lets reasoning errors affect later action tokens.
- Large-scale embodied CoT labels are noisy, especially detector-based coordinates such as bounding boxes and gripper positions, so scaling the data can hurt control if the model must rely on explicit CoT.

## Approach
- The paper builds an embodied CoT corpus with structured fields for task understanding, planning, spatial grounding, and action-level motion descriptions.
- ERVLA uses Qwen3-VL-4B as the vision-language backbone and a diffusion transformer action head trained with flow matching to generate continuous robot actions.
- The model receives CoT supervision during training, but reasoning dropout trains it to act with or without visible CoT at inference time.
- Auxiliary action-query regression teaches the VLM hidden states to predict action chunks, aligning language reasoning with control.
- Knowledge truncation lets the action model attend to the semantic-prefix KV cache while excluding appended state and action-query tokens that could create training shortcuts.

## Results
- The corpus contains 978,743 trajectories, 226.3M samples, and 2,592.5 hours of robot data, built from sources including Bridge, Fractal, Droid, MolmoAct, and AgiBot.
- ERVLA reports 86.9% average success on LIBERO-Plus and 100% success on the background and lighting variations of the LIBERO-Plus Spatial track.
- ERVLA reports 53.2% average success on VLABench, a benchmark with in-distribution and out-of-distribution tracks for category, commonsense, instruction, and texture shifts.
- In CoT-field ablations without pretraining, high-level fields alone hurt or barely help: Goal is -1.2, Planning is -0.8, Subtask is -0.6, and Reasoning is -1.0, while Movement is +4.1 and Point trajectory is +4.8.
- Combining semantic and action-grounded CoT works better: Movement+Reasoning gives +5.2, Subtask+Movement+Point trajectory gives +7.4, and full ECoT gives +8.2 without pretraining.
- Under autoregressive CoT+FAST scaling, adding Bridge+Fractal+MolmoAct+Droid reduces performance by -3.6 on VLABench In-dist., -3.0 on Cross-category, and -3.4 on Texture, supporting the paper's claim that explicit CoT prefixes do not scale reliably for action decoding.

## Link
- [https://arxiv.org/abs/2606.03784v1](https://arxiv.org/abs/2606.03784v1)
