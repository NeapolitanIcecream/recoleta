---
source: hn
url: https://schema.org/docs/full.html
published_at: '2026-03-03T23:43:32'
authors:
- vinhnx
topics:
- schema-org
- ontology
- knowledge-graph
- structured-data
- semantic-web
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Full Schema Hierarchy

## Summary
This text is not a robotics or machine learning research paper, but rather Schema.org's "full schema hierarchy" page, which describes the hierarchical structure of types and data types. Its main value lies in providing a unified semantic organization for web structured data, rather than proposing a new algorithm that can be experimentally validated.

## Problem
- The problem it addresses is: how to use a unified, extensible type hierarchy to describe real-world entities, properties, and their textual/data values.
- This matters because search, knowledge graphs, web annotation, and cross-system data exchange require shared semantics; otherwise, different sites are difficult to make interoperable.
- The provided excerpt does not focus on the user's topics such as robotics, VLA, world models, or general robot policies.

## Approach
- The core mechanism is to define **two hierarchies**: one for the "things being described (types/classes)," and one for the "values of text or data types (data types)."
- Each type can have one or more parent types, forming a hierarchical ontology; for ease of presentation, the page shows only one branch in the tree.
- By listing many specific types (such as `Movie`, `Organization`, `LocalBusiness`, `Taxon`, etc.), it standardizes a general semantic schema for reuse by websites and applications.
- In essence, this is not about "training a model," but about "building a shared vocabulary and inheritance relationships" so that machines can more easily understand structured metadata.

## Results
- The text does not provide any experimental setup, dataset, evaluation metric, or quantitative comparison with baselines, so there are **no paper-style quantitative results to report**.
- The strongest concrete claim is that Schema.org is defined as **two hierarchical structures**, covering thing types and data types respectively.
- Another concrete claim is that the main hierarchy contains many types, and types are allowed to have **multiple parent types**, although each type appears in only one branch of the tree in the display.
- The excerpt provides many example type names, but **no numerical statistics** (such as total number of types, coverage, percentage performance improvement, etc.).

## Link
- [https://schema.org/docs/full.html](https://schema.org/docs/full.html)
