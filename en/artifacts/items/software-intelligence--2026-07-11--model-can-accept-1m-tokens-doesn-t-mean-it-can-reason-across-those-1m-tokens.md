---
source: hn
url: https://twitter.com/0xCarnagee/status/2075983721841225885
published_at: '2026-07-11T23:23:57'
authors:
- annjose
topics:
- long-context-reasoning
- context-rot
- coding-agents
- continual-learning
- retrieval-evaluation
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Model can accept 1M tokens doesn't mean it can reason across those 1M tokens

## Summary
The excerpt argues that accepting a 1M-token context does not guarantee reliable reasoning across it. It reports a large retrieval drop at longer context lengths and points to continual learning, training on agent traces, and real-environment interaction as possible remedies.

## Problem
- Long-context models may accept large inputs while losing the ability to retrieve or reason over information distributed across the context.
- This matters for coding agents because large repositories, long execution traces, and tool outputs can exceed the range where the model works reliably.

## Approach
- Compare model performance at 256k and 1M tokens using a retrieval task.
- Describe the failure mode as "context rot," where reasoning quality declines as context grows.
- Recommend continual learning, training on a model's own traces, and interaction with real environments to improve long-horizon agent behavior.

## Results
- The excerpt claims GPT-5.5 scores 80% on retrieval at 256k tokens.
- At 1M tokens, the claimed score falls to 36%, a 44 percentage-point drop and a 55% relative decrease from the 256k result.
- The excerpt provides no dataset name, evaluation protocol, statistical analysis, or comparison with other models.
- It also promotes a short Claude Code course from Andrew Ng, but gives no evidence that the course improves coding-agent performance.

## Link
- [https://twitter.com/0xCarnagee/status/2075983721841225885](https://twitter.com/0xCarnagee/status/2075983721841225885)
