---
source: arxiv
url: https://arxiv.org/abs/2605.02010v1
published_at: '2026-05-03T18:31:45'
authors:
- Hengyu Liu
- Tianyi Li
- Zhihong Cui
- Yushuai Li
- Zhangkai Wu
- Torben Bach Pedersen
- Kristian Torp
- Christian S. Jensen
topics:
- ai-reliability
- human-ai-collaboration
- knowledge-objects
- implicit-knowledge
- agent-memory
- software-engineering
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# Reliable AI Needs to Externalize Implicit Knowledge: A Human-AI Collaboration Perspective

## Summary
The paper argues that AI reliability needs human-verifiable records of implicit knowledge, such as reasoning patterns, procedures, and domain judgment. It proposes Knowledge Objects as structured artifacts that expose this knowledge for validation, correction, reuse, and provenance tracking.

## Problem
- Current reliability methods mainly check explicit knowledge, such as retrieved documents, citations, confidence scores, or stored memories, while many useful AI behaviors come from implicit patterns learned during training.
- This matters in high-stakes knowledge work because hallucination, overconfidence, and prompt sensitivity can make capable systems unsafe or costly to trust.
- The paper cites concrete failure rates: specialized legal AI tools hallucinate in 17–34% of queries, general-purpose LLMs make legal errors on 58–88% of verifiable questions, and GPT-4 hallucinates 28.6% of medical references in systematic review tasks.

## Approach
- The core mechanism is a Knowledge Object: a structured record containing a claim or procedure, supporting evidence or reasoning, scope and limitations, and validation metadata.
- The AI generates candidate Knowledge Objects by externalizing patterns that would otherwise remain hidden in model behavior or interaction traces.
- Human experts inspect these objects, validate them, reject them, correct them, or add scope limits.
- The system stores provenance, validation status, and corrections so later users can see who checked a claim, when it was checked, and where it applies.
- In software engineering, a Knowledge Object might state that singleton database connections cause thread-safety issues above 100 requests per second in Java/Spring connection-pooling contexts, backed by 12 incident postmortems and load tests.

## Results
- This is a position paper and reports no new benchmark, user study, implementation result, or ablation result for Knowledge Objects.
- It claims the main gain is economic: AI drafts structured knowledge so experts verify bounded artifacts instead of re-checking each AI answer from scratch.
- It argues that only 5–20% of organizational knowledge is documented, leaving 80–95% as implicit knowledge that current RAG, fine-tuning, self-verification, and agent memory methods cannot make directly inspectable.
- It uses prior work to motivate the reliability gap: nominal 99% LLM confidence intervals cover the true answer only 65% of the time on average, sycophancy persists at 78.5% after correction attempts, and prompt format changes can shift accuracy by up to 76 percentage points.
- It claims validated Knowledge Objects would let reliability accumulate across users by preserving expert validation, corrections, scope limits, and provenance for later AI-assisted work.

## Link
- [https://arxiv.org/abs/2605.02010v1](https://arxiv.org/abs/2605.02010v1)
