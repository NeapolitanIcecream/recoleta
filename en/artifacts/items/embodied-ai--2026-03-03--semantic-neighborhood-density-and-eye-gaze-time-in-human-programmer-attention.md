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
- code-language-models
- human-attention
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Semantic Neighborhood Density and Eye Gaze Time in Human Programmer Attention

## Summary
This paper investigates whether the Semantic Neighborhood Density (SND) of source code tokens is related to programmers' eye-gaze fixation time, and conducts statistical and predictive analyses on two eye-tracking datasets in C and Java. The conclusion is that high-SND words usually receive longer fixation times, especially low-frequency words, but their overall predictive power is weak.

## Problem
- The paper aims to solve the question: **does whether words in source code are "semantically crowded" (high vs. low SND) affect how long programmers fixate on them while reading code**, and can this relationship help explain or predict programmer attention.
- This matters because eye-gaze time is often used as a proxy for **cognitive load, level of confusion, and allocation of attention**; understanding its drivers could improve program comprehension research, tool design, and attention modeling.
- In psycholinguistics, SND has already been shown to be related to natural language reading, but **it has been largely unstudied in software engineering/code reading contexts**, where its meaning may differ.

## Approach
- Uses two existing eye-tracking experiment datasets: a **C bug localization** dataset (21 programmers, about **31 hours**) and a **Java code summarization/documentation writing** dataset (10 programmers, about **60 hours**).
- Extracts tokens from code repositories; for Java, additionally performs **camelCase/underscore splitting** and lowercasing to build language-specific vocabularies.
- Uses two kinds of language models to generate word embeddings: **GPT2 (350M models trained separately for C and Java)** and **CodeLLaMA 7B**; then computes SND following the ARC approach of Shaoul & Westbury: first uses **10k random word pairs** to estimate a global distance threshold, then takes the average cosine similarity of neighbors within that threshold for each word as its SND.
- Also computes term frequency (TF), and performs two kinds of analysis: first, a **model-free statistical analysis**, dividing words into high/low SND, high/low frequency, and "high SND and low frequency" groups, and comparing four eye-tracking metrics (SFD, FFD, GD, RPD); second, a **model-based analysis** to examine the predictive discriminative power of SND and frequency for fixation duration.

## Results
- In terms of scale, the study covers **2 programming language/task settings**: the C dataset has **21 people, 31 hours**, and the Java dataset has **10 people, 60 hours**; this indicates the analysis is based on long periods of real code reading.
- The paper's core finding is that: **high-SND words tend to have higher gaze time than low-SND words**, and this phenomenon is more evident in the **C dataset**; the abstract excerpt does not provide specific significance values, effect sizes, or complete statistical tables for each metric.
- Another explicit conclusion is that: **there is an interaction between SND and word frequency**, where **low-frequency and high-SND** words are more likely to receive higher visual attention; the authors use this to respond to the "high SND × low frequency" effect in psycholinguistics.
- Regarding model choice, the authors claim that this relationship is stronger when using **custom GPT2 to compute SND**; however, the abstract excerpt does not provide quantitative comparison values against **CodeLLaMA**.
- On prediction, the authors state that **SND and frequency have only minor predictive power for gaze time**, indicating that although they are related to attention, they are not sufficient to strongly predict fixation duration in noisy eye-tracking data.
- **No clear quantitative results are provided**: the given excerpt does not report specific p-values, FDR correction results, Hedges' g, accuracy/AUC, or the magnitude of improvement relative to any baseline model.

## Link
- [http://arxiv.org/abs/2603.03566v1](http://arxiv.org/abs/2603.03566v1)
