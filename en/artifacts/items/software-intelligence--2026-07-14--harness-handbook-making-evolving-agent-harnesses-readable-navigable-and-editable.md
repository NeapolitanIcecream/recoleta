---
source: arxiv
url: https://arxiv.org/abs/2607.13285v1
published_at: '2026-07-14T21:39:55'
authors:
- Ruhan Wang
- Yucheng Shi
- Zongxia Li
- Zhongzhi Li
- Yue Yu
- Junyao Yang
- Kishan Panaganti
- Haitao Mi
- Dongruo Zhou
- Leoweiliang
topics:
- code-intelligence
- automated-software-production
- agent-harness
- behavior-localization
- repository-understanding
- coding-agents
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Harness Handbook: Making Evolving Agent Harnesses Readable,Navigable, and Editable

## Summary
Harness Handbook represents an agent harness by runtime behavior and links each behavior to source locations. In evaluations on Codex and Terminus-2, handbook-guided planning improved plan quality and localization while reducing planner-token use.

## Problem
- Modification requests describe desired behavior, while production harnesses implement that behavior across distributed files, execution stages, functions, and shared state.
- Humans and coding agents must localize every affected implementation site before planning a safe edit, but existing repository maps, search, indexing, and long-context methods remain organized around code structure rather than behavior.
- Missing or incomplete localization can cause agents to overlook scattered, cross-module, or rarely executed paths, producing incomplete or over-broad edit plans.

## Approach
- Harness Handbook builds a behavior-centric representation with an L1–L3 hierarchy: system overview, component or stage overview, and source-linked implementation details. A complementary state-register view captures cross-stage dependencies.
- A construction pipeline combines deterministic static fact extraction, call-graph analysis, LLM-assisted behavioral organization, and hierarchical synthesis. It supports function-as-leaf and file-as-leaf representations.
- Behavior-Guided Progressive Disclosure (BGPD) navigates from relevant stages to state-linked components and source locations, expands candidates through call relations, and verifies each locator against the current repository.
- After edits, non-empty diffs trigger resynchronization so changed functions or files, program graphs, and handbook entries remain aligned with the repository; uncertain content is frozen or recorded rather than guessed.

## Results
- Across 30 requests for each of two open-source harnesses, Handbook-Assisted planning had higher overall judge win rates than the Baseline: 38.3% versus 28.3% on Codex and 45.6% versus 26.7% on Terminus-2.
- Average planner use decreased from 0.102M to 0.089M tokens per Codex request, a 12.7% reduction, and from 0.058M to 0.053M tokens per Terminus-2 request, an 8.6% reduction.
- Averaged across three judges, win-rate gains for Localization, Scope Control, and Reasoning were 2.2, 1.1, and 3.3 percentage points on Codex, and 12.2, 6.7, and 4.5 points on Terminus-2.
- Against Opus 4.8 reference plans on Codex, handbook guidance raised file-level F1 from 46.6 to 61.8 and symbol-level F1 from 38.3 to 57.1; the corresponding Wrong rates fell from 37.0% to 14.8% and from 44.4% to 18.5%.
- Against GPT-5.5 reference plans on Codex, handbook guidance raised file-level F1 from 47.3 to 52.3 and symbol-level F1 from 43.8 to 51.2; symbol-level Wrong fell from 28.6% to 21.4%.
- The supplied excerpt truncates the remainder of the Terminus-2 localization table, so the full set of reported comparison values is not available here. The paper reports that gains persist across Query, Cross-file, and Search-Hostile requests and across localization difficulty levels.

## Link
- [https://arxiv.org/abs/2607.13285v1](https://arxiv.org/abs/2607.13285v1)
