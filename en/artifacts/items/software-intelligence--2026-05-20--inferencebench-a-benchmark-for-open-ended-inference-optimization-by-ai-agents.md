---
source: hn
url: https://inferencebench.ai/
published_at: '2026-05-20T23:37:29'
authors:
- matt_d
topics:
- ai-agents
- llm-inference
- benchmarking
- code-intelligence
- software-optimization
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# InferenceBench: A Benchmark for Open-Ended Inference Optimization by AI Agents

## Summary
InferenceBench tests whether frontier coding agents can optimize LLM inference servers under a fixed compute budget. The main finding is that agents can beat vanilla PyTorch and many default inference-engine settings, but they still lose to simple hyperparameter search over existing engines.

## Problem
- LLM serving speed depends on many runtime choices, including batching, prefix caching, KV-cache settings, and engine flags.
- Agents often know the right optimization ideas, but they fail to run clean comparisons, keep the best setting, or submit a valid final server.
- This matters for automated software R&D because a useful agent must improve a system and preserve the improvement under correctness and integrity checks.

## Approach
- Each run gives an agent a base model, hardware environment, and a 2-hour wall-clock budget.
- The agent must build an OpenAI-compatible inference server and maximize speedup over a PyTorch baseline.
- The benchmark covers 4 scenarios: prefill latency, long generations, concurrent traffic, and balanced serving.
- Final submissions must pass correctness checks and an integrity audit. Failed, unreachable, reward-hacked, or regressed servers receive the PyTorch baseline score.
- Scores use geometric-mean speedup, with comparisons against PyTorch, default vLLM, SGLang, TGI, and a matched hyperparameter-search baseline.

## Results
- Across all 4 scenarios, agents beat the vanilla PyTorch baseline and most default inference engines, including default vLLM, SGLang, and TGI.
- Agents are worse than simple hyperparameter search over existing engine settings under the same time budget. The excerpt does not provide exact speedup values.
- Sonnet 4.6 ranks first on the leaderboard because it combines competitive per-scenario speedups with more reliable valid final submissions.
- The benchmark reports 180 runs. In those runs, agents often identify relevant optimizations in transcripts but fail to validate, commit to, or preserve them.
- 93.9% of runs submit a vLLM-based server.
- One trace reports a valid baseline server with generation throughput of 63.53 tokens/s, TTFT p50 of 51.8 ms, TTFT p90 of 400 ms, ITL p50 of 10.2 ms, and TPOT p50 of 15.7 ms.

## Link
- [https://inferencebench.ai/](https://inferencebench.ai/)
