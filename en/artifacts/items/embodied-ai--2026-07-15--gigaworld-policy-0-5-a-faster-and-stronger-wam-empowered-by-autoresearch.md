---
source: arxiv
url: https://arxiv.org/abs/2607.13960v1
published_at: '2026-07-15T15:46:42'
authors:
- GigaWorld Team
- Angen Ye
- Angyuan Ma
- Boyuan Wang
- Chaojun Ni
- Fangzheng Ye
- Guan Huang
- Guo Li
- Guosheng Zhao
- Haodong Yan
- Hengtao Li
- Jiwen Lu
- Kai Wang
- Mingming Yu
- Qitang Hu
- Qiuping Deng
- Songling Liu
- Xiaoyu Tian
- Xiaofeng Wang
- Xinyu Zhou
- Xiuwei Xu
- Xinze Chen
- Yang Wang
- Yejun Zeng
- Yifan Chang
- Yun Ye
- Zhenyu Wu
- Zhanqian Wu
- Zheng Zhu
topics:
- robot-foundation-model
- vision-language-action
- world-action-model
- robot-data-scaling
- real-time-control
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# GigaWorld-Policy-0.5: A Faster and Stronger WAM Empowered by AutoResearch

## Summary
GigaWorld-Policy-0.5 is an action-centered World Action Model that uses future visual dynamics for training but decodes only actions during deployment. Its Mixture-of-Transformers architecture and optimized runtime target faster closed-loop robot control while retaining the grounding benefits of world-model supervision.

## Problem
- Existing World Action Models often generate future videos during inference, which adds substantial computation and can limit real-time robot control.
- The paper addresses how to preserve dense supervision from future scene prediction without requiring future-video generation at deployment, a key issue for low-latency closed-loop manipulation.

## Approach
- Train the model jointly with World Action Modeling and Action-Conditioned World Modeling so action representations reflect their expected effects on future visual observations.
- Use an action-centered causal mask: action tokens can use current observations, state, and language, while future visual tokens can attend to the predicted actions; future visual tokens cannot leak information back into action prediction.
- Use a Mixture-of-Transformers design with separate visual and action experts, allowing the visual-dynamics pathway to be skipped during action-only inference.
- Initialize the visual expert from GigaWorld-1, pretrain on 2K hours of filtered robot data plus internal data, and use an agent-based AutoResearch pipeline to search training configurations.
- Accelerate deployment with KV caching, graph compilation, and a lightweight C++ runtime.

## Results
- The action-only inference path reaches approximately 85 ms latency on a local NVIDIA RTX 4090 setup.
- On a real-world fruit-picking task, the model achieves an average success rate of 0.85 across six instructions and 10 trials per instruction, compared with 0.76 for π0.5, 0.80 for Motus, 0.78 for FastWAM, and 0.80 for GigaWorld-Policy.
- It records the highest success rate for all six fruit categories; examples include 0.83 for lemon and 0.78 for avocado.
- On a compositional object-placement task, it achieves an average success rate of 0.89, exceeding the strongest reported baseline, Motus at 0.83, by 0.06.
- The provided excerpt reports real-world gains and ablation claims, but it does not include the full ablation tables or the complete set of long-horizon results, so the broader performance comparison cannot be assessed from this text alone.

## Link
- [https://arxiv.org/abs/2607.13960v1](https://arxiv.org/abs/2607.13960v1)
