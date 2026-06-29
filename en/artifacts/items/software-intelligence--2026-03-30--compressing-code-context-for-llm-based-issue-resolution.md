---
source: arxiv
url: http://arxiv.org/abs/2603.28119v1
published_at: '2026-03-30T07:31:12'
authors:
- Haoxiang Jia
- Earl T. Barr
- Sergey Mechtaev
topics:
- code-context-compression
- llm-program-repair
- swe-bench
- issue-resolution
- code-intelligence
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Compressing Code Context for LLM-based Issue Resolution

## Summary
This paper proposes SWEzze, a code-context compressor for LLM-based software issue resolution. It learns from oracle-distilled minimal sufficient contexts and cuts prompt size while improving fix success on SWE-bench Verified.

## Problem
- LLM issue-resolution systems often pass too much repository code into the prompt, which raises inference cost and makes the model attend to irrelevant code instead of bug-fixing evidence.
- Existing compressors either treat code like plain text and break useful program structure, or prune by shallow similarity and discard fix ingredients such as needed variables, expressions, or type information.
- This matters for real GitHub issue fixing because the needed patch context is sparse and may sit far from the bug description or localized file.

## Approach
- The paper defines a **minimal sufficient context**: the smallest 1-minimal subset of retrieved code that still lets a repair model generate a test-passing patch.
- It builds these contexts with **Oracle-guided Code Distillation (OCD)**. OCD uses a repair-and-test oracle, a genetic algorithm to find a passing subset, and hierarchical delta debugging to remove any code segment that is not individually necessary.
- Code is searched and pruned at structured units such as files, functions, class headers, and statement blocks, with omitted code replaced by placeholders so the prompt keeps its structure.
- The distilled training data is used to fine-tune **SWEzze**, a lightweight cross-encoder based on Qwen3-Reranker-0.6B with LoRA. At inference time, SWEzze scores code segments and greedily selects a compressed context under a token budget.
- Search is guided by training-time signals including overlap with gold patch files, failing-test coverage, and symbol overlap with the reference patch.

## Results
- On **SWE-bench Verified** with **GPT-5.2, DeepSeek-V3.2, and Qwen3-Coder-Next**, SWEzze keeps a stable compression rate of about **6x**.
- It reduces total token budget by **51.8% to 71.3%** relative to the uncompressed setting.
- It improves issue-resolution rates by **5.0% to 9.2%** over the uncompressed setup across the three frontier models.
- Against prior context compressors, the paper claims the best balance of repair effectiveness, compression, and latency, and says SWEzze covers **93.8% to 99.2%** of the union of all instances solved by any baseline.
- In a Matplotlib case study, SWEzze reached **BERTScore 0.44** against the distilled minimal context, versus **0.20** for LongCodeZip and **0.00** for SWE-Pruner.
- For training data, OCD distilled **3,157** successful instances from **41** repositories, with **156,545** labeled segments total; only **8.4%** of segments were relevant, and removing the genetic algorithm reduced successfully minimized instances by **52.7%**.

## Link
- [http://arxiv.org/abs/2603.28119v1](http://arxiv.org/abs/2603.28119v1)
