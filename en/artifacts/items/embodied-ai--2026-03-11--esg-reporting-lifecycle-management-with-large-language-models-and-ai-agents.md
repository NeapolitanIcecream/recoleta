---
source: arxiv
url: http://arxiv.org/abs/2603.10646v1
published_at: '2026-03-11T11:05:58'
authors:
- Thong Hoang
- Mykhailo Klymenko
- Xiwei Xu
- Shidong Pan
- Yi Ding
- Xushuo Tang
- Zhengyi Yang
- Jieke Shi
- David Lo
topics:
- esg-reporting
- llm-agents
- multi-agent-systems
- retrieval-augmented-generation
- compliance-checking
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# ESG Reporting Lifecycle Management with Large Language Models and AI Agents

## Summary
This paper proposes an LLM/AI-agent framework for the full lifecycle of ESG reporting, transforming the originally static, manually driven ESG disclosure process into a system that can be automated, interpreted, and continuously iterated. The paper also presents three implementation architectures—single-model, single-agent, and multi-agent—and evaluates them through a case study using a report compliance-checking prototype.

## Problem
- ESG report data sources are highly heterogeneous, commonly appearing in the form of tables, narratives, scanned documents, charts, and more, making automatic extraction and unified processing difficult.
- The same ESG metric may have different definitions and disclosure requirements across standards such as GRI, SASB, and TCFD, making cross-standard alignment and compliance validation complex.
- Existing ESG lifecycle frameworks are often designed for specific domains and lack automation and continuous feedback mechanisms, making them poorly suited to supporting frequently updated regulatory requirements and continuous improvement.

## Approach
- Proposes a **five-stage** agentic ESG lifecycle: identification, measurement, reporting, engagement, improvement, creating a closed-loop feedback process for ESG workflows.
- Designs specialized agents for each stage: ESIA is responsible for standard/metric identification, EDIA for data extraction and normalization, ECA for report generation and visualization, ESEA for stakeholder communication, and EPIA for risk assessment and continuous improvement.
- Uses LLMs as the core reasoning component, combined with mechanisms such as role prompting, multi-step prompting, and comparative prompting to break complex tasks into more executable subtasks.
- Defines four key task categories: report validation and compliance checking, multi-report comparison, automatic report generation, and ESG knowledge-base maintenance; and proposes quality attributes including accuracy, interpretability, faithfulness, modularity, and fault tolerance.
- Presents three system architectures: single-model (one LLM handles all tasks), single-agent (LLM + RAG + external tools), and multi-agent (one specialized agent per task, with agents exchanging results).

## Results
- The paper completes a manual structured analysis of **13 ESG reports** and maps disclosure content to the three standards **GRI, SASB, and TCFD**, in order to identify two core challenges: multi-standard alignment and heterogeneous formats.
- The case study implements **3 prototype architectures** (single-model, single-agent, multi-agent), focusing on the task of **report validation and compliance checking**, with **manual verification** used as the baseline.
- The paper explicitly states that the comparison dimensions include **accuracy, computational cost, energy consumption**.
- However, in the provided excerpt, **no specific quantitative results are given for these three architectures**, so it is not possible to report numerical comparisons for accuracy, cost, or energy consumption.
- The strongest empirical claim is that the authors not only propose a conceptual framework, but also implement runnable prototypes and release the **source code and data** to support reproducibility.

## Link
- [http://arxiv.org/abs/2603.10646v1](http://arxiv.org/abs/2603.10646v1)
