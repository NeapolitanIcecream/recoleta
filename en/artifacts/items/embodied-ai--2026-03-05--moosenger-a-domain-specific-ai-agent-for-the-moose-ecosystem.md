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
- scientific-computing
- simulation-authoring
- tool-augmented-llm
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# MOOSEnger -- a Domain-Specific AI Agent for the MOOSE Ecosystem

## Summary
MOOSEnger is a domain-specific AI agent for the MOOSE multiphysics simulation ecosystem, aimed at turning natural-language requirements into runnable `.i` input files, and then automatically checking, repairing, and validating them through execution. Its core value is in combining retrieval-augmented generation with a closed feedback loop from the MOOSE runtime, significantly improving the reliability of getting a runnable result on the first attempt.

## Problem
- MOOSE `.i` input files have strict syntax and a wide variety of object types, making modeling, debugging, and finding the correct configuration patterns costly for beginners.
- Pure one-shot LLM generation tends to produce two kinds of errors: **broken formatting/syntax**, and **hallucinated object or parameter names that do not exist**, causing simulations to fail to run at all.
- In multiphysics workflows, users need not only to “write the file,” but also to turn executor and solver error messages into actionable repair steps, which directly affects the speed of reaching the **first valid run**.

## Approach
- Uses a **core-plus-domain** architecture: general agent infrastructure handles configuration, tool dispatch, retrieval, persistence, and evaluation; the MOOSE plugin provides HIT parsing, input-file ingestion, syntax checking, and execution tools.
- Uses **RAG** to retrieve curated MOOSE documentation, example inputs, and discussion content; for `.i` files it uses **HIT/pyhit structure-preserving chunking** to avoid breaking apart semantically related blocks.
- Introduces an **input-precheck** pipeline: first cleans hidden formatting issues, then repairs broken HIT structure through a **bounded, grammar-constrained repair loop**, and corrects invalid object type names using **context-conditioned similarity search** based on the application syntax registry.
- Puts the **MOOSE runtime in the loop**: through an MCP backend or local fallback, it performs actual validation/smoke runs and turns solver and execution logs into iterative “verify-and-correct” updates, rather than relying only on language-model guessing.
- Built-in evaluation covers both retrieval quality and end-to-end agent success rate, including faithfulness, answer relevancy, context precision/recall, and whether real execution succeeds.

## Results
- Evaluated on a benchmark covering **175 prompts**, with tasks spanning **7 physics families**: diffusion, transient heat conduction, solid mechanics, porous flow, incompressible Navier–Stokes, phase field, and plasticity.
- MOOSEnger achieves an **execution pass rate** of **0.90**, while the **LLM-only baseline** reaches only **0.06**; this is an absolute improvement of **0.84**, or about **15×** the baseline.
- The paper attributes the main performance gains to the interaction of three factors: **structure-preserving retrieval**, **deterministic precheck/repair**, and **bringing the MOOSE executor into the loop** for validation and error correction.
- The paper also states that it provides retrieval-side evaluation metrics (faithfulness, relevancy, precision/recall), but the provided excerpt **does not include the specific numeric results for those metrics**. The strongest quantitative conclusion is that end-to-end execution success improves from **0.06 to 0.90**.

## Link
- [http://arxiv.org/abs/2603.04756v2](http://arxiv.org/abs/2603.04756v2)
