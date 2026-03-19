---
source: arxiv
url: http://arxiv.org/abs/2603.08165v1
published_at: '2026-03-09T09:46:28'
authors:
- Mohammad Abboush
- Ehab Ghannoum
- Andreas Rausch
topics:
- fault-diagnosis
- automotive-software
- explainable-ai
- cnn-gru
- hil-simulation
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# An explainable hybrid deep learning-enabled intelligent fault detection and diagnosis approach for automotive software systems validation

## Summary
This paper proposes an explainable hybrid deep-learning-based fault detection and diagnosis method for real-time validation of automotive software systems, combining 1dCNN-GRU with multiple XAI techniques to detect, identify, and localize faults from HIL test recordings. Its core selling point is turning an originally “black-box” diagnostic model into an explainable, optimizable white-box version, especially for single-fault and concurrent-fault scenarios.

## Problem
- Automotive software systems generate large volumes of complex time-series test recordings during HIL/real-time validation, which are difficult to analyze efficiently with manual or traditional rule-based methods, and root-cause localization is hard.
- Existing DL fault detection and diagnosis models are usually black boxes, making it difficult for engineers to understand “why the model made this decision,” which reduces trust in safety-critical scenarios and increases the cost of model optimization.
- Concurrent faults, class imbalance, and high-noise data further increase the difficulty of fault identification and localization, while most existing explainable FDD work focuses only on single faults.

## Approach
- Use an HIL real-time simulation platform to collect automotive software system test data, combining user driving behavior, virtual test drives, and CAN-bus-based fault injection to build datasets for healthy states, fault types, and fault locations.
- Preprocess the time-series data, including denoising, cleaning anomalous/redundant information, normalization, windowing, and using resampling strategies such as RUS, Class Weights, and SMOTE to address class imbalance.
- Build a hybrid 1dCNN-GRU model: 1dCNN extracts local patterns from raw time series, GRU models temporal dependencies, and a final fully connected layer outputs predictions of fault class/location; the fault-type classification model described in the paper has 199,335 parameters.
- Introduce four XAI methods—Integrated Gradients, DeepLIFT, Gradient SHAP, and DeepLIFT SHAP—to explain model predictions, identify key variables, and support root-cause analysis and feature selection.
- Construct a simplified “white-box” model based on the explanation results, aiming to reduce computational cost and model complexity while maintaining or improving diagnostic performance.

## Results
- The paper explicitly claims that on the HIL real-time simulation dataset, the proposed method outperforms state-of-the-art models in fault-type diagnosis and fault-location localization, but the current excerpt **does not provide specific accuracy, F1, AUC, or relative improvement percentages**.
- One of the most specific quantifiable points provided is that the paper compares four XAI techniques, focusing on differences in computational overhead and performance, but the excerpt **does not provide concrete numerical results**.
- The paper states that the method can handle **single faults and concurrent faults**, and is applicable to **class-imbalanced data**, which extends beyond many existing approaches that only handle single faults.
- The paper claims that XAI-driven identification of important variables can produce a **low-computational-cost, low-complexity** white-box DL model while also supporting engineers in root-cause analysis; however, the excerpt **does not provide compression ratios, inference latency, or resource-saving figures**.
- Visible structural figures include: the fault-type classification model (FTCM) has a total of **199,335** parameters, and the final output is **7 classes**; this suggests the model size is relatively moderate, but this is not a performance metric.

## Link
- [http://arxiv.org/abs/2603.08165v1](http://arxiv.org/abs/2603.08165v1)
