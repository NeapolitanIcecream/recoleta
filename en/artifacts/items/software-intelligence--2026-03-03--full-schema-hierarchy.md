---
source: hn
url: https://schema.org/docs/full.html
published_at: '2026-03-03T23:43:32'
authors:
- vinhnx
topics:
- schema-org
- knowledge-graph
- ontology
- structured-data
- metadata
relevance_score: 0.33
run_id: materialize-outputs
language_code: en
---

# Full Schema Hierarchy

## Summary
This is not a research paper, but the full Schema.org schema hierarchy page, which lists the classification system for "thing types" and "data types." Its value lies in providing a unified vocabulary for web pages, knowledge graphs, and structured metadata, but the text does not present any new algorithms or experimental results.

## Problem
- The problem it addresses is: how to use a unified, extensible schema to describe real-world entities, properties, and their hierarchical relationships in order to support structured data annotation.
- This matters because without unified semantics, interoperability among web data, knowledge bases, and applications becomes difficult, search understanding is poor, and the cost of automated processing is high.
- For software and intelligent systems, it provides a reusable semantic skeleton, but this page itself is more like reference documentation than research work.

## Approach
- The core mechanism is simple: Schema.org is defined as two hierarchical structures, one describing "things/types (classes)" and the other describing "textual property values/data types (data types)."
- Each type can have one or more parent types; for readability, the page shows only one branch position in the tree.
- The page constructs the full hierarchy by enumerating many specific types and enumeration values, such as `SoftwareSourceCode`, `WebSite`, `MedicalResearcher`, and `OrderStatus`.
- In essence, it is not a trained model or reasoning algorithm, but a manually designed general ontology/vocabulary hierarchy for annotation and semantic alignment.

## Results
- It provides a concrete artifact in the form of a **full hierarchy view**: covering many Schema.org types and enumeration items, but the excerpt **does not provide total node counts, coverage, or version comparison figures**.
- The text explicitly states that Schema.org is defined as **two hierarchies**: one for textual property values, and one for the things they describe.
- The text also explicitly notes that **types may have multiple parent types**, but on this page **each type is shown in only one branch of the tree**.
- It does not provide any experiments, benchmarks, accuracy, recall, ablation studies, or quantitative comparisons with other ontologies/schema languages.

## Link
- [https://schema.org/docs/full.html](https://schema.org/docs/full.html)
