---
source: arxiv
url: http://arxiv.org/abs/2603.10249v1
published_at: '2026-03-10T22:00:47'
authors:
- Alejandro Pradas-Gomez
- Arindam Brahma
- Ola Isaksson
topics:
- llm-agents
- engineering-automation
- tool-orchestration
- human-in-the-loop
- aerospace-analysis
relevance_score: 0.8
run_id: materialize-outputs
language_code: en
---

# DUCTILE: Agentic LLM Orchestration of Engineering Analysis in Product Development Practice

## Summary
This paper presents DUCTILE, an LLM agent orchestration approach for engineering analysis automation that uses adaptive agents to coordinate multi-tool workflows while keeping the actual engineering computations within verified deterministic tools. It targets the common problem of workflow brittleness in product development, and demonstrates robustness to input variation and practical supervised deployment in an aerospace structural analysis case.

## Problem
- Traditional engineering analysis automation depends on predefined interfaces, data formats, and fixed processes. When products evolve, tools are updated, or organizational changes occur, these automations are prone to failure.
- Engineers spend substantial time on “non-engineering judgment” work such as data preparation, format repair, and tool chaining, instead of interpreting analysis results and making design decisions.
- In safety-critical industries, processes must both adapt to real-world variation in formats, units, naming, and methodology, and remain traceable, auditable, and under human responsibility, making purely rule-based scripts or rigid workflows difficult to scale.

## Approach
- The core mechanism of DUCTILE is to **separate “adaptive orchestration” from “deterministic execution”**: the LLM agent reads documents, inspects inputs, decides the processing path, and generates code; verified engineering tools perform the actual computations.
- The agent does not replace domain software, but serves as a unified orchestration layer that connects engineering intent, documented design practices, existing tools, and data, absorbing input differences that would cause traditional scripts to fail.
- The system emphasizes **user supervision**: engineers review plans, supervise execution, validate outputs, and retain final judgment authority to satisfy governance and certification requirements in industries such as aerospace and automotive.
- The paper also proposes a requirements framework for engineering agent applications, including inspectability, reproducibility, deterministic execution boundaries, traceability, data governance, human oversight, robustness to common variation, observability, minimal coupling, repeated-run evaluation, and change control.

## Results
- In an industrial structural analysis task at an aerospace manufacturer, DUCTILE handled **4 categories** of input deviations that would break traditional scripted pipelines: **format, units, naming conventions, and methodological changes**.
- The paper states that evaluation was conducted over **10 independent runs**, and deployment/use involved **2 engineers with different supervision styles**.
- Compared with traditional scripted workflows, the authors claim the method still produces **correct and methodologically compliant** results under the above input variations, validated through **expert-defined acceptance criteria**.
- The abstract and introduction do not provide more detailed numerical metrics (such as accuracy, pass rate, percentage time savings, or quantitative differences versus specific baselines), so a fuller quantitative comparison cannot be reported.
- The paper’s strongest empirical claim is that, in a real industrial aerospace case, an LLM agent can **transparently** orchestrate existing verified tools and maintain acceptable results across **repeated independent runs**, without modifying the certified tools themselves.

## Link
- [http://arxiv.org/abs/2603.10249v1](http://arxiv.org/abs/2603.10249v1)
