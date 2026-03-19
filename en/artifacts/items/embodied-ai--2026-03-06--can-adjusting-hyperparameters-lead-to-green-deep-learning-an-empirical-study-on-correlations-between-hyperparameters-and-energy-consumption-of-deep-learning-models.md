---
source: arxiv
url: http://arxiv.org/abs/2603.06195v1
published_at: '2026-03-06T12:07:14'
authors:
- Taoran Wang
- Yanhui Li
- Mingliang Ma
- Lin Chen
- Yuming Zhou
topics:
- green-deep-learning
- hyperparameter-tuning
- energy-efficiency
- empirical-study
- parallel-training
relevance_score: 0.04
run_id: materialize-outputs
language_code: en
---

# Can Adjusting Hyperparameters Lead to Green Deep Learning: An Empirical Study on Correlations between Hyperparameters and Energy Consumption of Deep Learning Models

## Summary
This paper studies a very practical but often overlooked issue: tuning hyperparameters not only affects model performance, but also training energy consumption. By conducting “hyperparameter mutation” experiments on real deep learning models, the authors find that many hyperparameters are correlated with energy consumption, and that in some cases energy use can be reduced without harming performance.

## Problem
- The paper aims to solve the question: **how hyperparameters affect deep learning training energy consumption, and whether tuning them can make models more “green”**.
- This matters because larger datasets and more complex models are significantly increasing computational resources, electricity use, and carbon emissions, while also raising training and maintenance costs.
- Prior work has focused more on framework-level or performance optimization, while the **systematic relationship between hyperparameters and energy consumption** still lacks empirical analysis, especially in parallel training scenarios.

## Approach
- The core method is simple: treat the common process of “tuning” as a form of **hyperparameter mutation**. Starting from the original model, the authors randomly modify epochs, learning rate, and a third hyperparameter supported by each model (weight decay / gamma / threshold) around their default values.
- They train the original and mutated models on **5 real open-source models** and **3 datasets** (MNIST, CIFAR-10, Market-1501), collecting **CPU package, RAM, and GPU energy consumption**, training time, and accuracy.
- The mutation ranges are set around default values; for example, epochs is varied within **[0.75d, 1.25d]**, and learning rate within **[0.1d, d]** or **[d, 10d]**. For each model, they perform **5 mutations** for each of 3 hyperparameters, and each setting is run **5 times**, producing a total of **375 mutated models**.
- For analysis, they use **Spearman correlation analysis** to examine relationships between hyperparameters and energy/performance, and use the **Wilcoxon signed-rank test** and **Cliff’s delta** to compare trade-offs against the original model and determine whether greener settings exist.
- They also study **parallel training**: two models are trained in parallel at a time, and conclusions from single-model training are compared with those under parallel training.

## Results
- The paper claims that **many hyperparameters have either positive or negative correlations with energy consumption**. In the single-training scenario, Tables 4/5 show that epochs has the most stable correlation with energy: across energy metrics it shows **18** consistent correlation signals; learning rate shows **18** correlation signals on energy and **12** on time/performance.
- In the parallel scenario, energy consumption is more sensitive to hyperparameters. Table 6 shows a total of **60** energy-related correlation signals in parallel training (**30** from learning rate and **30** from epochs), clearly higher than the **54** total correlation signals in single training from Table 4; based on this, the authors argue that energy consumption changes more readily with hyperparameters in parallel environments.
- The paper gives a concrete example: when lowering the learning rate for a Siamese network, **average GPU energy consumption decreases by about 1.6 kJ**, while **average accuracy remains essentially unaffected**, serving as intuitive evidence that tuning can make training greener.
- The authors explicitly claim that some mutation settings can achieve **lower energy consumption with comparable or even better performance**, i.e., greener DL. However, in the provided excerpt, **no unified precise percentage improvement, complete baseline values, or detailed significance results for each model are given**.
- In terms of data and scale, the experiments cover **5 models, 3 datasets, and 375 mutated models**, while simultaneously measuring **pkg / ram / gpu / time / accuracy**, indicating that the conclusions are based on relatively systematic empirical evidence rather than a single case.

## Link
- [http://arxiv.org/abs/2603.06195v1](http://arxiv.org/abs/2603.06195v1)
