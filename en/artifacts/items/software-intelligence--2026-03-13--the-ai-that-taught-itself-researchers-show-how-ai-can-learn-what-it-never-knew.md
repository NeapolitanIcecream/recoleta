---
source: hn
url: https://viterbischool.usc.edu/news/2026/03/the-ai-that-taught-itself-usc-researchers-show-how-artificial-intelligence-can-learn-what-it-never-knew/
published_at: '2026-03-13T23:16:41'
authors:
- hhs
topics:
- llm-code-generation
- compiler-feedback
- low-resource-learning
- iterative-refinement
- program-synthesis
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# The AI that taught itself: Researchers show how AI can learn what it never knew

## Summary
This study shows that AI does not have to be entirely constrained by how much training data it has seen; as long as it is given a clear, verifiable external feedback loop, it can significantly improve its performance in extremely low-resource domains. The authors demonstrated this using the obscure programming language Idris, dramatically boosting GPT-5’s problem-solving success rate from a very low baseline.

## Problem
- The traditional assumption is that AI’s ability in a given domain is basically limited by the coverage of its training data; this is especially true for low-resource languages or niche tasks.
- This matters because many real-world tasks fall into scenarios that are “data-scarce but rule-clear,” such as niche programming languages, mathematical proofs, legal reasoning, and low-resource natural languages.
- The paper seeks to answer: **when a model has barely seen a domain, can structured feedback alone—rather than additional training data—raise performance far beyond its initial level?**

## Approach
- The researchers chose the extremely obscure programming language **Idris** as the test case; it has about **2,000** public code repositories, while Python has more than **24 million**, a difference of roughly **10,000x** in data volume.
- They had **GPT-5** complete **56** Idris programming exercises on Exercism, first measuring its raw capability and then comparing several enhancement methods.
- Simply providing documentation, error manuals, and reference materials produced only limited gains, showing that “giving it more explanatory material” was not the key breakthrough.
- The core mechanism was a **compiler feedback loop**: the compiler’s precise error messages were fed directly back to the model, which then fixed the errors and resubmitted; each problem was allowed up to **20** iterations.
- Put simply, the method is: **let the AI try first, then tell it in successive rounds the errors that a machine can identify objectively, until it gets them right.**

## Results
- On the **56** Idris problems, GPT-5 out of the box solved only **22/56**, a success rate of **39%**.
- For comparison, the article reports the same model’s success rates as: **Python 90%** and **Erlang 74%**, showing that Idris was dramatically worse at baseline.
- After only adding documentation, error manuals, and reference guides, Idris success rose only to the **low 60s**, without any decisive leap.
- After introducing the compiler feedback loop, the success rate increased from **39%** to **96%**; that is, from **22/56** to about **54/56**.
- The paper’s central claim is: **in domains with very weak training coverage, as long as there is a clear, correct, programmable feedback signal, a model’s capabilities can be “unlocked” and significantly exceed its initial zero-shot/few-shot performance.**
- The article also suggests possible extrapolations, such as 3D structural design, mathematical proofs, legal reasoning, and translation for low-resource human languages, but the provided text **does not yet include quantitative experimental results** for these extended applications.

## Link
- [https://viterbischool.usc.edu/news/2026/03/the-ai-that-taught-itself-usc-researchers-show-how-artificial-intelligence-can-learn-what-it-never-knew/](https://viterbischool.usc.edu/news/2026/03/the-ai-that-taught-itself-usc-researchers-show-how-artificial-intelligence-can-learn-what-it-never-knew/)
