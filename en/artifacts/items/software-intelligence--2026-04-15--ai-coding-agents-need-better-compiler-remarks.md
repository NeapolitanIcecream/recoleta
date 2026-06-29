---
source: arxiv
url: http://arxiv.org/abs/2604.13927v1
published_at: '2026-04-15T14:35:07'
authors:
- Akash Deo
- Simone Campanoni
- Tommy McMichen
topics:
- compiler-feedback
- code-intelligence
- ai-coding-agents
- auto-vectorization
- program-optimization
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# AI Coding Agents Need Better Compiler Remarks

## Summary
This paper argues that AI coding agents fail at compiler-guided performance refactoring because compiler remarks are vague, not because the models are too weak. On TSVC, more precise optimization feedback raises vectorization success rates and can make a 7B model much more effective.

## Problem
- AI agents try to refactor C/C++ code so compilers can auto-vectorize it, but compiler feedback is often unstructured and vague.
- Ambiguous remarks tell the agent that optimization failed without clearly stating the data dependence or code location that caused the failure.
- This matters because poor feedback leads to low optimization success and can push agents into semantics-breaking edits when they guess wrong.

## Approach
- The authors test a compiler-guided coding workflow where Qwen2.5-Coder 7B receives source code plus compiler warnings, errors, and optimization remarks, then rewrites the code to enable auto-vectorization.
- They evaluate on 151 TSVC loops with Clang 21.1.8 and Intel 2025.3, with and without remarks, at temperatures 0.2, 0.8, and 1.2, using 100 trials per loop.
- Success is checked by compiler optimization records for vectorization and by differential testing to catch semantic breakage.
- To isolate the effect of feedback quality, they use a single-pass setup rather than a longer iterative agent loop.
- They also replace some vague remarks with hand-written precise remarks that expose exact dependence relations and source locations, plus a concrete fix suggestion.

## Results
- Without remarks, success rates are very low: Clang reaches 0.20%, 0.80%, and 1.45% at T=0.2, 0.8, and 1.2; Intel reaches 1.10%, 2.38%, and 3.67%.
- With remarks, success rises to 0.64%, 2.68%, and 3.93% for Clang and 4.59%, 6.95%, and 7.83% for Intel. At T=0.8, remarks improve Clang from 0.80% to 2.68% and Intel from 2.38% to 6.95%, about 3.3x and 2.9x.
- Precise existing remark types can help a lot: Intel Output Dependence adds +26.00 points at T=0.8, Anti Dependence adds +15.50, and Multiple Exits adds +22.33 at T=0.2.
- Some vague remarks are weak or harmful. Clang ArrayBounds drops by -2.00 at T=0.8 and -3.00 at T=1.2; Libcall/Instr drops by -2.50 at T=0.8. The paper also reports that Clang NonReductionValue often triggered semantic-breaking hallucinations in case studies.
- Hand-written precise dependence remarks produce the biggest gains: ReadAfterWrite adds +50.00 at T=0.8 and +59.00 at T=1.2; WriteAfterRead adds +45.00 at T=0.2, +40.80 at T=0.8, and +35.20 at T=1.2.
- WriteAfterWrite gives smaller gains, up to +9.00 at T=0.8, which suggests that dependence labels alone are sometimes not enough and more analysis may be needed.

## Link
- [http://arxiv.org/abs/2604.13927v1](http://arxiv.org/abs/2604.13927v1)
