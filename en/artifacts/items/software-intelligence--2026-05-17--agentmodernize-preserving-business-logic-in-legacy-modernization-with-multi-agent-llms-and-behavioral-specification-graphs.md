---
source: arxiv
url: https://arxiv.org/abs/2605.17535v1
published_at: '2026-05-17T16:39:48'
authors:
- Sheikh Nazib Ahmed
- Marnim Galib
topics:
- multi-agent-software-engineering
- code-intelligence
- legacy-modernization
- behavioral-equivalence
- llm-agents
- software-foundation-models
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# AgentModernize: Preserving Business Logic in Legacy Modernization with Multi-Agent LLMs and Behavioral Specification Graphs

## Summary
AgentModernize is a multi-agent LLM system for legacy code modernization that tries to preserve business behavior, not just translate syntax. Its strongest claim is that an explicit Behavioral Specification Graph plus validation feedback improves behavioral equivalence over single-prompt and chain-of-thought baselines, though absolute BER remains low.

## Problem
- Legacy modernization can compile and still change business behavior, such as edge-case rules, validation logic, and exception handling hidden in COBOL, PL/SQL, shell scripts, and configuration files.
- This matters in banking, telecom, healthcare, and other regulated settings because undocumented rules often carry production and compliance meaning.
- Single-pass LLM translation has no explicit artifact for checking what the model understood before it writes new code.

## Approach
- Four agents split the task into legacy analysis, specification generation, code transformation, and equivalence validation.
- The Legacy Analyzer extracts business rules, control flow, constraints, source locations, and confidence labels into a Business Rule Inventory.
- The Specification Generator converts those rules into a Behavioral Specification Graph with operation nodes, control/data edges, preconditions, postconditions, invariants, inputs, outputs, and error behavior.
- The Transformer generates Python/FastAPI service code from the BSG, mapping operations to endpoints and translating contracts into validation and error handling.
- The Validator creates tests and differential traces from the BSG, reports behavioral failures, and sends targeted fixes back to the Transformer for up to 3 feedback iterations.

## Results
- On LegacyModernize-8, the benchmark has 8 scenarios, 7 telecom and 1 banking, with 12-15 rules per scenario and 195-310 LOC.
- With GPT-4o-mini, AgentModernize with feedback reached 9.4% mean Behavioral Equivalence Rate (BER); SP-LLM, CoT-LLM, and AgentModernize without feedback all scored 0.0% mean BER.
- GPT-4o results were 8.1% mean BER for full AgentModernize; the no-feedback variant reached 5.6% mean BER and only produced a non-zero score on S1 at 44.4%.
- GPT-5.3-codex reached 19.4% mean BER for full AgentModernize, while AgentModernize without feedback had 0.0% mean BER.
- SP-LLM and CoT-LLM scored 0.0% BER on every scenario and every tested backbone.
- The BSG captured 91.2% of gold-standard rules, so the paper argues that code generation and repair are the main bottlenecks after extraction.

## Link
- [https://arxiv.org/abs/2605.17535v1](https://arxiv.org/abs/2605.17535v1)
