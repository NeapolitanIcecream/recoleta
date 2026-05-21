---
source: arxiv
url: https://arxiv.org/abs/2605.17062v1
published_at: '2026-05-16T16:08:52'
authors:
- Aleksandr Churilov
topics:
- llm-code-generation
- package-hallucination
- software-supply-chain
- slopsquatting
- code-intelligence
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort

## Summary
The paper measures package-name hallucinations in five 2026 code-capable LLMs and finds that rates have converged near 5–6%, while slopsquatting risk remains. Its strongest new claim is a shared set of 127 nonexistent package names hallucinated by all five models.

## Problem
- Code-generating LLMs sometimes suggest nonexistent PyPI or npm packages in install commands or imports.
- Attackers can register those names and wait for developers to install malicious packages, creating a software supply-chain risk.
- The paper asks whether newer frontier models reduced this risk compared with Spracklen et al.'s 2024 cohort.

## Approach
- The study replicates Spracklen et al.'s package-hallucination method on Claude Sonnet 4.6, Claude Haiku 4.5, GPT-5.4-mini, Gemini 2.5 Pro, and DeepSeek V3.2.
- It runs 199,845 Python and JavaScript prompts, using the same Stack Overflow and LLM-synthesized prompt sets as the earlier work.
- It extracts package names from install commands and import statements, then checks them against PyPI and npm master lists.
- It reports hallucination rates, confidence intervals, pairwise model differences, language splits, and overlap in unique hallucinated names.

## Results
- Overall hallucination rates range from 4.62% for Claude Haiku 4.5 to 6.10% for GPT-5.4-mini; the 2024 Spracklen range was 5.2%–21.7%.
- The inter-model spread shrinks from 16.5 percentage points in the 2024 cohort to 1.48 percentage points in this 2026 cohort, an 11-fold narrowing.
- The paper identifies 127 package names hallucinated by all five models: 109 on PyPI and 18 on npm.
- Python hallucination rates exceed JavaScript rates for every model: Python ranges from 5.49% to 7.27%, while JavaScript ranges from 2.62% to 3.78%.
- Claude Haiku 4.5 hallucinates less than Claude Sonnet 4.6, 4.62% versus 5.41%, with a 0.79 percentage-point gap after Holm correction.
- DeepSeek V3.2 and GPT-5.4-mini have the highest overlap in hallucinated names, with Jaccard similarity J = 0.343; the mean pairwise Jaccard value is 0.222.

## Link
- [https://arxiv.org/abs/2605.17062v1](https://arxiv.org/abs/2605.17062v1)
