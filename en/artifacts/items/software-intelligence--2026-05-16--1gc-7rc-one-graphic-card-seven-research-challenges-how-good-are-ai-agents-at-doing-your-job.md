---
source: arxiv
url: https://arxiv.org/abs/2605.17046v2
published_at: '2026-05-16T15:35:22'
authors:
- Robin-Nico Kampa
- Fabian Deuser
- "Anna B\xF6\xDFend\xF6rfer"
- Konrad Habel
- Norbert Oswald
topics:
- coding-agents
- ml-benchmark
- automated-ml-engineering
- code-intelligence
- agent-evaluation
- single-gpu-training
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# 1GC-7RC: One Graphic Card -- Seven Research Challenges! How Good Are AI Agents at Doing Your Job?

## Summary
1GC-7RC is a benchmark for autonomous coding agents that build and train ML models under fixed compute limits. It tests whether agents can write useful training code across seven ML tasks on one A100 GPU without internet access.

## Problem
- Existing ML-agent benchmarks often allow pretrained weights, loose time limits, open-ended scoring, or narrower task coverage.
- The paper targets a practical question: can coding agents design, implement, train, and tune models from scratch across language, vision, graphs, tabular data, time series, and text classification?
- This matters because ML teams may use coding agents for end-to-end model work, and fixed metric-based tests are needed to compare agent behavior and failure modes.

## Approach
- The benchmark contains 7 tasks: TinyShakespeare language modeling, TinyImageNet classification, Pascal VOC segmentation, ogbg-molhiv graph classification, Forest Cover tabular classification, ETTh1 forecasting, and AG News text classification.
- Each task gives the agent a baseline `train.py`, a locked `prepare.py`, local data, and a metric. The agent can write improved `run_{x}.py` files, train models, and save scored checkpoints.
- Six tasks ban pretrained weights. The segmentation task allows two pre-downloaded DINOv3 backbones because useful Pascal VOC segmentation is hard to train from scratch within the budget.
- Runs use one NVIDIA A100 80 GB GPU, no internet, no package installation, and task budgets of 40 to 120 minutes.
- Scoring uses deterministic metrics and repeats each agent-task pair 5 times. The study evaluates 7 agents, for 245 total runs.

## Results
- The benchmark baselines are: T1 TinyShakespeare 3.438 bpb, T2 TinyImageNet 0.343 top-1 accuracy, T3 Pascal VOC 0.660 mIoU, T4 ogbg-molhiv 0.706 AUROC, T5 Forest Cover 0.806 accuracy, T6 ETTh1 0.384 MSE, and T7 AG News 0.793 accuracy.
- The excerpt shows one full agent row: Claude Code with Sonnet 4.6 reaches 2.2325 ± 0.2097 bpb on T1, 0.6813 ± 0.0252 accuracy on T2, 0.8322 ± 0.0074 mIoU on T3, 0.7663 ± 0.0116 AUROC on T4, 0.9632 ± 0.0063 accuracy on T5, 0.3809 ± 0.0049 MSE on T6, and 0.9211 ± 0.0024 accuracy on T7.
- Sonnet 4.6 improves over the provided baseline on all 7 visible task metrics, with the largest visible relative gains on TinyImageNet, Pascal VOC, Forest Cover, and AG News.
- The paper reports an aggregate baseline-relative score for Sonnet 4.6 of +0.293 across the 7 tasks.
- The study compares 7 agents: Claude Sonnet 4.6, Claude Opus 4.6, Claude Opus 4.7, GPT-5.5 via Codex CLI, Qwen 3.6+ via OpenCode, and Kimi K2.5/K2.6 via OpenCode. The supplied excerpt says proprietary agents outperform open-source alternatives, but the full per-agent table is truncated here.

## Link
- [https://arxiv.org/abs/2605.17046v2](https://arxiv.org/abs/2605.17046v2)
