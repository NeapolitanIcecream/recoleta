---
source: hn
url: https://www.wisdom.ai/blog/how-wisdom-gets-text-to-sql-right
published_at: '2026-06-22T23:48:57'
authors:
- sharva
topics:
- text-to-sql
- context-learning
- data-agents
- enterprise-analytics
- llm-evaluation
relevance_score: 0.67
run_id: materialize-outputs
language_code: en
---

# What it takes to get high Text-to-SQL accuracy in production

## Summary
WisdomAI claims high production Text-to-SQL accuracy depends on continuously managed business context, not only model choice. Its Adaptive Context Engine builds context from schemas, samples, logs, documents, feedback, and admin review, then updates it as definitions and data use change.

## Problem
- Enterprise Text-to-SQL fails when business terms, schema names, metric definitions, and team-specific rules drift after setup.
- Fixed context can make the same question return different numbers over time, which damages trust in analytics workflows.
- Public benchmarks such as BIRD-SQL can miss this issue because some questions include needed context in the prompt and some reference SQL has errors.

## Approach
- ACE bootstraps context from database schema, crawled data samples, warehouse query logs, dbt, LookML, wikis, knowledge bases, MCP sources, SaaS apps, and web pages.
- Each extracted context fragment gets a confidence score, so admins can auto-accept high-confidence items and review edge cases.
- User feedback drives learning: clear feedback is stored directly, while ambiguous feedback triggers offline generation and testing of multiple candidate SQL queries.
- New context is checked against existing context before storage to detect conflicts such as two definitions of “revenue” or two column mappings for the same filter.
- Evaluation uses three phases: baseline with schema and sampling, after bootstrap with knowledge files, and after learning with one-shot feedback based on execution output while hiding ground-truth SQL.

## Results
- On 5 filtered query-only datasets from livesqlbench-base-full-v1, reported aggregate accuracy rises from 20% baseline to 50% after adding knowledge-base files, then to 85% after context learning, with no model changes, SQL tuning, or manual context building.
- WisdomAI reports 80–92% accuracy on the BIRD dev set with the context learning loop active, while saying BIRD is a poor fit for enterprise context learning.
- The post states that the current top performer on the LiveSQLBench leaderboard is at 48% accuracy across all case types, while WisdomAI reports 85% on its filtered query-only setup.
- Human review of suggested context and reviewed queries is reported to push production accuracy above 95%.
- In one solar_panel example, learning fixed “latest” row selection: the baseline returned 352 rows, while the correct answer had 336 rows using composite-key ordering on snapts and snapkey.
- In another solar_panel example, learning fixed hidden maintenance-cost logic: the baseline returned $4,850, while the correct answer was $1,541 after applying expected failures over two years with a positive MTBF record.

## Link
- [https://www.wisdom.ai/blog/how-wisdom-gets-text-to-sql-right](https://www.wisdom.ai/blog/how-wisdom-gets-text-to-sql-right)
