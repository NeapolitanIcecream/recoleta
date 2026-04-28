---
source: arxiv
url: http://arxiv.org/abs/2604.16198v1
published_at: '2026-04-17T16:08:05'
authors:
- Jia Li
- Ruiqi Bai
- Yangkang Luo
- Yiran Zhang
- Wentao Yang
- Zeyu Sun
- Tiankuo Zhao
- Dongming Jin
- Lei Li
- Zhi Jin
topics:
- code-generation
- requirement-alignment
- llm-evaluation
- program-synthesis
- code-intelligence
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Bridging the Gap between User Intent and LLM: A Requirement Alignment Approach for Code Generation

## Summary
REA-Coder improves LLM code generation by checking whether the model understood the requirement before and after writing code. Across four LLMs and five benchmarks, it beats strong reasoning and repair baselines, with the largest gains on harder competitive programming sets.

## Problem
- Existing code generation methods usually assume the LLM understood the prompt correctly, then focus on better reasoning or code repair.
- The paper argues that many failures start earlier: the model misreads the requirement, so later planning and repair operate on the wrong task.
- This matters because requirement misunderstanding can block functional correctness even when the model can write valid code.

## Approach
- REA-Coder builds a requirement-focused question checklist from the problem statement, with reference answers that cover core requirement dimensions.
- The LLM answers those questions, compares its answers with the reference answers, and uses mismatches to rewrite the requirement into an aligned version with missing or ambiguous details made explicit.
- The model generates code from this aligned requirement and checks it with public tests.
- If the code fails, REA-Coder masks key semantic spans in the requirement and asks the LLM to recover them from the generated code. Recovery errors show where the code and requirement still disagree.
- Those new errors are turned into updated checklist items, and the alignment-plus-generation loop repeats until the code passes tests or hits the iteration limit.

## Results
- The paper reports that REA-Coder outperforms 8 baselines on all 20 model-benchmark settings tested: 4 LLMs × 5 benchmarks.
- Average improvement over the best baseline is **7.93% on APPS**, **30.25% on CodeContests-raw**, **26.75% on CodeContests**, **8.59% on xCodeEval**, and **8.64% on LiveCodeBench-Lite**.
- On **Qwen3-Coder**, REA-Coder reaches **66.67% Pass@1 on APPS**, **40.61% on CodeContests-raw**, **33.33% on CodeContests**, **52.00% on xCodeEval**, and **38.29% on LC-Lite**. The listed gains over the strongest baseline are **17.68%**, **76.34%**, **66.65%**, **16.41%**, and **15.54%**.
- On **DeepSeek-v3.2**, REA-Coder gets **81.67% / 67.27% / 61.82% / 70.33% / 62.86% Pass@1** on APPS, CodeContests-raw, CodeContests, xCodeEval, and LC-Lite, with gains of **9.87% / 24.71% / 24.39% / 8.20% / 11.12%** over the best baseline.
- On **GPT-5-mini**, it gets **85.00% / 73.33% / 60.61% / 71.33% / 62.86%**, with gains of **2.55% / 11.01% / 5.26% / 3.38% / 4.77%**.
- On **Gemini-3-Flash**, it gets **88.33% / 81.21% / 75.15% / 83.33% / 75.43%**, with gains of **1.63% / 8.93% / 10.71% / 6.38% / 3.13%**. The paper also states that using only pre-generation requirement alignment improves the first generated code over zero-shot by **210.44% on APPS** and **344.67% on xCodeEval**.

## Link
- [http://arxiv.org/abs/2604.16198v1](http://arxiv.org/abs/2604.16198v1)
