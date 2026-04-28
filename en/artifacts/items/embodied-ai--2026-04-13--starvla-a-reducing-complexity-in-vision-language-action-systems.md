---
source: arxiv
url: http://arxiv.org/abs/2604.11757v1
published_at: '2026-04-13T17:30:01'
authors:
- Jinhui Ye
- Ning Gao
- Senqiao Yang
- Jinliang Zheng
- Zixuan Wang
- Yuxin Chen
- Pengguang Chen
- Yilun Chen
- Shu Liu
- Jiaya Jia
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- benchmarking
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# StarVLA-$α$: Reducing Complexity in Vision-Language-Action Systems

## Summary
StarVLA-α argues that a plain VLM-to-action setup is enough to reach top-tier VLA performance across several robot benchmarks. The paper’s main claim is methodological: many common additions in VLA systems change results less than backbone choice and clean training setup.

## Problem
- VLA papers are hard to compare because they mix different backbones, robot datasets, embodiments, preprocessing, and benchmark-specific tuning.
- That makes it unclear which parts of a system actually improve robot performance and which gains come from engineering around a benchmark.
- This matters because the field wants general robot policies, but fragmented evaluation hides whether methods transfer across tasks and embodiments.

## Approach
- The authors build **StarVLA-α**, a simple baseline: a pretrained **Qwen3-VL** backbone plus a small **MLP action head** that predicts continuous action chunks from an action token.
- They keep the data pipeline minimal: raw RGB images, language instruction, training-split action normalization, and official benchmark evaluation without benchmark-specific tuning.
- They test the same setup across **LIBERO, SimplerEnv, RoboTwin 2.0, and RoboCasa-GR1**, and also train one joint generalist model with zero-padded actions up to dimension 32.
- Under matched backbone/data/training settings, they compare action-head choices: discrete FAST-style tokens, direct continuous regression, diffusion/flow-matching, and a dual-system GR00T-style design.
- They also ablate robot-data pretraining and common data engineering choices such as proprioception, history frames, delta actions, and relative actions.

## Results
- **Main benchmark results (specialist StarVLA-α):** LIBERO **99.0 / 99.8 / 98.5 / 94.1**, average **98.8** across Spatial/Object/Goal/Long; SimplerEnv **64.6** on WidowX, **70.2** on Google VA, **76.0** on Google VM; RoboTwin 2.0 **50.3** clean, **88.2** clean*; RoboCasa-GR1 **53.8**. In the table, this beats **OpenVLA-OFT** average LIBERO **97.9**, **π0.5** RoboTwin clean **60.2** and clean* **82.7**, and **GR00T-N1.6** RoboCasa **47.6**.
- The abstract claims the single generalist model beats **π0.5 by 20% on the public real-world RoboChallenge benchmark**, but the excerpt does not provide the raw benchmark numbers for that comparison.
- **Action-head ablation:** the simple MLP head is competitive with more complex continuous heads. On RoboCasa-GR1, MLP reaches **53.8**, versus **52.8** for GR00T-style and **48.9** for diffusion-style π; discrete FAST is weaker at **45.0**. On SimplerEnv Google VM, MLP gets **76.0** versus **60.1** for FAST.
- **Robot pretraining ablation:** extra action-data pretraining does not help consistently. Baseline StarVLA-α reaches RoboTwin clean **50.3** and RoboCasa **53.8**; **+OXE** drops to **30.2** and **27.8**; **+InternData-A1** improves RoboTwin clean to **63.6** but lowers RoboCasa to **35.4**; **+RoboTwin-Rand** raises RoboTwin clean to **79.7** but lowers RoboCasa to **33.3**.
- **Data engineering ablation:** some additions help in low-data settings, but gains shrink with more task data. On RoboCasa **24×10**, baseline is **9.8**, delta action reaches **15.8**, relative action **13.6**, proprioception **12.5**. With **24×1000**, baseline is **53.8** and variants are close: proprioception **54.2**, delta **54.8**, relative **55.5**.
- The paper’s claimed breakthrough is not a new architecture. It is the result that a strong pretrained VLM plus a small continuous action head can match or beat recent VLA systems across multiple benchmarks under one controlled recipe.

## Link
- [http://arxiv.org/abs/2604.11757v1](http://arxiv.org/abs/2604.11757v1)
