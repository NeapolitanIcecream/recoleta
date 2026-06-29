---
source: arxiv
url: http://arxiv.org/abs/2604.08491v1
published_at: '2026-04-09T17:30:58'
authors:
- Yifang Wang
- Rui Sheng
- Erzhuo Shao
- Yifan Qian
- Haotian Li
- Nan Cao
- Dashun Wang
topics:
- llm-interfaces
- scientific-discovery
- visual-analytics
- provenance
- human-ai-interaction
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Figures as Interfaces: Toward LLM-Native Artifacts for Scientific Discovery

## Summary
The paper proposes **LLM-native figures**, where a scientific figure carries its own data, code, provenance, and interaction mapping so an LLM can operate on the figure as an analytical object, not just as pixels. It presents **Nexus**, a proof-of-concept system for iterative scientific exploration in the science-of-science domain.

## Problem
- Scientific figures are usually static outputs. They show patterns to people, but they hide the data subset, transformation steps, and code that produced them.
- In current human-AI workflows, multimodal LLMs often have to recover meaning from images or captions, which weakens reproducibility, traceability, and follow-up analysis.
- Scientific exploration is iterative and non-linear, but many LLM research tools still center on linear chat or one-shot generation, which makes it hard to refine, audit, and reuse analysis steps.

## Approach
- The core idea is to store each figure as a structured object \(F_t = \{V_t, C_t, D_t, M_t\}\): visualization output, executable code and analytical actions, underlying data, and metadata/history.
- The system keeps a **bidirectional mapping** between visual marks and analytical operations. A language request can generate a figure, and a direct interaction with the figure, such as brushing points or time ranges, can map back to the exact data rows and produce the next analysis.
- The paper groups linked figures and their history into a **data-driven artifact** that records user input, derived figures, code, data, and coordination rules across steps. This artifact is versioned as a DAG so prior states can be revisited and replayed.
- An LLM runs a plan-action-observation loop over a constrained action space such as filtering, transformation, modeling, and visualization, then executes code and uses the outputs to decide the next step.
- Nexus implements this design for science-of-science analysis, where users mix natural-language instructions with figure manipulation during exploration.

## Results
- The paper claims three main gains: faster iterative discovery, stronger reproducibility, and more transparent reasoning through stored provenance and executable history.
- It presents a case study in the science-of-science domain using Nexus to explore inventor-level innovation data from a large U.S. research university, with interactive follow-up changes such as log-scaling axes and drilling into selected regions.
- It also states that the system was evaluated with a computational test of the **fidelity of the bidirectional mapping** between figures and analytical operations.
- The provided excerpt does **not include quantitative metrics or benchmark numbers** for accuracy, speed, or user outcomes, so no numeric improvement over baselines can be extracted from the text given.
- Concrete technical claims in the excerpt are that figures can be deterministically reconstructed from stored code and data except in non-deterministic analyses, and that linked figures can update automatically through precomputed coordination relations and code templates.

## Link
- [http://arxiv.org/abs/2604.08491v1](http://arxiv.org/abs/2604.08491v1)
