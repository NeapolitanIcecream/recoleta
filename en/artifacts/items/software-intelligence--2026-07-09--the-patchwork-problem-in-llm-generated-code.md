---
source: arxiv
url: https://arxiv.org/abs/2607.08981v1
published_at: '2026-07-09T23:01:54'
authors:
- Viraaji Mothukuri
- Reza M. Parizi
topics:
- code-intelligence
- software-foundation-model
- automated-software-production
- static-analysis
- multi-agent-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# The Patchwork Problem in LLM-Generated Code

## Summary
The paper defines the patchwork problem: LLM-generated code can pass local checks while violating repository-wide structural contracts. It proposes graph-based invariant checking to detect cross-file, configuration, dependency, resource, control-flow, and security wiring failures that standard CI often misses.

## Problem
- Generated code may compile and pass tests while referencing missing configuration keys, nonexistent packages, undefined resources, incompatible schemas, or unprotected routes.
- Type checking, tests, and SAST tools provide limited coverage for failures that span files and repository artifacts.
- These defects matter because they can remain latent until deployment, especially when humans review or integrate large volumes of AI-generated code.

## Approach
- Model repository artifacts as eight coordinated graphs: import, call, dependency, configuration, schema, resource, control-flow, and routing graphs.
- Define eight structural failure categories with explicit consistency invariants, including dependency hallucination, phantom internal APIs, cross-file contract violations, and security structural regressions.
- Use a hybrid verifier: delegate language-specific checks to mypy, tsc, pylint, and ESLint, while custom detectors check cross-graph constraints that existing tools do not cover.
- Validate dependencies against PyPI and npm, inspect configuration and resource references, compare producer and consumer schemas, and check route guard coverage.
- Produce localized evidence traces containing the violated invariant, affected files and lines, and the constraint required for coherence.

## Results
- The evaluation covers 336 generations from 2 frontier models under 4 prompting strategies.
- The paper claims that most structural failures evade type checking, testing, and SAST, but the excerpt provides no failure-rate, precision, recall, or baseline comparison numbers.
- Failure profiles differ qualitatively between the 2 models, which challenges mitigation methods that assume one model-independent error pattern.
- External validation on 43 real-world AI-generated repositories reports that structural failures occur outside controlled experiments.
- The strongest concrete claim is coverage: the verifier targets eight repository graph types and eight structural failure categories, including failures that conventional CI does not detect.

## Link
- [https://arxiv.org/abs/2607.08981v1](https://arxiv.org/abs/2607.08981v1)
