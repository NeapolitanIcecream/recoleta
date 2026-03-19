---
source: arxiv
url: http://arxiv.org/abs/2603.05250v1
published_at: '2026-03-05T15:04:35'
authors:
- Philipp-Lorenz Glaser
- "Lola Burgue\xF1o"
- Dominik Bork
topics:
- benchmarking-framework
- model-datasets
- model-driven-engineering
- dataset-quality
- research-infrastructure
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# A Benchmarking Framework for Model Datasets

## Summary
This paper proposes a benchmarking framework and platform for **software model datasets themselves**, aiming to make datasets in MDE/AI research—which are often assembled ad hoc—measurable, comparable, and reproducible. The core contribution is not a new learning model, but treating model datasets as first-class research objects and systematically evaluating their quality, representativeness, and task suitability.

## Problem
- Model datasets in existing MDE research are typically **collected or constructed ad hoc**, lacking quality assurance for specific tasks.
- **Clones, fake/toy models, format heterogeneity, and missing annotations and metadata** in datasets can affect the training and evaluation of AI/LLM methods, leading to incomparable results, poor reproducibility, and potential bias.
- The community lacks a **unified framework** to analyze datasets themselves across modeling languages and formats, rather than only benchmarking algorithms or tasks.

## Approach
- Proposes a **benchmarking framework for model datasets**: instead of evaluating modeling algorithms, it systematically measures dataset quality, representativeness, and suitability for specific tasks.
- Designs a **Benchmark Platform for MDE** that accepts models such as UML, ArchiMate, and Ecore, parses them into a unified **intermediate representation**, and then extracts descriptive and structural statistics through a metrics engine.
- Methodologically, it treats models as **typed graphs** constrained by metamodels rather than pure text sequences, and therefore considers properties such as lexical features, structural complexity, construct coverage, duplication/near-duplication, and parsability.
- The framework emphasizes **explicit reporting of dataset properties**, supports cross-dataset comparison, generates benchmark reports, and helps researchers determine whether a dataset is suitable for different tasks such as classification, completion, repair, and refactoring.
- The paper also presents a research agenda: surveying benchmarking methods in related fields, formalizing core metrics, implementing a multilingual prototype, and evaluating practicality on existing MDE datasets and published studies.

## Results
- The paper claims the platform can handle **multiple modeling languages**; it explicitly mentions support for **UML, ArchiMate, and Ecore**, and can generate unified reports across languages/formats.
- The paper reviews and compares multiple existing datasets with a wide range of sizes, for example **ModelSet 10,586** models, **EA ModelSet 977**, **Golden UML 45**, **Lindholmen about 93,000**, **SAP-SAM Signavio 1,021,471** models, **AtlanMod Zoo about 300**, **OntoUML/UFO 127**, and **Labeled Ecore 555**.
- The paper explicitly states that the platform will be demonstrated on **3 representative datasets**, but the provided excerpt **does not provide specific experimental metrics, performance numbers, or quantitative comparisons with existing methods**.
- The strongest concrete claim is that the framework can improve **dataset quality transparency, cross-study comparability, and reproducibility**, and fill the gap in existing MDE benchmarking, which mainly focuses on algorithms/tasks rather than on the **dataset itself**.

## Link
- [http://arxiv.org/abs/2603.05250v1](http://arxiv.org/abs/2603.05250v1)
