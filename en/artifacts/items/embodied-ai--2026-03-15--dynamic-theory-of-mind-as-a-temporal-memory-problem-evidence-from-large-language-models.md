---
source: arxiv
url: http://arxiv.org/abs/2603.14646v1
published_at: '2026-03-15T22:54:03'
authors:
- Thuy Ngoc Nguyen
- Duy Nhat Phan
- Cleotilde Gonzalez
topics:
- theory-of-mind
- temporal-memory
- llm-evaluation
- belief-tracking
- social-reasoning
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Dynamic Theory of Mind as a Temporal Memory Problem: Evidence from Large Language Models

## Summary
This paper reframes dynamic Theory of Mind (ToM) as a problem of **temporal memory and retrieval**, rather than just single-step static inference. The authors propose DToM-Track, which uses multi-turn conversations to test whether large language models can track how others’ beliefs change over time.

## Problem
- Most existing ToM evaluations only ask “what does someone believe at a given moment,” overlooking a more important ability in real interactions: **remembering and retrieving prior beliefs after an update occurs**.
- This matters because long-term human–AI interaction requires systems to continuously track users’ changing beliefs, goals, and misunderstandings; if a system can only capture the “latest state,” it will make mistakes in historical consistency and social reasoning.
- The authors ask: do LLMs actually possess dynamic ToM, or are they mainly good at inferring current beliefs from the most recent information?

## Approach
- They propose the **DToM-Track** evaluation framework, constructing multi-turn conversations with prearranged belief updates and specifically testing three types of dynamic questions: **recall of pre-update beliefs**, **inference of current post-update beliefs**, and **detection of when the update occurred**.
- The conversations are generated through controlled **LLM–LLM role-play**; before each turn, each role has hidden “inner speech” that explicitly records its private mental state, which is invisible to the dialogue partner, thereby creating information asymmetry.
- The framework maintains a structured mental-state tracker that records belief type, source turn, whether it was updated, and the pre-update content, enabling automatic generation of temporal questions and also supporting second-order belief and false belief questions.
- A multi-stage LLM filtering pipeline is used to verify whether planned updates were actually realized in the conversations, whether the questions are answerable, and whether distractors are reasonable; the final dataset contains **5,794** questions.
- Zero-shot multiple-choice evaluation is conducted on **6 models**: LLaMA 3.3-70B, Mistral Large, Ministral-14B, GPT-4o-mini, LLaMA 3.1-8B, and LLaMA 3.2-3B.

## Results
- The dataset contains **5,794** questions; the distribution by question type is Temporal **1,807 (31.2%)**, False Belief **1,761 (30.4%)**, Second-Order **768 (13.3%)**, Update Detection **591 (10.2%)**, Post-Update **527 (9.1%)**, and Pre-Update **340 (5.9%)**.
- In overall accuracy, all 6 models exceed the **25%** random baseline, ranging from **35.7%** (LLaMA 3.2-3B) to **63.3%** (LLaMA 3.3-70B), with GPT-4o-mini at **55.1%**.
- Averaged by question type, **Update Detection at 67.5%** is highest, followed by **Post-Update at 63.9%**, but **Pre-Update is only 27.7%**, showing that models are much better at answering “what is believed now” than recalling “what was believed before the update.”
- Compared with standard ToM questions, dynamic memory is clearly harder: **Pre-Update at 27.7%** is lower than **False Belief at 44.7%**, indicating that “tracking belief trajectories” is an independent challenge distinct from classical false-belief reasoning.
- For the strongest model, LLaMA 3.3-70B, accuracies by question type are Temporal **65.5%**, Update Detection **76.1%**, Post-Update **71.3%**, False Belief **59.2%**, Second-Order **62.0%**, and Pre-Update **40.9%**; even the strongest model shows a substantial drop on pre-update belief recall.
- The paper’s central empirical conclusion is that this stable asymmetry—“strong after updates, weak before updates”—appears across model families and scales, supporting the authors’ explanation in terms of **recent-information bias / interference**.

## Link
- [http://arxiv.org/abs/2603.14646v1](http://arxiv.org/abs/2603.14646v1)
