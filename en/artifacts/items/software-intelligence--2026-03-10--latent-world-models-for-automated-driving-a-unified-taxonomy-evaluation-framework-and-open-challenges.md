---
source: arxiv
url: http://arxiv.org/abs/2603.09086v1
published_at: '2026-03-10T01:56:17'
authors:
- Rongxiang Zeng
- Yongqi Dong
topics:
- world-models
- autonomous-driving
- latent-representation
- evaluation-framework
- survey
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Latent World Models for Automated Driving: A Unified Taxonomy, Evaluation Framework, and Open Challenges

## Summary
This paper is a survey/position paper on latent world models for automated driving. It proposes a unified taxonomy, evaluation framework, and list of open challenges. Its core argument is that the field should be organized around **how latent representations support closed-loop decision-making**, rather than treating existing methods as fragmented by task or network architecture.

## Problem
- Automated driving requires long-horizon, safety-critical decision-making under high-dimensional multi-sensor inputs, but real-world long-tail/dangerous scenarios are scarce, while pure simulation suffers from a sim-to-real gap.
- Existing research is often fragmented along dimensions such as prediction, planning, diffusion, Transformers, and open-loop/closed-loop evaluation, making it difficult to explain which shared mechanisms truly determine robustness, generalization, and deployability.
- Open-loop perception/generation metrics often do not align with closed-loop driving safety performance, so a more unified, decision-oriented modeling and evaluation framework is needed.

## Approach
- The paper proposes a unified latent-space taxonomy for automated driving world models, organized by **latent representation target** (latent worlds / latent actions / latent generators), **representation form** (continuous / discrete / hybrid), and **structural priors** (geometry / topology / semantics).
- It places four major directions into the same comparative framework: neural simulation, latent planning and reinforcement learning, generative data synthesis/scene editing, and cognitive reasoning with latent chain-of-thought.
- The paper identifies five cross-domain "internal mechanisms": structural isomorphism, long-horizon temporal stability, semantic and reasoning alignment, value-aligned objectives and post-training, and adaptive computation/deliberative reasoning, and analyzes how they affect closed-loop robustness and deployment.
- It also proposes evaluation recommendations: not only considering open-loop metrics, but also adopting a closed-loop metric suite and including resource-aware deliberation cost to measure the cost introduced by reasoning/deliberative computation.
- Finally, it lays out a future research agenda emphasizing decision-ready, verifiable, and resource-efficient latent world model design.

## Results
- The paper's main contribution is **framework-level and methodological**, rather than introducing a new experimental model; the excerpt **does not provide new quantitative experimental results or unified benchmark numbers**.
- Its explicitly stated contributions include **5 items**: a unified taxonomy, a summary of **5** internal mechanisms, **1** closed-loop evaluation prescription, design recommendations and a research agenda, and a summary of representative benchmarks/methods to support reproducibility.
- The covered method landscape is organized into **4 categories**: Neural Simulation & World Modeling, Latent-Centric Planning & RL, Generative Data Synthesis & Scene Editing, Cognitive Reasoning & Latent CoT.
- The most specific claim in the paper is that closed-loop evaluation should address the open-loop/closed-loop mismatch and explicitly account for deliberation cost; however, the excerpt does not report any quantified improvement of this evaluation framework over existing standards.

## Link
- [http://arxiv.org/abs/2603.09086v1](http://arxiv.org/abs/2603.09086v1)
