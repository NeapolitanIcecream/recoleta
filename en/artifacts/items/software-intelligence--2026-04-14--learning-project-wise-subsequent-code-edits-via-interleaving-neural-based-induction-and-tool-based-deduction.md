---
source: arxiv
url: http://arxiv.org/abs/2604.12220v1
published_at: '2026-04-14T02:56:21'
authors:
- Chenyan Liu
- Yun Lin
- Yuhuan Huang
- Jiaxin Chang
- Binhang Qi
- Bo Jiang
- Zhiyong Huang
- Jin Song Dong
topics:
- project-wise-code-editing
- code-intelligence
- cross-file-refactoring
- llm-tool-integration
- interactive-code-assistance
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Learning Project-wise Subsequent Code Edits via Interleaving Neural-based Induction and Tool-based Deduction

## Summary
TRACE is a project-wide code editing system that mixes LLM predictions with IDE tools such as rename and def-use analysis. It targets cross-file follow-up edits, where pure neural editors miss locations or cost too much to scan the whole project.

## Problem
- Developers often make incremental, project-wide edits such as refactors, bug fixes, and feature changes; the paper cites prior evidence that these account for over 70% of commit-history changes.
- Existing tools trade off scope, accuracy, and speed: local editors work well in a small area, while project-wide neural systems pay high location cost and can miss or hallucinate cross-file edits.
- Git-diff style edit labels are too coarse for training because one hunk can contain multiple edit semantics; the authors measure this in 18.04% of hunks.

## Approach
- TRACE predicts the next edit from the project, prior edits, and an optional prompt.
- It interleaves **neural induction** for semantic edits with **tool deduction** for syntactic edit patterns. In simple terms: if the recent edit looks like a rename, signature update, clone update, or diagnose-fix pattern, TRACE calls IDE/LSP tools to find related edits; otherwise it runs neural location and generation models over code windows.
- The system has three parts: an edit-composition invoker that decides when to call tools, an edit locator that labels lines and gaps as edit targets, and an edit generator that writes the code change.
- The paper also adds a finer edit representation with 6 labels instead of the usual 3: `<KEEP>`, `<REPLACE>`, `<DELETE>`, `<NULL>`, `<INSERT>`, and `<BLOCK-SPLIT>`. This separates mixed edit semantics inside one hunk.
- The representation is built by parsing code with Tree-sitter, aligning old and new tokens with LCS, then assigning line and inter-line edit labels.

## Results
- Evaluation covers **38K commits**, **678 projects**, and **5 programming languages**.
- Against prior systems such as **CoEdPilot, GrACE, and CCT5**, TRACE improves **edit-location precision by 43.76%**, **recall by 9.96%**, and **edit-generation accuracy by 11.16%**.
- The edit-composition invoker reaches **92.45% precision** and **94.63% recall** for deciding tool invocation.
- The new edit representation improves the neural **edit locator by 14.57%** and the **edit generator by 7.40%**.
- In interactive edit simulation, TRACE reduces **time cost by 14.40%** and reaches **27.71% suggestion acceptance**; the abstract also states an acceptance rate **6.15% higher than Cursor**.
- The paper reports a user study with **24 participants** across **3 tasks** and says TRACE leads on cross-file global edits, but the excerpt does not provide detailed task-level numeric scores.

## Link
- [http://arxiv.org/abs/2604.12220v1](http://arxiv.org/abs/2604.12220v1)
