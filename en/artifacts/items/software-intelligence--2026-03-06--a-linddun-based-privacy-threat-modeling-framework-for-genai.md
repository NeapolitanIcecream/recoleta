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
- ai-agents
- multi-agent-systems
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# A LINDDUN-based Privacy Threat Modeling Framework for GenAI

## Summary
This paper proposes a **LINDDUN**-based privacy threat modeling framework for generative AI (**GenAI**), aiming to enable software engineers without deep GenAI security experience to systematically identify privacy risks. Its core contribution is integrating fragmented GenAI privacy research and case analyses into a reusable engineering knowledge base and methodology.

## Problem
- Existing general-purpose security/privacy threat modeling methods are not specific enough for GenAI scenarios and struggle to cover emerging privacy risks such as output leakage, agent invocation, and propagation through RAG/multi-agent systems.
- When organizations integrate GenAI into enterprise systems, they need to meet risk-oriented privacy governance and compliance requirements, but lack a specialized framework that can be directly used for system architecture analysis.
- This matters because cited studies indicate that models such as GPT-4 and ChatGPT leak private information with probabilities of **39%** and **57%**, respectively, in certain situations, suggesting that real-world system integration can amplify privacy exposure risks.

## Approach
- The framework uses **LINDDUN** as its foundation rather than rebuilding from scratch, because it is mature, extensible, and already tool-supported, making it suitable for domain-specific enhancement for GenAI privacy threats.
- It adopts a two-track construction method: a **top-down** systematic review of GenAI privacy threats in the literature, and a **bottom-up** data flow diagram (**DFD**) and privacy threat analysis of a representative **HR chatbot**.
- On the literature side, the authors retrieved **65** papers, and the contribution description states that **58** frontier papers were systematically included to extract GenAI usage paradigms, attacker models, and threat characteristics, which were then mapped into the LINDDUN knowledge base.
- The framework identifies **4** categories of GenAI system paradigms and **6** Common Attacker Models (**CAMs**), covering data flow scenarios such as user-system interaction, cross-boundary flows, agent interaction, and residual leakage inside the system.
- In the end, it extends **3** of LINDDUN’s **7** privacy threat categories and adds **100** new GenAI-related threat examples; it is then validated on an **AI Agent / multi-agent assistant** case and reviewed by academic and industry experts.

## Results
- The paper’s main “breakthrough result” is the proposal of an operational **GenAI-specific privacy threat modeling framework**, rather than a model or algorithm, so the results are expressed primarily through knowledge base expansion and case validation rather than standard ML performance metrics.
- The framework is built from a systematic synthesis of **58** frontier papers (with the methods section mentioning an initial identification of **65** papers), combined with one **HR chatbot** case and one additional **multi-agent GenAI assistant** validation case to construct and test coverage.
- Compared with the original LINDDUN, the authors claim that the framework affects/extends **3** of the **7** privacy threat categories and adds **100** GenAI examples to the knowledge base; this is the clearest quantified contribution in the paper.
- The literature statistics report the occurrence shares of the 6 CAMs: **CAM2 45%**, **CAM6 24%**, **CAM1 13%**, **CAM5 13%**, **CAM4 4%**, **CAM3 3%**, indicating that system-to-user leakage and residual leakage within the system are the most common risk patterns in the literature.
- The paper also cites external baseline observations to illustrate severity: in the cited study, **GPT-4 39%** and **ChatGPT 57%** of scenarios lead to private information leakage; this is not an experimental result of this paper, but it forms the practical motivation for the framework.
- The provided excerpt **does not** give finer-grained quantitative comparative experiments (such as direct baseline comparisons with other threat modeling frameworks on recall, coverage, or time cost). The strongest empirical claim is that the framework supported a “more comprehensive privacy analysis” on an AI agent system and was validated by **3** academic threat-modeling experts and **2** industry privacy experts.

## Link
- [http://arxiv.org/abs/2603.06051v1](http://arxiv.org/abs/2603.06051v1)
