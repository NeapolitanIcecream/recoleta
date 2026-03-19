---
source: hn
url: https://news.ycombinator.com/item?id=47381988
published_at: '2026-03-14T22:30:45'
authors:
- trapani
topics:
- skill-management
- developer-tools
- team-collaboration
- knowledge-organization
relevance_score: 0.51
run_id: materialize-outputs
language_code: en
---

# Show HN: The best way to manage your skills – Better-Skills

## Summary
This is a project introduction for a "skill management" tool, advocating a simpler, shareable, and composable way to organize and use skills. Its focus is to make it easier for people and "harnesses" to create, edit, connect, and reuse skills within teams.

## Problem
- Existing skill management is "terrible," making it difficult to conveniently manage, share, and maintain skills.
- Skills often have dependencies and relationships, but traditional approaches are not good at expressing and maintaining these connections.
- In team collaboration, there is a lack of a unified and easy-to-use mechanism for creating, editing, linking, and reusing skills, which affects scalability and efficiency.

## Approach
- Treat "skills" as the core abstraction, emphasizing that skills should be easy to manage and share.
- Explicitly acknowledge that skills should be able to reference one another, organizing related skills together rather than relying on more complex higher-level skill graph abstractions.
- Let "harnesses" handle creating, editing, and linking skills while following best practices.
- Also let "harnesses" directly consume and use skills, thereby simplifying the system interface and workflow.
- Another design goal is to make team-wide skill collaboration and management easier to implement.

## Results
- The text does not provide any quantitative experimental results, benchmarks, or public evaluation data.
- The strongest concrete claim is that the author says they "achieved" the following goals: skills are easy to manage and share, skills can reference one another, harnesses can create/edit/link skills, harnesses directly use skills, and team management is easier.
- Two verifiable artifacts are provided: the project website `better-skills.dev` and the open-source repository `github.com/leonardotrapani/better-skills`.
- Because there are no metrics, datasets, comparison baselines, or user studies, it is not possible to confirm the extent of any performance improvement over existing solutions.

## Link
- [https://news.ycombinator.com/item?id=47381988](https://news.ycombinator.com/item?id=47381988)
