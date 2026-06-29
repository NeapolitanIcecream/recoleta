---
source: hn
url: https://mukulsingh105.github.io/articles/slm-routing-knowledge-workers.html
published_at: '2026-06-19T23:09:41'
authors:
- azhenley
topics:
- model-routing
- small-language-models
- knowledge-work
- domain-tuning
- cost-latency
- code-intelligence
relevance_score: 0.64
run_id: materialize-outputs
language_code: en
---

# Knowledge workers don't need frontier models

## Summary
The article argues that most knowledge-worker tasks can use small, domain-tuned language models selected by a cheap router, with frontier models reserved for harder cases. Its main claim is lower cost and latency with quality close to frontier-only systems on GDPVal and Microsoft MAI examples.

## Problem
- Knowledge workers often handle structured tasks in spreadsheets, email, and documents, where context, speed, and reliability matter more than peak reasoning.
- Sending every request to a frontier model raises inference cost and latency when many tasks fit smaller models.
- The cost gap matters at scale: the article uses a premise that 80% of requests could use a model that is 10× cheaper and 2× faster.

## Approach
- A nano-model router classifies each user task and sends it to GPT-5.5 for hard cases or GPT-5.4 Mini for easier cases.
- The router locks the selected model for the session to preserve prompt caches and keep output behavior stable.
- Routing overhead is reported as less than $0.01 per request.
- The article pairs routing with domain post-training: distillation, reinforcement learning, and domain adaptation on clean data, described through Microsoft MAI and Frontier Tuning examples.

## Results
- On GDPVal-AA, GPT-5.4 Mini alone scores 1417 ELO, GPT-5.5 alone scores 1769 ELO, and the routed GPT-5.5/GPT-5.4 Mini setup scores 1759 ELO.
- The routed setup is reported as #2 overall among 368 model configurations and within 10 ELO points of GPT-5.5 alone.
- The article claims GPT-5.5 costs more than 10× GPT-5.4 Mini, while the routed system loses only 10 ELO points versus GPT-5.5 alone.
- MAI-Code-1-Flash, with about 5B active parameters, is reported to beat Claude Haiku 4.5 on all tested coding benchmarks, including SWE-Bench Pro at 51.2% versus 35.2%, while using up to 60% fewer tokens.
- MAI-Thinking-1, with 35B active parameters, is reported to match Claude Opus 4.6 on SWE-Bench Pro, score 97% on AIME 2025, and win blind human preference tests against Sonnet 4.6 across 1,276 tasks.
- The article claims Frontier-Tuned MAI for Excel matches GPT-5.4 at up to 10× lower inference cost, and the overall routing plus tuned-SLM setup gives 75–90% cost reduction and 2–3× latency improvement.

## Link
- [https://mukulsingh105.github.io/articles/slm-routing-knowledge-workers.html](https://mukulsingh105.github.io/articles/slm-routing-knowledge-workers.html)
