---
source: arxiv
url: http://arxiv.org/abs/2603.05839v1
published_at: '2026-03-06T02:49:49'
authors:
- Anushka Debnath
- Stephen Cranefield
- Bastin Tony Roy Savarimuthu
- Emiliano Lorini
topics:
- llm-interpretability
- trust-modeling
- activation-space
- contrastive-prompting
- white-box-analysis
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Evaluating LLM Alignment With Human Trust Models

## Summary
This paper studies whether large language models internally represent “trust” in a way that resembles human trust theories. Through a white-box analysis of GPT-J-6B’s activation space, the authors find that its internal representation of “trust” is closest to Castelfranchi’s socio-cognitive trust model, followed by the Marsh model.

## Problem
- Existing research on LLM trust reasoning is mostly black-box, focusing only on inputs and outputs, with very little understanding of how the model represents “trust” **internally**.
- Without knowing which human trust theories an LLM’s internal trust concept aligns with, it is difficult to judge whether its social reasoning is reliable or to design interpretable trust mechanisms for human–AI collaboration systems.
- Trust is important for cooperation, multi-agent systems, and human–computer interaction, so understanding how LLMs encode trust has practical significance.

## Approach
- The study uses the open-source model **EleutherAI/gpt-j-6B**, whose layer activations are accessible, and performs a white-box analysis of its hidden representations.
- Trust-related concepts are extracted from 5 classic human trust models, and dyadic relationships are treated as directed binary relations (e.g., Katherine→Alice and Alice→Katherine).
- Using **contrastive prompting**, the authors generate 100 one-sentence stories for both positive and negative cases of each concept; they average tokens and samples across the hidden states of GPT-J-6B’s 28 layers, then compute a concept vector as “positive mean - negative mean,” and finally average across layers into a single concept embedding.
- They first expand 30 emotion/relationship concepts into 60 directional concepts, compute the pairwise cosine similarity distribution, and set **0.6** (the top 20% of similarities) as the threshold for “significant alignment.”
- They then compute cosine similarities between trust1 and the concepts associated with each trust model, and compare models using two metrics: **average similarity** and **number of concepts exceeding the 0.6 threshold**.

## Results
- In the pairwise comparisons among 60 general concepts, the authors set **cosine similarity 0.6** as the threshold for significant alignment, corresponding to the **top 20%** of the overall distribution.
- By **average cosine similarity**, the alignment between the 5 trust models and trust1 ranks from high to low as: **Castelfranchi 0.7303** > **Marsh 0.6973** > **McAllister 0.6704** > **McKnight 0.6640** > **Mayer 0.4530**.
- By **number of concepts exceeding the threshold**, the results are: **Castelfranchi 8** > **Marsh 7** > **Mayer 5** = **McKnight 5** > **McAllister 4**.
- In the Castelfranchi model, concepts highly similar to trust1 include: confidence1 **0.9225**, reputation1 **0.8963**, willingness2 **0.8858**, competence2 **0.8504**, commitment2 **0.8450**, security1 **0.8089**, reliability2 **0.7667**, predictable2 **0.7141**.
- The paper also notes some negative similarities that are inconsistent with theory: in the Mayer model, **risk1 = -0.8462** and **benevolence2 = -0.1434**; in the McKnight model, **benevolence2 = -0.1434**. This suggests that GPT-J-6B does not necessarily encode the relationship between “risk” or “benevolence” and trust in the way these theories assume.
- The core conclusion is that GPT-J-6B’s internal trust representation more closely resembles a **socio-cognitive** view of trust rather than a purely organizational behavior or initial-trust framework; the authors treat this as evidence that LLM activation spaces can be used to compare theories of social cognition.

## Link
- [http://arxiv.org/abs/2603.05839v1](http://arxiv.org/abs/2603.05839v1)
