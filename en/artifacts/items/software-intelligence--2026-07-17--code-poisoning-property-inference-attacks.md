---
source: arxiv
url: https://arxiv.org/abs/2607.15970v1
published_at: '2026-07-17T14:04:59'
authors:
- Xukun Luan
- Yuhui Gong
- Gang Zhang
- Zixuan Huang
- Yuanguo Bi
- Xuesong Li
- Jinyan Liu
topics:
- code-poisoning
- property-inference
- ml-security
- privacy-attacks
- coding-agents
- software-supply-chain
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Code-Poisoning Property Inference Attacks

## Summary
CPPIA is a code-poisoning attack that makes machine-learning models reveal global properties of their private training data through label-only queries. The paper reports perfect property-inference accuracy without reducing task accuracy, shadow models, or requiring access to training data or model internals.

## Problem
- Existing property-inference attacks often require training-data access, model control, logits, or shadow models, and may reduce model accuracy or fail against defenses.
- The problem matters because users increasingly adopt opaque code from repositories and coding agents to train models on sensitive data, creating a supply-chain path for dataset-level privacy leakage.

## Approach
- A malicious code provider publishes a repository or uses a coding agent to insert poisoned training code.
- During training, the code embeds the target property into secret samples or model behavior while preserving the model's normal task performance.
- After deployment, the attacker queries the model using those secret samples and decodes the returned top-1 labels to infer whether a property exists, distinguish property proportions, or estimate the property's size.
- CPPIA assumes no access to the private training set, target model parameters, logits, or shadow models; the attacker receives only label-only black-box outputs.

## Results
- The paper reports 100% attack accuracy with no degradation in model accuracy.
- Across 4 datasets, 8 model architectures, and 18 property types, CPPIA is reported to generalize across image generation, text-to-image, regression, and natural-language-processing tasks.
- The method reportedly remains effective under 3 categories of defense mechanisms and requires minimal computational overhead without shadow models.
- As a concrete estimation result, 10 synthetic samples reportedly suffice to infer a target property's proportion to 3 decimal places, regardless of training-set size.
- The excerpt does not provide per-dataset metrics, baseline values, query counts, or numerical accuracy comparisons beyond these aggregate claims.

## Link
- [https://arxiv.org/abs/2607.15970v1](https://arxiv.org/abs/2607.15970v1)
