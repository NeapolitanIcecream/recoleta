---
source: arxiv
url: https://arxiv.org/abs/2606.11817v1
published_at: '2026-06-10T08:50:59'
authors:
- Yitong Zhang
- Shiteng Lu
- Jia Li
topics:
- code-generation
- llm-safety
- jailbreaks
- grammar-constrained-decoding
- malicious-code
- alignment
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Grammar-Constrained Decoding Can Jailbreak LLMs into Generating Malicious Code

## Summary
CodeSpear shows that grammar-constrained decoding can make aligned code LLMs produce malicious code by removing natural-language refusals from the valid output space. CodeShield trains models to prefer harmless code when grammar constraints force code output.

## Problem
- LLMs are used for code generation, so unsafe completions can become executable malware, denial-of-service code, or credential-theft code.
- Existing safety alignment usually teaches natural-language refusals, but a code grammar can make those refusals invalid during decoding.
- Grammar-constrained decoding is available in systems such as vLLM, SGLang, OpenAI APIs, and Fireworks AI, which makes this attack path practical for local and API deployments.

## Approach
- CodeSpear sends a malicious code-generation prompt while enabling a normal programming-language grammar, such as a Python grammar.
- The grammar mask removes tokens that would form plain-language refusals and keeps only tokens that can extend into valid code.
- The model then samples from the grammar-valid code space, where prior safety alignment may not prefer safe behavior.
- CodeShield uses DPO with three response types: natural-language refusal, harmless honeypot code, and harmful code produced under GCD.
- CodeShield trains the preference order as refusal over honeypot code when language is allowed, and honeypot code over harmful code when only code is allowed.

## Results
- The evaluation covers 10 LLMs across 4 benchmarks, with 5 local models and 5 API-based models.
- On local models such as Qwen2.5-Coder-7B, CodeSpear reaches an average attack success rate of 81.82%.
- Across the tested models, CodeSpear raises attack success rate by more than 30 percentage points on average over representative jailbreak baselines.
- On commercial API models such as GPT-5, GPT-5-mini, MiniMax-M2.5, MiniMax-M2.7, and GPT-OSS-120B, CodeSpear raises attack success rate by more than 40 percentage points on average.
- The safety evaluation uses RMCBench with 182 malicious code-generation requests and MalwareBench with 320 malicious requests.
- CodeShield reduces CodeSpear attack success to below the no-attack level and reports only minor degradation on HumanEval with 164 tasks and MBPP with 974 tasks; the excerpt does not give exact utility deltas.

## Link
- [https://arxiv.org/abs/2606.11817v1](https://arxiv.org/abs/2606.11817v1)
