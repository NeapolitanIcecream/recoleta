---
source: arxiv
url: https://arxiv.org/abs/2605.30054v1
published_at: '2026-05-28T15:05:53'
authors:
- Boqi Chen
- "Jos\xE9 Antonio Hern\xE1ndez L\xF3pez"
- Aren A. Babikian
topics:
- constrained-decoding
- semantic-validation
- code-generation
- partial-models
- software-engineering
- llm-decoding
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Projectional Decoding: Towards Semantic-Aware LLM Generation

## Summary
Projectional decoding keeps a partial graph model beside the token stream so an LLM can reject semantically invalid software artifacts during generation. The paper claims preliminary gains on CLEVR DSL program generation, with semantic validity rising to 73.33%–79.67% across Qwen3 models.

## Problem
- LLMs can produce syntactically valid software artifacts that still violate type rules, invariants, data-flow constraints, contracts, or domain rules.
- Post-generation repair can fail when the output is too broken to interpret, and it gives no guarantee during decoding.
- This matters for code generation, DSL generation, modeling, API use, and other software engineering tasks where invalid artifacts can break execution or integration.

## Approach
- The method maintains two linked states during decoding: the text prefix and a partial graph model of the artifact being generated.
- Each candidate token first passes syntax checking, then updates the partial model according to the metamodel and constraints.
- The partial model records certain, possible, absent, and error elements, which lets the decoder reason about incomplete artifacts.
- Tokens that create constraint violations are masked before sampling; remaining tokens keep generation on paths that may still produce a valid artifact.
- The paper connects this mechanism to graph pattern matching for structural constraints and abstract interpretation for behavioral constraints.

## Results
- On CLEVR program generation with Qwen3-4B, semantic validity improved from 4.33% with no guidance and 48.67% with syntax-only decoding to 73.67% with projectional decoding.
- On Qwen3-8B, semantic validity improved from 60.33% with no guidance and 61.00% with syntax-only decoding to 79.67% with projectional decoding.
- On Qwen3-14B, semantic validity improved from 55.44% with no guidance and 58.33% with syntax-only decoding to 73.33% with projectional decoding.
- Task accuracy with projectional decoding was 36.00% on 4B, 40.00% on 8B, and 37.33% on 14B; it beat syntax-only decoding in all three cases and no guidance in 2 of 3 cases.
- Average generation-time overhead versus no guidance was 1.1x for Qwen3-4B, 1.5x for Qwen3-8B, and 1.1x for Qwen3-14B.
- The evaluation is preliminary and uses one DSL benchmark; the method still failed to reach 100% semantic validity because decoding can reach prefixes with no valid completion.

## Link
- [https://arxiv.org/abs/2605.30054v1](https://arxiv.org/abs/2605.30054v1)
