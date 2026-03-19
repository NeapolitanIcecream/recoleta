---
source: arxiv
url: http://arxiv.org/abs/2603.10469v1
published_at: '2026-03-11T06:40:44'
authors:
- Yuquan Li
- Lianjie Ma
- Han Ding
- Lijun Zhu
topics:
- vision-language-action
- robotic-manipulation
- token-merging
- depth-guided-compression
- inference-acceleration
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# DepthCache: Depth-Guided Training-Free Visual Token Merging for Vision-Language-Action Model Inference

## Summary
DepthCache proposes a **training-free, model-free** visual token compression method that uses depth information to guide VLA (Vision-Language-Action) models to merge image tokens more intelligently during inference, thereby reducing robot control latency. It prioritizes preserving the nearby manipulation area and critical boundaries, achieving acceleration across multiple VLA architectures with almost no loss in task success rate.

## Problem
- VLA models are slow at inference in robotic manipulation because each image frame produces a large number of visual tokens that are fed into a large language model, making it difficult to meet the requirements of real-time closed-loop control.
- Existing token pruning/merging methods usually **compress the entire image uniformly** or directly discard tokens, which can easily damage the fine-grained spatial relationships needed for grasping, alignment, and placement.
- Different VLA architectures use different vision encoders, and many existing merging methods require modifying the internal model implementation, resulting in poor cross-model portability.

## Approach
- Use the **depth map as a structural prior**: partition unprotected image patches by depth, applying higher merge ratios to farther regions while preserving as much detail as possible in the nearby workspace.
- Use a **dual protection mechanism** to avoid mistakenly compressing critical tokens: one part comes from language-model cross-attention to protect task-relevant targets; the other comes from depth-gradient edges to protect object boundaries and occlusion contours.
- Instead of completing merging all at once within a single frame, **distribute the merging process across consecutive frames** and complete it gradually, leveraging temporal redundancy and reducing inter-frame instability.
- Monitor depth changes; if a region becomes dynamic, restore that region to full resolution and restart progressive merging.
- For the wrist camera, add a **state machine based on end-effector motion**: compress more aggressively during movement, and restore the full view during fine-grained grasp/release actions.

## Results
- On the **LIBERO** benchmark across 3 VLA models, DepthCache achieves **1.07×–1.28×** inference speedup while keeping the **average success rate drop below 1%**.
- **OpenVLA**: baseline average success rate **76.7%**; with DepthCache, **75.7% (-1.0)**, speed **1.21×**, token retention rate **78.9%**. Compared with **FastV**: **64.0% (-12.7)**, **1.39×**; **SP-VLA**: **71.9% (-4.8)**, **1.50×**.
- **π0.5**: baseline **97.9%**; DepthCache **97.6% (-0.3)**, speed **1.28×**, token retention rate **68.2%**. Compared with **FastV**: **77.6% (-20.3)**, **1.30×**; **ToSA**: **73.8% (-24.1)**, **0.94×**.
- **GR00T**: baseline **93.1%**; DepthCache **92.9% (-0.2)**, speed **1.07×**, token retention rate **87.5%**.
- Under dual-camera steady-state conditions, the number of tokens drops from **512** to about **300**.
- In real-world robotic arm experiments (based on **π0.5**), the total number of successful executions across 3 core tasks changed from **55/60** to **52/60**, average latency dropped from **191 ms** to **143 ms**, and speed improved by **1.33×**; the authors also claim faster task throughput and more timely closed-loop responses in latency-sensitive scenarios.

## Link
- [http://arxiv.org/abs/2603.10469v1](http://arxiv.org/abs/2603.10469v1)
