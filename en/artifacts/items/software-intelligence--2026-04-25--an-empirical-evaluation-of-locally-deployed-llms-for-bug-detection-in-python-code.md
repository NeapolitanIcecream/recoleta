---
source: arxiv
url: http://arxiv.org/abs/2604.23361v1
published_at: '2026-04-25T16:05:30'
authors:
- "Jelena Ili\u0107 Vuli\u0107evi\u0107"
topics:
- local-llms
- bug-detection
- python-code
- code-intelligence
- offline-inference
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# An Empirical Evaluation of Locally Deployed LLMs for Bug Detection in Python Code

## Summary
This paper tests whether small open-weight LLMs running fully offline can find real Python bugs. On 349 BugsInPy cases, LLaMA 3.2 and Mistral reached about 43% to 45% accuracy, with many additional responses that spotted the problem area but missed the exact fix.

## Problem
- The paper studies bug detection with locally deployed LLMs, where cloud models are often unusable because of privacy, cost, or internet requirements.
- Prior work focused more on cloud systems, synthetic tasks, or narrower bug classes, so the practical value of offline consumer-hardware models for real Python bugs was unclear.
- This matters for code intelligence and developer tooling because teams may want bug analysis on proprietary code without sending source code to external services.

## Approach
- The authors evaluate two local models, **LLaMA 3.2 8B** and **Mistral 7B**, using **Ollama** on a **MacBook Pro 14-inch (2021) with M1 Pro and 16GB RAM**, fully offline with **4-bit quantization**.
- They use the **BugsInPy** benchmark and successfully process **349 of 501 bugs** from **17 Python projects** after excluding cases where source retrieval or function extraction failed.
- For each bug, they extract the enclosing function around the buggy line and give the model a **zero-shot prompt**: “Here is a Python function. It contains a bug. Find the bug and explain how to fix it.”
- They score free-text answers with an automated keyword method based on tokens added in the fix, labeling outputs as **correct**, **partial**, or **wrong**; a manual check of **50 responses** found high agreement with the automatic labels.
- They also break results down by project and by **9 bug types**, such as Null/None checks, return value bugs, indexing, and complex multi-component bugs.

## Results
- Overall accuracy was **43.3%** for **LLaMA 3.2** (**151/349 correct, 171 partial, 27 wrong**) and **44.4%** for **Mistral** (**155/349 correct, 161 partial, 33 wrong**).
- The gap between models was small: **McNemar’s test p = 0.68**, with paired outcomes of **126 both-correct**, **169 both-wrong**, **25 LLaMA-only correct**, and **29 Mistral-only correct**. The paper treats this as no significant difference.
- Accuracy varied a lot by project: examples include **PySnooper 100%** for both models, **black 73.7% / 68.4%**, **fastapi 69.2% / 61.5%**, **pandas 38.5% / 44.8%**, and **tqdm 0.0% / 14.3%** for LLaMA/Mistral.
- By bug type, both models did best on **Null/None Check** bugs (**59.5% LLaMA, 60.8% Mistral**) and **Return Value** bugs (**51.3% for both**). They did poorly on **Type Conversion** (**0.0% for both**) and **Other/Complex** bugs (**21.7% LLaMA, 16.7% Mistral**).
- Inference was feasible on consumer hardware: average response time was about **7 seconds** for **LLaMA 3.2** and **13 seconds** for **Mistral**, for total runs of about **40 minutes** and **75 minutes**.
- The strongest practical claim is that local models can catch a meaningful share of real bugs and often narrow the search area, but precise localization remains weak when the bug depends on wider program context or cross-function behavior.

## Link
- [http://arxiv.org/abs/2604.23361v1](http://arxiv.org/abs/2604.23361v1)
