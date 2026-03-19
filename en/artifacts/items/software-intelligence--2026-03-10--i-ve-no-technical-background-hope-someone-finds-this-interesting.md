---
source: hn
url: https://github.com/aleflow420/rinoa
published_at: '2026-03-10T22:54:03'
authors:
- aleflow420
topics:
- personalized-llm
- lora-finetuning
- human-feedback
- local-ai
- rag
- evaluation
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# I've no technical background, hope someone finds this interesting

## Summary
This work proposes a personalized protocol for writing personal knowledge directly into the weights of a local large model. Using “contrastive human feedback,” it trains an adapter that can recognize the user’s style and knowledge with very little data and zero cloud cost. The author argues that, compared with retrieving external memory on every query, placing knowledge in the weights enables a more stable, lower-cost, lower-latency personal AI.

## Problem
- Existing personal AI systems mostly rely on RAG: they must retrieve from a database on every query and stuff the context into the prompt, so cost grows linearly with queries, and knowledge is never truly consolidated into the model.
- Generic automatic evaluation is more biased toward “generalization quality” than toward “being recognized by the user as sounding like themselves,” making it difficult to measure whether a personalized model has truly learned the user’s knowledge and expressive style.
- Personalized training is usually assumed to require technical expertise, substantial compute, or cloud dependence; the author wants to show that it can be done on ordinary consumer hardware.

## Approach
- The core mechanism is simple: first let the model explain or guess the user’s knowledge, then have the user correct it; the “model’s wrong answer vs. the user’s corrected answer” forms a contrastive training pair, and the larger the gap, the stronger the training signal.
- Using 93 “fact/correction” samples, the author trains a LoRA adapter in SFT form, compressing personal knowledge and expressive style into the weights rather than leaving them only in an external database.
- The system is designed in five layers: identity and thinking style in the weights, episodic memory (RAG) in an SQLite vector store, continuously injected environmental awareness, a reflection thread that proactively discovers knowledge gaps during idle time, and conversational working memory.
- The protocol was validated to converge on two base models: Qwen3-14B-4bit and Qwen3.5-9B-4bit, both trained locally on Apple Silicon under the MLX framework with 24GB memory.
- The author also constructed a controlled evaluation to reduce “role-play contamination”: the base model uses a neutral identity prompt, the adapted model uses a personal identity prompt, and general questions are compared separately from personal questions.

## Results
- Training cost is very low: on a MacBook Pro M4 Pro 24GB, training 25.7M / 14.8B trainable parameters (0.174%) takes about **16 minutes** per run, and the author claims the compute cost is **$0**.
- On a controlled benchmark, the author claims the adapted model is more efficient while preserving general ability: **10/10 correct on general knowledge questions, the same as the base model**; meanwhile, the adapted model uses **5.7× fewer tokens** on that benchmark.
- Reproducible across architectures: Qwen3-14B and Qwen3.5-9B both “converged” on the same data to a concise, direct, non-role-playing style; before adaptation, the former had **16/20** responses showing roleplay, while the latter had **12/20** showing reasoning loops.
- The author reports signs of cross-domain compositionality: in one cross-domain setting not jointly trained, the cosine similarity between responses and personal facts reached **0.813**; in another 19th-century novel test, **5/6** answers connected literary content to personal principles.
- Automatic evaluation is considered ineffective: keyword matching initially hit **3/14**, but manual review revised this to **7+/14**; LLM/user agreement on 13 A/B blind-test questions was only **6/13 = 46%**, which the author considers close to random, suggesting that automatic metrics fail to capture the “sense of personal recognizability.”
- In another comparison, SFT-only scored higher than RAFT on the “knowledge-lake similarity” metric (**0.795 vs 0.783**), but the author says users preferred RAFT on cross-domain questions, further supporting the claim that existing automatic metrics are misaligned with personalization goals.

## Link
- [https://github.com/aleflow420/rinoa](https://github.com/aleflow420/rinoa)
