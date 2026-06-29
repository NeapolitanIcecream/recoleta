---
source: arxiv
url: https://arxiv.org/abs/2606.27243v1
published_at: '2026-06-25T16:30:39'
authors:
- Shaohua Liu
- Liang Fang
- Yilong Sun
- Shudong Huang
- Qingsong Luo
- Xiaoyang Chen
- Dongqiang Liu
- Chuangang Ma
- Zhenzhen Chai
- Henghuan Wang
- Shijie Quan
- Changyuan Cui
- Zhangbin Zhu
- Peng Chen
- Wei Xu
- Lei Xiao
- Haijie Gu
- Jie Jiang
topics:
- multi-agent-software-engineering
- code-intelligence
- automated-software-production
- recommender-systems
- architecture-search
- model-verification
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems

## Summary
NOVA is an agent harness for changing production recommender architectures while checking whether each generated change is structurally valid before costly training or online tests.

## Problem
- Industrial ad recommenders gain value from architecture changes such as RankMixer, TokenMixer-Large, and MixFormer, but these changes need expert work across model graph, feature routing, shapes, dtypes, serving limits, and business metrics.
- AutoML mainly tunes local hyperparameters, while generic LLM coding agents can produce code that runs yet breaks recommender semantics, such as masks, attention behavior, or logit fusion.
- These runnable invalid candidates can cause silent failures that waste training and online experiment budget and may hurt AUC, calibration, GMV, or bias.

## Approach
- NOVA stores each candidate architecture as model graph, structural hyperparameters, and feature configuration.
- Its core mechanism is an architecture gradient: a structured update signal built from the previous change, verification diagnostics, offline metric change, and search history.
- The harness proposes architecture modifications, filters infeasible or forbidden directions, checks semantic validity and local executability, then trains surviving candidates for offline AUC.
- Failed candidates are written back as forbidden directions so later rounds avoid similar structural mistakes.
- L1–L4 task levels control risk: simple tuning and ScaleUp can run automatically, while uncovered or high-risk literature-transfer and open-ended tasks can require human confirmation.

## Results
- In an industrial advertising system serving over 1 billion users, NOVA reports the highest effective pass rate on L2 ScaleUp and L3 Literature-to-Production tasks: 54.5% EPR for L2 and 60.0% EPR for L3.
- On L3 Literature-to-Production, NOVA reports 86.7% LPR and 60.0% EPR, with EPR more than 2x the human expert loop baseline.
- One Literature-to-Production cycle took over 13x less human-attended time than the reported manual process.
- Online A/B tests for the selected L3 candidate improved GMV on three pCVR objectives by +1.25%, +1.70%, and +2.02%.
- The same online tests reduced pCVR bias by 58.8%, 66.7%, and 37.3% on the three objectives.
- The excerpt says NOVA reduces silent failures versus coding-agent baselines, but it does not give the exact silent-failure rate in the provided text.

## Link
- [https://arxiv.org/abs/2606.27243v1](https://arxiv.org/abs/2606.27243v1)
