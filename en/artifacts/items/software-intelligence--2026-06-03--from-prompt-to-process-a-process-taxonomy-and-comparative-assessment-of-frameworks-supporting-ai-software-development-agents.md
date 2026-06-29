---
source: arxiv
url: https://arxiv.org/abs/2606.04967v1
published_at: '2026-06-03T14:49:15'
authors:
- Sanderson Oliveira de Macedo
topics:
- ai-software-development
- coding-agents
- multi-agent-software-engineering
- spec-driven-development
- process-taxonomy
- human-ai-interaction
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# From Prompt to Process: a Process Taxonomy and Comparative Assessment of Frameworks Supporting AI Software Development Agents

## Summary
This paper proposes a six-dimension taxonomy for comparing process frameworks that run on top of AI coding agents. It finds that current frameworks add traceability through artifacts, roles, and review, but none covers specification, context, roles, execution, validation, and portability well at the same time.

## Problem
- AI coding agents can plan, edit files, run commands, and iterate, but raw agent sessions can lose context, hide decisions, and make review hard.
- Existing surveys classify agents, LLM tasks, or agent internals; product guides compare tools by installation and features. They do not compare support frameworks as software engineering processes.
- The gap matters because teams need a way to judge whether an AI development workflow preserves specifications, context, validation evidence, and portability across agents.

## Approach
- The paper defines a support framework as a structured set of artifacts, commands, roles, templates, workflows, or policies used by a developer who already works with an AI coding agent.
- It uses a directed qualitative search over formal papers, official documentation, repositories, community lists, and public tool comparisons.
- Inclusion requires process support, use over an existing coding agent, exclusion of agents or closed IDEs themselves, and exclusion of general agent-building SDKs.
- A traction filter keeps candidates with at least 1,000 GitHub stars and at least one push in the previous 6 months, measured through the GitHub API on May 26-28, 2026.
- The core method is a scoring rubric over 6 process dimensions: specification, context, roles, execution, validation, and portability.

## Results
- The final set contains 6 frameworks: GitHub Spec Kit, GSD, OpenSpec, BMAD Method, Spec Kitty, and Reversa.
- Reported traction at selection time was: GitHub Spec Kit 106,786 stars, GSD 63,754, OpenSpec 51,404, BMAD Method 48,209, Spec Kitty 1,273, and Reversa 1,100.
- The taxonomy is applied to the 6 selected frameworks and to 1 out-of-sample case, Spec-Flow, which had 85 stars and was excluded for low traction.
- The paper claims a main comparative finding: no framework strongly covers all 6 dimensions.
- It identifies a trade-off between process depth and portability across agents: frameworks with richer artifacts and control tend to depend more on specific conventions, tools, or platforms.
- The paper reports no independent quantitative performance benchmark for complete development processes. Its strongest concrete claims are the 6-dimension taxonomy, the auditable selection filter, the comparison of 6 high-traction frameworks, and the risk map covering specification-code drift, over-trust in generated artifacts, fragile community extensions, platform dependence, and missing benchmarks.

## Link
- [https://arxiv.org/abs/2606.04967v1](https://arxiv.org/abs/2606.04967v1)
