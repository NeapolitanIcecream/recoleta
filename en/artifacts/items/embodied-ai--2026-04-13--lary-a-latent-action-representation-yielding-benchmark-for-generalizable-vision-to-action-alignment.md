---
source: arxiv
url: http://arxiv.org/abs/2604.11689v1
published_at: '2026-04-13T16:30:35'
authors:
- Dujun Nie
- Fengjiao Chen
- Qi Lv
- Jun Kuang
- Xiaoyu Li
- Xuezhi Cao
- Xunliang Cai
topics:
- vision-language-action
- latent-action-representation
- robot-benchmark
- generalist-robot-policy
- world-model
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# LARY: A Latent Action Representation Yielding Benchmark for Generalizable Vision-to-Action Alignment

## Summary
LARYBench is a benchmark for testing whether latent action representations learned from video actually help with action understanding and robot control. The paper’s main claim is that strong general visual encoders such as V-JEPA 2 and DINOv3 beat specialized latent action models on both semantic action decoding and low-level control prediction.

## Problem
- Vision-language-action models need action data, but labeled robot action datasets are small and expensive, while human videos are large but unlabeled.
- Many papers propose latent actions as a bridge from video to control, but there is no standard evaluation that measures the quality of those representations directly across both semantic actions and physical control.
- Without that evaluation, it is hard to tell whether a latent action model learned useful action structure or whether downstream policy results came from other parts of the system.

## Approach
- The paper introduces **LARYBench**, a benchmark that scores representations on two tasks: semantic action classification for **what to do** and trajectory regression for **how to do it**.
- It builds a large curated dataset with about **1.2M short videos / 1,000+ hours**, **151 action categories**, **620K image pairs**, and **595K motion trajectories**, covering human and robot data, egocentric and exocentric views, real and simulated settings, and **11 robot embodiments**.
- For semantic evaluation, the benchmark probes representations with classification on **28 atomic robot primitives** and **145 composite human/robot actions**.
- For control evaluation, it trains a simple MLP regressor to map latent features from image pairs to robot action chunks and reports **MSE** on datasets including **CALVIN, VLABench, RoboCOIN, and AgiBotWorld-Beta**.
- It compares **11 models** across embodied latent action models, general semantic encoders, pixel-based generative encoders, and hybrid “general LAM” models built by putting LAPA-style training on top of frozen general vision backbones.

## Results
- On semantic action classification, **V-JEPA 2** is best with **76.62% average accuracy**, beating **DINOv3 at 68.68%**, all general LAM variants at about **40.78% to 49.36%**, and embodied LAMs such as **LAPA 20.17%**, **UniVLA 17.99%**, and **villa-X 20.90%**.
- On the three classification subsets, **V-JEPA 2** gets **79.09%** on **Atomic Robot**, **80.35%** on **Composite Human**, and **70.43%** on **Composite Robot**. **DINOv3** gets **60.79% / 76.19% / 69.06%** on the same tasks.
- A hybrid model with a general backbone can beat specialized embodied LAMs by a large margin on semantics. The paper states **LAPA-DINOv2 reaches 43.67% average** versus **UniVLA at 17.99%**.
- On low-level control regression, **DINOv3** is best among the shown models with **0.19 average MSE**, compared with **V-JEPA 2 at 0.25**, **Wan2.2 at 0.30**, **FLUX.2-dev at 0.35**, and **LAPA at 0.97**.
- For regression by dataset, **DINOv3** reports **0.22 on CALVIN**, **0.06 on VLABench**, **0.22 on RoboCOIN**, and **0.24 on AgiBotWorld-Beta**. **V-JEPA 2** reports **0.27 / 0.07 / 0.32 / 0.33**.
- The main empirical conclusion is that off-the-shelf general visual representations already contain action-relevant information, and **latent feature spaces align with robot control better than pixel-reconstruction spaces** in this benchmark.

## Link
- [http://arxiv.org/abs/2604.11689v1](http://arxiv.org/abs/2604.11689v1)
