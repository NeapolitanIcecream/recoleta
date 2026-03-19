---
source: arxiv
url: http://arxiv.org/abs/2603.05147v1
published_at: '2026-03-05T13:14:41'
authors:
- Riccardo Andrea Izzo
- Gianluca Bardaro
- Matteo Matteucci
topics:
- vision-language-action
- adaptive-inference
- ood-detection
- robot-safety
- uncertainty-estimation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Act, Think or Abstain: Complexity-Aware Adaptive Inference for Vision-Language-Action Models

## Summary
This paper proposes an adaptive inference framework for Vision-Language-Action (VLA) models that switches between **direct execution (Act)**, **additional reasoning (Think)**, and **refusal to execute (Abstain)** based on the complexity of the current state, aiming to balance efficiency, generalization, and safety. The key finding is that for judging task complexity, **visual embeddings are more reliable than language or fused features**.

## Problem
- Existing VLA systems often improve generalization through reasoning methods such as chain-of-thought, but **reasoning at all times** increases computational cost and latency and wastes resources on simple tasks.
- These methods usually **lack uncertainty / out-of-distribution recognition capability**, and may become overconfident on OOD tasks, leading to catastrophic execution failures.
- Robot deployment must simultaneously satisfy **real-time performance, generalization, and safety**, so a mechanism is needed to first determine **whether the system should act directly at all**.

## Approach
- Extract three types of embeddings—**vision, text, and fused**—from the VLM backbone of a pretrained VLA/SmolVLA; the authors also explicitly prevent the text encoder from seeing the image to isolate language uncertainty.
- First apply **PCA to reduce to 64 dimensions**, then score features with two novelty estimators: **GMM + Mahalanobis distance** to model the global distribution, and **1-NN** to capture local anomalies; the GMM uses **Ledoit-Wolf shrinkage** to stabilize covariance estimation.
- Aggregate the scores into a small vector (mainly including GMM scores for vision/text/fused features and a visual kNN score), feed it into a lightweight **MLP**, and output a three-way decision: **Act / Think / Abstain**.
- The “Think” branch is triggered only **once at the first timestep of each episode**, appending scene cues and subgoals to the text prompt before handing control back to the VLA; “Abstain” directly refuses high-risk OOD tasks.
- To train the intermediate “partially OOD / Think” state, in addition to using **LIBERO-PRO**, the authors synthesize intermediate samples between ID and OOD features using **Beta(0.5,0.5) mixup**.

## Results
- Evaluated on **LIBERO / LIBERO-PRO / a real robot (SO-ARM 101)**; the best configuration is **MLP + GMM (vision-only)** with **Macro F1 = 84.34%**, outperforming all alternatives.
- Compared with a **Baseline MLP** trained directly on the raw embeddings, the proposed method is substantially stronger: the baseline reaches only **63.81% Macro F1**; moreover, **86% of “Think” samples are misclassified as “Act”**, showing that the baseline is overconfident in ambiguous scenarios.
- **Visual kNN** is also competitive, reaching **73.90% F1**, and the authors state that in the confusion matrix there is **no confusion between “Act” and “Abstain”**, meaning tasks that should be stopped are never mistakenly allowed to execute directly.
- Multimodality does not provide gains: **ensemble (all GMM + kNN) 71.41% F1**, **text-only 54.76% F1**, and text-only fails to correctly identify **even a single “Think”** sample. This supports the argument that **the semantic invariance of language can mask physical anomalies**.
- In terms of data efficiency, the baseline remains almost stuck at **F1≈0.60** across different data scales; in contrast, **vision-only GMM** outperforms the baseline by **15%** using only **1% of the data** (fewer than 1000 samples), and approaches peak performance with **5% of the data**. The abstract also reports that its **vision-only configuration reaches 80% F1 using only 5% of the training data**.
- Ablation on the number of GMM components shows the best result at **k=3**; **k=1** is clearly insufficient, while larger k brings diminishing returns and extra computational overhead.

## Link
- [http://arxiv.org/abs/2603.05147v1](http://arxiv.org/abs/2603.05147v1)
