---
source: arxiv
url: http://arxiv.org/abs/2603.11649v1
published_at: '2026-03-12T08:20:26'
authors:
- Gal Versano
- Itzik Klein
topics:
- state-estimation
- unscented-kalman-filter
- ins-gnss-fusion
- sim2real
- neural-adaptive-filtering
relevance_score: 0.19
run_id: materialize-outputs
language_code: en
---

# A Hybrid Neural-Assisted Unscented Kalman Filter for Unmanned Ground Vehicle Navigation

## Summary
This paper proposes a hybrid neural-assisted Unscented Kalman Filter (ANPMN-UKF) for INS/GNSS navigation of unmanned ground vehicles. Without modifying the core UKF equations, it uses neural networks to predict process noise and measurement noise online. Its key selling point is that it is trained only on simulated data while achieving more robust localization accuracy gains across multiple real vehicles and environments.

## Problem
- Classical UKF typically uses fixed process noise covariance **Q** and measurement noise covariance **R**, but real roads, sensors, and environmental conditions are time-varying, which can easily degrade estimation performance or even destabilize the filter.
- Traditional model-based adaptive methods rely on innovation statistics and sliding windows. They can adapt to some changes, but have limited ability to handle complex, nonlinear, and hard-to-model noise patterns.
- This matters because UGVs require continuous, accurate, and robust navigation in tasks such as agriculture, logistics, and search and rescue; localization errors directly affect safety and mission quality.

## Approach
- The core idea is simple: **keep the standard UKF unchanged, and only let two small neural networks predict how large the current noise is**, then fill these predicted values into the UKF’s **Q** and **R**.
- Specifically, **σQ-Net** regresses 6-dimensional inertial noise standard deviations from raw IMU window data (3-axis accelerometer + 3-axis gyroscope, 1 second/100 points); **σR-Net** regresses 3-dimensional position noise standard deviations from GNSS position window data (3 channels, 1 second/100 points).
- The network backbone is lightweight 1D convolution + fully connected layers + LayerNorm, with the goal of real-time operation, and the same architecture design is shared for both types of noise estimation.
- Training uses **sim2real**: training is done only on simulated trajectories, using known ground truth to automatically generate IMU and GNSS data with different noise levels, and then using MSE to supervise learning of the noise standard deviations, avoiding extensive real-world data collection and labeling.
- The simulated data is based on five types of trajectories (straight line, rectangle, circle, sine wave, etc.), with a sampling rate of 100 Hz; the IMU noise standard deviation range is **[0.001, 0.02]**, the GNSS position noise standard deviation range is **[1.5, 3.0] m**, and each noise setting has **25** levels.

## Results
- Evaluation was conducted on **3 real datasets** totaling **160 minutes** of testing, covering **3 types of platforms**: an off-road vehicle, a passenger car, and a mobile robot, with different sensors, road surfaces, and environmental conditions.
- The paper claims an average localization accuracy improvement of **22.70%** relative to the standard UKF.
- Relative to the model-based adaptive UKF, the average localization accuracy improvement is **12.72%**; the abstract also describes this as about **12.7%** position improvement.
- The main breakthrough is not changing the UKF formulas, but showing that a neural noise estimator trained **only on simulation** can generalize to real vehicle navigation scenarios and consistently deliver gains across cross-platform and cross-environment testing.
- The provided text does not include finer per-dataset values, the specific error metric names (such as RMSE/ATE), or detailed tables against more baselines, so a more precise quantitative comparison cannot be further expanded.

## Link
- [http://arxiv.org/abs/2603.11649v1](http://arxiv.org/abs/2603.11649v1)
