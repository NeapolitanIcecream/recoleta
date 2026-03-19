---
source: arxiv
url: http://arxiv.org/abs/2603.06308v1
published_at: '2026-03-06T14:12:32'
authors:
- Philipp Zech
- Yanis Mair
- Michael Vierhauser
- Pablo Oliveira Antonino
- Frank Schnicke
- Tony Clark
topics:
- digital-twin
- feature-model
- systematic-literature-review
- model-driven-engineering
- design-science-research
relevance_score: 0.16
run_id: materialize-outputs
language_code: en
---

# A Generalized Feature Model for Digital Twins

## Summary
This paper proposes a generalized feature model (GFM) for digital twins, aiming to unify the description of mandatory and optional features for digital models, digital shadows, and digital twins. Its value lies in providing a clearer structured basis for the design, development, and verification of digital twins, but the paper excerpt mainly presents the method and conceptual framework, with limited quantitative results.

## Problem
- The paper addresses the problem that the current digital twin field lacks a **cross-domain, systematic** generalized feature model, making it impossible to clearly distinguish which capabilities are required and which are optional.
- This is important because digital twins have expanded into multiple scenarios such as manufacturing, vehicles, emergency response, and healthcare; without a unified feature framework, design decisions, capability grading, development roadmaps, and testing/validation all lack a solid basis.
- The authors also point out that existing research does not clearly define the boundaries between digital models (DM), digital shadows (DS), and digital twins (DT), affecting terminological consistency and maturity assessment.

## Approach
- The core method is straightforward: the authors first conduct a **systematic literature mapping/literature review**, extract common features from existing digital twin research, and then organize them into a generalized feature model.
- The model divides digital systems into **Digital Model, Digital Shadow, Digital Twin**, and distinguishes between **mandatory** and **optional** features, forming a structured classification.
- The model covers a capability chain from low to high, including monitoring, state representation, visualization, goals, context detection, decision support, behavior, simulation, adaptation, and control.
- The authors align these concepts with **Wagg's digital twin maturity model (Level 1–5)** to explain how different features support the progressive capability development from monitoring to autonomous control.
- Methodologically, the work adopts **Design Science Research (DSR)** and claims that the feature model can support model-driven engineering (MDE), helping derive development roadmaps and test cases.

## Results
- The paper's main contribution is the proposal of a **generalized feature model (GFM)**, which it states is derived from a systematic literature analysis covering **6 application domains**.
- The paper excerpt does not provide the kind of quantitative metric results common in machine learning papers (such as accuracy, F1, percentage improvement, etc.), so there are **no standard quantitative performance figures to report**.
- The most concrete validation claim given in the text is that the model was applied to **3 use cases/domains** for validity checking, namely **emergency, vehicular, and manufacturing**, to demonstrate applicability and practicality.
- The authors claim that the model can more clearly distinguish among **DM / DS / DT** system types, and map features to **Level 1–5 maturity**, supporting capability evolution from “monitoring/visualization” to “simulation/adaptation/autonomous control.”
- The paper also provides a market-background figure: according to a cited source, the digital twin market is expected to grow from **USD 7 billion in 2022** to **USD 183 billion by 2031**, used to illustrate the practical significance of establishing systematic engineering methods, though this is not an experimental result of the model itself.

## Link
- [http://arxiv.org/abs/2603.06308v1](http://arxiv.org/abs/2603.06308v1)
