---
source: arxiv
url: http://arxiv.org/abs/2604.09089v1
published_at: '2026-04-10T08:19:48'
authors:
- Li Huang
- Zhongxin Liu
- Yifan Wu
- Tao Yin
- Dong Li
- Jichao Bi
- Nankun Mu
- Hongyu Zhang
- Meng Yan
topics:
- secure-code-generation
- code-llm
- multi-layer-representations
- vulnerability-detection
- lora-fine-tuning
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# DeepGuard: Secure Code Generation via Multi-Layer Semantic Aggregation

## Summary
DeepGuard hardens code LLMs against insecure code generation by using security signals from multiple transformer layers instead of only the final layer. It combines multi-layer feature aggregation, security-aware fine-tuning, and a cheap inference-time logit bias to raise secure-and-correct code generation rates.

## Problem
- Code LLMs often reproduce insecure coding patterns from training data, and prior work reports large failure rates such as about 40% vulnerable code in Copilot-generated samples.
- Many security-tuning methods supervise only the final transformer layer, but the paper shows vulnerability cues peak in intermediate-to-upper layers and weaken near the output layer.
- This matters because secure code generation must improve security without breaking functional correctness, which is the main value of code models in development workflows.

## Approach
- DeepGuard probes model layers and finds that vulnerability-discriminative information is strongest in a band of upper layers, not at the last layer alone.
- It builds an attention-based aggregator over the top N layers to fuse their hidden states into a single security-sensitive representation for each token.
- A small security analyzer scores tokens and sequences using the aggregated representation plus a learned token-level security embedding; training pushes secure code to score higher than matched vulnerable code with a margin loss.
- The model is adapted with LoRA under a multi-objective loss: next-token loss on secure code, a security contrastive loss between vulnerable and secure pairs, and KL regularization to stay close to the base model.
- At inference, DeepGuard computes one prompt-conditioned security score, combines it with a token prior learned from secure vs. vulnerable training data, and adds a fixed bias to logits during decoding without per-step analyzer calls.

## Results
- Across five code LLMs, DeepGuard improves the secure-and-correct generation rate by **11.9% on average** over the strong baseline **SVEN**.
- On **Qwen2.5-Coder-3B**, **sec-pass@1** rises from **70.47%** with **SVEN** to **80.76%** with **DeepGuard**; **pass@1** is **86.65%**, which the paper says is close to the original model.
- On **Qwen2.5-Coder-7B**, DeepGuard reports **pass@1 83.18%**, **sec@1_pass 88.19%**, **sec-pass@1 73.35%**, and **SVEN-SR 89.21%**.
- On **DeepSeek-Coder-1.3B**, DeepGuard reports **pass@1 81.06%**, **sec@1_pass 84.91%**, **sec-pass@1 68.82%**, and **SVEN-SR 87.71%**.
- On **DeepSeek-Coder-6.7B**, DeepGuard reports **pass@1 88.47%**, **sec@1_pass 79.52%**, **sec-pass@1 70.35%**, and **SVEN-SR 81.82%**.
- On **Seed-Coder-8B**, DeepGuard reports **pass@1 86.59%**, **sec@1_pass 93.21%**, **sec-pass@1 80.71%**, and **SVEN-SR 93.21%**; the paper also claims generalization to held-out vulnerability types, but the excerpt does not provide the held-out split numbers.

## Link
- [http://arxiv.org/abs/2604.09089v1](http://arxiv.org/abs/2604.09089v1)
