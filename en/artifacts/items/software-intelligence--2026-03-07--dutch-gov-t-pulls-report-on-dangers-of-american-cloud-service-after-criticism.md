---
source: hn
url: https://nltimes.nl/2026/03/05/dutch-govt-pulls-report-dangers-american-cloud-service-criticism
published_at: '2026-03-07T23:36:37'
authors:
- vrganj
topics:
- digital-sovereignty
- cloud-security
- government-it
- legal-risk
- aws
- policy-governance
relevance_score: 0.21
run_id: materialize-outputs
language_code: en
---

# Dutch gov't pulls report on dangers of American cloud service after criticism

## Summary
This is a policy and technology governance news item discussing how the Dutch government withdrew a legal report on the risks of Amazon’s “European Sovereign Cloud” after external criticism. The core dispute is: even if data centers and employees are located in Europe, as long as the service belongs to a U.S. parent company, government data may still be affected by U.S. law, sanctions, and black-box technical control.

## Problem
- The problem to be addressed is whether the government can safely use so-called “European sovereign” U.S. cloud services, and whether such services truly meet digital sovereignty requirements.
- This matters because if governments and critical infrastructure depend on U.S. cloud vendors, they may face the risk of **data being accessed by the U.S. government** or **services being interrupted due to sanctions**.
- The article also points out another key issue: the service is delivered as a “black box,” making it difficult for the government to verify at the **source-code level** whether backdoors or security risks exist.

## Approach
- The article is not an academic paper, but a **legal risk study** commissioned by the Dutch Ministry of Justice and Security and conducted by the U.S. law firm Greenberg Traurig to analyze Amazon’s European Sovereign Cloud.
- The core mechanism of the study is simple: rather than testing the system’s technical implementation, it assesses from a **legal and policy perspective** whether the U.S. government could access data or force service suspension through law or informal pressure.
- The lawyers concluded that the U.S. government **could possibly** access data or interrupt services, but they believed this scenario was **unlikely to occur**.
- External experts then criticized it from a broader digital sovereignty and security perspective, arguing that conducting only legal analysis without technical, compliance, and real-world risk assessment would underestimate the actual risks.

## Results
- No rigorous experiments, benchmarks, or dataset results are provided; this is not quantitative research and has **no performance metrics**.
- The most specific quantifiable fact is that the report was deleted **within 3 days** of publication, and republished about **1 week later (February 26)** with an explanatory note.
- The main conclusion of the legal study is that it **is possible** for the U.S. government to obtain data or suspend services through sanctions, but this was assessed as **low probability / unlikely**.
- The critics’ core rebuttal is that even if the data center is in Europe and operated by European employees, as long as the customer is dealing with a **U.S. parent company**, the digital sovereignty risk has not fundamentally disappeared.
- The article also presents a clear technical claim: to truly verify the security of government data, it should be possible to inspect for backdoors at the **source-code level**, but the current service is considered a “black box.”

## Link
- [https://nltimes.nl/2026/03/05/dutch-govt-pulls-report-dangers-american-cloud-service-criticism](https://nltimes.nl/2026/03/05/dutch-govt-pulls-report-dangers-american-cloud-service-criticism)
