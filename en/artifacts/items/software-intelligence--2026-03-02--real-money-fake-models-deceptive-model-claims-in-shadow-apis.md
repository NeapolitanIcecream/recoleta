---
source: arxiv
url: http://arxiv.org/abs/2603.01919v2
published_at: '2026-03-02T14:33:05'
authors:
- Yage Zhang
- Yukun Jiang
- Zeyuan Chen
- Michael Backes
- Xinyue Shen
- Yang Zhang
topics:
- llm-api-audit
- shadow-apis
- model-verification
- benchmarking
- safety-evaluation
relevance_score: 0.63
run_id: materialize-outputs
language_code: en
---

# Real Money, Fake Models: Deceptive Model Claims in Shadow APIs

## Summary
This paper systematically audits whether unofficial "shadow APIs" truly provide services consistent with official large-model APIs. The conclusion is that they often do not live up to their claims and can undermine research reproducibility and application reliability. The authors provide the first systematic evidence across four dimensions: usage scale, performance, safety, and model fingerprinting.

## Problem
- The paper addresses the question of whether third-party "shadow APIs," which claim to provide low-cost, cross-region access to official frontier LLMs, actually return model behavior consistent with the official APIs.
- This matters because these services have already been used in **187 papers**; if they are actually calling different models or behave unstably, they can directly harm scientific reproducibility, downstream system reliability, and user interests.
- Shadow APIs are also a black-box supply chain and may perform undisclosed operations in request forwarding, model substitution, retries, and safety policies, affecting the reputation and compliance of official model providers.

## Approach
- The authors first identified **17 shadow APIs** by tracing paper code repositories and GitHub endpoints, and quantified their spread in academic papers and the open-source community.
- They then selected **3 representative shadow APIs** and conducted a multidimensional audit of **8 models** across three families (OpenAI, Google, and DeepSeek), comparing differences between official APIs and shadow APIs on scientific, medical, legal, and safety tasks.
- Utility evaluation covered **AIME 2025, GPQA, MedQA, LegalBench**; safety evaluation used **JailbreakBench** and **AdvBench**, combined with multiple jailbreak attacks to observe changes in harmfulness scores.
- To verify whether they were "really the same model," the authors further used **LLM fingerprinting (LLMmap)** and output metadata analysis to check whether the model identities claimed by shadow APIs matched the official models.

## Results
- The authors identified **17 shadow APIs**, which appeared in **187 papers**, of which **116 (62.03%)** were published in peer-reviewed conferences/journals; the most popular related service accumulated **5,966 citations** and **58,639 GitHub stars**.
- On scientific tasks, the average accuracy gap between shadow APIs and official APIs was notably large: the average gaps for shadow API A/H were **9.81** and **6.46** percentage points, respectively; on **AIME 2025**, shadow API A dropped by **40.00** and **38.89** percentage points relative to the official API for **Gemini-2.5-pro** and **DeepSeek-Reasoner**, respectively.
- Degradation was even more severe in high-risk domains: on **MedQA**, **Gemini-2.5-flash** fell from **83.82%** on the official API to an average of about **36.95%** on shadow APIs, a performance loss of **46.51–47.21** percentage points; on **LegalBench**, all shadow APIs were **40.10–42.73** percentage points lower than the official endpoints.
- Safety behavior was highly unstable: for example, under the Base64 attack on **GPT-5-mini**, the harmfulness score of shadow API A was **0.04**, which is **2 times** the official API's **0.02**; for **Gemini-2.5-flash** under FlipAttack, the official API's harmfulness score reached **0.90**, while shadow APIs were about **0.67–0.68**, a difference of about **0.23**, indicating that their safety conclusions are not interchangeable.
- Fingerprint verification provided direct evidence: among **24 evaluated endpoints**, **45.83%** failed fingerprint identity verification, and another **12.50%** showed significant cosine-distance shifts, indicating model substitution or behavioral masquerading.
- Compliance and transparency were also poor: among the **17** services, **15** were operated by individuals lacking transparent identity information, only **1** had verifiable corporate registration, and **2** services had already ceased operation.

## Link
- [http://arxiv.org/abs/2603.01919v2](http://arxiv.org/abs/2603.01919v2)
