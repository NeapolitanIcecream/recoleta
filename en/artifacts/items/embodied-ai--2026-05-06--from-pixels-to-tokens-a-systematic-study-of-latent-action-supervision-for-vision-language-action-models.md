---
source: arxiv
url: https://arxiv.org/abs/2605.04678v1
published_at: '2026-05-06T09:27:07'
authors:
- Yihan Lin
- Haoyang Li
- Yang Li
- Haitao Shen
- Yihan Zhao
- Chao Shao
- Jing Zhang
topics:
- vision-language-action
- latent-actions
- robot-policy-learning
- action-tokenization
- generalist-robot-policy
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# From Pixels to Tokens: A Systematic Study of Latent Action Supervision for Vision-Language-Action Models

## Summary
This paper compares four ways to train Vision-Language-Action models with latent action supervision. The main claim is that discrete latent action token prediction is the strongest training signal, with image-based tokens helping long-horizon tasks and action-based tokens helping complex motor control.

## Problem
- VLA datasets mix robot platforms, action formats, and human videos, so raw action labels can have mismatched meanings across data sources.
- Prior VLA papers use latent actions in different ways, which makes it hard to tell whether gains come from the latent action type, the integration method, or the base model.
- The problem matters because general robot policies need supervision that can work across different robots and tasks without adding extra inference steps.

## Approach
- The authors use one Qwen3-VL-2B-based VLA baseline with the same backbone, placeholders, aggregation, and continuous action head across all variants.
- They compare image-based latent actions, learned from visual transitions, against action-based latent actions, learned by tokenizing continuous action chunks.
- They test four strategies: LA-Align aligns hidden states to image-latent embeddings; LA-Direct predicts image-latent tokens; LA-Cond predicts image-latent tokens and conditions action decoding on them; LA-Tok predicts action-latent tokens.
- All latent action models are frozen during VLA training, and all four strategies run in one forward pass at test time.

## Results
- On LIBERO, the baseline averages 93.1% success. LA-Direct reaches 97.1% (+4.0), LA-Align reaches 97.0% (+3.9), LA-Cond reaches 96.6% (+3.5), and LA-Tok reaches 95.5% (+2.4).
- On LIBERO-Long, LA-Direct scores 96.6% versus 85.8% for the baseline, a +10.8 point gain. LA-Align scores 94.8% (+9.0), LA-Cond scores 94.2% (+8.4), and LA-Tok scores 92.6% (+6.8).
- On RoboTwin 2.0, the baseline averages 60.5% success. LA-Tok reaches 78.0% (+17.5), LA-Cond reaches 73.8% (+13.3), LA-Direct reaches 71.8% (+11.3), and LA-Align reaches 70.5% (+10.0).
- RoboTwin task gains support the paper's formulation-task claim: LA-Tok improves Move playingcard away from 73% to 89% (+16) and Move Can Pot from 46% to 70% (+24), while LA-Cond improves Pick Dual Bottles from 37% to 78% (+41).
- The authors also report real-world JAKA experiments with 10 rollouts per model-task and completion scores on a 0-100 scale, but the provided excerpt does not include enough complete numeric results to compare all methods.

## Link
- [https://arxiv.org/abs/2605.04678v1](https://arxiv.org/abs/2605.04678v1)
