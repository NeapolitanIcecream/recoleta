---
source: arxiv
url: http://arxiv.org/abs/2604.18883v1
published_at: '2026-04-20T22:05:09'
authors:
- Vassilios Exarhakos
- Jinghui Cheng
- Jin L. C. Guo
topics:
- ai-assisted-programming
- code-intelligence
- ide-plugin
- human-ai-interaction
- provenance-tracking
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Choose Your Own Adventure: Non-Linear AI-Assisted Programming with EvoGraph

## Summary
EvoGraph is a VS Code plugin for AI-assisted programming that treats coding history as a branching graph instead of a single chat thread. The paper argues this better matches how developers explore alternatives, revisit prior states, and inspect AI-generated changes.

## Problem
- Current AI coding tools are mostly linear chat interfaces, but programming work often branches, backtracks, and compares alternatives.
- Developers in the authors' preliminary study reported three recurring issues: poor support for exploring multiple solution paths, difficulty tracking long prompt sequences, and weak visibility into which code came from which AI interaction.
- This matters because developers can lose useful intermediate work, struggle to recover context in long sessions, and have a harder time reviewing or trusting AI-generated edits.

## Approach
- The authors built **EvoGraph**, a VS Code extension that records AI interactions and code changes as a development graph with checkpoints.
- The graph stores three checkpoint types: manual checkpoints, AI prompt checkpoints, and AI code-application checkpoints.
- Users can revisit earlier nodes, branch from past states, compare alternatives, merge paths, and inspect code changes together with the prompts that produced them.
- The system includes provenance support so developers can trace code edits back to their originating prompt context, and it can include the existing graph history as context for future AI interactions.
- The design was informed by interviews with **8 developers** and evaluated in a within-subjects study with **20 participants** against a baseline AI-assisted programming interface.

## Results
- The paper reports a preliminary interview study with **8 developers** that identified the main workflow problems EvoGraph targets: exploration history, long interaction management, and authorship/provenance tracking.
- In a user study with **20 participants**, EvoGraph reportedly helped developers explore alternatives, manage prompt interactions, and track AI-generated changes better than a baseline interface.
- Participants also reported **lower cognitive load** with EvoGraph than with the baseline, but the excerpt does **not provide numeric cognitive-load scores, p-values, or effect sizes**.
- The strongest concrete claims in the excerpt are qualitative: participants said the graph supported safer exploration, faster iteration, and better reflection on AI-generated code.
- The excerpt does **not include task completion times, accuracy, acceptance rates, or other quantitative performance metrics** for EvoGraph versus the baseline.

## Link
- [http://arxiv.org/abs/2604.18883v1](http://arxiv.org/abs/2604.18883v1)
