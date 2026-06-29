---
source: arxiv
url: https://arxiv.org/abs/2605.27238v1
published_at: '2026-05-26T16:17:47'
authors:
- Qianru Meng
- Xiao Zhang
- Zhaochun Ren
- Joost Visser
topics:
- agentic-program-repair
- code-intelligence
- automated-software-production
- test-driven-repair
- llm-agents
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# EviACT: An Evidence-to-Action Framework for Agentic Program Repair

## Summary
EviACT is an agentic program repair system that ties localization, patching, and validation to concrete evidence from failing tests, compiler output, and code structure. It claims higher resolve rates and lower API cost than comparable GPT-4o baselines across Defects4J 2.0 and SWE-bench variants.

## Problem
- Agentic APR systems often see execution evidence, then lose it across stages, causing wrong localization, invalid patches, and repeated expensive validation.
- The problem matters because repository-level repair needs cross-file search, build feedback, and test feedback; weak control wastes model calls and accepts work on the wrong code.

## Approach
- EviACT uses a Setup → Localize → Patch → Verify pipeline with three evidence gates between stages.
- The retrieval scaffold parses code with Tree-sitter, builds AST spans and a lightweight code graph, then maps RED failing-test evidence to the top-3 suspect spans using symbol, location, graph-distance, relation-support, and span-length signals.
- The compile gate rejects malformed diffs, unappliable patches, and patches that fail syntax or build checks before test validation.
- The test-driven gate reruns the originally failing tests first; only patches that turn those tests GREEN run full regression.
- Failed compile or GREEN checks return structured diagnostics to guide the next patch attempt or trigger re-localization when budget remains.

## Results
- With GPT-4o, EviACT reports the best resolve rate among comparable systems on all four evaluated settings: 25.0% on Defects4J 2.0, 40.4% on SWE-bench Verified, 38.0% on SWE-bench Lite, and 16.0% on SWE-bench Live.
- Against the strongest comparable GPT-4o baseline for each dataset, the reported gains are 5.4 percentage points on Defects4J 2.0, 1.6 on SWE-bench Verified, 6.0 on SWE-bench Lite, and 4.0 on SWE-bench Live.
- Reported GPT-4o per-bug API costs are $0.17 on Defects4J 2.0, $0.20 on SWE-bench Verified, $0.19 on SWE-bench Lite, and $0.23 on SWE-bench Live; where baseline costs are available, this is 70.1–88.6% lower.
- With GPT-5.2, EviACT reports higher resolve rates: 47.3% on Defects4J 2.0, 70.2% on SWE-bench Verified, 64.0% on SWE-bench Lite, and 36.0% on SWE-bench Live.
- DeepSeek-V3.2 gives the lowest reported cost while ranking second among EviACT backbones: 38.3% at $0.04 on Defects4J 2.0, 58.4% at $0.05 on SWE-bench Verified, 55.7% at $0.03 on SWE-bench Lite, and 28.0% at $0.04 on SWE-bench Live.
- In a 200-instance ablation using DeepSeek-V3.2, full EviACT improves resolve rate by 13.0 percentage points over the no-guardrail variant while using 84.1K fewer tokens and 195.3 seconds less runtime per run.

## Link
- [https://arxiv.org/abs/2605.27238v1](https://arxiv.org/abs/2605.27238v1)
