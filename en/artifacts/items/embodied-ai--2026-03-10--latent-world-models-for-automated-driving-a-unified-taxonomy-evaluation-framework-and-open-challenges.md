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
- latent-representations
- evaluation-framework
- survey
relevance_score: 0.52
run_id: materialize-outputs
language_code: en
---

# Latent World Models for Automated Driving: A Unified Taxonomy, Evaluation Framework, and Open Challenges

## Summary
This is a survey/position paper on latent world models for automated driving, proposing a unified taxonomy, evaluation framework, and list of open challenges. Its core value lies in comparing previously fragmented approaches in generation, planning, reinforcement learning, and reasoning under a single “latent representation” perspective, while emphasizing closed-loop deployment and resource constraints.

## Problem
- Automated driving requires long-horizon decision-making from high-dimensional multi-sensor inputs, but real-world long-tail/dangerous scenarios are scarce, closed-loop validation is expensive, and pure simulation suffers from a sim-to-real gap.
- Existing research is fragmented by task or architecture (prediction, planning, diffusion, Transformer, open-loop/closed-loop), making it hard to explain which design choices truly affect robustness, generalization, and safety.
- Open-loop perception or generation metrics often do not align with closed-loop driving performance, so there is a lack of unified analysis and evaluation principles aimed at “deployable decision-making.”

## Approach
- The paper proposes a unified latent-space framework that organizes automated driving world models by **latent targets** (worlds/actions/generators), **latent forms** (continuous/discrete/hybrid), and **structural priors** (geometry/topology/semantics).
- It organizes methods into four major paradigms: neural simulation and world modeling, latent-space planning and reinforcement learning, generative data synthesis and scene editing, and cognitive reasoning with latent chain-of-thought.
- It distills five cross-method internal mechanisms: structural isomorphism, long-horizon temporal stability, semantic/reasoning alignment, value-aligned objectives and post-training, and adaptive computation with deliberate reasoning.
- It further proposes evaluation recommendations: emphasizing a closed-loop metric suite and adding a resource-aware deliberation cost to reduce the mismatch between open-loop scores and closed-loop safety.

## Results
- This paper **does not report new experimental quantitative results**; based on the provided abstract and excerpt, its main contribution is a structured synthesis and evaluation agenda rather than proposing and validating a new model.
- It explicitly claims **5** contributions: a unified taxonomy, a summary of **5** internal mechanisms, a closed-loop evaluation suite and resource cost, design recommendations and a research agenda, and a synthesis of representative benchmarks and methods.
- The methodological landscape it covers includes at least **4** major categories: neural simulation, latent planning/RL, data synthesis/editing, and cognitive reasoning/latent CoT.
- The core evaluation claim is that **open-loop / closed-loop mismatch** should be reduced, and that “deliberate reasoning under resource constraints” should be incorporated into evaluation rather than focusing only on visual realism or open-loop prediction error.
- The paper lists many representative methods (such as BEVWorld, OmniGen, Think2Drive, WorldRFT, LCDrive, FutureX, etc.), but the provided text **does not include unified numerical comparisons, specific dataset results, or percentage improvements**.

## Link
- [http://arxiv.org/abs/2603.09086v1](http://arxiv.org/abs/2603.09086v1)
