---
source: arxiv
url: http://arxiv.org/abs/2603.11649v1
published_at: '2026-03-12T08:20:26'
authors:
- Gal Versano
- Itzik Klein
topics:
- unscented-kalman-filter
- sensor-fusion
- ugv-navigation
- sim2real
- noise-estimation
relevance_score: 0.14
run_id: materialize-outputs
language_code: en
---

# A Hybrid Neural-Assisted Unscented Kalman Filter for Unmanned Ground Vehicle Navigation

## Summary
This paper proposes a neural-network-assisted unscented Kalman filter (ANPMN-UKF) for INS/GNSS integrated navigation of unmanned ground vehicles, adaptively estimating time-varying noise without modifying the core UKF equations. Its key selling point is training only on simulated data and then directly generalizing to multiple real vehicles and environments.

## Problem
- Traditional UKF usually uses fixed process noise covariance **Q** and measurement noise covariance **R**, making it difficult to adapt to time-varying sensor noise and environmental disturbances in the real world.
- When **Q/R** are poorly tuned, navigation and positioning performance degrades and may even cause filter instability; this is critical for continuous and reliable localization of unmanned vehicles.
- Purely model-based adaptive methods can adjust noise online, but they often struggle to capture complex, nonlinear noise variation patterns.

## Approach
- The authors propose **ANPMN-UKF**: keeping the standard UKF prediction/update equations unchanged, while adding only two small neural networks to predict noise magnitude.
- **σQ-Net** regresses inertial noise standard deviation from raw IMU windowed data (3-axis acceleration + 3-axis gyroscope, 1 second/100 points), which is used to construct the process noise covariance **Q**.
- **σR-Net** regresses position noise standard deviation from GNSS position window data (3 channels, 1 second/100 points), which is used to construct the measurement noise covariance **R**.
- The network backbone uses a shared design of 1D convolution + fully connected layers + layer normalization, aiming to be lightweight, real-time, and suitable for time-series noise regression.
- Training uses **sim2real**: 100 Hz data are generated on 5 types of simulated trajectories, with 25 noise levels injected (IMU noise standard deviation range **[0.001, 0.02]**, GNSS position noise standard deviation range **[1.5, 3.0] m**), and MSE loss is supervised using only simulated ground truth.

## Results
- Evaluated on **3 real datasets** totaling **160 minutes** of testing, covering **an off-road vehicle, a passenger car, and a mobile robot**, as well as different IMUs, road surfaces, and environmental conditions.
- The paper claims an overall average localization accuracy improvement of **22.70% over standard UKF**.
- Relative to the **model-based adaptive UKF**, the average localization improvement is **12.72%**.
- The abstract likewise emphasizes a **12.7%** position improvement over the adaptive model-based method across 3 datasets, which is broadly consistent with the **12.72%** reported in the main text.
- The text does not provide finer-grained per-dataset values, absolute errors, variances, or significance tests; the strongest quantitative conclusions are the two average relative improvements above.

## Link
- [http://arxiv.org/abs/2603.11649v1](http://arxiv.org/abs/2603.11649v1)
