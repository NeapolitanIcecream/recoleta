---
source: hn
url: https://cfrg.github.io/draft-irtf-cfrg-cryptography-specification/draft-irtf-cfrg-cryptography-specification.html
published_at: '2026-03-02T23:44:02'
authors:
- themaxdavitt
topics:
- cryptography-specification
- technical-writing
- secure-implementation
- interoperability
- threat-modeling
relevance_score: 0.19
run_id: materialize-outputs
language_code: en
---

# Guidelines for Writing Cryptography Specifications

## Summary
This is a guidance document for authors of cryptography specifications, with the goal of making specifications clearer, more precise, more consistent, and implementable, thereby improving security and interoperability. It does not propose new cryptographic algorithms; rather, it systematically summarizes how to write high-quality specifications for cryptographic protocols and primitives.

## Problem
- If cryptography specifications contain ambiguity, imprecision, or inconsistent representation, they can directly lead to implementation errors, interoperability failures, and security vulnerabilities.
- Different audiences—implementers, researchers, and protocol designers—have different needs from specifications; if a specification cannot serve these groups simultaneously, software assurance and security review will both suffer.
- If mathematical notation, threat models, security definitions, error handling, and test vectors are described incompletely, this can create divergence between the specification and real-world implementations, affecting deployment security.

## Approach
- It proposes a set of writing principles that emphasize **simplicity, precision, and consistency**, requiring clear language, unified terminology, logical structure, and explicit steps to reduce misunderstanding.
- For cryptography-specific content, it provides conventions for mathematical representation: normative algorithm descriptions must use ASCII; it requires a "Mathematical Operators and Symbols" table, forbids assigning multiple meanings to the same symbol, and recommends using pseudocode, examples, and diagrams to aid explanation.
- It emphasizes that the specification content itself should be reusable and complete: reuse existing primitives and specifications where possible, adopt modular interfaces, and define behavior for all inputs, especially covering deserialization, error handling, and edge cases.
- It requires clearly stated security goals, formal security definitions, and threat models, and calls for explaining residual risks, side-channel considerations, and trade-offs between security and performance.
- For implementers, it sets verifiability requirements: provide test vectors covering logical branches, reproducible experimental steps, and persistent machine-readable test vectors (such as JSON).

## Results
- The document’s main output is **guidance for specification writing and mandatory/recommended checklist items**, rather than experimental algorithmic results; the excerpt **does not provide quantitative benchmarks, datasets, or performance metrics**.
- It explicitly claims that following these guidelines can bring less ambiguity, more consistent and correct implementations, easier security analysis, and stronger interoperability, but it does not provide quantified improvement magnitudes.
- It gives several concrete and actionable specification requirements, for example: normative algorithm descriptions **must use ASCII-only**; each operator in the symbol table must include **3 pieces of information** (ASCII form, operation description, and whether it is constant-time or variable-time).
- It sets specific coverage requirements for test vectors: they should cover **all logical paths**, valid but degenerate error/early-exit cases, and exceptions triggerable by **attacker-controlled inputs**; for branches with extremely low probability and infeasible reproduction, it may be noted that no test vector is provided.
- It imposes strong constraints on symbol usage: for example, `^` **must not** be reused within the same specification to represent two different operations; if Unicode symbols are used, they may appear only in explanatory examples/figures and an ASCII fallback must be provided.

## Link
- [https://cfrg.github.io/draft-irtf-cfrg-cryptography-specification/draft-irtf-cfrg-cryptography-specification.html](https://cfrg.github.io/draft-irtf-cfrg-cryptography-specification/draft-irtf-cfrg-cryptography-specification.html)
