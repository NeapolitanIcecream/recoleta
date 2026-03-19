---
source: arxiv
url: http://arxiv.org/abs/2603.03739v1
published_at: '2026-03-04T05:19:20'
authors:
- Zehua Fan
- Wenqi Lyu
- Wenxuan Song
- Linge Zhao
- Yifei Yang
- Xi Wang
- Junjie He
- Lida Huang
- Haiyan Liu
- Bingchuan Sun
- Guangjun Bao
- Xuanyao Mao
- Liang Xu
- Yan Wang
- Feng Gao
topics:
- vision-language-navigation
- vision-language-action
- world-model
- 3d-spatial-representation
- streaming-policy
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# PROSPECT: Unified Streaming Vision-Language Navigation via Semantic--Spatial Fusion and Latent Predictive Representation

## Summary
PROSPECT is a unified streaming model for vision-language navigation that places action decision-making, 2D semantic understanding, 3D spatial perception, and future latent representation prediction into a single framework. Its core claim is that predicting future semantic/spatial latents, rather than pixels, can improve long-horizon navigation robustness without increasing inference overhead.

## Problem
- Existing zero-shot or end-to-end VLN/VLA methods are better at “understanding what they see and producing actions,” but often lack an internalized predictive capability for future environmental changes and spatial structure, which can hurt long-horizon and complex-instruction navigation.
- Using only a 2D semantic encoder lacks stable spatial intelligence; meanwhile, some 3D methods have high memory costs on long sequences or provide only relative-scale representations, which is unfavorable for consistent spatial representation in streaming navigation.
- Directly predicting explicit modalities such as pixels and depth can easily overfit task-irrelevant details like texture and lighting, reducing cross-scene and cross-lighting robustness. This motivates a more abstract, task-relevant prediction target.

## Approach
- Uses a streaming VLA policy as the navigation backbone: it takes language instructions and continuous RGB observations as input and outputs discrete navigation actions; it handles long context via a short-term sliding window + long-term memory tokens.
- Uses frozen SigLIP to extract 2D semantic features and frozen CUT3R to extract streaming 3D absolute-scale spatial features, then fuses them through cross-attention into representations used by the LLM/policy.
- During training, it additionally introduces learnable stream query tokens, allowing the model to “query backward” from historical streaming context for the next step’s 2D/3D latents; the prediction targets are not pixels, but latent features from frozen teacher SigLIP/CUT3R.
- 2D prediction uses cosine loss, 3D prediction uses MSE, and both are jointly trained with the navigation action loss; the predictive branch is completely removed at inference time, so the authors claim there is no additional inference latency.
- Designs a dedicated streaming-causal attention mask to enforce temporal causality, isolate queries from different time steps, and isolate 2D/3D queries from each other, reducing information leakage and cross-task interference.

## Results
- On VLN-CE R2R val-unseen, PROSPECT* achieves **NE 5.31 / OSR 60.3 / SR 52.0 / SPL 46.2**, outperforming StreamVLN* at **5.47 / 57.8 / 50.8 / 45.7**; in the same table it is also above Uni-Navid at **SR 47.0 / SPL 42.7**.
- Under a setting with more additional data, PROSPECT† reaches **NE 4.92 / OSR 65.2 / SR 58.9 / SPL 54.0** on R2R val-unseen, outperforming StreamVLN† at **5.10 / 64.0 / 55.7 / 50.9**; on RxR val-unseen it reaches **NE 5.70 / SR 54.6 / SPL 46.2 / nDTW 62.1**, slightly better than StreamVLN† at **6.22 / 52.9 / 46.0 / 61.9**.
- Module ablations (R2R val-unseen) show: the SigLIP-only baseline is **NE 6.05 / SR 45.5 / SPL 41.6**; adding CUT3R changes this to **5.91 / 46.7 / 41.8**; adding 2D+3D world-model latent prediction further reaches **5.82 / 48.7 / 42.9**, indicating that both 3D fusion and latent prediction contribute.
- In spatial encoder ablations, VGGT encounters **OOM** in this streaming long-context setting; InfiniteVGGT takes **0.284s** and achieves **SR 43.2 / SPL 38.0 / OSR 54.4 / NE 6.61**; CUT3R takes **0.245s** and reaches **SR 48.7 / SPL 42.9 / OSR 57.6 / NE 5.82**, indicating it is better suited to streaming navigation in both efficiency and performance.
- Grouped by task length, on R2R long horizon (>=100), relative to the baseline, PROSPECT improves **SR from 20.18 to 24.32 (+4.14)**, **SPL from 10.61 to 14.25 (+3.64)**, **OSR from 34.21 to 40.75 (+6.54)**, and reduces **NE from 9.11 to 8.74 (-0.37)**, supporting its claim of being “more robust over long horizons.”
- For real-robot deployment, the authors report remote inference at about **0.25–0.27 s/step (around 4 Hz)** and claim robust performance across indoor/outdoor settings and diverse lighting; however, the excerpt does not provide more complete quantitative metrics such as real-robot success rate.

## Link
- [http://arxiv.org/abs/2603.03739v1](http://arxiv.org/abs/2603.03739v1)
