---
source: arxiv
url: http://arxiv.org/abs/2603.08124v1
published_at: '2026-03-09T09:03:25'
authors:
- Xiang Shi
- Wenlong Huang
- Menglin Zou
- Xinhai Sun
topics:
- vision-language-action
- robotics
- compute-aware-inference
- frozen-vlm
- categorical-control
relevance_score: 0.45
run_id: materialize-outputs
language_code: en
---

# SaiVLA-0: Cerebrum--Pons--Cerebellum Tripartite Architecture for Compute-Aware Vision-Language-Action

## Summary
SaiVLA-0 proposes a neuroscience-inspired tripartite Vision-Language-Action architecture that separates high-level semantic understanding, semantic-to-control compilation, and low-latency action execution to improve compute controllability, stability, and reproducibility. The paper is positioned as a concept-and-protocol paper, and provides preliminary LIBERO evidence suggesting that feature caching and a modular control design may enable faster training and higher success rates.

## Problem
- Existing VLA systems often couple semantic understanding and high-frequency control within a single large model, leading to **high latency, poor stability, and high computational cost**, and they are also prone to overfitting in low-data settings.
- Relying only on the final-layer representation makes it difficult to simultaneously cover **global semantics** and **local geometric/contact details**; meanwhile, inconsistencies between prompts and calibration further weaken reproducibility.
- This matters because online robot control must achieve both **task understanding** and **low-latency closed-loop execution** at the same time; otherwise, reliable deployment on real robots and under constrained compute becomes difficult.

## Approach
- It adopts a tripartite architecture: **Cerebrum** is a low-frequency, frozen VLM that provides multi-layer high-level semantic priors; **Pons Adapter** fuses these semantic features with current perception/proprioceptive state and compresses them into executable context tokens; **Cerebellum** uses ParaCAT to output actions at high frequency.
- The core of **ParaCAT** is simple: instead of directly regressing continuous actions, it predicts `-1/0/+1` three-class increments for each action dimension and generates the next **K=20** steps in parallel in a single forward pass; it then combines **hysteresis, EMA, temperature, entropy** for smoothing and debouncing.
- **Fixed-rate scheduling** enables compute awareness: Cerebrum is invoked only once every **N=5** Cerebellum chunks, while Cerebellum reuses the multi-step results from a single forward pass, thereby reducing the calling frequency of the large model.
- **Two-stage feature caching** improves training efficiency and reproducibility: Stage A offline-caches multi-layer features from the frozen Cerebrum; Stage B trains only Pons + Cerebellum. Upgrading the brain requires retraining only Pons, while changing robots requires training only Cerebellum.
- On the perception side, it introduces **geometrically bound wrist ROI**: the end effector is projected into the main camera image to crop a high-resolution local view, which is fused with the global main view through cross-attention to capture fine-grained pose and contact changes.

## Results
- The paper explicitly states that it is a **concept-and-protocol paper with preliminary evidence**, not a fully conclusive SOTA report.
- Under the official **N1.5 head-only training** setting on **LIBERO**, **split feature caching** reduces training time from **7.5h to 4.5h**, while improving average success rate from **86.5% to 92.5%**.
- The paper reports that **SaiVLA-0 achieves 99.0% mean success on LIBERO**.
- The system's default key numbers include: fixed scheduling **N=5**, single-forward reuse **K=20**, dual-arm action dimension **D=16**, main view resized to **256×256**, and two wrist ROIs each at **256×256**.
- The paper proposes jointly reporting **success, jitter/jerk, f_fwd, f_eff, SR_cn, latency split**, but the provided excerpt **does not include these more complete comparative values**; larger-scale real-robot and compute-normalized validation is left to future experiments.

## Link
- [http://arxiv.org/abs/2603.08124v1](http://arxiv.org/abs/2603.08124v1)
