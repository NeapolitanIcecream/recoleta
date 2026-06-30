---
source: arxiv
url: https://arxiv.org/abs/2606.30182v1
published_at: '2026-06-29T11:57:32'
authors:
- Tom Adamczewski
- David Owen
- David Rein
- Florian Brand
- Giles Edkins
- Allen Hart
- Daniel O'Connell
topics:
- code-intelligence
- software-benchmarks
- autonomous-coding
- program-synthesis
- ai-agents
- software-engineering
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# MirrorCode: AI can rebuild entire programs from behavior alone

## Summary
MirrorCode is a benchmark for testing whether AI agents can rebuild full command-line programs from behavior, without source code. The paper claims frontier agents can already complete some long software reimplementation tasks when the specification is precise and the inference budget is large.

## Problem
- Current coding benchmarks mostly test short tasks, so they give weak evidence about autonomous work on larger software projects.
- One-off demos, such as an AI building a compiler or browser, are hard to compare because human guidance and completeness are unclear.
- The problem matters because long-horizon autonomous coding is closer to real software production than small bug fixes or isolated functions.

## Approach
- MirrorCode gives an agent execute-only access to an existing CLI program, documentation, and visible input-output tests, but no source code or internet access.
- The agent writes a replacement program in one of six languages: Python, C, Rust, Go, OCaml, or Ada.
- Scoring uses end-to-end tests: the replacement must match the original program’s `stdout` and `stderr` exactly.
- Hidden tests, averaging 34% of the tests, check that the agent implemented behavior rather than memorizing visible cases.
- The benchmark has 25 target programs across Unix utilities, data serialization, query tools, bioinformatics, interpreters, static analysis, cryptography, and compression; 22 targets are released and 3 are private.

## Results
- Claude Opus 4.7 had the best reported score: 56% average 100%-solve rate across MirrorCode. GPT-5.5 scored 44%, and Gemini 3.1 Pro Preview scored 32%.
- At the ≥99% test-pass threshold, Claude Opus 4.7 scored 77%, GPT-5.5 scored 57%, and Gemini 3.1 Pro Preview scored 44%.
- Across 25 target programs, 17 had at least one perfect-scoring run, and 4 more had a run above 99%.
- Claude Opus 4.7 reimplemented `gotree`, a bioinformatics toolkit with about 16,000 lines of Go and 40+ commands, in 14 hours for $251, passing 2,000 of 2,001 tests, or 99.95%. The authors estimate a human engineer without AI would need 2–17 weeks.
- The paper reports that Opus 4.7 also reimplemented `pkl`, an Apple configuration language with about 60,000 lines of code.
- The hardest tasks remain open: 8 of 25 targets never reached 100%, 4 of 25 never reached 99%, and the best runs on `ruff` reached only 67% on hidden tests.

## Link
- [https://arxiv.org/abs/2606.30182v1](https://arxiv.org/abs/2606.30182v1)
