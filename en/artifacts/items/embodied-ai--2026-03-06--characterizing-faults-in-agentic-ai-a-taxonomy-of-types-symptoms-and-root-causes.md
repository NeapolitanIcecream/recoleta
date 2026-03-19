---
source: arxiv
url: http://arxiv.org/abs/2603.06847v1
published_at: '2026-03-06T20:12:29'
authors:
- Mehil B Shah
- Mohammad Mehdi Morovati
- Mohammad Masudur Rahman
- Foutse Khomh
topics:
- agentic-ai
- fault-taxonomy
- failure-analysis
- software-debugging
- reliability-engineering
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Characterizing Faults in Agentic AI: A Taxonomy of Types, Symptoms, and Root Causes

## Summary
This paper systematically studies faults in agentic AI systems and proposes an empirical taxonomy that links **fault types, observable symptoms, and root causes**. Its core value is showing that these failures are not random or chaotic, but structured, able to propagate across components, and amenable to systematic debugging.

## Problem
- The paper addresses the following problem: after **agentic AI** combines LLM reasoning, tool invocation, long-horizon control, and interaction with external environments, it exhibits new kinds of faults that differ from those in traditional software or standalone LLM applications, yet there is currently a lack of empirical understanding of **how these faults arise, how they manifest, and how they propagate across components**.
- This matters because agentic AI is being used in high-risk settings such as enterprise automation, software engineering, robotics, and decision support; without understanding fault patterns, it may lead to data deletion, security vulnerabilities, economic losses, and even physical risks in safety-critical domains.
- Existing research mostly remains at the level of task failure or behavior, and lacks analysis that maps failures to **specific system components**, making it difficult to support reliable debugging, observability, and reliability engineering.

## Approach
- The authors mined **13,602** closed issues and merged PRs from **40 open-source agentic AI repositories** as a source of real-world fault data.
- They used **stratified sampling** to select **385** faults for in-depth manual analysis, in order to preserve representativeness across different repository categories.
- They then used **grounded theory** for inductive coding: first extracting fine-grained phenomena from issues, logs, stack traces, and repair commits, and then gradually aggregating them into a higher-level taxonomy, ultimately producing a structured classification of fault types, symptoms, and root causes.
- To understand “how faults propagate,” they encoded each fault as a transaction of “fault category + symptom + root cause” and used **Apriori association rule mining** to identify statistically significant propagation relationships.
- Finally, they validated whether the taxonomy matched practical development experience through a survey of **145 developers**.

## Results
- The paper produced a relatively comprehensive taxonomy: **5 architectural fault dimensions, 13 symptom classes, and 12 root cause categories**.
- In the quantitative distribution, the authors note that **Runtime and Environment Grounding**-related faults had **87** instances; the main root causes were **Dependency and Integration Failures (19.5%)** and **Data and Type Handling Failures (17.6%)**.
- Association rule mining shows that faults often propagate across components rather than remaining isolated at a single point: for example, **authentication request failures** are strongly associated with fragile token refresh mechanisms, with reported **lift = 181.5**; **incorrect time values** are strongly associated with improper datetime conversion, with **lift = 121.0**.
- The developer validation results were strong: the taxonomy’s representativeness received an average score of **3.97/5**, internal consistency was **Cronbach's α = 0.904** (around **0.91** in the paper’s RQ3 section), **83.8%** of respondents said the taxonomy covered faults they had personally encountered, and **74.5%** of ratings were **4 or higher**.
- Compared with performance papers that aim to “beat some baseline model,” this work does not propose higher task scores, but instead claims a **fault classification and propagation framework supported by large-scale repository mining and developer validation**, which can serve as a foundation for agentic AI debugging and reliability engineering. The paper does not provide traditional ML benchmark comparisons such as accuracy / F1 / success-rate.

## Link
- [http://arxiv.org/abs/2603.06847v1](http://arxiv.org/abs/2603.06847v1)
