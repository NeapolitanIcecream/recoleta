---
kind: trend
trend_doc_id: 273
granularity: day
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-05T00:00:00'
topics:
- robotics
- vision-language-action models
- robot data
- inference latency
- simulation augmentation
run_id: materialize-outputs
aliases:
- recoleta-trend-273
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/robot-data
- topic/inference-latency
- topic/simulation-augmentation
language_code: en
pass_output_id: 130
pass_kind: trend_synthesis
---

# Robot VLA deployment claims face data scale and control latency tests

## Overview
The period’s strongest signal is practical deployment pressure on Vision-Language-Action (VLA) robot policies. MolmoAct2 makes the reproducibility case with open weights and robot datasets. Latent Bridge and the asynchronous-inference benchmark focus on whether policies can keep control rates high without losing task success.

## Findings

### Open VLA models and robot datasets
MolmoAct2 is the clearest deployment-oriented release in the period. The paper describes an open VLA system with released weights, code, and training data. Its backbone, Molmo2-ER, is a 4B vision-language model (VLM) trained on a 3.3M-sample embodied-reasoning corpus, then connected to robot actions through an action tokenizer and a continuous action expert.

The data release is a large part of the claim. The authors report 720 hours of bimanual YAM data, a filtered SO-100/101 community dataset with 38,059 episodes, and a filtered DROID Franka subset with 74,604 successful episodes. They also report 63.8% average performance across 13 embodied-reasoning benchmarks for Molmo2-ER, with a 17-point gain over Molmo2. The provided excerpt says MolmoAct2 beats strong baselines across simulation and real-world benchmarks, but it does not include the underlying task success rates.

#### Sources
- [MolmoAct2: Action Reasoning Models for Real-world Deployment](../Inbox/2026-05-04--molmoact2-action-reasoning-models-for-real-world-deployment.md): Summary lists MolmoAct2 components, released assets, datasets, and reported benchmark results.

### Simulation video transfer for VLA training data
Seeing Realism from Simulation targets the data bottleneck by turning simulated robot videos into more realistic training videos while preserving the action trajectory. The pipeline captions simulation videos, rewrites scene descriptions to vary appearance, uses depth as a geometry condition, and generates realistic videos with Cosmos-Transfer 2.5. A coreset sampler selects examples by action-prediction loss and visual diversity, so the method avoids augmenting every trajectory.

The gains are strongest when evaluation adds visual or language variation. On RoboTwin 2.0, RDT-1B improved by 10.0 points on Hard single-task settings and 8.0 points in a 32-task multi-task setting with a 10% augmented coreset. On LIBERO-Plus, pi_0 improved by 5.1 points overall, with larger gains on object layout and instruction changes. Standard LIBERO saw small drops, which fits the paper’s own explanation that train and test settings there are already similar.

#### Sources
- [Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation](../Inbox/2026-05-04--seeing-realism-from-simulation-efficient-video-transfer-for-vision-language-action-data-augmentation.md): Summary gives the augmentation pipeline and reported RoboTwin, LIBERO-Plus, and LIBERO results.

### Inference speed and stale-observation control
Two papers treat latency as a core VLA deployment constraint. Latent Bridge reduces calls to the large VLM backbone by predicting feature or key-value cache deltas between full backbone steps. On LIBERO, it reports 94.54% success at 49 ms per step for GR00T-N1.6-3B, compared with 96.58% at 90 ms for synchronous inference. For pi_0.5, it reports 96.92% at 46 ms, compared with 96.96% at 76 ms.

The asynchronous-inference benchmark studies the related problem of stale observations when action chunks are generated too slowly. It compares IT-RTC, TT-RTC, VLASH, and A2C2 under matched settings. A2C2 performs best at high delay in the reported tests: on Kinetix it stays above 90% solve rate up to delay d=8, and on LIBERO it reaches about 58% success at d=20 while the naive asynchronous baseline is around 10–12%. TT-RTC has the simplest runtime profile when it works, with no added inference overhead.

#### Sources
- [Latent Bridge: Feature Delta Prediction for Efficient Dual-System Vision-Language-Action Model Inference](../Inbox/2026-05-04--latent-bridge-feature-delta-prediction-for-efficient-dual-system-vision-language-action-model-inference.md): Summary reports Latent Bridge method, VLM-call reduction, latency, and success rates.
- [Understanding Asynchronous Inference Methods for Vision-Language-Action Models](../Inbox/2026-05-04--understanding-asynchronous-inference-methods-for-vision-language-action-models.md): Summary reports the asynchronous-inference comparison and high-delay results.
