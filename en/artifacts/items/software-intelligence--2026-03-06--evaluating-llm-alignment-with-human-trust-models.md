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
- white-box-analysis
- activation-space
- human-ai-interaction
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Evaluating LLM Alignment With Human Trust Models

## Summary
This paper investigates whether large language models truly “understand” human trust theories internally, rather than merely appearing able to talk about trust in their outputs. Through a white-box analysis of GPT-J-6B’s activation space, the authors find that its internal representation of “trust” is closest to Castelfranchi’s socio-cognitive trust model, followed by the Marsh model.

## Problem
- The paper addresses the question of how LLMs internally represent “trust,” and whether that representation is consistent with existing human trust theories.
- This matters because trust is a core factor in human–AI collaboration, multi-agent cooperation, and decision-making; if the model’s internal trust representation is highly biased or misaligned, both system design and behavior interpretation may be affected.
- Prior work has mostly taken a black-box input–output view, lacking direct white-box examination of internal activations and conceptual structure.

## Approach
- The authors use the open-source model **EleutherAI/gpt-j-6B**, whose layer activations are accessible, to conduct a white-box analysis of its internal representations related to “trust.”
- They compile trust-related concepts from 5 classic human trust models, then use **contrastive prompting** to construct “positive story vs. negative story” examples for each concept, producing concept direction vectors.
- Within a fixed workplace context involving software engineering colleagues, they generate bidirectional relational concepts such as Katherine→Alice and Alice→Katherine; each concept is built from **100** positive and **100** negative one-line stories.
- They extract representations from the **28 layers** of GPT-J-6B’s hidden states; for each layer, each token is **4096-dimensional**. They first average over tokens, then over samples, and finally compute “positive mean - negative mean” to obtain a concept vector, which is then averaged across layers into a single concept embedding.
- They first expand **30 emotion/relationship concepts** into **60 bidirectional concepts**, compute the distribution of pairwise cosine similarities, and use **0.6**, corresponding to the **80th percentile**, as the threshold for “significant alignment”; they then compare trust against concepts from each trust model by mean similarity and number of above-threshold matches.

## Results
- In the pairwise similarity analysis over 60 general concepts, the authors set **0.6** as the significant alignment threshold, corresponding to the **top 20%** of the cosine similarity distribution across all concept pairs.
- Among the five trust models, the **Castelfranchi model** has the highest average similarity with trust1 at **0.7303**, with **8** concepts exceeding the threshold; this is the paper’s main conclusion.
- The **Marsh model** ranks second, with an average similarity of **0.6973** and **7** concepts above threshold; it is followed by **McAllister 0.6704 (4 concepts)**, **McKnight 0.6640 (5 concepts)**, and **Mayer 0.4530 (5 concepts)**.
- In the Castelfranchi model, the concepts closest to trust1 include: **confidence1 0.9225**, **reputation1 0.8963**, **willingness2 0.8858**, **competence2 0.8504**, **commitment2 0.8450**, and **security1 0.8089**.
- The paper also finds that a small number of concepts that should theoretically be positively correlated are instead negatively correlated in the model’s internal space; for example, in the Mayer model, **risk1 = -0.8462** and **benevolence2 = -0.1434**. Based on this, the authors argue that the LLM’s internal representations do not fully follow traditional theoretical definitions.
- There is no direct baseline comparison against other LLMs, other white-box methods, or downstream task accuracy; the core contribution is the first quantitative alignment analysis of LLM internal “trust” concepts against human trust models using a white-box activation-similarity framework.

## Link
- [http://arxiv.org/abs/2603.05839v1](http://arxiv.org/abs/2603.05839v1)
