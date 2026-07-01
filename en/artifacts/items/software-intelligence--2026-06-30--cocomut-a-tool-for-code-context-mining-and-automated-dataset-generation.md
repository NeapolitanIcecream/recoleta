---
source: arxiv
url: https://arxiv.org/abs/2606.31971v1
published_at: '2026-06-30T17:12:44'
authors:
- Alessandro Botta
- Shiven Garisa
- Jaya Vardhini Akurathi
- Ahsanul Ameen Sabit
- Trey Woodlief
- Soneya Binta Hossain
topics:
- code-context-mining
- java-static-analysis
- dataset-generation
- call-graph-reconciliation
- software-engineering-ai
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# CoCoMUT: A Tool for Code-Context Mining and Automated Dataset Generation

## Summary
CoCoMUT extracts method-level Java context and writes versioned JSONL datasets for code-intelligence research. It matters because LLM and learned software-engineering tools often need callers, callees, class context, docs, and metadata that are hard to collect consistently.

## Problem
- Software assistants need context beyond a single method body, including enclosing class details, Javadoc, callers, callees, type hierarchy, and structural metrics.
- Java context extraction is hard to reproduce because source declarations, bytecode signatures, build metadata, dependencies, overloads, generics, nested types, and synthetic methods do not line up cleanly.
- Task-specific data extractors make comparisons harder and can introduce hidden assumptions about method identity and context boundaries.

## Approach
- CoCoMUT builds a Spoon source model and records stable source method URIs, Javadoc, annotations, hierarchy data, source positions, fields, overloads, sibling methods, and metrics.
- It builds a SootUp static call graph from compiled project bytecode and dependencies, using RTA by default or CHA when selected.
- It matches bytecode call targets to source methods only when there is a unique match; ambiguous and unmatched targets keep the bytecode `target_uri` and explicit resolution metadata.
- It writes one deterministic JSONL record per selected method, with source, local class, documentation, caller/callee, provenance, and confidence fields.

## Results
- On 20 real Java repositories, split into 10 Maven and 10 Gradle projects, CoCoMUT completed build, bytecode availability, call-graph construction, and JSONL emission for all 20.
- It emitted 56,512 method-context records and 386,048 serialized caller/callee entries.
- Every caller/callee entry preserved a bytecode `target_uri`; 294,242 of 300,743 recognized project targets were linked to a source `method_uri`.
- Source-bytecode reconciliation reached 97.8% overall, with 98.4% on Maven projects and 93.8% on Gradle projects; CoCoMUT abstained on 6,501 project targets.
- Runtime across repositories was 9/65/275 seconds for min/average/max; Maven averaged 88 seconds and Gradle averaged 42 seconds.
- In a manual audit of 200 records across 10 repositories and 406,312 production SLOC, 198 records passed all applicable checks, giving a 99.0% pass rate; annotator agreement was 100.0% with Cohen’s κ = 1.00.

## Link
- [https://arxiv.org/abs/2606.31971v1](https://arxiv.org/abs/2606.31971v1)
