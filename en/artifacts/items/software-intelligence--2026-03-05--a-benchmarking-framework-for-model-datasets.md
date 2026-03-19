---
source: arxiv
url: http://arxiv.org/abs/2603.05250v1
published_at: '2026-03-05T15:04:35'
authors:
- Philipp-Lorenz Glaser
- "Lola Burgue\xF1o"
- Dominik Bork
topics:
- benchmarking
- model-driven-engineering
- dataset-quality
- software-models
- llm-evaluation
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# A Benchmarking Framework for Model Datasets

## Summary
This paper proposes a benchmarking framework and platform for “model datasets” in model-driven engineering (MDE), aimed at evaluating the datasets themselves rather than only downstream models. Its goal is to make the quality, representativeness, and task suitability of software model datasets measurable, comparable, and reproducible.

## Problem
- Existing MDE and LLM research increasingly relies on software model datasets such as UML, Ecore, and ArchiMate, but these datasets are typically **collected ad hoc** and lack systematic quality evaluation for specific tasks.
- This leads to **incomparable research results, weak reproducibility, and biases that are hard to detect**; for example, duplicate samples, fake/placeholder models, heterogeneous formats, poor naming quality, and imbalanced structural distributions can all affect training and evaluation.
- This problem matters because AI/LLM methods are highly sensitive to data quality; if the datasets themselves are opaque or unrepresentative, downstream conclusions and automation capabilities may be misled.

## Approach
- The paper proposes a framework for **benchmarking the dataset itself**: instead of evaluating only algorithms, it systematically measures the **quality, representativeness, and suitability** of model datasets.
- It designs a unified **Benchmark Platform for MDE** that can ingest models in languages such as UML, ArchiMate, and Ecore, along with their different formats.
- The platform first parses input models into a **standardized intermediate representation** (treating models as typed graphs constrained by a metamodel), and then uses a dedicated metrics engine to extract **descriptive statistics and structural statistics**.
- It outputs **benchmark reports** to support cross-dataset comparison and help researchers determine whether a dataset is suitable for tasks such as classification, completion, repair, and refactoring.
- The paper also reviews the characteristics, lifecycle, and representative data sources of model datasets, providing a foundation for forming a core metric set and a prototype evaluation workflow.

## Results
- The paper’s main contribution is a **framework and platform proposal**, and it states that the platform will be demonstrated on **3 representative datasets**; however, the provided excerpt **does not include specific experimental metrics or performance numbers**.
- The paper lists the sizes of several existing datasets, showing that the problem has a practical basis: for example, **ModelSet 10,586** models, **EA ModelSet 977**, **Golden UML 45**, **SAP-SAM Signavio 1,021,471**, **Lindholmen about 93,000**, **AtlanMod Zoo about 300**, **OntoUML/UFO 127**, and **Labeled Ecore 555**.
- Compared with prior work, the authors claim the novelty is that existing benchmarks are mostly for **tools, tasks, or model transformations**, while **no prior work specifically benchmarks datasets themselves in MDE**.
- The platform claims to support unified analysis across **multiple modeling languages and multiple serialization formats**, and to improve **comparability, transparency, and reproducibility**; however, the excerpt does not provide quantitative improvement percentages or baseline comparison results versus existing methods.

## Link
- [http://arxiv.org/abs/2603.05250v1](http://arxiv.org/abs/2603.05250v1)
