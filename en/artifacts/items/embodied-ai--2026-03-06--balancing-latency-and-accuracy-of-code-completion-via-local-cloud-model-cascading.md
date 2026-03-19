---
source: arxiv
url: http://arxiv.org/abs/2603.05974v2
published_at: '2026-03-06T07:15:36'
authors:
- Hanzhen Lu
- Lishui Fan
- Jiachi Chen
- Qiuyuan Chen
- Zhao Wei
- Zhongxin Liu
topics:
- code-completion
- model-cascading
- speculative-decoding
- retrieval-augmented-generation
- latency-accuracy
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Balancing Latency and Accuracy of Code Completion via Local-Cloud Model Cascading

## Summary
This paper proposes MCCom, which cascades a local small model with a cloud large model to achieve both low latency and high accuracy in code completion. The core idea is to use the fast small model by default, and only escalate to the large model when confidence is low or user behavior indicates dissatisfaction, while enabling the two to collaborate through speculative decoding and iterative retrieval.

## Problem
- Line-level code completion requires **real-time** responses; excessive latency disrupts developer flow. The paper cites that **44%** of developers expect statement-level completion to finish within **0.5 seconds**.
- Existing methods involve a clear trade-off: large models are accurate but usually slower and more expensive; static analysis and small models are faster, but their completion quality is insufficient in complex scenarios.
- The key challenges are **when** to invoke the cloud large model, and **how** to make the local small model and large model collaborate effectively rather than duplicating computation.

## Approach
- The paper proposes **MCCom**: a local **121M** small model generates completions by default, and only escalates to a cloud large model when necessary, achieving a latency-accuracy trade-off.
- The routing strategy has two steps: first, it uses the average probability of the small model's first **3 tokens** as a confidence score, and escalates directly if it falls below a threshold; if the small model result is shown first, it then determines whether the user implicitly rejected it based on whether the user accepted it or kept typing, and triggers escalation accordingly.
- It adopts **two-stage speculative decoding**: first, it uses context/retrieved code as a cheap draft to accelerate the small model; if the small model result is rejected, it then uses that output as the speculative draft for the large model to accelerate large-model decoding.
- It adopts **iterative retrieval**: the initial retrieval constructs a query using left and right context; if the small model result is rejected, that output is used for a second retrieval round, and the original query score and small-model-output score are fused with weighted averaging based on small-model confidence to supplement more relevant repository context.
- Because suitable small models were lacking, the authors also trained a code-completion-specific **121M** model from scratch, using **41M** Python samples for training and **41K** for validation.

## Results
- On RepoEval and the newly constructed **StmtEval**, MCCom reduces inference latency by **5.8%–47.9%**, with an average speedup of **25.6%**.
- MCCom reduces cloud/large-model invocations by an average of **46.3%**, showing that the cascading strategy can significantly save computation and serving costs.
- Compared with the baseline that “always invokes the large model,” MCCom improves exact match rate by an average of **8.9%**, with gains ranging from **2.9%–13.5%**.
- The authors' trained **121M** small model reaches **73.8%** of the average performance of the state-of-the-art **7B** model; in the motivation experiment, even without RAG, this small model can produce correct completions on **37.8%** of samples.
- The paper also reports that when this **121M** local model runs on the client side, it is about **2×** faster than a **7B** large model deployed in the cloud on an **Nvidia A800 GPU**.
- The paper claims the method is consistently effective across multiple large models, but the excerpt does not provide a more detailed complete per-model table.

## Link
- [http://arxiv.org/abs/2603.05974v2](http://arxiv.org/abs/2603.05974v2)
