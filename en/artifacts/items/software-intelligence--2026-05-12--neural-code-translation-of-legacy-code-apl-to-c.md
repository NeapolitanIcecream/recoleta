---
source: arxiv
url: https://arxiv.org/abs/2605.13896v1
published_at: '2026-05-12T12:11:33'
authors:
- Abdulrahman Ramadan
- Hanen Borchani
- Iben Lilholm
- Mikkel Almind
- Allan Peter Engsig-Karup
topics:
- code-translation
- legacy-code
- apl-to-csharp
- code-intelligence
- llm-fine-tuning
- program-repair
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Neural Code Translation of Legacy Code: APL to C#

## Summary
The paper studies LLM-based translation of legacy APL code into C#. Its main contribution is a dedicated APL-to-C# dataset, guided translation methods, and a compile-and-run evaluation pipeline for functional correctness.

## Problem
- APL is concise, array-oriented, dynamically typed, and glyph-heavy, while C# is statically typed and more verbose. Direct translation often needs type mapping, overloads, loops, bounds checks, and index conversion from 1-based APL to 0-based C#.
- Legacy APL systems are hard to maintain as APL expertise declines, so automated migration to C# could reduce manual rewrite work.
- Public parallel corpora for APL-to-C# are scarce, which limits supervised training and standard benchmark evaluation.

## Approach
- The authors compare direct fine-tuned APL-to-C# translation with three guided methods: natural-language description mediation, retrieval-augmented translation, and iterative repair using compiler and test feedback.
- They build aligned APL and C# datasets: 800 curated basic pairs, 143 production-derived utility functions, 320 Rosetta Code pairs, and 45 APL idioms.
- They fine-tune open-weight models with LoRA and 8-bit quantization, using 1,066 training samples and a 2,048-token sequence length.
- They parse APL headers with an F# tool to generate C# method signatures, then include those signatures in prompts to help with C# typing.
- Evaluation compiles generated C# and runs it against input-output tests; the iterative method retries up to 5 times with compiler errors, expected outputs, actual outputs, and prior attempts in context.

## Results
- The provided excerpt does not include quantitative translation accuracy, compile pass rate, or execution pass rate for the main APL-to-C# task.
- The paper reports dataset sizes: Dataset A has 800 pairs, Dataset B has 143 production-derived functions, Dataset C has 320 Rosetta Code pairs, Dataset I has 45 idioms, and the training corpus has 1,066 samples.
- Production-oriented testing uses Dataset B's test split with 49 samples.
- Tokenizer analysis shows Qwen3-32B has a 0.715 APL single-token rate, 1.284 average tokens per glyph, 262.274 average tokens per sample, and 0 round-trip failures.
- Gemma-4-31b-it has a 0.671 APL single-token rate, 1.656 average tokens per glyph, 277.475 average tokens per sample, and 1 round-trip failure; Deepseek-Coder-6.7b-Instruct has 61 round-trip failures due to mishandling the APL division symbol.
- The abstract claims that added context and guidance improve model performance over direct translation, but the excerpt does not provide the accuracy numbers needed to measure that gain.

## Link
- [https://arxiv.org/abs/2605.13896v1](https://arxiv.org/abs/2605.13896v1)
