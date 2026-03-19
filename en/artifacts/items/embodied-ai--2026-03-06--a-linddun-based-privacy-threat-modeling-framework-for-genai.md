---
source: arxiv
url: http://arxiv.org/abs/2603.06051v1
published_at: '2026-03-06T09:04:32'
authors:
- Qianying Liao
- Jonah Bellemans
- Laurens Sion
- Xue Jiang
- Dmitrii Usynin
- Xuebing Zhou
- Dimitri Van Landuyt
- Lieven Desmet
- Wouter Joosen
topics:
- privacy-threat-modeling
- generative-ai
- linddun
- security-privacy
- ai-agents
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# A LINDDUN-based Privacy Threat Modeling Framework for GenAI

## Summary
This paper proposes a privacy threat modeling framework for generative AI applications, extending LINDDUN to cover privacy risks in GenAI scenarios that are often overlooked. It aims to organize scattered research findings into a practical knowledge base and process that software engineers can use directly.

## Problem
- Existing security/privacy threat modeling frameworks are often too general to cover the unique privacy risks introduced by data flows, prompts, memory, agents, and external tools in GenAI systems.
- Organizations are rapidly deploying GenAI, but engineers often lack systematic methods for identifying privacy threats; this creates risks around compliance, user trust, and sensitive information leakage.
- The paper explicitly focuses on two questions: what new privacy threats GenAI systems introduce, and how to turn that knowledge into a modeling framework usable by non-experts.

## Approach
- It uses **LINDDUN** as the foundation rather than starting from scratch; this allows reuse of existing methodology, threat trees, and tool support, while adding incremental extensions for GenAI.
- It adopts a “two-track” approach to building knowledge: a **top-down** systematic review of GenAI privacy literature. The paper says it identified 65 papers, and in the contribution statement summarizes this as a systematic analysis of **58 SOTA papers**.
- It also adopts a **bottom-up** case study: building a data flow diagram for a representative HR Chatbot, performing threat identification with traditional LINDDUN Pro by 3 researchers, and then having it reviewed by 2 industry experts.
- It maps findings from the literature and case study onto LINDDUN, extracting **4 GenAI system paradigms** and **6 common attacker models (CAMs)**, and submits the new threats to expert consensus review.
- The final output is a GenAI-specific knowledge base: the paper claims the framework **affects 3 of LINDDUN’s 7 privacy threat categories**, adds **100 new GenAI examples** to the knowledge base, and then validates coverage and practicality on a multi-agent AI Agent system.

## Results
- The paper’s core output is a **domain-specific GenAI privacy threat modeling framework**, not a new model or defense algorithm; its main result is an extension of methodology and knowledge base.
- Quantitative/semi-quantitative results include: a review based on **58 papers** (contribution statement) / **65 papers** (identified in the methods section); identification of **4** GenAI system paradigms and **6** CAMs; extensions affecting **3 of LINDDUN’s 7 categories**; and **100** new GenAI threat examples.
- For the case study and validation: the HR Chatbot threat analysis was conducted by **3** researchers and reviewed by **2** industry practitioners; framework validation involved **3** academic threat modeling experts and **2** industry privacy experts, and was applied to a more complex AI Agent system.
- The paper also cites external studies to emphasize the importance of the problem: GPT-4 and ChatGPT leak private information **39%** and **57%** of the time, respectively, in certain contexts; however, these are not results from this paper itself, but motivation evidence.
- The provided excerpt **does not report performance metrics on standard benchmark datasets** (such as accuracy, recall, F1, percentage improvement in coverage, or quantitative comparison with baseline frameworks); the strongest specific claim is that the framework can support more comprehensive privacy analysis of GenAI applications and has been validated in an AI Agent case.

## Link
- [http://arxiv.org/abs/2603.06051v1](http://arxiv.org/abs/2603.06051v1)
