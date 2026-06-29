---
source: arxiv
url: https://arxiv.org/abs/2606.25257v1
published_at: '2026-06-24T00:32:18'
authors:
- Gianmario Voria
- Alfonso Cannavale
- Andrea De Lucia
- Yutaro Kashiwa
- Gemma Catolino
- Fabio Palomba
topics:
- agent-context-files
- coding-agents
- code-quality
- software-maintenance
- empirical-software-engineering
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# How Do Developers Maintain and Evolve Their Agents' Instructions? An Empirical Study

## Summary
This paper proposes an empirical study of how developers change Agent Context Files such as CLAUDE.md, AGENTS.md, and copilot-instructions.md in repositories that use coding agents. It links instruction-file changes to later agent-generated code quality and to timing patterns across repository history.

## Problem
- Autonomous coding agents need project-specific instructions, but developers lack evidence on how those instruction files change over time.
- Poorly maintained Agent Context Files can reduce control over agent behavior, make intent harder to trace, and affect code quality.
- The study matters for software teams that treat agent instructions as versioned engineering artifacts rather than one-off prompts.

## Approach
- The study mines two datasets: AIDev, with 116,211 repositories and 932,791 pull requests involving agent-generated code, and an ACF dataset with 2,303 context files from 1,925 repositories.
- It reconstructs Agent Context File history at the commit level by comparing before and after versions of files such as CLAUDE.md, AGENTS.md, and copilot-instructions.md.
- It builds a taxonomy of ACF changes through qualitative coding, then maps the categories to software maintenance types such as corrective, preventive, adaptive, perfective, and additive changes.
- It defines development windows between consecutive ACF-modifying commits and measures later agent-generated code in each window using cyclomatic complexity, lines of code, coupling, and Corrective Commit Probability.
- It plans chi-square tests for category distributions, Kruskal-Wallis and Wilcoxon tests for quality differences, Cohen’s kappa for annotation agreement, and Cliff’s Delta for effect sizes.

## Results
- The excerpt reports a study design, so it has no completed empirical results on ACF change distributions, code quality effects, or lifecycle timing.
- Feasibility evidence includes over 10,000 ACF-modifying commits in the source ACF dataset for the taxonomy work.
- A preliminary pipeline produced 10,763 commit snapshots with context files, 18,213 commits with file metadata, and 8,600 commits with intersecting ACF and agent-code information.
- The planned agreement threshold for the qualitative taxonomy is Cohen’s kappa ≥ 0.70 before large-scale labeling.
- Prior input data cited by the paper includes 2,303 ACFs across 1,925 repositories and AIDev’s 116,211 repositories with 932,791 pull requests, but the paper does not yet claim measured quality gains or losses from ACF changes.

## Link
- [https://arxiv.org/abs/2606.25257v1](https://arxiv.org/abs/2606.25257v1)
