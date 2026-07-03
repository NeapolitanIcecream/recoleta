---
source: hn
url: https://soteria-tools.com/blog/teaching-ai
published_at: '2026-07-01T22:25:12'
authors:
- giltho
topics:
- software-foundation-model
- code-intelligence
- software-verification
- symbolic-execution
- bug-detection
- ai-training-data
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Teaching AI to Reason About Software

## Summary
AWS researchers trained Qwen3-8B on Soteria symbolic execution traces so it could reason about C program behavior and detect correctness violations better. The reported gain is strongest for bug detection: the trained 8B model beat an untrained 32B model on violation detection in the cited setup.

## Problem
- Code models often produce plausible C code while missing behavior errors such as memory safety bugs, overflows, nontermination, reachability failures, and data races.
- In a 500-task SV-COMP 2025 C verification evaluation, models scored above 90% on many property-holds cases but were weaker on real violations; 4 of 14 models caught fewer than half of the bugs.
- Better violation detection matters because pull-request review, debugging, refactoring, and verification need models to track execution behavior, not only source-code patterns.

## Approach
- The researchers ran Soteria on open-source C code filtered from the CodeParrot dataset and collected symbolic execution traces.
- Each trace records execution paths, program states, symbolic values, path conditions, branch choices, and the conditions that lead to a property violation.
- They used a few thousand Soteria traces for continued pretraining of Qwen3-8B, with training data separate from the SV-COMP benchmark.
- At inference time, the best setup combined trace-trained Qwen3-8B with step-by-step reasoning.

## Results
- The evaluation used 500 C verification tasks from SV-COMP 2025 across 5 property types: memory safety, overflows, termination, reachability, and data races.
- Across 14 models from 6 families, most models scored above 90% on cases where the property holds, while 4 of 14 caught fewer than 50% of real bugs.
- One model fell below 10% accuracy on programs of 100–200 lines, showing a sharp length-related failure in the reported benchmark.
- Training on Soteria bug traces plus step-by-step reasoning improved violation detection by 17.9 percentage points over the baseline.
- Reasoning alone changed violation detection by -1.4 points, and trace training alone improved it by +7.3 points, so the combined setup produced the largest reported gain.
- The trained Qwen3-8B detected violations at 67%, compared with 57% for untrained Qwen3-32B with reasoning disabled.

## Link
- [https://soteria-tools.com/blog/teaching-ai](https://soteria-tools.com/blog/teaching-ai)
