---
source: hn
url: https://github.com/aleflow420/rinoa
published_at: '2026-03-10T22:54:03'
authors:
- aleflow420
topics:
- personalized-llm
- lora-finetuning
- local-ai
- contrastive-feedback
- rag
- evaluation
relevance_score: 0.07
run_id: materialize-outputs
language_code: en
---

# I've no technical background, hope someone finds this interesting

## Summary
This work proposes a localized protocol for writing personal knowledge into personal AI: using a small amount of contrastive feedback in the form of “model interpretation - user correction” to compress personal knowledge into the weights of a small open-source model. The author claims this enables personalized AI based on “recognition” rather than retrieving and stitching context on every query, with zero cloud dependency and very low training cost on consumer hardware.

## Problem
- Existing personal AI mostly relies on RAG: every query searches a database and stuffs context into the prompt, so cost grows linearly with interaction, and knowledge never truly settles into the model parameters.
- For “personal knowledge,” which base models originally know nothing about, standard LoRA/automatic evaluation may not be effective; the author reports that common automatic metrics are biased toward “general quality” and cannot measure the personalized effect of “being recognized by the user.”
- This matters because if personal knowledge can enter local weights, users could gain long-term personalized AI that is low-latency, offline, portable, and private, rather than depending on a cloud memory store.

## Approach
- The core mechanism is simple: first let the model offer an interpretation or guess about the user’s knowledge, then have the user provide a correction; the “wrong answer vs correct correction” forms a contrastive training pair, and the model updates along the difference between them, so the most wrong areas receive the strongest training signal.
- The training target is a small LoRA adapter on a local 4-bit Qwen model; the example configuration is Qwen3-14B-4bit, with only 25.7M/14.8B trainable parameters (0.174%), training for about 16 minutes per run on a MacBook Pro M4 Pro 24GB.
- The dataset is very small: the author uses 93 “contrastive facts” for supervised fine-tuning, and removes samples that dilute identity signals through multi-version iteration.
- The system has a five-layer structure: the weights layer handles “user thinking/style,” the RAG “lake” handles event memory, plus current context, an idle reflection thread, and conversation history; training only modifies the weights layer, while the memory store grows automatically.
- The author also reproduces the setup on a second model, Qwen3.5-9B-4bit, using the same data and similar parameters, as a preliminary validation across architectures but not across model families.

## Results
- On a controlled benchmark, the author claims the **adapted model uses 5.7× fewer tokens than the base model**, while **general knowledge questions remain unimpaired: 10/10 correct vs 10/10 for the base**; the author interprets this as evidence that once personal knowledge enters the weights, it can be “recognized” more directly.
- For cross-domain compositional ability, the author reports **0.813 cosine similarity between knowledge from different domains that were never jointly trained**, and gives an example where one version synthesized **3 different training facts** into a new sentence not present in the training set, as a sign of compositional generalization.
- On the task of classifying 25,000 abstracts into 19 categories, the author’s conclusion is **“All negative”**: the LoRA route is not suitable for this setting; the author also notes that **the base model itself already had 49% classification accuracy**, so this task does not represent “zero-knowledge injection” of personal knowledge.
- Automatic evaluation mostly fails: automatic keyword matching hits only **3/14**, while after manual review the author believes at least **7+/14** is more reasonable; blind LLM evaluation agrees with user judgment only **6/13 = 46%**, which the author says is close to random, indicating that automatic metrics failed to capture the goal of “personal recognition.”
- On 6 questions about a 19th-century novel **not in the training data**, **5/6** model answers connected the literary content to the user’s personal principles; the author treats this as qualitative evidence of cross-domain transfer.
- In dual-model testing, the two base models had different failure modes: **Qwen3-14B had 16/20** roleplay drift cases, while **Qwen3.5-9B had 12/20** reasoning loops; the author says both converged after adaptation to being “concise, direct, zero roleplay.” At the same time, with reasoning disabled, **the adapted model’s performance dropped 57%**, while the base dropped only **34%**, interpreted as “it knows more, so it needs to think less.” However, the author also explicitly acknowledges that the results come from only a **single user**, rely heavily on subjective evaluation, and have not yet been validated across users; code and full reproduction experiments have also not yet been released.

## Link
- [https://github.com/aleflow420/rinoa](https://github.com/aleflow420/rinoa)
