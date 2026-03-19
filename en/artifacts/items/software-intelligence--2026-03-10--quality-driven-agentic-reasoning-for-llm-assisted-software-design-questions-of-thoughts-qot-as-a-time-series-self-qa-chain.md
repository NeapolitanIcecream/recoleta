---
source: arxiv
url: http://arxiv.org/abs/2603.11082v1
published_at: '2026-03-10T23:49:09'
authors:
- Yen-Ku Liu
- Yun-Cheng Tsai
topics:
- llm-agents
- software-design
- inference-time-reasoning
- self-verification
- code-quality
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Quality-Driven Agentic Reasoning for LLM-Assisted Software Design: Questions-of-Thoughts (QoT) as a Time-Series Self-QA Chain

## Summary
This paper proposes QoT (Questions-of-Thoughts), a quality-oriented reasoning scaffold for software design that has an LLM first decompose engineering steps and then perform self-questioning checks for each step. It aims to reduce omissions, improve modularity and security, and leave behind a reusable lightweight reasoning record.

## Problem
- Existing LLM-assisted software development can often generate code that "looks usable," but it is frequently inadequate in **completeness, modularity, and security**, especially in multi-module, long-chain tasks where key constraints are easily missed.
- Checking only whether functionality runs is not enough, because real software systems also need to be **maintainable, auditable, and deployable**; this is especially important for backend systems, enterprise workflows, and compliance scenarios.
- Existing CoT/ToT/self-correction methods usually focus more on "generate first, then revise," and lack a **front-loaded constraint-organizing and step-by-step verification mechanism** centered on software quality attributes.

## Approach
- QoT first breaks the user goal into **ordered engineering steps** (Sequential Process Chain), for example, user modules first, then business modules, then routing and integration, to avoid missing dependency relationships during one-shot generation.
- For each step, the model automatically raises a set of **self-check questions** (Question-Answer Chain). Put simply, it is "asking itself while working: Is there access control? Is there error handling? Are there concurrency/consistency issues?"
- The system continuously writes intermediate conclusions into a **Reasoning Knowledge Base**, which serves as context for later steps and helps subsequent design stay consistent with earlier constraints.
- This method is an **inference-time enhancement** rather than training a new model: the base model remains unchanged, and only a quality-driven agentic scaffold is wrapped around the inference process.
- In evaluation, the authors use an ISO/IEC-inspired quality rubric to score **Scalability, Completeness, Modularity, and Security** on a 1–4 scale, and compare differences among QoT, NoQoT, and CoT.

## Results
- In the **QoT vs CoT** comparison, **llama3.1_70b** shows the clearest improvement: API Design **+5.8±1.30**, Data Communication **+6.6±0.89**, File Systems **+3.2±1.48**.
- In **QoT vs CoT**, **llama3.3_70b** is also positive across all three domains: API **+2.2±2.28**, Data Communication **+4.8±2.17**, File Systems **+2.2±3.90**.
- Smaller models also benefit but are less stable: **llama3.1_8b** improves over CoT by API **+2.0±1.73**, Communication **+2.4±3.05**, FS **+1.2±2.77**; **llama3.2_3b** achieves API **+3.6±2.51**, Communication **+1.4±1.67**, FS **+1.4±5.86**.
- In **QoT vs NoQoT**, the results show capacity dependence and task dependence: for example, **llama3.1_70b** gets API **+3.4±1.34**, Communication **+5.4±1.67**, but File Systems **-2.8±1.10**; **llama3.3_70b** also shows **-3.0±3.46** in FS, which the authors interpret as possible "overthinking/over-engineering."
- The percentage summary shown in the figure indicates that **llama3.2_3b** reaches a total improvement of **101.49%** under QoT vs NoQoT, while **llama3.1_70b** is **23.08%**, **llama3.1_8b** is **23.81%**, and **llama3.3_70b** is **2.80%**.
- The paper's central breakthrough claim is that QoT can significantly improve software design quality through "stepwise planning + self-check Q&A + cumulative memory" **without changing model parameters**, and in some scenarios allows **smaller models to approach the one-shot generation quality of larger models**.

## Link
- [http://arxiv.org/abs/2603.11082v1](http://arxiv.org/abs/2603.11082v1)
