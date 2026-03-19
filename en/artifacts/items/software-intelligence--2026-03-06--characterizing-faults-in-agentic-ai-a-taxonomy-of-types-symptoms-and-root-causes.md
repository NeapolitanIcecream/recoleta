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
- software-debugging
- reliability-engineering
- empirical-study
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Characterizing Faults in Agentic AI: A Taxonomy of Types, Symptoms, and Root Causes

## Summary
This paper analyzes real defects in open-source Agentic AI projects and proposes an empirical taxonomy of fault types, symptoms, and root causes, while also studying how these faults propagate across components. Its value lies in providing a more systematic foundation for debugging, observability, and reliability engineering for agentic systems.

## Problem
- Agentic AI combines **LLM reasoning, tool invocation, and long-horizon control**, and its fault patterns differ from those of traditional software or purely chat-based LLMs, yet there is currently a lack of systematic empirical understanding.
- These systems have already entered critical scenarios such as automation, software engineering, and robotics; without understanding how faults arise, manifest, and propagate, there are risks to reliability, safety, and economic outcomes.
- Existing research often remains at the level of task failures or high-level behavioral errors, and less often establishes clear mappings between faults and **specific system components, observable symptoms, and root causes**.

## Approach
- The authors collected **13,602** closed issues and merged PRs from **40 open-source agentic AI repositories**, and used stratified sampling to select **385** faults for in-depth manual analysis.
- Using **grounded theory**, they derived three taxonomies from real issue descriptions, logs, stacks, and fix commits: **5 architectural fault dimensions, 13 symptom classes, and 12 root cause classes**.
- They used **Apriori association rule mining** to analyze high-strength co-occurrence relationships among “fault type–symptom–root cause” in order to discover cross-component fault propagation paths.
- They then validated whether the taxonomy matched real development experience through a survey of **145 developers**, and examined its completeness and practicality based on the feedback.

## Results
- The paper produced a structured taxonomy: **5 fault dimensions, 13 symptom categories, and 12 root cause categories**, showing that failures in agentic AI are not random but can be systematically characterized.
- In the sample, **Runtime and Environment Grounding**-related faults appeared **87** times; the main root causes included **Dependency and Integration Failures（19.5%）** and **Data and Type Handling Failures（17.6%）**.
- The association rules show clear cross-layer propagation: for example, the association strength between **authentication request failures ↔ fragile token refresh mechanisms** had **lift = 181.5**; **incorrect time values ↔ improper datetime conversion** had **lift = 121.0**.
- The developer validation results were strong: the taxonomy’s average representativeness rating was **3.97/5**, internal consistency was **Cronbach's α = 0.904** (another place in the paper reports approximately **0.91**), and **83.8%** of respondents said it covered faults they had encountered.
- In the survey, **74.5%** of ratings were **4 or above**, indicating that most categories were considered practically relevant.
- The paper did not report “performance improvement” style results against existing methods on a unified benchmark; its strongest claim is that it is the first to establish a componentized taxonomy and propagation patterns for diagnosing agentic AI faults using large-scale open-source evidence and developer validation.

## Link
- [http://arxiv.org/abs/2603.06847v1](http://arxiv.org/abs/2603.06847v1)
