---
source: arxiv
url: http://arxiv.org/abs/2603.09542v1
published_at: '2026-03-10T11:51:54'
authors:
- Ziyue Zhu
- Shangyang Wu
- Shuai Zhao
- Zhiqiu Zhao
- Shengjie Li
- Yi Wang
- Fang Li
- Haoran Luo
topics:
- vision-language-action
- neuro-symbolic-ai
- robotic-manipulation
- reinforcement-learning
- data-efficient-learning
relevance_score: 0.42
run_id: materialize-outputs
language_code: en
---

# NS-VLA: Towards Neuro-Symbolic Vision-Language-Action Models

## Summary
NS-VLA proposes a vision-language-action framework for robotic manipulation that combines neural perception, symbolic primitive reasoning, and online reinforcement learning. Its core goal is to achieve stronger generalization, robustness, and exploration capability with fewer demonstration data.

## Problem
- Existing VLA methods often use end-to-end approaches to directly regress actions from images and instructions, making it difficult to explicitly learn reusable manipulation primitives; as a result, long-horizon tasks and cross-task generalization remain weak.
- Many methods rely on large models and large-scale demonstration data, but collecting high-quality demonstrations for each robot task is expensive, limiting practical deployment.
- Pure imitation learning mainly reproduces demonstration trajectories and lacks online exploration capability, making it hard to continually improve under perturbed environments or unseen situations.

## Approach
- A pretrained VLM is used to encode vision and language first, then generate a plan composed of discrete symbolic primitives; during execution, a symbolic classifier with monotonic constraints determines which primitive stage the system is currently in.
- A symbolic solver converts the “current primitive” into actions: it first applies Top-K sparse selection over visual tokens based on the primitive, retaining only relevant regions, and then uses a causal Transformer to output a chunk of continuous actions rather than densely regressing step by step.
- During online training, the VLM backbone is frozen and only lightweight modules are updated; reinforcement learning is performed with segmented rewards, progress shaping, and GRPO under KL constraints, encouraging exploration beyond demonstrations while reducing policy drift.
- Overall, the method can be understood simply as: first decompose the task into reusable substeps such as “pick,” “place,” “open,” and “close,” then focus only on the currently relevant visual regions, and use RL to make these steps more stable and effective through real interaction.

## Results
- Under LIBERO 1-shot training (only 1 demonstration per task), NS-VLA leads with **69.1% Avg. SR**: higher than VLA-Adapter’s **65.3%**, EVOLVE-VLA’s **61.3%**, UniVLA’s **55.1%**, OpenVLA-OFT’s **48.9%**, and OpenVLA’s **35.7%**; its model size is **2B**, smaller than several **7B** baselines.
- Under the same 1-shot setting, NS-VLA achieves subset SRs of **85.7 / 75.3 / 70.7 / 45.2** (Spatial/Object/Goal/Long), outperforming VLA-Adapter’s **80.6 / 71.6 / 69.8 / 39.2**, with an especially notable gain of about **6.0** percentage points on long-horizon tasks.
- Compared with its full-data training version, NS-VLA drops by only **29.5** percentage points on average under 1-shot training, better than VLA-Adapter’s **33.2**, EVOLVE-VLA’s **34.5**, UniVLA’s **40.1**, OpenVLA-OFT’s **48.2**, and π0’s **56.8**, supporting its claim of “high data efficiency.”
- On the LIBERO-Plus generalization test (trained on full LIBERO), NS-VLA reaches **79.4% Avg. SR**, significantly higher than OpenVLA-OFT’s **69.6%**, RIPT-VLA’s **68.4%**, π0-Fast’s **61.6%**, VLA-Adapter’s **58.9%**, and π0’s **53.6%**.
- On LIBERO-Plus, NS-VLA’s subset SRs are **88.1 / 79.0 / 70.2 / 80.3**, where the Long-task score of **80.3%** clearly exceeds RIPT-VLA’s **67.5%** and OpenVLA-OFT’s **66.4%**.
- Ablation experiments show that full NS-VLA achieves **98.6%** average SR on LIBERO; removing plan constraints drops it to **79.7%**, removing the visual extractor yields **90.1%**, removing the action generator yields **85.2%**, and removing RL yields **91.6%**, indicating that plan constraints and the overall neuro-symbolic + RL design contribute substantially.

## Link
- [http://arxiv.org/abs/2603.09542v1](http://arxiv.org/abs/2603.09542v1)
