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
- llm-audit
- api-reliability
- model-verification
- safety-evaluation
- shadow-api
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# Real Money, Fake Models: Deceptive Model Claims in Shadow APIs

## Summary
This paper systematically audits whether third-party "shadow APIs" truly provide capabilities consistent with official large-model APIs. The conclusion is: these services are widely used in research, but they are often inconsistent with official APIs in performance, safety behavior, and model identity, and they present clear risks of misleading users.

## Problem
- The paper aims to answer whether shadow APIs can truly serve as equivalent substitutes for official LLM APIs, and whether this substitution is safe and trustworthy for research reproducibility, application reliability, and user interests.
- This matters because official APIs face pricing, payment, and regional restrictions, leading many researchers and developers to turn to shadow APIs; if what these services actually return is not the model they claim, experimental conclusions and downstream systems may both be distorted.
- The authors also investigate how widespread the shadow API market really is, and whether verification methods can uncover evidence of model swapping or false claims.

## Approach
- The authors first conduct a market and literature survey: they identify 17 shadow APIs and trace 187 academic papers that use them, compiling statistics on citations, GitHub stars, geographic distribution, and compliance transparency.
- They then select 3 representative shadow APIs and run multidimensional comparative tests against official APIs, covering 3 model families and 8 models, including high-risk tasks such as scientific reasoning, medicine, and law.
- For utility evaluation, they use benchmarks such as AIME 2025, GPQA, MedQA, and LegalBench to compare the accuracy and variance of official and shadow APIs.
- For safety evaluation, they use JailbreakBench and AdvBench, combined with attacks such as GCG, Base64, Combination, and FlipAttack, to compare differences in harmfulness scores between shadow APIs and official APIs.
- Finally, they use model fingerprinting and metadata auditing (such as LLMmap and output metadata) to verify whether the returned model is באמת the official model it claims to be, seeking direct evidence of model substitution or identity anomalies.

## Results
- Survey results: a total of **17** shadow APIs were identified, appearing in **187** papers, of which **116 (62.03%)** were published in peer-reviewed conferences/journals; the most popular service is associated with papers totaling **5,966** citations and related repositories totaling **58,639** GitHub stars.
- Compliance and transparency: **15/17** services are operated by individuals with opaque identities; only **1** provider has verifiable corporate registration, and **2** services have already ceased operation.
- On scientific tasks, shadow APIs often diverge from official APIs: shadow API E has an average gap of only **2.64** percentage points, but A and H show average accuracy gaps of **9.81** and **6.46** percentage points respectively; on AIME 2025, shadow API A drops by **40.00** percentage points relative to the official API for **Gemini-2.5-pro**, and by **38.89** percentage points for **DeepSeek-Reasoner**.
- The gap is even larger in high-risk domains: on MedQA, the official accuracy of **Gemini-2.5-flash** is **83.82%**, while shadow APIs average only **36.95%**, a drop of **46.51–47.21** percentage points; on LegalBench, all shadow APIs score **40.10–42.73** percentage points lower than official APIs. Overall, the average drops for A/E/H on sensitive tasks are **16.96/15.71/14.75** percentage points, respectively.
- Safety behavior is unpredictable: for example, under the Base64 attack, the harmfulness score of shadow API A for **GPT-5-mini** is **0.04**, which is **2x** the official **0.02**; for **Gemini-2.5-flash**, the official score under FlipAttack is **0.90**, while all shadow APIs are around **0.67–0.68**, underestimating risk by about **0.23**.
- Model identity verification reveals clear anomalies: among **24** tested endpoints, **45.83%** fail fingerprint verification, and another **12.50%** show significant cosine-distance deviations; Table 2 also shows that some endpoints replace the claimed model with other models, such as matching GPT-5 to **glm-4-9b-chat** and DeepSeek-Chat to **gemma-2-9b-it**.

## Link
- [http://arxiv.org/abs/2603.01919v2](http://arxiv.org/abs/2603.01919v2)
