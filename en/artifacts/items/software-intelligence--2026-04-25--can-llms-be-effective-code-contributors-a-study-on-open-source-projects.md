---
source: arxiv
url: http://arxiv.org/abs/2604.23340v1
published_at: '2026-04-25T15:00:14'
authors:
- Chun Jie Chong
- Muyeed Ahmed
- Zhihao
- Yao
- Iulian Neamtiu
topics:
- llm-code-generation
- open-source-software
- code-repair
- software-testing
- static-analysis
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Can LLMs be Effective Code Contributors? A Study on Open-source Projects

## Summary
This paper tests whether current LLMs can produce commit-ready code for real open-source C projects. Across 212 real commits in eight projects, the authors find that success is uneven and often blocked by compile errors, static-analysis failures, test failures, context limits, and likely training-set memorization.

## Problem
- The paper studies whether LLMs can fix bugs or add small features in real repositories well enough for direct integration into production code.
- This matters because LLM-written code is already common, but benchmark performance does not show whether models can work inside large codebases with existing files, build rules, static checks, and test suites.
- The authors also want to measure how these models fail: syntax errors, wrong fixes, unsafe code, weak handling of large context, and cases where success may come from memorized training examples.

## Approach
- The authors build an automated evaluation framework that takes a real source file and a prompt, asks an LLM for a patch, inserts that patch into the pre-commit codebase, then checks it with the Clang static analyzer and the project's test suite.
- They evaluate 212 real commits from 8 open-source C projects: 187 bug fixes and 25 feature enhancements from projects including FFmpeg, wolfSSL, jansson, Bison, Vsftpd, packcc, libhl, and Collections-C.
- The tested models are GPT-4o, Ministral3-14B, and Qwen3-Coder-30B.
- Prompts are built from the real commit message plus the affected function name, and the changed file from the parent commit is given as context.
- The study uses one-shot generation only; the authors do not retry with iterative prompting.

## Results
- Across projects, overall success rate ranges from **0% to 60%**, depending on the project.
- On the 212 commits, LLM-generated code **failed to compile in 2 to 32 cases**, depending on the model.
- For code that compiled, static verification still found **9 to 18 null-pointer dereferences** and **9 to 72 unsafe casts**.
- Among **98 to 143 commits** where the authors could run tests, test-suite pass rate was **71.8% to 86.7%**, depending on the model and project coverage.
- The commits were small, usually **4 to 15 LOC**, yet the models still often produced partial fixes, empty patches, wrong fixes, unrelated deletions, undeclared identifiers, and incorrect assumptions about APIs or struct members.
- The paper claims success drops when context gets too large, models struggle to generate new code more than simple edits, and some successful outputs appear to come from parroting code changes seen during training rather than reasoning from the repository state.

## Link
- [http://arxiv.org/abs/2604.23340v1](http://arxiv.org/abs/2604.23340v1)
