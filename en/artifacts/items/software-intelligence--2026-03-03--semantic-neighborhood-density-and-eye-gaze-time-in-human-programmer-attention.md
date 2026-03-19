---
source: arxiv
url: http://arxiv.org/abs/2603.03566v1
published_at: '2026-03-03T22:51:04'
authors:
- Robert Wallace
- Emory Michaels
- Yu Huang
- Collin McMillan
topics:
- program-comprehension
- eye-tracking
- semantic-neighborhood-density
- code-embeddings
- human-attention
relevance_score: 0.64
run_id: materialize-outputs
language_code: en
---

# Semantic Neighborhood Density and Eye Gaze Time in Human Programmer Attention

## Summary
This paper investigates whether the Semantic Neighborhood Density (SND) of source-code tokens is related to programmers' eye-gaze fixation time, and conducts statistical and predictive analyses on two real eye-tracking datasets in C and Java. The conclusion is that high-SND words, especially low-frequency words, usually receive longer fixation time, but this information provides only a small gain for predicting fixation time.

## Problem
- The paper aims to solve the following question: **does how “crowded” a word’s semantic neighborhood is in source code affect programmers’ visual attention and cognitive load during reading**, and can this effect be used to predict eye-gaze time.
- This matters because eye-gaze time is often used as a proxy signal for program comprehension difficulty and attention allocation; if we can explain which code words are more “attention-grabbing” or more confusing, it could help improve program comprehension, code presentation, and human-centered software design.
- Existing SND research is mainly in natural language reading, and its meaning in software engineering is unknown. In particular, code words are often abstract but lack the emotional factors present in natural language, so they may exhibit different patterns.

## Approach
- Uses two existing eye-tracking datasets: **C bug localization** (21 programmers, about **31 hours**) and **Java code summarization/documentation writing** (10 programmers, about **60 hours**).
- Extracts tokens from code repositories; for Java, additionally performs camelCase/snake_case splitting and lowercasing. It then uses two kinds of code language models to generate word embeddings: **GPT2-like 350M** trained separately for C/Java, and the multilingual code model **CodeLLaMA 7B**.
- Computes **SND** for each word following the ARC method of Shaoul & Westbury: first estimates a global distance threshold in embedding space using 10k randomly sampled word pairs, then averages the cosine similarity of neighbors within that threshold; it also computes corpus-level **term frequency (TF)**.
- Conducts two kinds of analyses: first, a **model-free statistical analysis**, grouping words by high/low SND, frequency, and “high SND and low frequency,” and comparing four eye-tracking metrics: **SFD/FFD/GD/RPD**; second, a **model-based analysis** testing whether SND and frequency have predictive power for fixation time.

## Results
- Main finding: **high-SND words are more likely than low-SND words to receive longer eye-gaze time**, and this trend is more pronounced in the **C dataset**, especially when SND is computed using **custom GPT2**.
- In terms of interaction effects, **low-frequency and high-SND words** are the most likely to receive more visual attention; the authors explicitly summarize this as: **rarer words with denser semantic neighborhoods tend to be fixated longer**.
- In terms of dataset scale, the experiments are based on two real tasks: the C dataset includes **21 people / 31 hours / 8 bug reports**, and the Java dataset includes **10 people / 60 hours / 40 methods**; the regression rate in C is about **43.0%–67.0%**, and in Java about **49.8%–56.6%**.
- On the modeling side, SND is computed using **GPT2 350M (1024-dimensional embeddings)** and **CodeLLaMA 7B (4096-dimensional embeddings)**; the paper claims that GPT2-derived SND performs better in terms of association, suggesting that language-specific embeddings may be more suitable for this analysis than cross-language large-model embeddings.
- For prediction, the authors state that **SND and frequency have only “minor predictive power”** for gaze time; the excerpt provided **does not include specific predictive metric values** (such as AUC, R², F1, or error reduction), so it is not possible to report quantitatively how much better it is than any baseline.

## Link
- [http://arxiv.org/abs/2603.03566v1](http://arxiv.org/abs/2603.03566v1)
