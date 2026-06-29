---
source: arxiv
url: http://arxiv.org/abs/2604.13108v1
published_at: '2026-04-11T00:26:31'
authors:
- Ruoqi Jin
topics:
- ai-coding-agents
- software-architecture
- code-navigation
- code-intelligence
- context-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Formal Architecture Descriptors as Navigation Primitives for AI Coding Agents

## Summary
Formal architecture descriptors help AI coding agents find the right code with fewer exploration steps. The paper argues that the main gain comes from giving agents explicit architectural structure, while the exact file format matters less for model comprehension.

## Problem
- AI coding agents waste many tool calls on codebase exploration such as grep, file search, and module reading before they can edit code.
- Existing context files like `CLAUDE.md` or `AGENTS.md` are informal, while automated repo maps capture syntax but often miss design intent, constraints, and data flow.
- This matters because extra navigation raises cost and can hurt task success, especially on larger codebases where blind search is harder.

## Approach
- The paper introduces **intent.lisp**, a formal architecture descriptor written as nested S-expressions that records pillars, components, symbols, constraints, and data flows.
- A survey tool scans a repository and uses an LLM to draft the descriptor; coding agents then read that descriptor as a navigation entry point during tasks.
- The authors run three studies: a controlled code-localization experiment across context formats, an artifact-vs-process test using auto-generated descriptors with no human refinement, and an observational field study over 7,012 Claude Code sessions.
- They also test writer-side reliability by asking an LLM to generate descriptors in S-expression, JSON, YAML, and Markdown, then injecting structural errors to compare parse failure and silent corruption.
- The paper’s format claim is narrow: S-expressions are not easier for the model to understand, but they are shorter, enforce hierarchy by syntax, and degrade better than YAML or Markdown when generation errors occur.

## Results
- In 24 code-localization tasks on a 22K-line Rust project with Claude Sonnet 4.6, architecture context cut average navigation steps from **5.2 blind** to **3.4 with S-expression**, **3.4 with JSON**, and **2.9 with Markdown**, a **33–44% reduction**; blind vs context was significant with **Wilcoxon p=0.009** for S-expr and effect size **d=0.92**.
- Accuracy in that same experiment changed less than steps: **54% (13/24) blind**, **58% (14/24) S-expression**, **58% (14/24) JSON**, **63% (15/24) Markdown**. A separate 20-question comprehension test found **95% accuracy in all four formats**, and pairwise format differences were not significant.
- In the artifact-vs-process study on 15 tasks in a 43K-line Rust project, an **auto-generated 170-line descriptor** reached **100% accuracy** versus **80% blind** with **p=0.002** and **d=1.04**, showing that the descriptor file itself can help even without developer cleanup or code restructuring.
- In that same study, the **curated 698-line descriptor** got **87% accuracy** and **2.9 steps** versus **3.9** for AutoGen and **5.6** blind; AutoGen beat Curated on accuracy, though the AutoGen-Curated difference was **not significant (p=0.515)**.
- In 96 generation runs, parse-valid output rates were **100% for JSON**, **95.8% for S-expressions**, and **91.7% for YAML**. In 96 error injections, **silent corruption** was **21% for JSON**, **50% for S-expressions**, **50% for YAML**, and **100% for Markdown**; S-expressions detected **100% of structural completeness errors**, while YAML detected only **50%** of that error type.
- Across **7,012 Claude Code sessions** and **484,937 messages**, introducing formal descriptors correlated with a drop in the IQR of explore/edit ratios from **2.24 to 1.08**, a **52% reduction in behavioral variance**. The field study is correlational, and the paper notes that larger codebases and non-localization tasks still need direct testing.

## Link
- [http://arxiv.org/abs/2604.13108v1](http://arxiv.org/abs/2604.13108v1)
