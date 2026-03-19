---
source: arxiv
url: http://arxiv.org/abs/2603.04756v2
published_at: '2026-03-05T03:06:06'
authors:
- Mengnan Li
- Jason Miller
- Zachary Prince
- Alexander Lindsay
- Cody Permann
topics:
- domain-specific-agent
- rag
- code-generation
- scientific-simulation
- tool-augmented-llm
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# MOOSEnger -- a Domain-Specific AI Agent for the MOOSE Ecosystem

## Summary
MOOSEnger is a domain-specific AI agent for the MOOSE multiphysics simulation ecosystem, designed to convert natural-language requirements into runnable MOOSE input files. By combining retrieval-augmented generation, deterministic prechecks, and closed-loop validation with the MOOSE runtime in the loop, it significantly improves first-pass runnability.

## Problem
- MOOSE ".i" input files use strict HIT hierarchical syntax, with many components and detailed rules, making it difficult for newcomers to quickly write correct and runnable configurations.
- When generating this kind of domain DSL using only a general-purpose LLM, it is easy to produce formatting errors, broken syntactic structure, hallucinated object type names, and solver/configuration errors that only surface at runtime.
- This matters because the first runnable example in multiphysics simulation modeling is often the starting point for subsequent tuning, debugging, and scientific analysis; if the first-round failure rate is high, engineering and research efficiency are significantly slowed.

## Approach
- A **core-plus-domain** architecture separates general agent infrastructure from MOOSE-specific capabilities: the core layer handles configuration, tool registration, retrieval, persistence, and evaluation, while the MOOSE plugin layer handles HIT parsing, input file ingestion, type repair, and execution tools.
- **RAG** is used to retrieve curated documentation, examples, and input files; for MOOSE ".i" files, it uses structure-preserving chunking based on HIT syntax blocks rather than ordinary text chunking, increasing the chance of retrieving the correct block.
- A deterministic **input-precheck** pipeline is added after generation: it cleans hidden formatting contamination, repairs malformed HIT structures through a bounded, grammar-constrained loop, and corrects invalid object/type names using context-conditioned similarity search over the application syntax registry.
- The MOOSE executable is placed into the loop through an **MCP-backed** or local backend: it first validates and then optionally performs a smoke test, feeding solver errors and logs back to the agent for iterative “verify-and-correct” repair.
- Built-in evaluation covers both retrieval quality (faithfulness, answer relevancy, context precision/recall) and end-to-end execution success rate, using actual execution results to measure whether the system truly generated usable inputs.

## Results
- Evaluation was conducted on a benchmark covering **175 prompts**, with tasks spanning **7 MOOSE physics families**: diffusion, transient heat conduction, solid mechanics, porous flow, incompressible Navier–Stokes, phase field, and plasticity.
- MOOSEnger achieves an end-to-end **execution pass rate = 0.90**, while the **LLM-only baseline = 0.06**, an absolute improvement of **0.84**, or about **15×** the baseline.
- The paper mainly attributes this improvement to the combination of three mechanisms: retrieval augmentation, deterministic precheck repair, and involving the MOOSE runtime in validation and iterative error correction.
- The paper also claims the system can evaluate RAG faithfulness, relevancy, and precision/recall, but the provided excerpt **does not include the specific values for these metrics**.

## Link
- [http://arxiv.org/abs/2603.04756v2](http://arxiv.org/abs/2603.04756v2)
