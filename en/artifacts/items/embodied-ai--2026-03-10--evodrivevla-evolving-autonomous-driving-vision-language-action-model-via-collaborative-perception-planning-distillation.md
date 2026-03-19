---
source: arxiv
url: http://arxiv.org/abs/2603.09465v1
published_at: '2026-03-10T10:19:07'
authors:
- Jiajun Cao
- Xiaoan Zhang
- Xiaobao Wei
- Liyuqiu Huang
- Wang Zijian
- Hanzhen Zhang
- Zhengyu Jia
- Wei Mao
- Hao Wang
- Xianming Liu
- Shuchang Zhou Liu
- Yang Wang
- Shanghang Zhang
topics:
- autonomous-driving
- vision-language-action
- knowledge-distillation
- trajectory-planning
- perception-planning
- closed-loop-evaluation
relevance_score: 0.67
run_id: materialize-outputs
language_code: en
---

# EvoDriveVLA: Evolving Autonomous Driving Vision-Language-Action Model via Collaborative Perception-Planning Distillation

## Summary
EvoDriveVLA proposes a collaborative distillation framework for autonomous driving VLA models that improves both perception and planning. The core idea is to use “self-anchoring” to protect visual representations and an “oracle teacher” to provide stronger trajectory supervision, thereby improving both open-loop and closed-loop driving performance.

## Problem
- Existing autonomous driving VLAs often damage the general perception capabilities learned during pretraining when the visual encoder is unfrozen during fine-tuning, leading to perceptual degradation.
- Long-horizon trajectory planning is prone to instability; meanwhile, in conventional distillation, if the teacher is trained under the same conditions as the student, its planning ability has no clear advantage and it is difficult for it to provide high-quality guidance.
- Existing multi-trajectory distillation methods typically rely on predefined planning vocabularies, so trajectory diversity and scene adaptability remain limited, which affects generalization and safety in real driving.

## Approach
- Proposes **collaborative perception-planning distillation**: jointly distilling perception and planning, rather than only distilling the final trajectory.
- On the perception side, it uses **self-anchored visual distillation**: first copying the student’s current visual encoder as a “self-anchored teacher,” then constraining the student’s visual tokens during training not to drift too far, so that the original visual capabilities are preserved while adapting to driving tasks.
- Designs **AnchorFormer**, which uses instructions, vehicle state, and ground-truth future trajectories to assign different anchoring strengths to different visual regions; key regions more relevant to future trajectories are constrained more strongly.
- On the planning side, it builds a **future-aware oracle teacher** that uses future images and future ego states, first generating coarse trajectories and then applying **coarse-to-fine refinement** to obtain better trajectory candidates.
- It then uses **MC-dropout sampling** to generate more high-quality, diverse candidates with relatively low additional cost, and selects the candidate with the smallest cross-entropy to the ground truth as the soft target, performing two-level distillation on the student’s hidden states and logits.

## Results
- Achieves SOTA on **nuScenes open-loop evaluation**. Using the **ST-P3 protocol** as an example, EvoDriveVLA attains an average L2 error of **0.26 m**, outperforming **DiMA 0.27 m**, **OpenDriveVLA 0.33 m**, and **OmniDrive 0.33 m**; its 3s L2 is **0.43 m**, better than **DiMA 0.44 m**.
- On **nuScenes / ST-P3 collision**, the average collision rate is **0.06%**, tied with **DistillDrive 0.06%**, and better than **DiMA 0.08%** and **OpenDriveVLA 0.10%**; 3s collision is **0.12%**, better than **DiMA 0.15%**.
- On **nuScenes open-loop evaluation (UniAD protocol)**, the average L2 is **0.52 m**, outperforming **DiMA 0.57 m**, **OpenDriveVLA 0.67 m**, and **GPT-Driver 0.84 m**; the 1s/2s/3s L2 values are **0.16/0.44/0.96 m**, respectively.
- However, under **UniAD protocol collision**, not all metrics are best: EvoDriveVLA has an average collision rate of **0.12%**, and compared with **DiMA 0.07%** and **OpenDriveVLA 0.30%**, the best-performing components are inconsistent; for example, 2s collision is **0.02%**, better than **DiMA 0.05%**, but 3s is **0.33%**, worse than **DiMA 0.16%**.
- On **NAVSIM closed-loop navtest**, EvoDriveVLA achieves **PDMS of 85.3**, outperforming **PARA-Drive 84.0**, **TransFuser 84.0**, **UniAD 83.4**, and **QwenVL2.5-8B 83.3**; meanwhile, **EP=81.1**, higher than **UniAD 78.8** and **InternVL3-8B 78.9**.
- Other closed-loop metrics also reach best or tied-best results: **NC 98.0**, **DAC 93.3**, **TTC 93.1**, **Comfort 100**, overall showing that it not only improves open-loop prediction accuracy but also enhances real decision-making performance in the closed loop.

## Link
- [http://arxiv.org/abs/2603.09465v1](http://arxiv.org/abs/2603.09465v1)
