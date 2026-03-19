---
source: hn
url: https://viterbischool.usc.edu/news/2026/03/the-ai-that-taught-itself-usc-researchers-show-how-artificial-intelligence-can-learn-what-it-never-knew/
published_at: '2026-03-13T23:16:41'
authors:
- hhs
topics:
- iterative-feedback
- low-resource-learning
- code-generation
- compiler-guidance
- self-correction
relevance_score: 0.14
run_id: materialize-outputs
language_code: en
---

# The AI that taught itself: Researchers show how AI can learn what it never knew

## Summary
This study shows that in extremely low-resource domains, AI is not entirely limited by its training data. With the right external feedback loop, its performance can improve dramatically. Using code-generation experiments with GPT-5 in the niche programming language Idris, the authors demonstrate this kind of “self-correcting” improvement.

## Problem
- The traditional assumption is that a model’s capability in a given domain is largely constrained by the amount of data it has seen; low-resource domains therefore perform poorly.
- This is especially important in scenarios such as niche programming languages, formal reasoning, and low-resource human languages, where available training data is extremely limited.
- The research asks: when there is almost no sufficient training coverage, can AI learn to complete tasks it was not originally good at by leveraging external feedback?

## Approach
- The researchers chose the extremely low-resource language **Idris** as the test case: there are about **2,000** public repositories, while Python has more than **24 million**, a data gap of roughly **10,000×**.
- They had **GPT-5** solve **56** Idris programming exercises on Exercism, first measuring baseline performance and then comparing different enhancement methods.
- They tried static aids such as documentation, error manuals, and reference materials, but these methods only raised the success rate to a little over **60%**.
- The core method was a **compiler feedback loop**: the specific compiler error messages were fed directly back to the model, allowing it to fix errors and retry, with up to **20 attempts** per problem.
- The mechanism is essentially simple: the model writes code, the compiler points out what is wrong, the model revises based on the error messages, and the process repeats until it passes.

## Results
- On Idris, GPT-5 out of the box solved only **22/56** problems, for a success rate of **39%**.
- For comparison, the article says GPT-5 achieves about **90%** success on **Python** and about **74%** on **Erlang**, showing that Idris is indeed a clearly difficult low-resource case.
- After providing documentation and reference materials, the Idris success rate rose only to a little over **60%**, a limited improvement that still did not approach mainstream-language performance.
- After using the compiler feedback loop, the success rate increased from **39% to 96%**, or about **54/56** problems, an improvement of **57 percentage points** over the baseline.
- Based on this, the authors claim that as long as a task has a clear, correct, and automatically generable feedback signal, AI may significantly exceed what “training data alone” would allow in domains with insufficient training coverage.
- The article does not provide finer-grained statistical significance tests, ablation studies, or systematic cross-model / cross-task evaluations; applications to mathematical proofs, legal reasoning, 3D modeling, and low-resource human languages are currently mainly forward-looking extrapolations.

## Link
- [https://viterbischool.usc.edu/news/2026/03/the-ai-that-taught-itself-usc-researchers-show-how-artificial-intelligence-can-learn-what-it-never-knew/](https://viterbischool.usc.edu/news/2026/03/the-ai-that-taught-itself-usc-researchers-show-how-artificial-intelligence-can-learn-what-it-never-knew/)
