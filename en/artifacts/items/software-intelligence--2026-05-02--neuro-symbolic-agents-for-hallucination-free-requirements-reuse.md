---
source: arxiv
url: https://arxiv.org/abs/2605.01562v2
published_at: '2026-05-02T18:16:04'
authors:
- Ahmed F. Ibrahim
topics:
- requirements-engineering
- multi-agent-systems
- neuro-symbolic-ai
- software-reuse
- llm-validation
- model-driven-engineering
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Neuro-Symbolic Agents for Hallucination-Free Requirements Reuse

## Summary
This paper turns OOMRAM requirements reuse into a constrained multi-agent workflow where an LLM suggests requirement choices and a deterministic validator blocks invalid combinations. It matters because requirements tools need natural-language input without allowing missing mandatory requirements, mutually exclusive selections, or invented IDs.

## Problem
- OOMRAM can reuse validated requirements, but its original retrieval method needs exact requirement identifiers, which makes natural-language project visions hard to use.
- Plain LLM-based requirements generation can invent requirement IDs, omit mandatory nodes, select mutually exclusive options, or create orphaned children.
- In regulated or safety-sensitive requirements work, a valid-looking but structurally invalid specification can create compliance and design risk.

## Approach
- The system stores each product-family model as a formal OOMRAM lattice: requirement nodes, parent-child edges, node types, and Boolean selection constraints.
- A LangGraph workflow uses four agents: Navigator chooses the next decision point, Interpreter maps the project vision to child requirement IDs, Validator checks the proposed selection, and Scribe writes the final specification.
- The Validator is plain Python with no LLM call. It enforces core-node inclusion, single-adaptor exactly-one selection, multiple-adaptor at-least-one selection, and parent-child consistency.
- If the Interpreter proposes an invalid selection, the Validator rejects it and sends the error back for correction before traversal continues.
- Subgraph navigation shows only local children to the Interpreter at each step, keeping prompt size constant and traversal time linear in the number of decision points.

## Results
- On 10 project visions across 2 application families, eRecordKeeping with about 60 requirements and SmartHome with about 20 requirements, all runs completed successfully.
- The paper reports 100% requirement coverage and 100% structural validity for generated final specifications.
- The constraint-violation rate was 0.2%: 1 violation occurred during an intermediate er_small_biz run and was corrected after Validator rejection, leaving final outputs violation-free.
- For the 3 visions with complete gold standards, F1 scores were 0.471 for er_small_biz, 0.576 for er_gov_agency, and 0.811 for sh_elderly; exact match was false for all 3 because multiple valid optional choices exist.
- Average latency across 10 visions was 210 seconds with 78 LLM calls per vision; eRecordKeeping averaged 263 seconds and 95 calls, while SmartHome averaged 160 seconds and 60 calls.
- The paper gives only qualitative baseline evidence for unconstrained LLM runs, reporting frequent cardinality errors, missing mandatory requirements, and orphaned children before adding the Validator loop.

## Link
- [https://arxiv.org/abs/2605.01562v2](https://arxiv.org/abs/2605.01562v2)
