---
source: hn
url: https://dimensionaldesign.org/
published_at: '2026-05-30T23:09:09'
authors:
- etothepii
topics:
- ai-validation
- software-engineering
- human-ai-interaction
- document-processing
- workflow-design
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# The Manifesto for Dimensional Design

## Summary
Dimensional Design argues that AI systems should handle tasks where approximate answers are safe, while deterministic software or small human checks should guard places that need exact answers. Its main contribution is a design manifesto for validation, file formats, and review tasks around predictive AI.

## Problem
- Predictive AI can produce plausible wrong outputs; chained steps compound error, so line-by-line review and majority voting can miss faults.
- Hidden structure in formats such as Word, PowerPoint, and PDF gives AI more state to preserve, which raises error risk during editing.
- This matters for software and document workflows because AI can generate more output than inherited review processes can check.

## Approach
- Split work by tolerance: use AI where “probably right” is acceptable and use deterministic checks where exactness is required.
- Validate output on an independent dimension, such as comparing digitized invoice values with the printed total rather than re-reading entries.
- Use deterministic programs as pass-fail gates; if AI output fails, generate again until it passes.
- Keep content in plain text or other low-dimensional forms during collaboration; add formatting and layout at publication through deterministic tooling.
- Where deterministic validation is impossible, make human review small, itemized, and recorded.

## Results
- The excerpt reports 0 empirical benchmarks: no dataset, baseline, sample size, accuracy, runtime, or ablation result is given.
- It gives an illustrative 99-in-100 correctness case to argue that line-by-line review cannot reliably catch the 1 wrong output.
- It claims independent checks such as invoice total reconciliation and double-entry debit/credit balance can detect errors without re-reading every item.
- It states 4 values and 8 principles for AI-assisted work: separate approximate and exact tasks, use deterministic gates, validate independently, and keep content low-dimensional until publication.

## Link
- [https://dimensionaldesign.org/](https://dimensionaldesign.org/)
