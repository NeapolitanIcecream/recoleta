---
source: arxiv
url: https://arxiv.org/abs/2607.05666v1
published_at: '2026-07-06T22:15:54'
authors:
- Illia Dovhoshliubnyi
- Nima Soroush
- Ashkan Sami
- Alexander Brownlee
topics:
- ai-coding-agents
- code-intelligence
- software-performance
- genetic-improvement
- mutation-taxonomy
- llm-as-judge
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# What Do AI Agents Actually Change? An Empirical Taxonomy of Mutation Patterns in Performance-Improving Pull Requests

## Summary
The paper maps what AI coding agents change in performance-related pull requests by classifying code diff hunks into mutation categories. Its main claim is that agent identity and optimization target can help choose a smaller set of mutation operators for search-based software engineering.

## Problem
- AI coding agents submit production pull requests, but their internal decision process is hard to inspect; the observable signal is the code they change.
- Search-based software engineering and genetic improvement need mutation operators that match real code transformations, especially for performance optimization.
- Performance PRs are rare in AIDev-pop: 324 of 33,596 agent PRs carry a performance label, which is under 1%.

## Approach
- The authors use AIDev-pop pull requests from Devin, GitHub Copilot, Cursor, OpenAI Codex, and Claude Code across 100 starred repositories.
- They reduce 324 performance-labeled PRs to 280 retrievable diffs, 269 source-code PRs, and 216 PRs with accepted performance-relevant hunks.
- They classify 1,254 performance-relevant diff hunks with the 18-category syntactic mutation taxonomy from Even-Mendoza et al. (2025).
- Two LLM judges, claude-sonnet-4-6 and gpt-5.4, classify each hunk; full agreement keeps the label, partial agreement keeps the category intersection, and full disagreement is discarded.
- In simple terms, the method treats each code change as evidence, labels the kind of edit it made, then compares label patterns by agent and optimization strategy.

## Results
- The top mutation categories are name_modification at 37.0% of 1,254 hunks, object_creation at 26.4%, type_change at 22.7%, control_flow at 20.9%, and statement_splitting at 18.5%.
- Prior genetic-improvement data had no_change at 84% of patches; this corpus reports no_change at 0.0%, so agent performance PRs have a different mutation profile.
- name_modification and type_change co-occur with lift 3.07 in Apriori mining.
- Performance strategy explains part of the pattern: 253 of 284 type_change labels, or 89%, occur in Data Structure changes; 345 of 463 name_modification labels, or 75%, occur in Build & Infrastructure changes.
- Agent profiles differ: Devin has 361 name_modification labels out of 670 total category assignments, Copilot has 224 type_change labels out of 591, Codex has 136 control_flow labels out of 574, and Cursor has 41 comment_modification labels out of 184.
- The authors claim that conditioning on target strategy and agent can reduce the mutation-operator space from 18 categories to roughly 5 in a genetic-improvement loop.

## Link
- [https://arxiv.org/abs/2607.05666v1](https://arxiv.org/abs/2607.05666v1)
