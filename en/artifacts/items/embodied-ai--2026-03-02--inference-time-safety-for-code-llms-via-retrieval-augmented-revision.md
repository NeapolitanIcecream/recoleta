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
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# Inference-Time Safety For Code LLMs Via Retrieval-Augmented Revision

## Summary
This paper proposes SOSecure: an **inference-time safety layer** for code LLMs that first retrieves Stack Overflow security discussions similar to the generated code, and then has the model revise the code accordingly. Its significance is that it can leverage continuously updated community security knowledge without retraining, improving the trustworthiness and security of code generation.

## Problem
- Although code LLMs can generate runnable code, they often reproduce outdated or dangerous implementation patterns, allowing security vulnerabilities to enter real software development workflows.
- Relying only on training-time data or retraining makes it difficult to adapt promptly to new vulnerabilities, API changes, and security standard updates, so deployed models may continue to output unsafe code.
- Existing prompting methods or approaches that provide only CWE labels lack interpretable and actionable security reasoning, making it hard to reliably fix latent vulnerabilities.

## Approach
- The core method is simple: **generate code first, then perform a “security review + rewrite”**; during review, the model does not rely only on its own reasoning, but first retrieves security discussions from Stack Overflow about similar code patterns.
- The authors build a security-oriented Stack Overflow knowledge base, filtering answers and comments that explicitly mention vulnerabilities, risky usage, deprecated interfaces, and similar issues, with light quality filtering applied (at least one upvote).
- The retrieval stage uses **BM25** rather than dense vector retrieval, because code security often depends on specific APIs, parameters, or flags (such as `shell=True`, `pickle.loads`, `debug=True`), where lexical matching is more reliable.
- The system inserts the retrieved discussions into the revision prompt as **advisory context**, allowing the LLM to decide whether changes are needed; this community content is not directly copied into the code, and the model may also leave the code unchanged.
- This mechanism is a model-agnostic inference-time intervention layer that requires no fine-tuning or retraining, emphasizing interpretability, adaptability to new security knowledge, and real-time interception of unsafe outputs before deployment.

## Results
- On **SALLM**, Fix Rate increases from **49.1% (Prompt-only)** to **71.7% (SOSecure)**, higher than **GPT-4+CWE 58.5%**, for a gain of **+22.6 percentage points**; **Intro Rate = 0.0%**.
- On **LLMSecEval**, Fix Rate increases from **56.5%** to **91.3%**, higher than **GPT-4+CWE 69.6%**, for a gain of **+34.8 percentage points**; **Intro Rate = 0.0%**.
- On real user conversation data **LMSys**, Fix Rate increases from **37.5%** to **96.7%**, higher than **GPT-4+CWE 45.8%**, for a gain of **+59.2 percentage points**; **Intro Rate = 0.0%**.
- In the LMSys ablation study, **Revision-only 41.2%**, **GPT-4+CWE 45.8%**, and **SOSecure 96.7%**, showing that the main gains come from **community discussion retrieval**, rather than simply asking the model to revise its own output.
- On the **C language** subset of LLMSecEval, SOSecure achieves a Fix Rate of **73.3%**, outperforming **Prompt-only 53.3%** and **GPT-4+CWE 60.0%**, with **Intro Rate = 0.0%**, indicating that the method is not limited to Python.
- The paper’s central breakthrough claim is: **without retraining, inference-time retrieval plus revision alone can significantly improve the code security fix rate while introducing no new vulnerabilities under static analysis.**

## Link
- [http://arxiv.org/abs/2603.01494v1](http://arxiv.org/abs/2603.01494v1)
