---
source: hn
url: https://www.percepta.ai/blog/can-llms-be-computers
published_at: '2026-03-11T23:28:16'
authors:
- E-Reverance
topics:
- llm-computation
- transformer-execution
- program-execution
- inference-speed
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# 30k Tok/S (Allegedly)

## Summary
This article explores whether large language models can execute programs directly inside the Transformer like a computer, thereby enabling faster inference. The core claim is that by "executing programs" within the model rather than generating every intermediate step token by token, inference for certain computational processes can become exponentially faster.

## Problem
- Traditional LLMs, when performing tasks that require multi-step computation, algorithmic reasoning, or programmatic operations, usually rely on generating intermediate steps token by token, which makes inference slow and costly.
- If a model can only simulate computer execution through natural-language chain-of-thought reasoning, then latency for complex tasks grows quickly with the number of steps, limiting practical usability.
- Making the Transformer directly act as a "computer" matters because it could significantly improve efficiency on algorithmic tasks and expand the model's ability to handle program execution.

## Approach
- The article's central direction is to have programs executed inside the Transformer, rather than explicitly outputting every intermediate computation step as tokens.
- Put simply, it turns "writing out the solution process step by step" into "doing the computation inside the network and only outputting the result."
- The author claims this can yield exponentially faster inference, meaning that for some program/algorithmic tasks, execution time is no longer strictly constrained by the length of explicit intermediate tokens.
- From the title "30k Tok/S (Allegedly)" and the subtitle, it is clear that the focus is on high-throughput inference and internal program execution mechanisms in Transformers, rather than traditional text-generation optimization.

## Results
- The provided excerpt does not include verifiable experimental tables, datasets, baseline models, or detailed metrics.
- The title claims **30k Tok/S** is achievable, but it also includes **"Allegedly"**, indicating this is an attention-grabbing performance claim rather than a result fully demonstrated in the excerpt.
- The subtitle explicitly claims that executing programs inside Transformers can enable **"exponentially faster inference"**, but the excerpt does not provide a specific speedup factor, task setup, or comparison baseline.
- Based on the current text, the strongest concrete claim is: **internal program execution + exponentially faster inference + throughput on the order of about 30k tok/s**; however, there is not enough evidence to assess its generality or rigor.

## Link
- [https://www.percepta.ai/blog/can-llms-be-computers](https://www.percepta.ai/blog/can-llms-be-computers)
