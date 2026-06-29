---
source: arxiv
url: https://arxiv.org/abs/2606.03618v1
published_at: '2026-06-02T13:17:45'
authors:
- Mehmet Utku Colak
topics:
- code-agents
- prompt-compression
- multilingual-code
- local-llm
- context-optimization
- software-engineering
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Cross-Lingual Token Arbitrage: Optimizing Code Agent Context Windows via Local LLM Preprocessing

## Summary
This paper proposes a local pre-flight rewriter that makes multilingual code-agent prompts cheaper before they reach a cloud model. On OMH-Polyglot, it cuts prompt tokens by 34–47% and keeps or improves accuracy across gpt-3.5-turbo, gpt-4o, and gemini-2.5-flash-lite.

## Problem
- Non-English developer prompts can use 2–3x more tokens than equivalent English prompts under common LLM tokenizers, which raises API cost before the model starts solving the task.
- Conversational prompts add filler and loose structure, which can cause code agents to retrieve too much context and produce longer answers.
- Existing prompt compressors usually act after the prompt has already grown, or require extra cloud-side calls, so they do not remove the token cost at the edge.

## Approach
- A TypeScript gateway intercepts each IDE or benchmark query before cloud dispatch.
- A local Llama 3.2 3B model running through Ollama translates non-English text into English, removes filler, and rewrites the request into a compact [CONTEXT]/[TASK] format.
- The [TASK] block keeps required function names and copies Python assert lines verbatim, so the cloud model still sees the executable grading constraints.
- A regex validator rejects empty output, leaked code blocks, malformed sections, and other bad rewrites, with up to two repair attempts.
- A token-budget guard forwards the original prompt when the rewrite is not at least 5% smaller, which prevents a larger cloud-billed payload.

## Results
- OMH-Polyglot has 200 coding tasks with Turkish, Arabic, Chinese, and code-switched specifications; its mean tokenization-overhead ratio is 2.05x, with p90 at 4.02x and a worst case of 6.15x.
- On gpt-3.5-turbo, prompt tokens drop from 53,713 to 28,661, total tokens drop from 94,338 to 86,474 (-8.3%), and accuracy stays at 99.50%.
- On gpt-4o, prompt tokens drop from 43,565 to 28,776, total tokens drop from 139,085 to 127,594 (-8.3%), and accuracy rises from 98.33% to 99.50%; the paper says this accuracy change is within run-level variation.
- On gemini-2.5-flash-lite, prompt tokens drop from 44,918 to 29,398, total tokens drop from 116,653 to 94,725 (-18.8%), and accuracy rises from 95.00% to 98.00%.
- Against LLMLingua-2 at matched compression rate, the method reports higher OckScore on all three backends: 99.08 vs 76.91 on gpt-3.5-turbo, 98.88 vs 96.56 on gpt-4o, and 97.54 vs 33.85 on gemini-2.5-flash-lite.
- Dollar cost changes vary by backend: +15.1% on gpt-3.5-turbo, -0.4% on gpt-4o, and -12.4% on gemini-2.5-flash-lite; output-token pricing offsets some input-token savings.

## Link
- [https://arxiv.org/abs/2606.03618v1](https://arxiv.org/abs/2606.03618v1)
