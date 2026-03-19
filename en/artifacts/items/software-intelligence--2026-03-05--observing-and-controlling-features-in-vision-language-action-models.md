---
source: arxiv
url: http://arxiv.org/abs/2603.05487v1
published_at: '2026-03-05T18:53:50'
authors:
- Hugo Buurmeijer
- Carmen Amo Alonso
- Aiden Swann
- Marco Pavone
topics:
- vision-language-action
- activation-steering
- mechanistic-interpretability
- robot-control
- linear-probes
relevance_score: 0.3
run_id: materialize-outputs
language_code: en
---

# Observing and Controlling Features in Vision-Language-Action Models

## Summary
This paper studies how to directly observe and control the internal representations of Vision-Language-Action models (VLAs), so as to steer robot behavior in real time without fine-tuning the model. The core idea is to transfer activation interpretability and activation steering methods from LLMs to VLAs, and formalize them as "feature-observability" and "feature-controllability."

## Problem
- Although VLAs are powerful, their behavior is often unpredictable, hard to correct in real time, and may deviate from user preferences or safety requirements, which is critical for real-world robot deployment.
- Existing LLM activation steering methods cannot be directly applied to VLAs, because VLAs have multimodal inputs, continuous action outputs, and closed-loop control properties.
- A method is needed that can **precisely control behavior while preserving as much of the original natural closed-loop behavior as possible**, rather than relying on expensive fine-tuning or retraining.

## Approach
- The paper proposes two formal concepts: **feature-observability** (whether behavior-relevant features can be read out from a layer’s hidden states) and **feature-controllability** (whether those features can be pushed into a target range by modifying that layer’s hidden states).
- A **linear observer** is used to read out robot state or action features from activations at a Transformer layer, i.e., by training a linear probe / classifier / regressor to predict those features.
- A **minimum-norm linear intervention** is used to control internal representations: if the observed feature falls outside the target range, a closed-form minimum additive perturbation is applied along the direction of the linear probe weights.
- The controller can run online at inference time, be inserted directly into a VLA’s Transformer layer, has very low computational overhead, and does not require fine-tuning or retraining.
- The method is validated on two VLA architectures: the pure-Transformer OpenVLA, and the hybrid Transformer + flow-matching $\pi_{0.5}$.

## Results
- The paper claims that on **$\pi_{0.5}$ (Libero dataset)** and **OpenVLA (BridgeData V2 dataset)**, robot **state and action features can be linearly read out from internal representations with linear probes**, indicating that VLAs contain interpretable internal structure.
- The authors further claim that these linear observation results are **robust** to small perturbations, supporting online control; however, the provided excerpt **does not include explicit numerical tables or complete metrics** (such as specific MAE, R², or accuracy values).
- On the control side, the paper claims that **lightweight, targeted linear interventions can reliably steer robot behavior while preserving closed-loop capability**, and can achieve **online adaptation without fine-tuning** to satisfy user preferences and task constraints.
- The excerpt mentions that Figure 3 shows **MAE** and **accuracy** compared with baselines, and Figure 4 shows the average change in **delta yaw action** after interventions at different layers of $\pi_{0.5}$; however, **the specific numbers are not provided in the supplied text**.
- Compared with related work cited by the authors, the paper’s strongest concrete claim is that the method enables **real-time policy steering** across **different VLA architectures**, **preserves natural behavior**, supports **closed-loop online alignment**, and requires **no fine-tuning**.

## Link
- [http://arxiv.org/abs/2603.05487v1](http://arxiv.org/abs/2603.05487v1)
