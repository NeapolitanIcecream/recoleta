---
source: hn
url: https://abidsikder.pages.dev/blog/2026-03-14-ai-music-taste/
published_at: '2026-03-14T23:57:07'
authors:
- caaaadr
topics:
- audio-llm
- multimodal-evaluation
- model-behavior
- subjective-judgment
- music-analysis
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# AI's Music Taste

## Summary
This article presents a lightweight, fun experiment: having multimodal audio models write short reviews and assign ratings to different songs in order to observe the "music taste" of AI. It is more of a model-behavior showcase than a rigorous academic paper, but it can still reflect differences and instability among current audio-input large models on subjective aesthetic tasks.

## Problem
- The author wants to answer a simple but interesting question: **what kinds of "aesthetic preferences" do different AI models show after listening to music**.
- The importance of this question is not in establishing a standard music evaluation benchmark, but in revealing that when models handle **open-ended, highly subjective audio tasks**, their outputs may show clear disagreement, odd preferences, and stability issues.
- The article also implicitly points out a practical constraint: **there are very few available audio-input models**, and they also need to support **structured output**, which limits systematic comparison.

## Approach
- The author selected a small batch of models available through **OpenRouter** that support both **audio input** and **structured output** for testing.
- These models were played a series of songs and sound samples, and were asked to **generate short comments and give ratings**.
- The author compared how different models evaluated the same audio, observing whether there were consistent preferences, extreme scores, or obviously anomalous results.
- Abnormal cases were recorded; for example, **Healer Alpha** often produced strange outputs and errors, so some results were marked as **NA**.

## Results
- The article **does not provide systematic quantitative metrics**, such as sample size, average score, variance, accuracy, or statistical significance, so there are no strict, reproducible numerical conclusions.
- The most concrete findings are several differences in model preferences: **Gemini** clearly dislikes *Never Gonna Give You Up*, while **voxtral** likes it very much.
- **voxtral** even liked the "**nails on a chalkboard**" sample, an intentionally unpleasant sound inserted by the author, suggesting that its aesthetic judgment may differ sharply from human intuition.
- For **Ye's Champion**, **Gemini** rated it from low to neutral, but the author says it rated works from the **Yeezus** era more highly.
- **Gemini Pro** strongly dislikes **Rebecca Black - Friday**; meanwhile, a smaller version of the model seems to like it a lot. A similar split also appears for **PSY - GANGNAM STYLE**.
- Overall, the strongest conclusion of the article is that current audio-capable LLMs/multimodal models show clear **inter-model differences, instability, and anomalous preferences** in **subjective music evaluation**.

## Link
- [https://abidsikder.pages.dev/blog/2026-03-14-ai-music-taste/](https://abidsikder.pages.dev/blog/2026-03-14-ai-music-taste/)
