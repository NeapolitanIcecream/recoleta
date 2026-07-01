---
source: arxiv
url: https://arxiv.org/abs/2606.31206v1
published_at: '2026-06-30T06:38:56'
authors:
- Xutian Li
- Yifeng Zhu
- Xianlin Zhao
- Yanzhen Zou
- Lu Zhang
- Bing Xie
topics:
- software-evolution
- code-intelligence
- repository-level-editing
- llm-agents
- human-ai-interaction
- automated-software-production
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# FeatX: Editing Software by Editing Features for Repository-Level Code Evolution

## Summary
FeatX lets developers change an existing Java repository by editing a feature list, then maps those feature edits to code patches. It reports lower user workload and better function-level localization than ChatGPT, Cursor Agent, and direct LLM baselines on 38 feature-editing commits.

## Problem
- Repository-level feature changes often span several files and functions, so developers must connect product intent to code locations before making edits.
- Chat and autocomplete tools leave much of the repository context selection to the user, which raises workload in unfamiliar codebases.
- The paper cites prior work that about 60% of repository maintenance tasks involve feature evolution, making this a common software maintenance case.

## Approach
- FeatX extracts a two-level epic-feature hierarchy from a repository and links each feature to classes, methods, or files.
- It builds feature groups by combining static dependency signals with semantic similarity from LLM summaries and Sentence-BERT embeddings, then clusters them with the Leiden algorithm.
- A three-stage Evolution Agent expands context, localizes changed feature intent to code regions, and generates class-wise line-level diffs.
- The UI has Feature, CodeMap, Agent, and Diff panels so users edit features, inspect mapped code, review the agent plan, and confirm patches.

## Results
- In a 10-person study, mean NASA-TLX workload dropped from 12.5 with ChatGPT to 7.4 with FeatX, a 41% reduction.
- SUS usability rose from 73 with ChatGPT to 84 with FeatX, a 15% increase; confidence improved with p<0.001.
- On 38 feature-editing commits across five Java repositories, FeatX reached 41.6% precision, 35.8% recall, and 0.385 F1 for function-level modification localization.
- Claude-opus-4.5 was the strongest direct LLM baseline with 50.7% precision, 18.4% recall, and 0.270 F1; FeatX reports a 42.6% relative F1 gain over it.
- FeatX cost $0.07 total in the replay study, compared with $45.05 for direct Claude-opus-4.5 and $1.28 for GPT-4o-mini.

## Link
- [https://arxiv.org/abs/2606.31206v1](https://arxiv.org/abs/2606.31206v1)
