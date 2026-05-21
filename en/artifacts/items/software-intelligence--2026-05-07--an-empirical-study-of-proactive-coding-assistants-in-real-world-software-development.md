---
source: arxiv
url: https://arxiv.org/abs/2605.05700v1
published_at: '2026-05-07T05:44:52'
authors:
- Lehui Li
- Ruixuan Jia
- Guo-Ye Yang
- Jia Li
topics:
- proactive-coding-assistants
- code-intelligence
- developer-behavior-data
- software-benchmarks
- llm-agents
- ide-interaction-traces
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# An Empirical Study of Proactive Coding Assistants in Real-World Software Development

## Summary
The paper introduces ProCodeBench, a real-world benchmark for predicting a developer’s intent from VS Code interaction traces and repository context. Its main claim is that LLM-simulated IDE traces differ enough from real developer behavior that simulation-only evaluation can overstate proactive coding assistant performance.

## Problem
- Proactive coding assistants need to infer intent before a developer writes a prompt, which can reduce prompt-writing effort and help when the developer has not stated the task clearly.
- Prior work mainly trains and evaluates on LLM-generated IDE traces because real IDE behavior data is hard to collect and has privacy constraints.
- The paper tests whether simulated traces match real developer behavior and whether current LLM, RAG, and agent baselines can predict intent from real traces.

## Approach
- The authors built a VS Code extension that logs 8 operation types: edit, copy/paste, view switching, cursor selection, terminal execution, debug output, accepted code completion, and agent request.
- They collected real IDE traces from 1,246 experienced industry developers over 3 consecutive days, then generated one paired LLM-simulated trace for each real trace under matched profile, length, and operation-type constraints.
- They compare real and simulated traces across operation-type diversity, time intervals, operation transitions, and noisy exploratory behavior.
- They convert continuous traces into intent-prediction samples with a 3-step annotation process: LLM sliding-window intent detection with N=50 operations, filtering for substantial edits or AI requests plus semantic checks, and manual expert review.
- They evaluate 13 baselines: 7 LLMs, 4 retrieval-augmented methods, and 2 agent methods, using LLM-as-judge semantic matching and Pass@K.

## Results
- The real-world collection contains about 4.63 million IDE operation events from 1,246 developers across backend, frontend, full-stack, algorithm, and database work.
- ProCodeBench contains 5,492 annotated intent-prediction samples, split chronologically into 3,576 train samples, 1,142 validation samples, and 774 test samples.
- Developer domains in the collection are backend 412 developers (33.1%), frontend 287 (23.0%), full-stack 208 (16.7%), algorithm 183 (14.7%), and database 156 (12.5%).
- The excerpt does not provide Pass@K tables or exact baseline scores. It states that current LLM, RAG, and agent baselines perform much worse on real-world traces than on simulation-based benchmarks.
- Repository-level code context improves intent prediction across backbone models, and agent methods perform best among the tested baselines through multi-turn tool use.
- Simulated-data-only fine-tuning does not transfer well to real traces, while training on simulated data before real-data fine-tuning improves real-world performance; the excerpt gives no numeric gain.

## Link
- [https://arxiv.org/abs/2605.05700v1](https://arxiv.org/abs/2605.05700v1)
