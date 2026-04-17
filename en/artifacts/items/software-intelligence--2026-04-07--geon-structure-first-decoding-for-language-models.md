---
source: hn
url: https://github.com/singhalpm-hub/geon-decoder
published_at: '2026-04-07T22:51:23'
authors:
- singhalpm
topics:
- code-generation
- structured-decoding
- language-models
- program-synthesis
- code-intelligence
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# GEON: Structure-first decoding for language models

## Summary
GEON changes decoding so a language model picks from structurally valid options before it picks the next token. In the provided code-generation examples and 10-task benchmark description, the claimed gain is better functional correctness on Python tasks where plain token decoding often writes plausible but wrong code.

## Problem
- Standard language-model decoding chooses the next token by probability, which can produce code that looks plausible but has wrong logic or incomplete structure.
- For code generation, syntax alone is not enough; the output also needs matched structure, admissible continuations, and behavior that passes the task.
- The paper argues this matters because many code errors come from decoding without structural constraints, which leads to incorrect programs even when the model knows the task pattern.

## Approach
- GEON inserts a structural decoding layer before token choice.
- It maps candidate tokens into equivalence classes, checks those classes under structural constraints, and removes options that are not admissible.
- After this filtering step, the decoder samples or selects a token only from the remaining valid set.
- The method aims to enforce syntactic closure, consistent control-flow structure, and other validity rules during generation rather than repairing outputs after generation.
- In simple terms: resolve the allowed structure first, then choose a token that fits inside that structure.

## Results
- The excerpt describes evaluation on 10 Python code-generation tasks: factorial, sum_list, max_element, count_vowels, reverse_string, is_even, is_sorted, count_positive, first_char, and square_list.
- It also mentions a smaller 3-task harness with factorial, sum_list, and max_element.
- For both baseline token decoding and GEON, the excerpt says outputs were syntactically valid Python.
- The claimed difference is at the structural and semantic level: baseline decoding often produced plausible but incorrect programs, while GEON produced consistent semantic correctness across all 10 tasks.
- No exact quantitative metrics are provided in the excerpt: no pass rate, accuracy, sample count, model name, or numerical baseline comparison.
- The concrete examples show the intended effect: GEON blocks structurally invalid continuations such as unmatched parentheses and incorrect branch structure, which the authors link to better functional correctness.

## Link
- [https://github.com/singhalpm-hub/geon-decoder](https://github.com/singhalpm-hub/geon-decoder)
