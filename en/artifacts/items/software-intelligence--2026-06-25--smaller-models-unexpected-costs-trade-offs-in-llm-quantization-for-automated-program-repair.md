---
source: arxiv
url: https://arxiv.org/abs/2606.27205v1
published_at: '2026-06-25T16:02:05'
authors:
- Fernando Vallecillos-Ruiz
- Giordano d'Aloisio
- Max Hort
- Luca Traini
- Antinisca Di Marco
- Leon Moonen
topics:
- llm-quantization
- automated-program-repair
- code-intelligence
- software-engineering
- energy-efficiency
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Smaller Models, Unexpected Costs: Trade-offs in LLM Quantization for Automated Program Repair

## Summary
This paper shows that LLM quantization for automated program repair can save memory but can also change which bugs get repaired and raise inference cost. The study finds no single best quantization setting across models, benchmarks, and efficiency goals.

## Problem
- Larger code LLMs need high GPU memory, which limits local APR use and raises operating cost.
- Quantization is often judged by aggregate benchmark scores, but those scores can hide changes in which bugs a model can fix.
- APR needs this analysis because a quantized model with a similar pass count may repair a different set of defects than the base model.

## Approach
- The authors evaluate 13 post-training quantization configurations across six LLMs: Llama-3-8B, Llama-3-70B, DeepSeek-Coder-6.7B, DeepSeek-Coder-33B, Mistral-7B, and Mixtral-8x7B.
- They test both model-weight quantization and KV-cache quantization, using AQLM, AWQ, BitsAndBytes, HQQ, and Quanto at 2-, 3-, 4-, and 8-bit settings where supported.
- They run APR on HumanEval-Java with 164 problems and a Defects4J v2.0 subset with 525 single-function bugs.
- They measure pass@10, solved-set overlap through a proposed Jaccard Consistency Rate, inference time, GPU energy, in-memory model size, and peak inference memory.
- They compare configurations with Pareto dominance to find settings that are worse than alternatives on effectiveness and efficiency.

## Results
- Quantization reduced memory footprint by up to 85%, but the paper reports higher inference time and higher energy use in many settings, attributed to poor hardware use on the tested stack.
- On HumanEval-Java, at least one quantized variant beat the base model for all six LLMs. DeepSeek-Coder-6.7B improved from 90 to 107 plausible repairs with quanto4 model quantization, a 19% gain.
- On Defects4J, quantized variants beat the base model in 5 of 6 model cases. DeepSeek-Coder-6.7B improved from 43 to 82 plausible repairs, a 91% gain.
- Similar repair counts often came from different solved-problem sets, so pass@10 alone did not capture behavior changes after quantization.
- Very low-bit settings often failed: 2-bit or 3-bit quantization produced weak results in several cases, including four cases with 0 or 1 plausible patch across a benchmark.
- Pareto analysis found that 48% of evaluated quantization configurations were strictly dominated by another setting.

## Link
- [https://arxiv.org/abs/2606.27205v1](https://arxiv.org/abs/2606.27205v1)
