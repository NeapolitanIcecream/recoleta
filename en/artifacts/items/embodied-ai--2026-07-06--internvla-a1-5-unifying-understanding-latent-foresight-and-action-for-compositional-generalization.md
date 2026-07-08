---
source: arxiv
url: https://arxiv.org/abs/2607.04988v1
published_at: '2026-07-06T12:25:30'
authors:
- Haoxiang Ma
- Junhao Cai
- Xiaoxu Xu
- Hao Li
- Yuyin Yang
- Yang Tian
- Jiafei Cao
- Hongrui Zhu
- Zherui Qiu
- Zhaxizhuoma
- Yuqiang Yang
- Jiaqi Peng
- Xueyuan Wei
- Yangkun Zhu
- Jiahao Jiang
- Xing Gao
- Hanqing Wang
- Feng Yuan
- Kailin Li
- Xueyue Zhu
- Tai Wang
- Yan Ding
- Jiangmiao Pang
- Jia Zeng
- Jingjing Zhang
- Bowen Zhou
- Yao Mu
- Chunhua Shen
- Weinan Zhang
topics:
- vision-language-action
- robot-foundation-model
- world-model
- compositional-generalization
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# InternVLA-A1.5: Unifying Understanding, Latent Foresight, and Action for Compositional Generalization

## Summary
InternVLA-A1.5 is a vision-language-action robot policy that keeps VLM instruction understanding while adding latent future prediction and continuous action generation. Its main claim is stronger compositional generalization and long-horizon manipulation without running a video generator at inference.

## Problem
- Unified robot policies often lose language and visual semantics when action learning and future prediction are added to a pretrained VLM.
- Prior future-prediction branches often learn pixel-space generation from scratch, which is costly and misses dynamics knowledge already present in pretrained video models.
- The problem matters because compositional instructions, long-horizon tasks, and real-time control need both semantic grounding and physical foresight.

## Approach
- The model uses Qwen-3.5 2B as the VLM backbone and keeps training it on VQA, subtask prediction, and discrete FAST action-token prediction.
- A 460M-parameter unified expert shares full-attention layers with the VLM and predicts continuous action chunks with flow matching.
- It adds 50 learnable foresight tokens that read the current image, language, state, and subtask context, then produce a compact future code.
- During training, that code conditions a frozen WAN2.2-5B video generator on 4 future frames, so gradients teach the foresight tokens to encode task-relevant future states.
- At inference, the WAN video branch is removed, and the policy outputs 50-step continuous action chunks in real time.

## Results
- Pretraining uses 1.2M robot episodes and 861M frames from 6 robot data sources, plus about 3M multimodal samples.
- The paper claims the best overall results on all 6 simulation benchmarks: LIBERO, RoboTwin 2.0, EBench, SimplerEnv, LIBERO-Plus, and DOMINO.
- LIBERO-Plus and DOMINO are used as zero-shot generalization tests, and the paper claims InternVLA-A1.5 leads on both.
- In real-world tests, it is compared with π0.5 and Motus on 3 instruction-following tasks with held-out instruction bindings and a long-horizon chemistry procedure.
- The excerpt does not provide success-rate tables or exact benchmark scores, so the strongest quantitative claims available are the 6-benchmark sweep, 1.2M-episode robot corpus, 3M multimodal samples, 50 foresight tokens, 4 predicted future frames, and 50-step action chunks.

## Link
- [https://arxiv.org/abs/2607.04988v1](https://arxiv.org/abs/2607.04988v1)
