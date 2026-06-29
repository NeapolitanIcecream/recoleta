---
source: arxiv
url: https://arxiv.org/abs/2606.09956v1
published_at: '2026-06-08T11:15:49'
authors:
- Nikolai Rozanov
topics:
- bug-localization
- code-intelligence
- software-verification
- llm-fine-tuning
- line-level-classification
- developer-tools
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Multi-task LLMs for Bug Classification: Efficient Inference with Auxiliary Decoding Heads

## Summary
The paper proposes MLC, a line-level bug localization method that adds a small bug/no-bug decoding head to a frozen code LLM. It targets faster full-file bug classification by predicting all buggy lines with one generated token per file.

## Problem
- LLM coding tools can generate code quickly, but verification and bug localization remain slow, costly, and often too coarse for repair.
- Agentic bug localization can take 1 to 2 minutes per file and generate thousands of tokens, while many methods only identify files or functions rather than exact lines.
- Prior line-level LLM methods often use short context windows or rely on newline tokens, which are unreliable because tokenizers can merge newlines with surrounding text.

## Approach
- MLC runs a pretrained code LLM over the whole file and keeps the backbone frozen in the main setup.
- A token-line alignment algorithm maps tokenizer output back to source lines, avoiding the assumption that newline tokens cleanly separate lines.
- The model aggregates token hidden states for each line using sum, mean, or last-token pooling.
- A small auxiliary decoding head predicts BUG or NO BUG for each line; optional LoRA/PEFT adapters can train extra bug-localization features.
- Training uses weighted binary cross-entropy over all lines in a file at once to handle class imbalance and variable file length.

## Results
- On full-file Defects4J, MLC Qwen1.7B + PEFT reaches Top-1 16.3%, Top-3 23.3%, and Top-5 39.5%, compared with DeepFL at 14.4%, 24.1%, and 34.2%, and Ochiai at 4.8%, 16.5%, and 25.1%.
- The supervised fine-tuning baseline on Defects4J performs poorly: SFT QwenCode7B scores Top-1 0.0%, Top-3 7.4%, and Top-5 14.3%.
- On PypiBugs, MLC Qwen1.7B + PEFT scores Top-1 8.6%, Top-3 27.4%, and Top-5 37.1%; the best non-PEFT result listed is MLC Qwen8B at 10.3%, 26.3%, and 36.6%.
- In a short-context Defects4J v1.2.0 comparison, MLC CodeGen16B scores Top-1 28.6% and Top-5 71.4%, compared with LLMAO CodeGen16B at 22.3% and 46.3%.
- Against function-level agentic systems, MLC CodeGen16B's Top-5 71.4% is close to MemFL with GPT-4.1-mini at 73.9%, but MemFL reports function-level results while MLC reports line-level results in the short-context setup.
- On the out-of-domain BugsEval set, trained from PypiBugs, MLC Qwen8B reaches Top-1 13.8%, Top-3 23.1%, and Top-5 29.2%; BugsEval contains 12 projects, 121 bugs, and 67 files.

## Link
- [https://arxiv.org/abs/2606.09956v1](https://arxiv.org/abs/2606.09956v1)
