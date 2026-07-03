---
source: arxiv
url: https://arxiv.org/abs/2607.01456v1
published_at: '2026-07-01T20:21:33'
authors:
- David Boram Hong
- Aaron Imani
- Iftekhar Ahmed
topics:
- agent-skills
- skill-smells
- llm-agents
- software-quality
- code-intelligence
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# From Anatomy to Smells: An Empirical Study of SKILL.md in Agent Skills

## Summary
The paper studies SKILL.md files used by Agent Skills and finds that authoring problems are widespread. It defines a taxonomy of SKILL.md content, extracts authoring practices, and builds a detector for violations called skill smells.

## Problem
- Agent Skills give LLM agents task-specific instructions through SKILL.md files, but the Markdown body is largely unconstrained, so poor guidance can waste context and steer agent behavior poorly.
- Existing work studied skill effectiveness, security, and optimization, while SKILL.md authoring quality and authoring practice violations had little empirical evidence.
- The problem matters because public skill marketplaces already contain more than 100,000 skills, and bad SKILL.md patterns may spread through copied skills, generated skills, or future training data.

## Approach
- The authors curated 238 English SKILL.md files from a skills.sh dump of 133,149 skills across 8,808 publishers and 13,460 repositories, after filtering by downloads, repository stars, deduplication, and repository diversity.
- Two authors qualitatively coded SKILL.md bodies at the H2 heading level and built a taxonomy of semantic components.
- They reviewed 29 web sources through a multivocal literature review, extracted SKILL.md authoring best practices, and inverted violations into 26 skill smells.
- They built Skill Smell Detector, using scripts for 5 statically detectable smells and Qwen3.6-27B with 4-bit AWQ quantization for 21 semantic smells.
- They mined 1,295 commit records, then analyzed 142 changing SKILL.md files across 1,199 commits and 35 weekly time windows to measure smell persistence.

## Results
- The taxonomy contains 13 higher-level and 44 lower-level semantic components in SKILL.md bodies.
- Common higher-level components include Task at 74.4%, Introduction at 63.5%, References at 57.1%, Principles at 42.0%, Usecase at 32.8%, and Context at 28.2% of the 238-file sample.
- Frequent lower-level components include Steps Instruction at 49.2%, Rules at 39.1%, Prerequisites at 31.1%, Reference Files at 31.1%, Subtask Instruction at 24.0%, Skill Trigger at 23.1%, and Return Artifact at 21.9%.
- The best-practice review produced 26 skill smells, split into 5 static smells and 21 semantic smells.
- More than 99% of SKILL.md files contained at least one skill smell, according to the paper.
- The longitudinal analysis found that once skill smells appeared, they rarely disappeared; the excerpt does not provide precision, recall, or F1 values for the detector.

## Link
- [https://arxiv.org/abs/2607.01456v1](https://arxiv.org/abs/2607.01456v1)
