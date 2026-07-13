---
source: hn
url: https://mrzk.io/posts/qmlx-maximising-ai-psychosis-minmaxing-mac-studio/
published_at: '2026-07-11T22:54:06'
authors:
- marzukia
topics:
- local-inference
- long-context-caching
- code-intelligence
- apple-silicon
- model-serving
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Fixed three bugs that made Qwen3.5-122B a daily driver on Mac Studio

## Summary
qMLX makes Qwen3.5-122B practical for long-context local coding on an M3 Ultra Mac Studio by fixing three cache and history bugs. Disk-based KV restoration reduces repeated 32k-token prefill from 88 seconds to 0.64 seconds, while decode runs at 28-55 tokens per second.

## Problem
- Long-context follow-ups took 3-5 minutes before the first token, making local pair programming impractical.
- The serving stack repeatedly recomputed conversations because the system prompt changed, interrupted replies were missing from history, and unmatchable checkpoints evicted valid disk checkpoints.
- The problem matters because a 122B model can fit in 96GB of unified memory, but repeated full-context prefill removes the practical benefit of local inference.

## Approach
- Fork rapid-mlx into qMLX with hybrid-attention support for Qwen3.5 and Qwen3.6 models on Apple Silicon.
- Restore reusable attention KV state from SSD so each turn prefills only tokens added after the previous checkpoint.
- Remove a per-turn message ID from the cached system prompt to preserve byte-exact prefix matching.
- Save streamed assistant replies when generation is interrupted, keeping server state and conversation history aligned.
- Prioritize matchable checkpoints during eviction and disable junk checkpoint writes when restore is enabled.

## Results
- On an M3 Ultra Mac Studio with 96GB unified memory, a repeated 32k-token prompt took 88 seconds without caching and 0.64 seconds with disk restore, a 137x improvement.
- The same benchmark reports cache acceleration of 13x at 1k tokens and 137x at 32k tokens.
- In a conversation growing from 31k to 57k tokens, warm turns restored about 53k-56k cached tokens and required 33-1,869 new prefill tokens, with measured prefill times of 33-1,871 milliseconds.
- Prefill throughput reached about 700 tokens per second at short context and 386 tokens per second at 64k context; decode throughput declined from 55 to 28 tokens per second.
- At 168k tokens, a 67-token follow-up reached the first token in 2.6 seconds, while an additional 1,800-token tool result took about 17 seconds to prefill.
- The claims come from one M3 Ultra system and have not been reproduced on other Apple Silicon configurations.

## Link
- [https://mrzk.io/posts/qmlx-maximising-ai-psychosis-minmaxing-mac-studio/](https://mrzk.io/posts/qmlx-maximising-ai-psychosis-minmaxing-mac-studio/)
