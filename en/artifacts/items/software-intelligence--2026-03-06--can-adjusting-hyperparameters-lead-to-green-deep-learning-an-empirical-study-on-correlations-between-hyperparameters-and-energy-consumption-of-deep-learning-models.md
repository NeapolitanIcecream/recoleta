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
relevance_score: 0.44
run_id: materialize-outputs
language_code: en
---

# Can Adjusting Hyperparameters Lead to Green Deep Learning: An Empirical Study on Correlations between Hyperparameters and Energy Consumption of Deep Learning Models

## Summary
This paper studies whether hyperparameter adjustments during deep learning training affect energy consumption, and examines whether it is possible to achieve "greener" training without harming performance. The conclusion is that many hyperparameters are correlated with energy consumption, and this sensitivity is even stronger during parallel training.

## Problem
- Existing deep learning increasingly relies on larger datasets and more complex models, causing training energy use and costs to keep rising, along with higher carbon emissions.
- Previous research has mostly focused on the impact of hyperparameters on performance metrics such as accuracy, but the question of "how hyperparameters affect energy consumption" lacks systematic empirical evidence.
- This matters because if training energy consumption can be reduced simply through hyperparameter tuning without lowering performance, then green AI practices can be improved at very low engineering cost.

## Approach
- The authors model "hyperparameter tuning" as a **hyperparameter mutation** process: around the original default configuration, they randomly change epochs, learning rate, and a third hyperparameter specific to each model (weight decay, gamma, or threshold).
- Using 5 real open-source deep learning models and 3 commonly used datasets, they separately train the original models and mutated models, recording package, RAM, and GPU energy consumption, as well as performance metrics such as training time and accuracy.
- They use `perf` and `nvidia-smi` to collect energy data, and conduct comparative analysis under both **single-model training** and **two-model parallel training** scenarios.
- They use Spearman correlation analysis to study the relationship between "hyperparameters and energy/performance"; they use the Wilcoxon signed-rank test and Cliff’s delta to compare the energy-performance trade-offs of mutated models and original models, determining whether greener configurations emerge.
- The experiments construct a total of **375 mutated models** (5 models × 3 hyperparameters × 5 mutations × 5 runs); elsewhere the paper also states that the study covers "five models," while one part of the contribution section says "six models," indicating an inconsistency in wording.

## Results
- In the single-model scenario, **epochs shows the most stable correlation with energy consumption**: in Table 4, epochs is **0/0/0/0/6** for package/ram/gpu energy, and the total is **0/0/0/0/18**, indicating that the 6 correlation tests counted by the authors are all significant correlations in the same direction.
- In the single-model scenario, **the effect of learning rate is more complex but more widespread**: in Table 4, the total is **0/4/13/1/0**; for the corresponding performance and time results (Table 5), the total is **0/5/6/1/0**, indicating that learning rate affects energy, time, and performance simultaneously.
- In the parallel scenario, correlations are clearly stronger: in Table 6, the total for epochs is **0/0/0/0/30**, the total for learning rate is **1/5/23/1/0**, and the total for weight decay is **0/3/13/2/0**. Compared with the single-model scenario, this covers more significant relationships, supporting the conclusion that "energy consumption is more sensitive to hyperparameters during parallel training."
- The paper provides a concrete example: when lowering the learning rate on a Siamese network, **average GPU energy consumption decreases by about 1.6 kJ**, while **average accuracy remains basically unchanged**, showing that hyperparameter tuning can reduce training energy consumption while maintaining performance.
- The authors claim that across five real models and three types of datasets, they observe that some mutated configurations are **greener** than the default configuration, meaning **lower energy consumption with comparable or better performance**; however, in the provided excerpt, RQ2 does not give the complete significance values for each model, specific energy reduction amounts, or a unified baseline improvement percentage.

## Link
- [http://arxiv.org/abs/2603.06195v1](http://arxiv.org/abs/2603.06195v1)
