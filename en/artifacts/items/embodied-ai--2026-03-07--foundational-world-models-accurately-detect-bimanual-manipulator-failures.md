---
source: arxiv
url: http://arxiv.org/abs/2603.06987v1
published_at: '2026-03-07T02:11:29'
authors:
- Isaac R. Ward
- Michelle Ho
- Houjun Liu
- Aaron Feldman
- Joseph Vincent
- Liam Kruse
- Sean Cheong
- Duncan Eddy
- Mykel J. Kochenderfer
- Mac Schwager
topics:
- world-model
- failure-detection
- bimanual-manipulation
- conformal-prediction
- robot-anomaly-detection
- foundation-vision-model
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Foundational World Models Accurately Detect Bimanual Manipulator Failures

## Summary
This paper proposes a method for runtime failure detection in bimanual robots: train a probabilistic world model in the compressed latent space of a pretrained visual foundation model, and use its uncertainty as an anomaly score. The core value is that it can detect impending or ongoing manipulation failures more reliably without explicitly enumerating failure modes in a high-dimensional space.

## Problem
- The paper addresses the problem of **how to detect anomalous failures in real time during deployment of bimanual visuomotor robots**; this matters because failures can lead to degraded performance, equipment damage, and even risks to human safety.
- The state space of such robots is enormous, including multi-view images, actions, and proprioceptive signals, making it **almost impossible to manually define all failure modes**.
- Traditional statistical or simple reconstruction-based anomaly detection methods struggle with **high-dimensional, multimodal, temporally correlated** robot behavior data.

## Approach
- First use the pretrained visual foundation model **NVIDIA Cosmos Tokenizer** to compress multi-view images into a latent space, then combine action and proprioceptive history to train a **history-conditioned probabilistic world model** that predicts the next state.
- The world model uses a **VAE-style** output of the future latent variable distribution; its **predictive variance/standard deviation** can be directly used as a score for “how uncertain I am about the current behavior.” Put simply: the model learns only “normal behavior,” and when it encounters behavior unlike the training distribution, uncertainty increases.
- The paper designs two failure scores: **(1) world model uncertainty**; **(2) world model prediction error** (the difference between the prediction and the true next state in latent space).
- It uses **conformal prediction** to automatically set thresholds on a calibration set containing only normal trajectories, thereby converting continuous scores into runtime “normal/anomalous” judgments while controlling the false positive rate.
- It also introduces a new real-world dataset, **Bimanual Cable Manipulation**, which includes multi-camera views, action/proprioceptive signals, and annotated failure trajectories, for evaluating failures such as dropped cables in real bimanual cable manipulation.

## Results
- On **Bimanual Cable Manipulation**, the authors’ method **WM uncertainty** achieves the best overall classification accuracy: **92.0±6.4%**, including **87.9±17.0%** on normal trajectories and **95.1±5.5%** on failure trajectories; the corresponding threshold is **85% conformal prediction threshold**.
- On the same dataset, **WM prediction error** reaches **87.9±6.4%** overall accuracy; it outperforms multiple baselines, but is lower than **92.0±6.4%** for WM uncertainty.
- Compared with learning-based baselines, the best author method is **about 2.7 percentage points** higher in overall accuracy than the second-best learning method **logpZO**, which has **89.3±6.8%**; the abstract also claims its **failure detection rate is 3.8% higher**.
- Compared with other baselines: **AE reconstruction error 61.0±4.2%**, **AE sim 66.4±6.1%**, **SPARC 42.6±6.8%**, **PCA K-means 48.6±12.6%**, **Random 38.7±6.4%**; this shows the method clearly outperforms statistical techniques and several common anomaly detection methods.
- In terms of parameter efficiency, the authors’ world model has only **569.7k** trainable parameters, while the second-best learning-based method has about **10M**; that is, it achieves better results with **about 1/20 the parameter count**.
- In the **Push-T** simulation, the method demonstrates the ability to distinguish **visual anomalies** (changing color) and **dynamics anomalies** (changing friction) using **1028** normal training trajectories, **128** validation trajectories, **512** normal test trajectories, and **2048** failure trajectories (**4** failure modes, **512** each), but the excerpt does not provide the full quantitative metrics for that experiment.

## Link
- [http://arxiv.org/abs/2603.06987v1](http://arxiv.org/abs/2603.06987v1)
