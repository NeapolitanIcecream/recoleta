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
- latency-accuracy-tradeoff
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Balancing Latency and Accuracy of Code Completion via Local-Cloud Model Cascading

## Summary
This paper proposes MCCom, which improves the latency-accuracy trade-off in code completion through a cascading setup that prioritizes a local small model and switches to a cloud large model only when necessary. Its core idea is to combine user behavior for routing and enable collaboration between the small and large models through speculative decoding and iterative retrieval.

## Problem
- Line-level code completion requires **real-time low latency** and **high accuracy** at the same time, but existing solutions usually force a trade-off: large models are more accurate but slower and more expensive, while small models/static-analysis methods are faster but often not good enough.
- This matters in real development: the paper cites research stating that **44%** of developers expect statement-level completion to return within **0.5 seconds**, while **45%** of users believe the main problem with current completion tools is low quality.
- To make model cascading work, there are two key challenges: **when to escalate to the large model** and **how to enable effective collaboration between the small and large models**; otherwise, either speed or accuracy will suffer.

## Approach
- Proposes **MCCom**: by default, it first runs a **121M** small model locally and calls the cloud large model only when necessary, thereby reducing average waiting time and cloud-side compute consumption.
- The routing strategy has two steps: first, it uses the average probability of the first **3 tokens** from the small model to predict low confidence; if the small model result has already been shown, it then uses whether the user keeps typing / accepts the completion to determine whether it was implicitly rejected, and escalates to the large model after rejection.
- To accelerate inference on both sides, it designs a **two-stage speculative decoding** strategy: it first uses exact context matching to construct an almost zero-cost draft for the small model; if the small model result is rejected, it then uses that result as the large model’s speculative draft to speed up large-model decoding.
- To improve large-model quality, it designs **iterative retrieval**: the first round uses left and right context for BM25 retrieval; if the small model output is rejected, that output is used as a new semantic clue for a second retrieval, and retrieval scores are fused with weights based on small-model confidence to provide more relevant context to the large model.
- Due to the lack of a suitable small model, the authors also trained a lightweight code completion model themselves based on **41M** Python training samples, and conducted analysis and validation on **41K** validation samples.

## Results
- The authors’ trained **121M** small model achieves **73.8% of the average performance of the state-of-the-art 7B model** on the benchmark; on **41K** validation samples from real repositories, it can correctly handle **37.8%** of cases even **without using RAG**.
- In terms of speed, the paper states that this **121M** local model is about **2x faster** in inference than a **7B** large model deployed in the cloud on an **Nvidia A800 GPU**.
- On **RepoEval** and the newly proposed **StmtEval**, MCCom reduces inference latency by **5.8%–47.9%**, with an average reduction of **25.6%**; the abstract also reports an average **46.3%** reduction in large-model usage.
- In terms of accuracy, compared with the baseline of “always calling the large model,” MCCom improves **Exact Match** by **2.9%–13.5%**, with an average improvement of **8.9%**.
- The paper also provides empirical observations supporting the cascading design: **14.4%** of small-model outputs appear directly in the left-side context; on a random sample of **1000** examples, the average **ES** similarity between small-model and large-model outputs is **78.4%**, indicating a practical basis for the two-stage speculative decoding design.
- The paper claims that the method shows consistently effective results across **multiple large models**, and additionally introduces a new benchmark, **StmtEval**, that is closer to real interactive scenarios; however, the excerpt does not provide finer-grained tables by model or dataset.

## Link
- [http://arxiv.org/abs/2603.05974v2](http://arxiv.org/abs/2603.05974v2)
