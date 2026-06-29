---
source: arxiv
url: http://arxiv.org/abs/2604.03978v1
published_at: '2026-04-05T05:51:54'
authors:
- Anh T. V. Dau
- Shin Hwei Tan
- Jinqiu Yang
- Nghi D. Q. Bui
- Anh Tuan Nguyen
topics:
- cobol-code-generation
- compiler-guided-repair
- llm-debugging
- legacy-software
- code-intelligence
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# COBOLAssist: Analyzing and Fixing Compilation Errors for LLM-Powered COBOL Code Generation

## Summary
COBOLAssist is a compiler-guided repair loop for LLM-generated COBOL code. It studies what kinds of compilation errors LLMs make in COBOL and shows that feeding compiler errors back to the model can raise both compilation success and test pass rates.

## Problem
- LLMs generate COBOL with frequent compilation failures because COBOL has rigid program structure, strict syntax, and limited public training data.
- This matters because COBOL still runs critical business and government systems, while experienced COBOL developers are harder to find.
- Prior COBOL generation work measured model performance, but did not focus on automatic repair of compilation errors in generated COBOL.

## Approach
- The paper first builds a COBOL-specific taxonomy for compilation errors in LLM-generated code using 876 generated programs, 980 compilation errors, two annotators, and Cohen's kappa of 0.9.
- It groups errors into three main classes: incomplete code errors, syntax errors, and type-related errors.
- COBOLAssist generates COBOL code, compiles it with GnuCOBOL, takes the compiler error log, and prompts the LLM to revise the code.
- This repair loop repeats until the code compiles or a maximum number of iterations is reached.
- Evaluation uses the COBOLEval benchmark with 146 tasks and several models: GPT-3.5, GPT-4, GPT-4o-mini, GPT-4o, and mAInframer variants.

## Results
- On error analysis, incorrect use of program structures is the largest error class in LLM-generated COBOL at 35.1%, versus 19.8% in human-written COBOL from prior work.
- Two error types are reported as unique to LLM-generated COBOL in this study: incorrect use of built-in functions at 17.2% and incomplete block termination at 5.6%.
- COBOLAssist raises compilation success for GPT-4o-mini from 29.5% to 64.38%.
- COBOLAssist raises compilation success for GPT-4o from 41.8% to 95.89%.
- The paper reports mAInframer-34B reaches 97.94% compilation success, the highest reported CSR among evaluated models, but with limited functional correctness.
- Functional correctness also improves: GPT-4 pass@1 rises from 9.1 to 22.6, and GPT-4o pass@1 rises from 16.4 to 29.45 on COBOLEval.

## Link
- [http://arxiv.org/abs/2604.03978v1](http://arxiv.org/abs/2604.03978v1)
