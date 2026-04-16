---
source: arxiv
url: http://arxiv.org/abs/2604.05150v1
published_at: '2026-04-06T20:25:20'
authors:
- Geert Trooskens
- Aaron Karlsberg
- Anmol Sharma
- Lamara De Brouwer
- Max Van Puyvelde
- Matthew Young
- John Thickstun
- Gil Alterovitz
- Walter A. De Brouwer
topics:
- llm-code-generation
- workflow-automation
- deterministic-execution
- code-intelligence
- enterprise-ai
- document-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation

## Summary
This paper studies "compiled AI": use an LLM once to generate workflow code, validate that code, then run the workflow as ordinary deterministic software. The main claim is that this trade gives up some runtime flexibility and gains lower cost, lower latency, stronger auditability, and better reliability for enterprise workflows.

## Problem
- Runtime LLM agents call the model on each transaction, which brings token cost, latency, and output variance even at temperature 0.
- In regulated workflows such as healthcare prior authorization, billing, and document processing, operators need deterministic behavior, audit trails, and security controls before deployment.
- Existing work shows agent reliability drops on multi-step tasks, so a system that moves model use to build time can fit high-volume, well-specified workflows better.

## Approach
- The system takes a workflow spec, selects validated templates and modules, and asks the LLM once to generate only a small business-logic function, usually 20 to 50 lines, inside that template.
- The generated artifact then goes through four required validation stages: security scanning, syntax and type checks, sandboxed execution tests, and output-accuracy checks against golden data.
- If any stage fails, the system regenerates code with the error context and retries before deployment.
- After a workflow passes validation, production execution uses static code with zero runtime LLM calls for the main compiled setting.
- For tasks that still need judgment on messy inputs, the paper adds a bounded variant called Code Factory, where compiled code can make narrow schema-constrained LLM calls with fallback logic and monitoring.

## Results
- On BFCL function calling (n=400), compiled AI reached 96% task completion (384/400) with zero execution tokens after a one-time 9,600-token compile cost.
- On BFCL, break-even versus direct LLM was about 17 transactions; at 1,000 transactions it used 57x fewer tokens than direct LLM and 84x fewer than AutoGen.
- At 1M transactions per month, reported total cost of ownership was $555 for compiled AI versus $22,000 for direct LLM, $29,400 for LangChain, and $31,900 for AutoGen.
- On BFCL latency, compiled AI ran at 4.5 ms P50 versus 2,004 ms for direct LLM, with 100% reproducibility and zero output entropy; direct runtime inference showed 95% reproducibility.
- On DocILE (5,680 invoices), Code Factory matched Direct LLM on KILE at 80.0% and beat it on LIR, 80.4% versus 74.5%; median latency was 2,695 ms versus 6,339 ms for Direct LLM. Pure deterministic regex was much faster at 0.6 ms but far worse on KILE at 20.3%.
- In security tests, prompt injection detection scored 95.8% recall and 100% precision on 30 adversarial inputs; the code safety gate scored 75% recall and 100% precision on 20 vulnerable and 20 benign fixtures. The abstract also reports 96.7% prompt-injection accuracy and 87.5% static-code safety accuracy across 135 test cases.

## Link
- [http://arxiv.org/abs/2604.05150v1](http://arxiv.org/abs/2604.05150v1)
