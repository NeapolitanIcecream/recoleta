---
source: arxiv
url: http://arxiv.org/abs/2604.08168v1
published_at: '2026-04-09T12:28:14'
authors:
- Jindi Lv
- Hao Li
- Jie Li
- Yifei Nie
- Fankun Kong
- Yang Wang
- Xiaofeng Wang
- Zheng Zhu
- Chaojun Ni
- Qiuping Deng
- Hengtao Li
- Jiancheng Lv
- Guan Huang
topics:
- robot-reinforcement-learning
- video-generation
- value-function
- vision-language-action
- real-world-manipulation
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# ViVa: A Video-Generative Value Model for Robot Reinforcement Learning

## Summary
ViVa uses a pretrained video diffusion model as a value function for robot reinforcement learning. It predicts future robot state and current task value from current images and proprioception, and the paper claims better value signals and better real-world box assembly inside the RECAP pipeline.

## Problem
- Existing robot value models built on vision-language models read mostly static frames, so they miss temporal dynamics that matter for long-horizon manipulation under partial observability and delayed feedback.
- Weak value estimates hurt reinforcement learning because RECAP depends on value predictions for advantage estimation and policy improvement.
- The paper targets value estimation that tracks real task progress, catches execution errors, and transfers to novel objects.

## Approach
- ViVa repurposes a pretrained video generator, Wan2.2, for value estimation instead of training a standard discriminative vision-language value model.
- Input: current multi-view RGB observations plus current robot proprioception. Output: a future proprioceptive state at horizon \(K=50\) and a scalar value for the current state.
- The model converts images, proprioception, and value into latent frames, then uses diffusion denoising with clean current observations as conditioning and noisy future-proprioception/value frames as targets.
- Value supervision uses a normalized return target derived from episode progress and final success or failure. Successful episodes map to values in \([0,1)\); failed episodes shift to \([1,2)\), giving a constant margin of 1.0 between success and failure at the same stage.
- ViVa replaces the VLM-based value function in RECAP while keeping the rest of the pipeline fixed, allowing a direct comparison of value-model design.

## Results
- The excerpt gives no full quantitative benchmark table, so exact success-rate gains are not available here.
- The paper claims "substantial improvements" on real-world box assembly in both success rate and throughput when ViVa is integrated into RECAP, compared with prior value-model choices.
- Qualitative results on 3 real-world tasks—shirt folding, box packaging/assembly, and toilet paper organization—show that ViVa tracks task progress more smoothly than a VLM-based value model.
- In box assembly, ViVa shows sharp value drops at 2 highlighted failure events, while the VLM-based value stays mostly monotonic and misses those errors.
- In toilet paper organization, ViVa shows clear value increases at 2 highlighted milestones: roll alignment and label application; the VLM-based value stays mostly flat.
- Implementation details with concrete numbers: 3 tasks, single-epoch training, batch size 192, prediction horizon \(K=50\), loss weights \(\lambda_{prop}=1.0\) and \(\lambda_{val}=0.5\), 1 denoising step at inference, and training on 8 NVIDIA A800 GPUs.

## Link
- [http://arxiv.org/abs/2604.08168v1](http://arxiv.org/abs/2604.08168v1)
