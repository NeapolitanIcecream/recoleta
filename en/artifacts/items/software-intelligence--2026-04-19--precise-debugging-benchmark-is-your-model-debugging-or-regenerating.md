---
source: arxiv
url: http://arxiv.org/abs/2604.17338v2
published_at: '2026-04-19T09:08:23'
authors:
- Wang Bill Zhu
- Miaosen Chai
- Shangshang Wang
- Yejia Liu
- Song Bian
- Honghua Dong
- Willie Neiswanger
- Robin Jia
topics:
- debugging-benchmark
- code-llm-evaluation
- precise-editing
- agentic-debugging
- software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Precise Debugging Benchmark: Is Your Model Debugging or Regenerating?

## Summary
PDB is a debugging benchmark that checks whether a model makes targeted fixes or rewrites large parts of the program. The paper shows that strong coding models often pass tests while making many unnecessary edits, so unit-test accuracy alone hides weak debugging behavior.

## Problem
- Current debugging benchmarks score models by unit-test pass rate, so a minimal fix, a full rewrite, and some forms of hard-coding can look equally good.
- Real debugging needs fault localization and small, reviewable edits; broad regeneration is costly and risky in real codebases.
- Existing evaluation also misses partial progress on multi-bug programs, because fixing one bug and fixing none can receive the same binary score.

## Approach
- The authors introduce **Precise Debugging Benchmarking (PDB)**, a pipeline that turns existing coding datasets into debugging benchmarks by injecting verified bugs into correct programs.
- PDB first creates **atomic bugs** with known ground-truth edits, then composes independent bugs into multi-bug programs so each bug can be measured separately.
- The benchmark adds two metrics beyond unit tests: **edit-level precision** for how many edits were actually needed, and **bug-level recall** for how many bugs were truly fixed.
- It includes two released benchmarks: **PDB-Single-Hard** with 5,751 hard examples built from single-line bugs, and **PDB-Multi** with 256 examples built from contiguous multi-line bugs.
- The evaluation also tests single-shot, iterative, and agentic debugging setups to see whether extra attempts or feedback improve precise editing.

## Results
- On **PDB-Single-Hard**, **GPT-5.1-Codex** gets **76.1%** unit-test score but only **39.7% precision** and **71.7% recall**. **DeepSeek-V3.2-Thinking** gets **79.0%** unit score with **45.0% precision** and **71.2% recall**.
- Models with lower test-pass rates can be more precise debuggers: **Qwen3-Coder-480B** gets **70.3%** unit score but **65.8% precision** and **77.2% recall**.
- The best precision on PDB-Single-Hard comes from **Claude-4.5-Sonnet** at **71.8% precision**, **81.4% recall**, **75.7%** unit score, and **Gemini-2.5-Pro** at **71.4% precision**, **83.5% recall**, **78.1%** unit score. Even these models stay below **72% precision**.
- On **PDB-Multi**, the same gap remains: **GPT-5.1-Codex** has the top unit-test score at **77.0%** but only **27.9% precision** and **59.4% recall**; **Claude-4.5-Sonnet** reaches **65.9% precision**, **73.9% recall**, **64.8%** unit score; **Gemini-2.5-Pro** gets **57.8% precision**, **73.2% recall**, **72.7%** unit score.
- Iterative and agentic debugging improve unit-test score and recall, but the paper says they do **not** improve precision in a meaningful way; even **Claude-Code** reaches only about **50% precision** in the agentic setting.
- Prompting matters: freeform debugging reduces precision and recall. The paper reports that even strong models drop below **60% precision** under freeform prompts, and **Gemini-2.5-Pro** loses about **40 percentage points** of precision in that ablation.

## Link
- [http://arxiv.org/abs/2604.17338v2](http://arxiv.org/abs/2604.17338v2)
