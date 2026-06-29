---
source: arxiv
url: https://arxiv.org/abs/2605.26457v1
published_at: '2026-05-26T02:12:48'
authors:
- Anmol Agarwal
- Natalie Neamtu
- Pranjal Aggarwal
- Seungone Kim
- Jannis Limperg
- Cedric Flamant
- Kanna Shimizu
- Bryan Parno
- Sean Welleck
topics:
- specification-autoformalization
- formal-verification
- code-intelligence
- ai-coding-agents
- verus
- software-benchmarks
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization

## Summary
Verus-SpecGym evaluates whether coding agents can turn natural-language programming tasks into faithful Verus specifications. This matters because verified code only helps when the formal specification matches the user's intent.

## Problem
- AI agents can generate code and proofs, but a verifier checks code against the formal spec, so a wrong spec can still certify the wrong behavior.
- Specification autoformalization is hard because natural-language programming tasks include input constraints, output rules, and edge cases that must become exact logical predicates.
- Existing evaluation routes are costly or weak: expert reference specs do not scale, and LLM judges can miss subtle specification errors.

## Approach
- The paper introduces Verus-SpecBench, a set of 581 specification-writing tasks derived from Codeforces problems and written for Verus, a Rust verifier.
- Verus-SpecGym gives an agent the informal problem, a Verus skeleton with `pre_spec` and `post_spec`, sample tests, examples, documentation, and tool access through Verus, bash, and the filesystem.
- The evaluator extends Verus `exec_spec` so generated logical specifications can run as executable Rust checks on concrete inputs and outputs.
- Each submitted spec is tested across four buckets: valid inputs accepted, invalid inputs rejected, correct outputs accepted, and incorrect outputs rejected.
- The hidden evaluation uses official Codeforces tests plus adversarial Codeforces hacks written by competitors to break wrong solutions.

## Results
- On 581 tasks, the best reported model, `gemini-3.1pro`, solves 77.8% of tasks.
- Other frontier models solve 51.1% to 57.8% of tasks under the paper's fixed compute and time budget.
- Open-source models reach 21.5% to 25.5%, giving a gap of at least 25.6 percentage points against the lowest reported frontier score.
- The paper evaluates 6 frontier and open-source agents.
- LLM-as-a-judge evaluation misses 26% of the failures caught by the executable evaluator.
- Reported failure modes include omitted input assumptions, accepted incorrect outputs, and rejected valid outputs.

## Link
- [https://arxiv.org/abs/2605.26457v1](https://arxiv.org/abs/2605.26457v1)
