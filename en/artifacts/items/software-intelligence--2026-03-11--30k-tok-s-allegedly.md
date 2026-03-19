---
source: hn
url: https://www.percepta.ai/blog/can-llms-be-computers
published_at: '2026-03-11T23:28:16'
authors:
- E-Reverance
topics:
- llm-inference
- program-execution
- transformers
- neural-computation
- code-intelligence
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# 30k Tok/S (Allegedly)

## Summary
This article proposes “compiling” programs into a Transformer so that the model performs computation during inference like executing a circuit, thereby claiming inference far faster than step-by-step token generation. Its core selling point is an inference mechanism with the potential for exponential speedups by executing programs inside the model.

## Problem
- Existing large language models typically generate token by token, leading to high inference latency and making it difficult to execute structured programs as efficiently as traditional computers.
- If models can only rely on autoregressive generation to “simulate” computation, then speed and cost become bottlenecks in complex reasoning, tool use, and program execution scenarios.
- This problem matters because faster internal computation mechanisms could change the efficiency frontier for code agents, automated software production, and broader AI systems.

## Approach
- The article argues that LLMs should not merely predict the next token, but directly “execute programs” inside the Transformer.
- Put simply: encode the required computation process into structures within the model so that one or a few forward passes are equivalent to running a program, rather than generating every intermediate step one by one.
- Its theoretical narrative is that if a program can be represented in an appropriate form inside a Transformer, then inference complexity could improve exponentially relative to traditional token-by-token methods.
- The “30k Tok/S” in the title suggests the authors connect this internal execution to ultra-high-throughput inference, attempting to show that LLMs can evolve toward “working like computers.”

## Results
- The provided excerpt does not include verifiable experimental settings, datasets, baseline models, or a complete evaluation table, so there are **not enough quantitative results to report**.
- From the title, the strongest quantitative claim appears to be a speed on the order of **30k tokens/s**, but the excerpt does not specify the hardware, model size, task type, or comparison baseline.
- The subtitle explicitly claims “**executing programs inside transformers with exponentially faster inference**,” i.e. the potential for **exponentially faster** inference than certain conventional methods, but the excerpt does not provide details of the proof.
- Based on the available text, what can be confirmed is that the authors position the contribution as an inference paradigm that treats the Transformer as a carrier for executable programs, rather than a standard optimization of autoregressive generation.

## Link
- [https://www.percepta.ai/blog/can-llms-be-computers](https://www.percepta.ai/blog/can-llms-be-computers)
