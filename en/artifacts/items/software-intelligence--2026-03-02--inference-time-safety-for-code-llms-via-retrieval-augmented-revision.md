---
source: arxiv
url: http://arxiv.org/abs/2603.01494v1
published_at: '2026-03-02T06:06:34'
authors:
- Manisha Mukherjee
- Vincent J. Hellendoorn
topics:
- code-llm-safety
- retrieval-augmented-generation
- secure-code-generation
- stack-overflow
- inference-time-revision
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Inference-Time Safety For Code LLMs Via Retrieval-Augmented Revision

## Summary
This paper proposes SOSecure: an **inference-time safety layer** for code LLMs that first retrieves relevant Stack Overflow security discussions for already generated code, then guides the model to perform security-oriented revision. Its core value is that it can leverage continuously updated community knowledge without retraining, improving both the security and interpretability of code generation.

## Problem
- Code LLMs often generate code that is **functionally correct but vulnerable**, which can create real security risks, especially in high-stakes software development scenarios.
- Relying only on training data makes it **difficult for models to adapt quickly to new vulnerabilities, deprecated APIs, and evolving security standards**, while retraining is costly and slow to update.
- Simply prompting the model to self-check, or only providing CWE labels, usually **lacks specific, actionable security reasoning context**, limiting remediation effectiveness.

## Approach
- The paper introduces **SOSecure**: a retrieval-augmented revision pipeline that runs after code generation, rather than modifying the model during training or injecting knowledge before generation.
- It builds a security-focused knowledge base from **Stack Overflow**, filtering answers and comments that explicitly mention security risks, vulnerabilities, or unsafe practices, with light quality control applied (at least 1 upvote).
- For model-generated code, it uses **BM25 lexical retrieval** to find community security discussions corresponding to similar code patterns; the authors argue that for security-critical markers such as `shell=True`, `pickle.loads`, and `debug=True`, BM25 is more reliable than dense retrieval.
- The retrieved discussions are inserted into the revision prompt as **advisory context**, requiring the LLM to decide whether modification is needed; this content is not copied directly into the code, and the model is also allowed to leave the code unchanged.
- The mechanism emphasizes three aspects: **interpretability** (revision rationale comes from human community explanations), **robustness** (new knowledge can be incorporated without retraining), and **safety alignment** (real-time intervention before deployment).

## Results
- On **SALLM**, Fix Rate improved from **49.1% (Prompt-only)** to **71.7% (SOSecure)**, also outperforming **GPT-4+CWE at 58.5%**; the gain was **+22.6 percentage points**; **Intro Rate = 0.0%**.
- On **LLMSecEval**, Fix Rate improved from **56.5%** to **91.3%**, exceeding **GPT-4+CWE at 69.6%**; the gain was **+34.8 percentage points**; **Intro Rate = 0.0%**.
- On real conversational data from **LMSys**, Fix Rate improved from **37.5%** to **96.7%**, higher than **GPT-4+CWE at 45.8%**; the gain was **+59.2 percentage points**; **Intro Rate = 0.0%**.
- In the **LMSys ablation study**, **Revision-only = 41.2%**, far below **SOSecure = 96.7%**, indicating that the improvement mainly comes from the **community-retrieved context** rather than merely asking the model to self-revise.
- On the **C-language LLMSecEval** subset, **SOSecure = 73.3% Fix Rate**, outperforming **Prompt-only at 53.3%** and **GPT-4+CWE at 60.0%**; **Intro Rate = 0.0%**, showing some cross-language generalization ability.
- The paper’s main breakthrough claim is that **inference-time, community-knowledge-driven security revision** can significantly improve vulnerability remediation rates across multiple datasets while **introducing no new vulnerabilities visible to static analysis**.

## Link
- [http://arxiv.org/abs/2603.01494v1](http://arxiv.org/abs/2603.01494v1)
