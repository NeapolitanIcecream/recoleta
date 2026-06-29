---
source: arxiv
url: http://arxiv.org/abs/2604.22102v1
published_at: '2026-04-23T22:17:45'
authors:
- Arthur Jakobsson
- Abhinav Mahajan
- Karthik Pullalarevu
- Krishna Suresh
- Yunchao Yao
- Yuemin Mao
- Bardienus Duisterhof
- Shahram Najam Syed
- Jeffrey Ichnowski
topics:
- dynamic-rope-manipulation
- system-identification
- sim-to-real
- zero-shot-control
- trajectory-optimization
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Wiggle and Go! System Identification for Zero-Shot Dynamic Rope Manipulation

## Summary
Wiggle and Go! estimates rope dynamics from one short probing motion, then uses those estimated parameters to plan a dynamic rope action in simulation and execute it in the real world without trial-and-error. The paper targets zero-shot rope tasks where failed attempts can be costly or unsafe.

## Problem
- Dynamic rope manipulation is hard because rope behavior depends on hidden properties such as stiffness, damping, mass distribution, and link count.
- Prior methods often need large real-world datasets or several task attempts to adapt, which is a poor fit when a bad throw can tangle, damage, or miss in ways that are hard to recover from.
- The paper aims to infer rope-specific dynamics once, reuse that estimate across tasks, and execute a goal-conditioned action zero-shot.

## Approach
- The method has two stages: perform a predefined low-risk "wiggle" to observe rope motion, then predict rope parameters and use them to optimize a task action.
- A temporal convolutional network takes tracked 2D rope keypoints and angle features from the wiggle and predicts 9 simulator parameters, including stiffness, damping, rope length, mass per unit length, lead mass, and link count.
- The model is trained in simulation, where parameter labels are known, with sim-to-real randomization for camera calibration noise, tracking noise, delayed recording, and masked time windows.
- For each task goal, the system runs CMA-ES trajectory optimization in Drake using the predicted rope parameters, then executes the resulting robot trajectory on an xArm 7.
- The same system-identification module is task-agnostic and is reused across three downstream tasks: 3D target striking, lobbing, and draping.

## Results
- On real 3D target striking, the method reports **3.55 cm average accuracy** when using predicted rope system parameters, compared with **15.34 cm** when the action model is not informed by system parameters.
- In the introduction, the paper also reports **median striking accuracy of 3.55 cm in real** and **2.1 cm in simulation**, versus **15.29 cm in real** and **12.8 cm in simulation** for the non-parameter-informed baseline.
- For transfer of identified dynamics to a different motion context, the paper reports a **Pearson correlation coefficient of 0.95** between Fourier frequencies of predicted-rope and real-rope behavior on an unseen trajectory.
- On more complex downstream tasks, the paper claims **over 50% success rate** for **lobbing** and **draping**.
- In the wiggle ablation table, the main wiggle gives low mean absolute error on several predicted parameters, including **0.098** for link count, **0.006 m** for rope length, **0.010 N·s/m** for ball damping, **0.002 m** for rope radius, **0.007 kg/m** for mass per unit length, **0.005 kg** for lead mass, and **0.111 N/m** for ball stiffness, with random wiggles performing worse on several parameters.
- The paper claims one wiggle observation can support multiple manipulation policies without retraining the identification module.

## Link
- [http://arxiv.org/abs/2604.22102v1](http://arxiv.org/abs/2604.22102v1)
