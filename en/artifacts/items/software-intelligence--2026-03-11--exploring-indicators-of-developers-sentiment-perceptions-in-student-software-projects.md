---
source: arxiv
url: http://arxiv.org/abs/2603.10864v1
published_at: '2026-03-11T15:16:58'
authors:
- Martin Obaidi
- Marc Herrmann
- Jendrik Martensen
- "Jil Kl\xFCnder"
- Kurt Schneider
topics:
- sentiment-analysis
- software-engineering
- developer-communication
- longitudinal-study
- human-factors
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# Exploring Indicators of Developers' Sentiment Perceptions in Student Software Projects

## Summary
This paper investigates why developers in student software projects may make different sentiment judgments about the same text message, and examines how those judgments change over time, mood, and team-related factors. The core conclusion is that sentiment perception is not stable within individuals and is more strongly influenced by the ambiguity of specific statements than by any clear project-phase effects.

## Problem
- Text-based communication in software teams affects the collaborative climate and emotional contagion, but the same sentence is often interpreted as positive, negative, or neutral by different developers—or even by the same developer at different times.
- Existing sentiment analysis research in software engineering is mostly based on static, cross-sectional labeling, with less attention to whether the perceptions of the **same person** change over time and whether they are related to mood, life circumstances, conflict, project phase, and similar factors.
- This matters because if sentiment perception itself is highly subjective and variable, the outputs of automated sentiment analysis tools may be overinterpreted, leading to misjudgments about team climate.

## Approach
- The authors conducted a **four-wave longitudinal survey study** involving **81 student developers** from team-based software project courses; the full course context included **204 students and 28 project teams**.
- In each wave, participants assigned one of three labels—positive / neutral / negative—to **30 decontextualized developer statements**; these statements were drawn from GitHub and Stack Overflow datasets, with balanced sampling across the positive / neutral / negative classes.
- They also collected multiple explanatory variables: long-term mood trait, emotional reactivity, short-term mood state (PANAS), life satisfaction, relationship conflict / task conflict, project phase, as well as labeling rationale, confidence, and reasons for uncertainty.
- The analysis first examined within-person stability and correlations, and then used **GEE repeated-measures models** at the statement level to analyze which factors made participants more likely to label a statement as positive, negative, or neutral.

## Results
- The study included **4 waves**, **81 participants**, and **30 statements** per wave; this enabled the authors to observe how labels assigned by the same developer changed over time.
- The authors explicitly report that **within-person sentiment perception is only moderately stable**, and that label changes are concentrated mainly on **ambiguity-prone statements**; this indicates that the **statement itself** is a strong influencing factor.
- Signals at the correlation level were generally **small**, and after **global multiple-testing correction** they were no longer significant; in other words, many apparent correlations were not robust.
- In the **GEE statement-level repeated-measures models**, **higher mood trait and reactivity** were associated with **a greater tendency toward positive labeling and less neutral labeling**; in contrast, **predictors of negative labeling were weaker**, with at most trend-level evidence, such as **task conflict**.
- For external contextual factors, the paper states that it **found no clear evidence of systematic project-phase effects**; in other words, approaching deadlines or later project stages did not show strong, stable evidence of changing perception.
- The abstract and introduction **do not provide specific effect sizes, accuracy, p-values, or baseline improvement figures**; the strongest quantitative facts are mainly the sample and design scale (81 people, 4 waves, 30 statements), along with conclusion-level statements such as “not significant after multiple correction,” “small effects,” and “moderate stability.”

## Link
- [http://arxiv.org/abs/2603.10864v1](http://arxiv.org/abs/2603.10864v1)
