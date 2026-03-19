---
source: arxiv
url: http://arxiv.org/abs/2603.08455v1
published_at: '2026-03-09T14:51:53'
authors:
- Zhe Hong
topics:
- world-models
- anomaly-detection
- concept-drift
- reinforcement-learning
- ood-detection
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# The Boiling Frog Threshold: Criticality and Blindness in World Model-Based Anomaly Detection Under Gradual Drift

## Summary
This paper investigates when anomaly detection based on world models suddenly shifts from blindness to awareness under "gradual observation drift," and argues that this boundary is not determined by the model alone. The authors find that detection exhibits a universal critical threshold, but periodic drift is systematically ignored, and some fragile environments fail before detection occurs.

## Problem
- The problem it addresses is: when an RL agent’s observations do not fail suddenly, but instead **drift slowly and continuously**, can the world model’s prediction error still detect anomalies in time, and what determines this "awakening boundary"?
- This matters because real-world sensor degradation, calibration shift, fogging, or gradual attacks usually occur **progressively**; if a system is only sensitive to abrupt changes, it can suffer from a "boiling frog" form of blindness.
- The authors also examine a more serious issue: in some environments, the agent may **collapse before becoming aware**, causing internal self-monitoring to fail in safety-critical settings.

## Approach
- They train PPO policies on 4 MuJoCo environments (HalfCheetah, Hopper, Walker2d, Ant), and train a forward world model for each environment, using next-state prediction error (PE) as the self-monitoring signal.
- They inject two types of observation drift: **linear drift** (monotonically accumulating over time) and **sinusoidal drift** (periodic, zero-mean), systematically scanning 16 magnitudes, with 1000 steps per episode and drift starting at step 300.
- They compare 3 detector families: the z-score-style Doubt Index, variance detectors, and percentile detectors; and sweep multiple hyperparameter settings to distinguish whether the "threshold phenomenon" is a detector artifact or a property of the world model.
- They conduct three core ablations: full threshold experiments, sinusoidal-drift control experiments, and model-capacity experiments (hidden sizes 128/512/1024), using 80 episodes per condition to estimate detection rates and confidence intervals.
- They further fit the relationship between the critical threshold \(\varepsilon^*\) and detector parameters, analyzing whether it can generalize across environments, in order to determine whether the deciding factor is the noise floor, detector sensitivity, or environment dynamics.

## Results
- **A sharp threshold exists universally**: under linear drift, all 4 environments, 3 detector families, and 3 model capacities show a **sigmoid-like jump** from about 0% to about 100% detection rate. Under DI, the \(\varepsilon^*\) ranges are: HalfCheetah **0.0003–0.004**, Hopper **0.007–0.012**, Walker2d **0.0003–0.003**, and Ant **0.0001–0.001**.
- **Sinusoidal drift is completely undetectable**: all detectors are "blind" to periodic drift across all environments and magnitudes. Even on HalfCheetah at \(\varepsilon=0.01\), linear drift raises PE spectral power to **201.6×** the baseline, while sinusoidal drift yields only **0.8×**, essentially the same as no drift.
- **Threshold position can be predicted by a power law within a single environment**: for the DI detector, \(\varepsilon^*\propto z^{\alpha}W^{\beta}\); the within-environment fit achieves \(R^2\) of **0.89–0.97** (Walker2d is **0.78** in the paper’s table), but a global cross-environment fit reaches only **0.45**, indicating that the missing variable is environment-specific dynamics, i.e., \(\partial \mathrm{PE}/\partial \varepsilon\).
- **Baseline MSE cannot predict detectability**: for example, Hopper has the lowest baseline MSE, only **0.002** (about 0.0024 in a detailed section of the paper), yet has the highest threshold; HalfCheetah has the highest baseline MSE at **0.163**, yet a lower threshold. This shows that a "more accurate model" does not necessarily mean "earlier drift detection."
- **A "collapse before awareness" region (CBA) exists**: in Hopper, the collapse rate is **>99%** at nearly all drift magnitudes; at \(\varepsilon=0.05\), the agent falls on average **25 steps** after drift begins, while the detector has still not fired. The paper notes that detection typically requires about **50 steps** of drift accumulation, creating a fatal but unmonitorable failure mode.
- **Model capacity has almost no effect on the threshold**: although HalfCheetah’s baseline MSE decreases with capacity from **0.254 → 0.163 → 0.145**, the detection curves and \(\varepsilon^*\) remain essentially unchanged; the authors therefore argue that the threshold is determined mainly by the **relative signal-to-noise ratio**, not the absolute accuracy of the world model.

## Link
- [http://arxiv.org/abs/2603.08455v1](http://arxiv.org/abs/2603.08455v1)
