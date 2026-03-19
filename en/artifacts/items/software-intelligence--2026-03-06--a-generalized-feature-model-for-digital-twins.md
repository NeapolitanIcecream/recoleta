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
- digital-twins
- feature-modeling
- systematic-literature-review
- model-driven-engineering
- design-science-research
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# A Generalized Feature Model for Digital Twins

## Summary
This paper proposes a generalized feature model (GFM) for Digital Twins, aiming to provide a unified description of the mandatory and optional features of Digital Models, Digital Shadows, and Digital Twins. Its significance lies in providing a cross-domain, reusable, structured foundation for the design, development, and validation of Digital Twins.

## Problem
- There is already a large body of research on Digital Twins, but there is a lack of a **general and systematic** feature model that clearly distinguishes which capabilities are required and which are optional.
- Digital Twins span multiple domains such as manufacturing, vehicles, and emergency response, but terminology and capability boundaries are not consistent, making design decisions, capability grading, and system comparison difficult.
- This matters because without a unified feature framework, it is hard to carry out model-driven development, maturity assessment, and subsequent validation and test-case derivation.

## Approach
- Based on a **systematic literature mapping/review**, the authors extract key features from the problem space, design space, and solution space in existing Digital Twin literature.
- On this basis, they construct a **generalized feature model (GFM)** that uniformly covers three categories: Digital Model, Digital Shadow, and Digital Twin.
- The model explicitly distinguishes **mandatory features** from **optional features**; the paper notes that monitoring and state representation are core mandatory capabilities, while visualization, intention, context detection, decision support, behavior, simulation, adaptation, control, and others extend across capability levels.
- The authors align these features with **Wagg's Digital Twin maturity model**: from monitoring/visualization to simulation, learning, and autonomous control, forming a progressive capability path.
- The research method follows **Design Science Research (DSR)**, and the applicability of the model is validated through three domain use cases (emergency, vehicular, and manufacturing).

## Results
- The core contribution of the paper is a generalized feature model for Digital Twins derived from **literature synthesis across six application domains**, but the abstract and excerpt **do not provide standard experimental metrics, accuracy, recall, or percentage performance improvements**.
- The paper explicitly claims that the model can provide a unified classification of **Digital Model / Digital Shadow / Digital Twin**, improve semantic clarity, and help distinguish mandatory from optional features.
- The model is connected to a **5-level Digital Twin maturity framework**: from measurement at Level 1, to simulation and decision support at Level 3, and then to autonomous control at Level 5.
- Validity is demonstrated through **3 use cases**: emergency services, vehicular systems, and manufacturing, based on which the authors claim cross-domain applicability and practical usefulness.
- The paper also makes strong engineering claims: the GFM can support model mapping in **Model-Driven Engineering (MDE)** and provide a foundation for **Verification & Validation (V&V) / test-case derivation**, but the excerpt does not provide quantitative comparative experiments.
- The background includes market-motivation data: according to a cited source, the Digital Twin market is expected to grow from **$7 billion in 2022** to **$183 billion by 2031**, illustrating the practical value of this kind of systematic engineering method.

## Link
- [http://arxiv.org/abs/2603.06308v1](http://arxiv.org/abs/2603.06308v1)
