---
source: arxiv
url: https://arxiv.org/abs/2605.03269v2
published_at: '2026-05-05T01:40:15'
authors:
- Dongyoung Kim
- Huiwon Jang
- Myungkyu Koo
- Suhyeok Jang
- Taeyoung Kim
- Beomjun Kim
- Byungjun Yoon
- Changsung Jang
- Daewon Choi
- Dongsu Han
- Donguk Lee
- Heeseung Kwon
- Hojin Jeon
- Jaehyun Kang
- Jaekyoung Bae
- Jihyuk Lee
- Jimin Lee
- John Won
- Joonwoo Ahn
- Junhyeong Park
- Junyoung Sung
- Kyungmin Lee
- Minseong Han
- Minsung Yoon
- Sejune Joo
- Seonil Son
- Seungcheol Park
- Seunggeun Cho
- Seungjun Moon
- Seungku Kim
- Yonghoon Dong
- Yongjin Cho
- Youngchan Kim
- Chang Hwan Kim
- Dohyeon Kim
- Heecheol Kim
- Heewon Lee
- Hensen Ahn
- Hyungkyu Ryu
- Hyunsoo Choi
- Hyunsoo Shin
- Jaeheon Jung
- Jaewoo Kim
- Jinwook Kim
- Joochul Chang
- Joonsoo Kim
- Junghun Park
- Jungwoo Park
- Junho Cho
- Junhyeok Park
- Junwon Lee
- Kangwook Lee
- Kwanghoon Kim
- Kyoungwhan Choe
- Manoj Bhadu
- Nayoung Oh
- Sangjun Kim
- Sangwoo Kim
- Seunghoon Shim
- Seunghyun Kim
- Seungjun Lee
- Seungyup Ka
- Sungryol Yang
- Wook Jung
- Yashu Shukla
- Yeonjae Lee
- Yeonwoo Bae
- Jinwoo Shin
topics:
- vision-language-action
- dexterous-manipulation
- generalist-robot-policy
- robot-data-scaling
- multimodal-transformer
- real-robot-evaluation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# RLDX-1 Technical Report

## Summary
RLDX-1 is a VLA robot policy for dexterous manipulation that adds motion, memory, and tactile/torque inputs to a Qwen3-VL-based policy. The report claims large gains over π_{0.5} and GR00T N1.6 on simulation and real-robot tasks, especially high-DoF humanoid tasks.

## Problem
- Existing VLAs often handle scene understanding and language instructions, but they struggle when manipulation needs motion tracking, long-term task state, or contact sensing.
- This matters for real robots because tasks such as conveyor-belt catching, shell-game-style selection, deformable-object grasping, and insertion can fail when the policy only sees the current image and instruction.

## Approach
- RLDX-1 uses Qwen3-VL 8B as the VLM base, fine-tuned with robot VQA data for spatial relations, subtask inference, and low-level action grounding.
- The model adds a motion module for multi-frame video, a memory module that stores 3 past cognition-feature chunks, and a physics stream for tactile and torque signals.
- Its Multi-Stream Action Transformer processes cognition, action/proprioception, and physics in separate streams, then lets them exchange information through joint self-attention while predicting action chunks with flow matching.
- Training has 3 stages: multi-embodiment pretraining, embodiment-specific mid-training with in-house and synthetic data, and task-specific post-training with optional reinforcement learning.
- The synthetic data pipeline uses image/video generation, inverse dynamics action labeling, video quality filtering, and motion-consistency filtering through simulator replay.

## Results
- On ALLEX humanoid tasks, RLDX-1 reports 86.8% success, while π_{0.5} and GR00T N1.6 are around 40%.
- On conveyor-belt fast-object catching, RLDX-1 reports over 87.5% success, while π_{0.5} stays below 29.2%.
- On GR-1 Tabletop, RLDX-1 reports 58.7% success versus 47.6% for GR00T N1.6.
- On OpenArm versatile-intelligence tests, RLDX-1 improves Unseen Object success from 37.5% with π_{0.5} to 54.2%, and Unseen Task success from 45.8% to 54.2%.
- On ALLEX Object-in-Box Selection, which needs long-term memory, RLDX-1 reports 91.7% success, while GR00T N1.6 and π_{0.5} are in the 30% range.
- Synthetic data adds 9.1 percentage points on GR-1 Tabletop over real-only training, and inference optimization cuts per-step latency on RTX 5090 from 71.2 ms to 43.7 ms, a 1.63x speedup.

## Link
- [https://arxiv.org/abs/2605.03269v2](https://arxiv.org/abs/2605.03269v2)
