---
source: arxiv
url: http://arxiv.org/abs/2603.29292v1
published_at: '2026-03-31T05:55:17'
authors:
- Huan Zhang
- Wei Cheng
- Wei Hu
topics:
- code-generation
- self-improvement
- preference-optimization
- uncertainty-estimation
- code-llms
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Self-Improving Code Generation via Semantic Entropy and Behavioral Consensus

## Summary
ConSelf is a self-improvement method for code LLMs that trains without teacher models, reference solutions, or test oracles. It uses execution behavior on test inputs to choose learnable problems and to weight noisy self-generated preferences during fine-tuning.

## Problem
- The paper targets code generation when only problem descriptions and test inputs are available, while reference solutions and test oracles are missing.
- This matters because many existing code-improvement methods depend on costly teacher models or reliable oracles, which are hard to obtain in real software settings.
- Self-training is unstable here: for hard problems, a model can generate many different wrong programs, and training on that noise can waste compute or hurt performance.

## Approach
- ConSelf first samples many candidate programs per problem through **observation-guided sampling**: the model writes diverse textual observations or plans, then generates code conditioned on them.
- It computes **code semantic entropy** for each problem by executing candidates on the available test inputs, clustering programs by identical execution traces, and measuring Shannon entropy over those behavioral clusters.
- Problems with zero entropy or overly high normalized entropy are filtered out. The remaining problems form a curriculum that is more likely to contain useful learning signal.
- For each kept problem, the method assigns every candidate a **behavioral consensus score** based on how often its outputs agree with other candidates across test inputs.
- It then fine-tunes with **consensus-driven DPO (Con-DPO)**: the top-consensus candidate is paired against lower-consensus candidates, and each DPO loss term is weighted by the winner's consensus score so noisy preference pairs count less.

## Results
- The paper reports **2.73% to 3.95% relative improvement** over base models on standard code-generation benchmarks.
- The abstract and introduction say ConSelf **significantly outperforms baselines** across multiple benchmarks and backbone LLMs, but the excerpt does not provide full benchmark names, absolute scores, or per-baseline numbers.
- The paper claims code semantic entropy is a better indicator of problem learnability than internal confidence measures such as **token-level entropy** and **negative log-likelihood**.
- The paper also claims that curriculum design is critical: filtering out zero-entropy and high-entropy problems improves self-improvement quality in the no-oracle setting.

## Link
- [http://arxiv.org/abs/2603.29292v1](http://arxiv.org/abs/2603.29292v1)
