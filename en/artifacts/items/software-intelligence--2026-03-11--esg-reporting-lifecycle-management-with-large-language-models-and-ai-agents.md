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
- llm-agents
- multi-agent-systems
- esg-reporting
- rag
- compliance-automation
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# ESG Reporting Lifecycle Management with Large Language Models and AI Agents

## Summary
This paper proposes an LLM- and AI-agent-based framework for the full lifecycle of ESG reporting, transforming what was originally a static, labor-intensive compliance reporting process into a system that can be automated and iteratively improved through feedback. The paper also presents three implementation approaches—single-model, single-agent, and multi-agent—and validates them with a prototype focused on the report validation task.

## Problem
- ESG reporting data sources are **unstructured and heterogeneous**, such as tables, narratives, scanned documents, and charts, making automated extraction and comparison difficult.
- Different standards (such as GRI, SASB, and TCFD) have **different interpretations and requirements for the same metric**, making multi-standard alignment complex and labor-intensive.
- Existing ESG lifecycle frameworks **lack automation, cross-domain adaptability, and continuous feedback mechanisms**, making them poorly suited to frequent regulatory changes and ongoing improvement needs.

## Approach
- The paper proposes a **five-stage agentic ESG lifecycle**: identification, measurement, reporting, engagement, improvement, covering the full closed-loop process from standard identification to continuous optimization.
- Specialized agents are designed for each stage: ESIA interprets standards and identifies metrics, EDIA extracts/normalizes/validates data, ECA generates and aligns reports, ESEA handles stakeholder feedback, and EPIA performs risk assessment and continuous improvement.
- **LLM prompting strategies** are embedded across the stages, combining role prompting, multi-step prompting, comparison prompting, report-generation prompting, and more. Put simply, this means “different AI assistants each handle one type of ESG task and pass the results to the next assistant.”
- Three system architectures are proposed: **single-model** (one LLM does everything), **single-agent** (one agent + RAG + external tools), and **multi-agent** (multiple specialized agents collaborating); the latter two use RAG to support the knowledge base, interpretability, and faithfulness.
- Four core task types are defined: report validation and compliance checking, multi-report comparison, automatic report generation, and ESG knowledge-base maintenance, along with quality attributes such as accuracy, scalability, fault tolerance, interpretability, and answer faithfulness.

## Results
- The paper includes a manual analysis of **13 ESG reports**, mapping them to the three standards **GRI, SASB, and TCFD** to identify two core challenges: multi-standard alignment and heterogeneous formats.
- The prototype system covers **3 architectures** (single-model, single-agent, multi-agent) and focuses on **1 case task**: ESG report validation and compliance checking.
- The evaluation states that it compares **3 metrics**: accuracy, computational cost, and energy consumption; **manual human validation** is used as the baseline.
- However, in the provided excerpt, **no specific quantitative results are given**, so it is not possible to report relative accuracy gains, cost reductions, or energy-use differences for each architecture versus the baseline.
- The strongest concrete claim is that the framework transforms ESG reporting from a static disclosure process into a **dynamic, accountable, and adaptive** governance system, while improving automation, interpretability, and continuous improvement capabilities through multi-agent task division.

## Link
- [http://arxiv.org/abs/2603.10646v1](http://arxiv.org/abs/2603.10646v1)
