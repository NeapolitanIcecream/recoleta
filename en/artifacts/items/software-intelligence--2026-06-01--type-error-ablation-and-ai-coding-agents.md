---
source: arxiv
url: https://arxiv.org/abs/2606.01522v1
published_at: '2026-06-01T01:09:13'
authors:
- Shriram Krishnamurthi
- Matthew Flatt
topics:
- ai-coding-agents
- type-errors
- program-repair
- compiler-diagnostics
- hindley-milner
- code-intelligence
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Type-Error Ablation and AI Coding Agents

## Summary
This paper tests whether verbose type-error messages help AI coding agents repair typed programs. In Shplait experiments, richer compiler diagnostics improved agent repair behavior, and 97.9% of repairs that removed the type error also passed the semantic tests.

## Problem
- Programming-language error messages have been tuned for human readers, so they are usually short and selective.
- AI coding agents can consume longer diagnostics, so terse compiler output may withhold useful repair information.
- The question matters because compiler diagnostics now feed automated repair loops, not only human debugging sessions.

## Approach
- The authors modified Shplait, an ML-style language with Hindley-Milner type inference, to expose several diagnostic modes.
- They built 10 correct Shplait programs and derived 60 broken variants, each with one deliberate type error and at least 5 failing tests when run without type checking.
- They compared four feedback modes: full unification stack, proximate error location, minimal type error, and untyped test-suite feedback.
- Aider drove the repair loop, mainly using qwen2.5-coder:14b through ollama; the authors also ran two full rounds with claude-haiku-4.5.
- A deterministic oracle classified each final attempt as still a type error, semantically wrong, or semantically correct by running the type checker and tests.

## Results
- The main qwen2.5-coder:14b experiment used 2,400 trials: 60 chaff programs × 4 feedback modes × 10 complete runs.
- The paper reports that more detailed type-error messages improved agent fix rates, with the full unification-stack mode outperforming less detailed diagnostics; the excerpt does not provide the exact per-mode rates.
- Typed feedback beat untyped test-suite-only feedback, so the type checker gave the agent useful repair signal beyond failed tests.
- Among cases where the agent fixed the type error, 97.9% also passed all semantic tests.
- In the proximate-location mode, the reported line matched the injected-error line in 39 of 60 chaffs; the other 21 cases showed why Hindley-Milner diagnostics can point away from the true source.
- The study also reports that leading agents could often repair programs even when all names were obfuscated, but the excerpt gives no exact success rate for that result.

## Link
- [https://arxiv.org/abs/2606.01522v1](https://arxiv.org/abs/2606.01522v1)
