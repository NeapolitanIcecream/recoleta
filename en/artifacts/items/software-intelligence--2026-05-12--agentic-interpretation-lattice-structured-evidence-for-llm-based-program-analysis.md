---
source: arxiv
url: https://arxiv.org/abs/2605.12694v1
published_at: '2026-05-12T19:46:24'
authors:
- Jacqueline L. Mitchell
- Chao Wang
topics:
- llm-program-analysis
- static-analysis
- evidence-lattices
- software-security
- agentic-systems
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# Agentic Interpretation: Lattice-Structured Evidence for LLM-Based Program Analysis

## Summary
Agentic interpretation structures LLM-based program analysis as evidence tracking over a finite lattice, with a worklist that revisits localized claims when related evidence changes. It targets analyses where source code alone is insufficient, such as opaque libraries, version-specific advisories, and informal API contracts.

## Problem
- One-shot LLM program analysis can hide which subclaims are supported, refuted, or unresolved, which makes audit and follow-up hard.
- Evidence-dependent program analyses matter because security and correctness can depend on documentation, package metadata, advisories, third-party behavior, and informal API contracts that a fixed static analyzer may not inspect.
- Generate-and-check LLM methods work when an external verifier can validate the LLM output, but many practical questions lack such a verifier.

## Approach
- The method decomposes a high-level analysis goal and a program graph into localized claims tied to program points, component boundaries, and auxiliary nodes.
- An LLM agent evaluates each claim with controlled context, including source snippets, related claims, prior evidence, and external information.
- The paper records each judgment in a finite-height assessment lattice rather than a single free-form answer.
- The worked example uses a graded evidence domain `A_Graded = {⊥, w, s} × {⊥, w, s}`, giving 9 lattice states for support and refutation strength.
- A worklist algorithm propagates context edges forward and feedback edges backward, so later findings can trigger narrower searches about earlier opaque components.

## Results
- The paper reports no experimental results, no implementation, and no benchmark numbers; it states that practical implementation and evaluation are future work.
- It claims 3 contributions: the agentic interpretation model, a formal core model, and a design-space discussion for evidence-dependent program analysis.
- The worked example defines 7 concrete claims across parser, verifier, processor, rejection, composition, and exit nodes for an opaque-component security review.
- The paper identifies 5 target categories for agentic interpretation, though the excerpt does not list their names in text.
- Its strongest concrete claim is that a finite lattice plus a worklist can make LLM evidence states bounded, inspectable, and reusable across later prompts, while still allowing the LLM to consult external evidence.

## Link
- [https://arxiv.org/abs/2605.12694v1](https://arxiv.org/abs/2605.12694v1)
