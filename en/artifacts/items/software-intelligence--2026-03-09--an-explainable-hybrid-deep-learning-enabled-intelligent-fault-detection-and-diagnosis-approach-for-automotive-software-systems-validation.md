---
source: arxiv
url: http://arxiv.org/abs/2603.08165v1
published_at: '2026-03-09T09:46:28'
authors:
- Mohammad Abboush
- Ehab Ghannoum
- Andreas Rausch
topics:
- automotive-software
- fault-diagnosis
- explainable-ai
- cnn-gru
- hardware-in-the-loop
relevance_score: 0.54
run_id: materialize-outputs
language_code: en
---

# An explainable hybrid deep learning-enabled intelligent fault detection and diagnosis approach for automotive software systems validation

## Summary
This paper proposes an explainable fault detection and diagnosis method for real-time validation of automotive software systems, combining hybrid deep learning with XAI to discover, identify, and localize faults from HIL test recordings. Its core value lies in transforming an originally hard-to-trust and hard-to-optimize black-box diagnostic model into a more interpretable and prunable white-box-style workflow.

## Problem
- The problem addressed is how to automatically analyze massive HIL test recordings during the real-time validation stage of automotive software systems (ASSs), completing fault detection, fault type identification, and fault location localization, while supporting **single faults and concurrent faults**.
- This is important because automotive system validation is constrained by safety requirements such as ISO 26262; traditional rules/tools struggle to efficiently process complex time-series data and are also weak at root cause analysis and distinguishing safety-related from critical faults.
- Existing DL-based FDD methods are effective, but they are usually black boxes; the lack of explainability reduces engineers' trust and increases the cost of model optimization and deployment, which is especially unfavorable for safety-critical real-time applications.

## Approach
- The core method is a **1dCNN-GRU hybrid model**: 1dCNN first captures local patterns from time series, then GRU models temporal dependencies, and finally fully connected layers output the fault class or fault location; this can be understood as “first finding signal segment features, then understanding how they evolve over time.”
- The data come from **HIL real-time simulation** and virtual test driving, including user driving behavior, high-fidelity automotive system models, and sensor/actuator faults injected through the CAN bus; it covers healthy, single-fault, and concurrent-fault scenarios.
- The preprocessing pipeline includes denoising, removing anomalies/redundancy, normalization, resampling, and window segmentation, and uses methods such as **RUS, Class Weights, SMOTE** to address class imbalance.
- To make the model explainable, the authors compare four XAI techniques: **Integrated Gradients, DeepLIFT, Gradient SHAP, DeepLIFT SHAP**, using them to identify important variables, support root cause analysis, and further perform feature selection and model simplification.
- The paper also presents a white-box version: key variables are retained based on interpretation results, with the goal of reducing complexity and computational cost while preserving diagnostic capability as much as possible.

## Results
- The abstract and excerpt explicitly claim that the method outperforms existing state-of-the-art models in **fault type diagnosis and fault location localization**, but the currently provided text **does not give specific accuracy, F1, recall, or comparative baseline values**.
- Quantifiable implementation details already provided include: the fault type classification model (FTCM) outputs **7 classes**, with about **199,335** total parameters; the model consists of multiple layers of Conv1d/BatchNorm/ReLU/MaxPool, **2 GRU layers**, and fully connected layers.
- The paper claims that after integrating XAI, a **high-performance, low-computational-cost** white-box DL model can be obtained, and that identifying significant variables improves performance and efficiency while reducing complexity, but the excerpt **does not provide the percentages or absolute values of these improvements**.
- The experimental data are based on an **HIL real-time simulation dataset**, considering user behavior and high-fidelity ASS models, and include **single faults and concurrent faults**; the authors also compare the computational cost and effectiveness of four XAI methods, but the current text does not provide specific ranking numbers.
- The authors claim that, to the best of their knowledge, this is the **first** study during the real-time validation stage of ASSs to combine XAI with hybrid DL-based FDD while explicitly considering concurrent faults.

## Link
- [http://arxiv.org/abs/2603.08165v1](http://arxiv.org/abs/2603.08165v1)
