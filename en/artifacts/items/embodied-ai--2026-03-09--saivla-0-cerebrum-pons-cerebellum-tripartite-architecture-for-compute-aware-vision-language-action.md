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
- robot-foundation-model
- compute-aware-control
- hierarchical-policy
- feature-caching
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# SaiVLA-0: Cerebrum--Pons--Cerebellum Tripartite Architecture for Compute-Aware Vision-Language-Action

## Summary
This paper proposes SaiVLA-0, a tripartite architecture for robotic Vision-Language-Action with a “division of labor between large and small brains,” decoupling high-level semantic understanding from high-speed low-level control and explicitly designing around compute and latency. The work is more like a concept-and-protocol paper, but it provides preliminary LIBERO evidence suggesting that feature caching and modular control may benefit training efficiency and success rate.

## Problem
- Existing VLA systems often couple semantic understanding and high-frequency control inside a single large model, leading to **high latency, unstable control, and high compute cost**, and they are especially prone to overfitting in small-data settings.
- Relying only on the final-layer representation of a large model often makes it difficult to capture both **global semantics** and **local geometry/contact details** at the same time; this is critical for fine manipulation and dexterous control.
- Training and evaluation often lack unified protocols for caching, prompting, calibration, and compute reporting, resulting in **poor reproducibility and unfair comparisons**.

## Approach
- The paper proposes a tripartite architecture: **Cerebrum** is a frozen large VLM that runs at low frequency and provides stable multi-layer semantic priors; **Pons Adapter** combines these high-level features with the current robot state and compresses them into executable context tokens; **Cerebellum** uses ParaCAT to output actions at high frequency.
- ParaCAT discretizes each action dimension into three classes, **-1/0/+1**, and **predicts K=20 steps in parallel in a single forward pass** rather than doing step-by-step continuous regression; it can be understood as “for each joint, only deciding whether the next small step should move forward, stay, or move backward.”
- It adopts **dual-rate scheduling**: the Cerebrum is called only once every **N=5** control chunks, while the low-level controller reuses high-level semantics; this amortizes the cost of the large model while trying to preserve task performance.
- It adopts **two-stage feature-cached training**: Stage A runs the frozen VLM offline and caches multi-layer features; Stage B trains only the Pons + Cerebellum. This reduces repeated large-model forward passes and improves training speed and reproducibility.
- It introduces **wrist ROIs** geometrically tied to the end effector, cropping high-resolution local regions from the main view that change stably with hand motion, supplementing the contact and fine-grained pose information missing from the global view.

## Results
- The paper explicitly positions itself as a **concept-and-protocol paper with preliminary evidence**, so full conclusive experiments are still not covered; the authors emphasize that they will report metrics such as success, latency, and `SR_cn` under matched GPU/resolution/batch conditions.
- In preliminary evidence on **LIBERO**, **split feature caching** reduces training time from **7.5h to 4.5h**, while increasing average success rate from **86.5% to 92.5%**; the paper states that this comparison was obtained under the **official N1.5 head-only training** setting.
- The paper also claims that **SaiVLA-0 reaches 99.0% mean success on LIBERO**, but the excerpt does not provide finer subset breakdowns, variance, baseline comparison tables, or full experimental conditions.
- The default key configuration of the system includes: **Cerebrum invocation frequency N=5**, **K=20 reused steps per forward pass**, dual-arm system action dimension **D=16**, main view **1028×800→256²**, and two wrist ROIs each at **256²**.
- The paper proposes a compute-normalized metric **`SR_cn = SuccessRate / ComputeBudget`** and argues that future comparisons should also report cold-start Cerebrum latency, Cerebellum single-step/single-forward latency, forward frequency `f_fwd`, and effective action frequency `f_eff`; however, the excerpt still contains **no complete quantitative benchmark table**.

## Link
- [http://arxiv.org/abs/2603.08124v1](http://arxiv.org/abs/2603.08124v1)
