---
source: arxiv
url: http://arxiv.org/abs/2603.14497v2
published_at: '2026-03-15T17:26:59'
authors:
- Stefan Englmeier
- Katharina Winter
- Fabian B. Flohr
topics:
- autonomous-driving
- vision-language-model
- world-model
- trajectory-prediction
- behavior-conditioning
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# WorldVLM: Combining World Model Forecasting and Vision-Language Reasoning

## Summary
WorldVLM proposes combining the high-level semantic reasoning of vision-language models with the dynamic prediction of world models for interpretable trajectory planning in autonomous driving. The core idea is to let the VLM first state "why to drive this way and how to drive next," and then hand this behavioral intent to the world model to generate physically consistent trajectories.

## Problem
- End-to-end autonomous driving must both understand complex scene semantics and accurately predict future dynamics, but VLMs alone typically lack fine-grained spatial/geometric understanding, while world models alone lack high-level semantic reasoning and interpretable decision-making.
- This is especially important in urban long-tail scenarios, because safe driving requires not only "understanding what is happening" but also "predicting correctly"; otherwise robustness, generalization, and trustworthiness are affected.
- The paper aims to solve: how to unify the semantic decision-making ability of VLMs with the physical prediction ability of WMs into an interpretable driving planning framework.

## Approach
- First, a VLM reads the front-view image, navigation instruction, and current vehicle speed, and outputs a structured JSON-style reasoning result: `justification` (why it is safe), `action` (what should be done), and `action token` (discrete action category).
- A behavior head is added on top of the VLM, mapping language hidden states to a low-dimensional continuous behavior vector, namely a 2D steering-speed control signal; training jointly optimizes text generation loss and behavior regression loss.
- This behavior vector is then injected as a conditioning input into the world model LAW: it is concatenated both to waypoint queries and to spatial visual features / the WM decoder, so that future latent prediction remains aligned with high-level behavioral intent.
- The trajectory is not directly regressed by the VLM, but instead extracted by the behavior-conditioned world model from future scene latents, thereby leveraging the WM's stronger spatiotemporal dynamics modeling capability.
- The authors also extend nuScenes to build a dataset with justification-action annotations, and compare design choices such as different condition types, condition injection locations, and token representation methods.

## Results
- **Main framework vs. the LAW baseline (nuScenes validation set, open-loop)**: WorldVLM's L2 error is essentially on par with LAW, with **0.31/0.62/1.03 m** at 1s/2s/3s respectively, compared with **0.31/0.61/1.02 m** for LAW; the 3s collision rate is **0.48%**, versus **0.44%** for LAW, indicating that VLM+WM fusion is achieved without an obvious loss in trajectory accuracy.
- **Compared with the version "without behavior conditioning"**: No Behavior has a 3s collision rate of **0.49%**, while WorldVLM has **0.48%**; the 1s/2s collision rates are both **0.10%/0.14%**, indicating that behavior conditioning mitigates some of the degradation caused by zero-padding adaptation over part of the prediction horizon.
- **VLM reasoning text quality improves significantly**: After fine-tuning Qwen1.5-0.5B relative to zero-shot, BERTScore F1 increases from **0.54→0.67**; ROUGE-1 from **0.09→0.47**; BLEU-1 from **0.04→0.36**; and BLEU-3 from **0.03→0.15**. The paper states that this means the model has learned to generate more reasonable action explanations and instructions.
- **Condition-type ablation shows continuous motion vectors perform best**: On a small data split, ground-truth Motion Vector (without navigation) reaches **0.20/0.27/0.28 m** L2 at 1s/2s/3s, with collision rates of **0.06/0.07/0.10%**; in the same table, the LAW baseline is **0.30/0.59/0.98 m** and **0.50/0.60/1.0%**. Based on this, the authors argue that fine-grained continuous behavior signals are more helpful for WM prediction than coarse discrete actions.
- **Condition injection ablation**: Using ground-truth motion vectors, the scheme with additional concatenation at the WM head achieves a 3s collision rate of **0.10%**, versus **0.11%** without it; both have L2 around **0.27–0.28 m**, suggesting that explicit behavior injection helps avoid behavioral ambiguity.
- **Behavior token representation ablation**: Feeding the first 16 VLM tokens into the behavior head works best, with angle/speed MAE of **0.0135/0.1788**; by contrast, the last 5 tokens yield **0.0508/0.5768**, indicating that early tokens or dedicated behavior tokens are better suited for extracting control intent.

## Link
- [http://arxiv.org/abs/2603.14497v2](http://arxiv.org/abs/2603.14497v2)
