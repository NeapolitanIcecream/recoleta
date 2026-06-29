---
source: arxiv
url: https://arxiv.org/abs/2605.11051v1
published_at: '2026-05-11T14:47:07'
authors:
- Kirill Gelvan
- Igor Slinko
- Felix Steinbauer
- Egor Bogomolov
- Florian Kofler
- Yaroslav Zharov
topics:
- software-engineering-agents
- context-compression
- code-intelligence
- swe-bench
- llm-agents
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# On Problems of Implicit Context Compression for Software Engineering Agents

## Summary
This paper tests ICAE-style continuous context compression for software engineering agents and finds a clear failure on multi-step coding tasks. It extends context and speeds generation, but solves fewer SWE-bench Verified issues than the uncompressed Qwen3-8B baseline.

## Problem
- LLM coding agents hit context limits as tool outputs, files, logs, and prior actions fill the prompt.
- Long SWE-bench-like tasks can require over 1 million consumed tokens on average, and model quality drops when key facts are buried in long histories.
- Dense memory tokens could reduce context cost, but the paper tests whether they preserve enough detail for multi-step code editing.

## Approach
- The authors adapt In-Context Autoencoder (ICAE): a trainable Qwen3-8B encoder compresses text into continuous memory tokens, and a frozen Qwen3-8B decoder reads those tokens plus the current prompt.
- Pretraining uses SlimPajama-6B with a 50/50 mix of text reconstruction and continuation objectives for 100,000 steps.
- Fine-tuning covers SQuAD, RepoQA, and SWE-Smith agent trajectories; in agent training, only observations longer than 256 tokens are compressed.
- For agent tasks, actions, short observations, and the system prompt stay as normal tokens, while the model learns to predict the next tool call from a history with compressed observations.
- Evaluation compares Base Qwen3-8B, task fine-tuned Qwen3-8B, and ICAE at a nominal 4x compression rate.

## Results
- On SQuAD, ICAE reaches BLEU 0.73 and EM 0.67, above Base at BLEU 0.67 and EM 0.54, and below SFT at BLEU 0.75 and EM 0.70; EM gain over Base has p < 0.0001.
- On RepoQA, ICAE reaches BLEU 0.87 and Pass@0.8 0.69, close to Base at BLEU 0.81 and Pass@0.8 0.65; SFT is higher at BLEU 0.90 and Pass@0.8 0.85; ICAE vs Base Pass@0.8 has p = 0.6075.
- On SWE-bench Verified, ICAE solves 7 issues out of 500, below Base at 19 and far below SFT at 86; the resolve-rate drop vs Base has p = 0.0062 in multi-run analysis.
- ICAE improves the intermediate SWE-bench trajectory-matching metric: BLEU_ref 0.51 vs Base 0.48, while SFT reaches 0.55.
- Effective compression is 1.46x on SQuAD, 3.74x on RepoQA, and 2.0x on SWE-bench Verified; on SWE-bench Verified it allows average trajectories of 113 steps vs 81 for Base and cuts generation time by 10%.
- The authors attribute the SWE-bench failure to reconstruction errors that compound across steps, such as wrong URLs or file paths, and to a training signal that optimizes only the latest compressed observation rather than future usefulness.

## Link
- [https://arxiv.org/abs/2605.11051v1](https://arxiv.org/abs/2605.11051v1)
