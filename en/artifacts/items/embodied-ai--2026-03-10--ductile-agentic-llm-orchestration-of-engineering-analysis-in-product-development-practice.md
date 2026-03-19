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
- workflow-orchestration
- aerospace-analysis
- human-in-the-loop
relevance_score: 0.09
run_id: materialize-outputs
language_code: en
---

# DUCTILE: Agentic LLM Orchestration of Engineering Analysis in Product Development Practice

## Summary
This paper introduces DUCTILE, an LLM-agent orchestration approach for engineering analysis automation in product development that separates “adaptive process coordination” from “deterministic execution by verified tools.” Its goal is to keep engineering analysis workflows usable, auditable, and engineer-supervised even when common changes occur in input formats, units, naming, and methods.

## Problem
- Traditional engineering analysis automation relies on predefined rigid interfaces, scripts, and workflows; when tools, data formats, units, naming, or processes change even slightly, the automation tends to fail.
- In safety-critical industries such as aerospace, this fragility consumes engineers’ time with data cleaning, tool handoffs, and script patching rather than critical engineering judgment.
- Simply adding more rules makes the system more complex and harder to maintain; relying only on expert manual adaptation is slow, dependent on individual experience, and difficult to scale.

## Approach
- The core mechanism of DUCTILE is to let an LLM agent “read documents, inspect inputs, and decide which processing path to take next,” while the actual engineering computations are still executed by verified deterministic tools.
- Based on design practices recorded in context, tool documentation, and input data, the agent adaptively generates/calls processing code and toolchains rather than hard-coding all possible situations into a fixed workflow in advance.
- The system emphasizes human oversight: engineers review plans, supervise execution, and make final judgments on outputs, satisfying requirements for traceability, auditability, and accountability.
- The paper also presents a set of engineering-grade requirements and evaluation principles, including inspectability, reproducibility, deterministic execution boundary, traceability, human oversight, robustness to variability, etc.

## Results
- In an industrial structural analysis task at an aerospace manufacturer, DUCTILE handled **4 categories** of input deviations that would cause traditional scripted pipelines to fail: **format, units, naming conventions, and methodological differences**.
- The paper states that the method was evaluated across **10 independent runs**, and **2 engineers** with different supervision styles participated in deployment/use.
- Results were assessed against expert-defined acceptance criteria; the authors claim the system can produce **correct and methodologically compliant** results across repeated independent runs.
- The text does not provide finer-grained quantitative metrics such as accuracy, pass rate, percentage time savings, or numerical gaps versus specific baselines, so more detailed benchmark figures cannot be reported.
- The paper’s strongest concrete claim is that, compared with traditional scripted automation that breaks under routine input changes, DUCTILE can absorb these changes without modifying verified engineering tools, while maintaining transparency and auditability.

## Link
- [http://arxiv.org/abs/2603.10249v1](http://arxiv.org/abs/2603.10249v1)
