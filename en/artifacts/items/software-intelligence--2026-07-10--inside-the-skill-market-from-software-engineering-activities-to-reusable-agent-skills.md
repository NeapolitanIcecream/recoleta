---
source: arxiv
url: https://arxiv.org/abs/2607.09065v1
published_at: '2026-07-10T03:21:16'
authors:
- Jialun Cao
- Xinru Yan
- Songqiang Chen
- Yaojie Lu
- Zhongxin Liu
- Shing-Chi Cheung
topics:
- agent-skills
- software-engineering
- skill-marketplaces
- software-lifecycle
- artifact-reuse
- empirical-study
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Inside the Skill Market: From Software Engineering Activities to Reusable Agent Skills

## Summary
This paper studies 11,497 software-engineering agent skills collected from four public marketplaces and repositories. It shows that reusable skills mainly cover coding, testing, and code review, while requirements, release, and deployment activities remain underrepresented.

## Problem
- Agent skill markets are growing, but there is no systematic account of which software-engineering activities they package for reuse.
- This gap makes it difficult to assess lifecycle coverage, compare skills across marketplaces, recommend skills, or judge whether a skill can transfer across projects.
- The problem matters because skills package instructions, workflows, tools, documentation, and executable assets that agents may reuse during software production.

## Approach
- The authors crawl ClawHub, SkillHub, SkillNet, and SkillsMP, collecting 775,790 entries before deduplication and filtering.
- They deduplicate by marketplace identifiers and repository URLs, apply rule-based and GPT-5.5 relevance filters, remove unavailable repositories, and produce a final dataset of 11,497 SE-related skills.
- They analyze skill length, structure, source marketplace, update history, versioning, evaluation practices, and lifecycle coverage.
- They map each skill to one of eight lifecycle stages using Qwen3.6-35B-A3B: Requirement, Plan & Design, Implementation, Code Review, Testing, Release, Deployment, and Maintenance & Operations.
- They classify skill assets into instructions, documentation, scripts, agent workflows, libraries, and applications to measure how much engineering functionality is packaged beyond natural-language guidance.

## Results
- Implementation contains 2,875 skills (25.0%), Testing contains 2,446 (21.3%), and Code Review contains 2,198 (19.1%); together they account for 65.4% of the dataset.
- Requirement has 255 skills (2.2%), Release has 363 (3.2%), and Deployment has 609 (5.3%), showing weak coverage of several lifecycle stages.
- SkillsMP contributes 5,322 skills (46.3%), while only 722 skills (6.3%) overlap across marketplaces.
- The average SKILL.md length is 2,078 tokens; 90% contain no more than 4,150 tokens and the longest contains 37,499 tokens.
- Instruction-only skills account for 63.8% of the dataset. Only 13.6% contain code-level executable assets, including scripts (10.5%), libraries (2.0%), and applications (1.1%).
- The paper reports no task-performance benchmark or accuracy comparison against a baseline. Its main evidence is the scale and analysis of the collected corpus, including 2,042 skill updates in January 2026 and structural coverage rates such as Frontmatter at 97.8%, Commands at 79.3%, and Verification at 73.7%.

## Link
- [https://arxiv.org/abs/2607.09065v1](https://arxiv.org/abs/2607.09065v1)
