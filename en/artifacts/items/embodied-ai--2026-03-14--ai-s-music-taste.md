---
source: hn
url: https://abidsikder.pages.dev/blog/2026-03-14-ai-music-taste/
published_at: '2026-03-14T23:57:07'
authors:
- caaaadr
topics:
- audio-understanding
- multimodal-llm
- model-evaluation
- music-preference
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# AI's Music Taste

## Summary
This article is not a formal academic paper, but rather a fun experimental blog post: the author had several large models that support audio input write short reviews and assign ratings to different songs, in order to observe the "musical taste of AI." It is more like a qualitative comparison and a collection of interesting cases than a systematic research paper.

## Problem
- Explore whether audio multimodal models can form comparable "preferences" for music, and whether they can comment on and rate songs.
- What makes this question interesting is that it tests the models' abilities in open-ended audio understanding, subjective evaluation, and structured output.
- However, there are currently very few available models, because they need to support both **audio input** and **structured output**, which limits the scope of testing.

## Approach
- The author selected a small batch of models available on OpenRouter that support both audio input and structured output for evaluation.
- Audio from a **wide range of songs** was fed in, and the models generated **short reviews** and assigned **ratings**, which were then compared horizontally across models for the same song.
- The results are presented mainly through interesting observations, such as differences in how various models respond to pop songs, meme songs, and even intentionally unpleasant sounds.
- The author also recorded abnormal cases: for example, Healer Alpha often produced strange results or errors, so some results were marked as NA.

## Results
- The excerpt **does not provide systematic quantitative metrics**, such as total sample size, average score, correlation coefficients, accuracy, or benchmark comparison results.
- The strongest concrete conclusions are several qualitative findings: **Gemini** really dislikes Rick Astley's *Never Gonna Give You Up*, while **voxtral** likes it a lot.
- **voxtral** even liked "**nails on a chalkboard**," an intentionally unpleasant sound, suggesting its preferences may differ markedly from human intuition.
- **Gemini** had mixed or lukewarm feelings about Ye's *Champion*, but rated works from his *Yeezus* era more highly.
- **Gemini Pro** clearly "hates" Rebecca Black's *Friday*; meanwhile, a smaller version of the model seems to love it, and a similar split appears for PSY's *GANGNAM STYLE*.
- **Healer Alpha** frequently produced anomalous outputs and errors, causing some results to be **NA**, which suggests that model stability itself is also a notable observation in the experiment.

## Link
- [https://abidsikder.pages.dev/blog/2026-03-14-ai-music-taste/](https://abidsikder.pages.dev/blog/2026-03-14-ai-music-taste/)
