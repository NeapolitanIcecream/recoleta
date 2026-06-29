---
source: arxiv
url: https://arxiv.org/abs/2606.05037v1
published_at: '2026-06-03T16:02:11'
authors:
- Arquimedes Canedo
- Grama Chethan
topics:
- llm-agents
- api-error-recovery
- structured-feedback
- agent-tool-use
- benchmark-leakage
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Self-Reflective APIs: Structure Beats Verbosity for AI Agent Recovery

## Summary
Self-reflective APIs add machine-readable repair suggestions to validation errors so an AI agent can fix a failed API call and retry. The paper reports large gains for Anthropic models on adversarial API-recovery tasks, with no significant gain for gpt-4o-mini in the pilot.

## Problem
- AI agents often fail after API validation errors because ordinary error messages say what failed but omit the exact request changes needed for recovery.
- This matters most when the API enforces domain-specific or proprietary rules, such as certified gluten-free brands, cuisine constraints, sourdough technique, or exact scaling values.
- Plain-English verbose errors can leak answers in benchmarks, so the paper also treats leakage auditing as part of the evaluation problem.

## Approach
- The API returns a top-level `recovery_feedback` object on validation failure, with a `suggestions[]` array containing typed actions and literal parameter values for the next request.
- A retry-loop agent calls the API up to 5 times, merges any suggested parameters into the next request, and retries without changing the validator or business logic.
- The experiment compares 3 response modes: Traditional generic errors, Traditional Verbose per-rule diagnoses without literal fixes, and Reflective diagnoses plus structured suggestions.
- The main testbed is a recipe-conversion API with 10 adversarial tasks covering ingredient compatibility, celiac certification, numeric precision, and multi-error recovery.
- The authors audit two leakage channels: validator messages that reveal fixes and task prompts that expose success criteria.

## Results
- Pilot design: 10 tasks × 3 modes × 3 runs × 3 LLMs, with 30 attempts per model/mode cell.
- On Anthropic models, structured suggestions improve task-completion rate by +36.7 to +40.0 percentage points over plain-English diagnoses, with Fisher’s exact p ≤ 0.0022.
- Token efficiency per success improves by 1.8× for claude-haiku-4-5 and 2.2× for claude-sonnet-4-6 compared with the Verbose baseline.
- On gpt-4o-mini, the lift is +13.3 percentage points and is not statistically significant: p = 0.435.
- For gpt-4o-mini, per-success token use is close between Reflective and Verbose: 3,548 vs 3,665 tokens.
- A second-domain billing API replication is reported to confirm the pattern, but the excerpt does not provide its detailed numeric results.

## Link
- [https://arxiv.org/abs/2606.05037v1](https://arxiv.org/abs/2606.05037v1)
