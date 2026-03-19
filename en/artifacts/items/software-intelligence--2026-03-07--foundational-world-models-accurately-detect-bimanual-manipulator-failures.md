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
- robot-failure-detection
- world-models
- bimanual-manipulation
- conformal-prediction
- vision-foundation-models
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# Foundational World Models Accurately Detect Bimanual Manipulator Failures

## Summary
This paper proposes a probabilistic world model trained in the compressed latent space of a vision foundation model for real-time detection of anomalous failures in bimanual manipulators. The core idea is to learn only the temporal dynamics of "normal behavior" and treat the model's predictive uncertainty as a failure signal.

## Problem
- When bimanual manipulators are deployed in high-risk settings, failures can cause performance degradation, equipment damage, or safety risks to people, so reliable online failure detection is needed.
- The robot state space consists of multi-view images, actions, and proprioception, making it extremely high-dimensional and preventing manual enumeration or definition of all failure modes.
- Existing statistical or simple reconstruction-based anomaly detection methods struggle to capture anomalous deviations in high-dimensional, temporal, multimodal robot behavior.

## Approach
- A pretrained vision foundation model, **NVIDIA Cosmos Tokenizer**, is used to compress multi-view images into a latent space, and a **history-conditioned probabilistic world model** is trained on top of it. The model takes a window of past images, proprioception, and actions as input and predicts the distribution over the next state.
- The world model uses a **VAE-style** mechanism that not only produces predictions but also outputs the standard deviation of the latent variable distribution; the mean of this standard deviation is used as the **world model uncertainty score**.
- A second score is also defined: **world model prediction error**, i.e., the difference between the predicted next-step latent representation and the latent representation of the true observation.
- The model is trained using only **nominal trajectories**, and **conformal prediction** is used to calibrate a threshold on held-out nominal data; at runtime, if a trajectory statistic exceeds the threshold, it is classified as anomalous/failure.
- The method is compared against multiple baselines, including normalizing flow, autoencoder reconstruction error, nearest-neighbor safe-set similarity, SPARC, PCA+K-means, and a random baseline; the paper also introduces a new **Bimanual Cable Manipulation** dataset.

## Results
- On the **Bimanual Cable Manipulation** dataset, using an **85% conformal threshold**, **WM uncertainty** achieves **92.0% ± 6.4** weighted total classification accuracy, including **87.9% ± 17.0** nominal accuracy and **95.1% ± 5.5** failure accuracy, the best in the table.
- On the same dataset, **WM prediction error** achieves **87.9% ± 6.4** weighted accuracy; the next-best learning baseline, **logpZO**, reaches **89.3% ± 6.8**, while **AE reconstruction** is only **61.0% ± 4.2** and **AE sim** is **66.4% ± 6.1**.
- The advantage over statistical methods is substantial: **SPARC 42.6% ± 6.8**, **PCA K-means 48.6% ± 12.6**, and **Random 38.7% ± 6.4**, showing that the world-model approach is significantly stronger on this task.
- The paper states that the method has only **569.7k** trainable parameters, while the “next-best learning-based method” has about **10M** parameters, or roughly **1/20** the parameter count; at the same time, its failure detection rate is still **3.8 percentage points higher**.
- In the **Push-T** simulation, the authors construct **4** failure modes (two recoloring variants, reduced friction, and removed friction), using **1028** nominal training trajectories, **128** nominal validation trajectories, **512** nominal test trajectories, and **2048** failure trajectories; the results show that world-model uncertainty can separate visual anomalies and dynamics anomalies from nominal trajectories, though the excerpt does not provide the full quantitative metrics for this experiment.
- The newly introduced **Bimanual Cable Manipulation** dataset contains **83** nominal training/validation trajectories, **7** nominal calibration trajectories, **7** nominal test trajectories, and **9** failure test trajectories; the task is bimanual cable insertion in data center maintenance, and the main failure mode is **dropping the cable**.

## Link
- [http://arxiv.org/abs/2603.06987v1](http://arxiv.org/abs/2603.06987v1)
