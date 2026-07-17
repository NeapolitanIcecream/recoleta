---
source: arxiv
url: https://arxiv.org/abs/2607.14439v1
published_at: '2026-07-16T00:21:54'
authors:
- Andrew Liao
- Hanchen Cui
- Karthik Desingh
- Aryan Deshwal
topics:
- robot-policy-evaluation
- generalist-robot-policy
- active-learning
- real-world-robotics
- factor-based-testing
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Active Real-World Factor-Based Evaluation for Generalist Robot Policies

## Summary
The paper presents an active real-world evaluation framework that estimates how a generalist robot policy performs across task-factor variations while reducing the number of physical trials. Across 2,331 evaluations of three manipulation tasks, it reports typically saving 20–40% of trials compared with uniform-random testing.

## Problem
- Generalist robot policies can fail under changes in object position, table height, camera viewpoint, and other deployment conditions, but exhaustive real-hardware evaluation across these factors is slow and costly.
- Narrow test suites and aggregate success rates can miss failure-prone regions and misrepresent a policy’s performance distribution and deployment readiness.

## Approach
- Represent each evaluation configuration by structured task factors and model the policy’s continuous performance score over the resulting design space.
- Fit a probabilistic surrogate, primarily a Gaussian Process with an RBF kernel and automatic relevance determination, to predict performance and uncertainty from previously evaluated configurations.
- Use Bayesian active-testing acquisition functions, including posterior standard deviation, negative integrated posterior variance, BALD, and EPIG, to select the next most informative real-world configuration.
- Begin with 30 randomly selected evaluations, then sequentially evaluate selected configurations and update the surrogate until the trial budget is exhausted.

## Results
- The study covers 2,331 valid real-world configurations across three UR5e manipulation tasks, three factors, an 11×11 object-position grid, three table heights, and three scene-camera viewpoints.
- It reports more than 700 ground-truth real-world evaluations per task; each evaluation took roughly one minute.
- With a 100-trial evaluation budget, active testing typically saves 20–40 trials, or 20–40% of the work, relative to typical random testing.
- The excerpt does not provide detailed numerical surrogate-prediction errors or per-method results; its strongest concrete claim is that active testing more efficiently characterizes the policy’s performance distribution and identifies failure-prone regions than random testing.

## Link
- [https://arxiv.org/abs/2607.14439v1](https://arxiv.org/abs/2607.14439v1)
