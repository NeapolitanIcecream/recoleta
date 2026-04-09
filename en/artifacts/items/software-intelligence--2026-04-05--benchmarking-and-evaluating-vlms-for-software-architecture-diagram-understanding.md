---
source: arxiv
url: http://arxiv.org/abs/2604.04009v1
published_at: '2026-04-05T07:54:18'
authors:
- Shuyin Ouyang
- Jie M. Zhang
- Jingzhi Gong
- Gunel Jahangirova
- Mohammad Reza Mousavi
- Jack Johns
- Beum Seuk Lee
- Adam Ziolkowski
- Botond Virginas
- Joost Noppen
topics:
- vision-language-models
- software-architecture
- diagram-understanding
- benchmarking
- multimodal-reasoning
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Benchmarking and Evaluating VLMs for Software Architecture Diagram Understanding

## Summary
This paper introduces SADU, a benchmark for testing whether vision-language models can read and reason over software architecture diagrams. Current models are far from reliable on this task: the best reported accuracy is 70.18%, and several widely used models perform much worse.

## Problem
- Software engineering benchmarks focus mostly on code, while early design artifacts such as architecture diagrams are less studied.
- Architecture diagrams carry system structure, behavior, and data relationships, so weak diagram understanding can break architecture-level assistance and create mismatches between design and implementation.
- General multimodal benchmarks do not test software-specific diagram semantics in a focused way.

## Approach
- The authors build **SADU**, a benchmark with **154** curated software architecture diagrams: **51 behavioral**, **53 structural**, and **50 ER** diagrams.
- Each diagram gets manual structured annotation in JSON, including entities, relations, clusters, and optional attributes or methods; the annotation took about **160 human hours**.
- The benchmark includes **2,431** QA tasks across **24** subtypes, covering counting, retrieval, and relation reasoning over diagram elements.
- They evaluate **11** VLMs from the **Gemini, Claude, GPT, and Qwen** families with temperature set to **0**, using both exact-match rule-based scoring and an LLM-as-a-judge protocol.
- They also analyze difficulty by diagram type, question subtype, complexity, and token cost.

## Results
- SADU is built from an initial pool of **1,044** diagrams, filtered down to **154** after removing **318** duplicates, **157** low-resolution images, **64** unreadable diagrams, and **311** items excluded for relevance or annotation quality.
- Best overall accuracy is **70.18%** for **gemini-3-flash-preview**. Next are **gemini-2.5-flash: 69.68%**, **gemini-3.1-flash-lite-preview: 66.31%**, **claude-sonnet-4.5: 56.36%**, **gpt-5-nano: 55.45%**, and **gpt-4o-mini: 17.77%**.
- Performance varies by diagram type. **gemini-3-flash-preview** scores **63.58%** on behavioral, **68.87%** on structural, and **78.53%** on ER diagrams. **gemini-2.5-flash** reaches the highest ER score reported in the excerpt at **82.54%**.
- Open-weight Qwen models trail the top closed models, with a size trend: **qwen-2.5-VL-32B: 45.17%**, **7B: 38.58%**, **3B: 31.30%** overall.
- Diagram complexity hurts all models: accuracy drops as the number of entities and relations grows, with behavioral diagrams and grounding-heavy retrieval tasks described as the hardest cases.
- Token cost differs sharply across models. **gpt-5-nano** uses **1475.19** completion tokens on average, while many lighter models stay around **13–20** tokens; **gemini-3.1-flash-lite-preview** is reported as a strong accuracy-cost tradeoff at **66.31%** accuracy with **16.94** average completion tokens.

## Link
- [http://arxiv.org/abs/2604.04009v1](http://arxiv.org/abs/2604.04009v1)
