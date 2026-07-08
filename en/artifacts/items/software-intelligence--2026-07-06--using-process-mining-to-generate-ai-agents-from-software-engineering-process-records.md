---
source: arxiv
url: https://arxiv.org/abs/2607.04948v1
published_at: '2026-07-06T11:22:25'
authors:
- Saimir Bala
- Fabiana Fournier
- Lior Limonad
- Andreas Metzger
topics:
- multi-agent-software-engineering
- process-mining
- software-agents
- repository-mining
- langgraph
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Using Process Mining to Generate AI Agents from Software Engineering Process Records

## Summary
pm4aa generates project-specific software engineering agents from repository process records. It mines GitHub event logs to derive roles, constraints, and LangGraph agent implementations instead of starting from fixed agent roles.

## Problem
- The paper addresses how to define AI agent roles for hybrid software engineering teams without making one large agent or many small agents with high coordination cost.
- Existing multi-agent software engineering systems often use fixed roles such as programmer, reviewer, and tester, so they miss project-specific work patterns.
- This matters because teams expect agents to follow their repository workflow, issue lifecycle, and contribution rules.

## Approach
- The pipeline extracts an Object-Centric Event Log from a GitHub repository using PyStack’t, with users, issues, commits, and later tasks as object types.
- It parses Conventional Commit messages to map commits to software engineering task classes such as feature development, defect resolution, documentation, and quality assurance.
- It assigns each contributor to one role using a rule-based profile built from activity distribution, commit count, and task-class distribution.
- It splits the log by role, then mines OC-DFGs, BPMN models, and DECLARE constraints to capture role scope, work sequences, object interactions, and behavioral guardrails.
- It uses GPT-4-mini for role process descriptions and IBM BOB to generate a LangGraph application with role-specific agent nodes, shared state, prompts, and routing logic.

## Results
- On the Commitizen repository, the raw log covered about 8 years of history, from November 2017 to November 2025, with 21,488 events and 4,813 objects.
- The dataset included 1,459 issues, 2,765 commits, and 589 user accounts; after task enrichment it contained 6,534 objects across commits, tasks, issues, and users.
- The commit parser matched 1,721 of 2,765 commits, or 62.2%, and created 1,721 task objects from Conventional Commit messages.
- The role classifier assigned 589 users to 8 roles: 425 issue_reporters, 66 contributors, 37 quality_engineers, 23 technical_writers, 20 feature_developers, 8 maintainers, 6 bots, and 4 devops_engineers.
- Role event volumes were uneven: issue_reporter had 16,037 events, bot had 3,394, maintainer had 2,149, and devops_engineer had 15, so some generated role specifications are exploratory.
- The proof of concept generated an issue-centric LangGraph application with 5 role-specific agents and was evaluated with functional tests plus a 10-participant exploratory user study, but the excerpt does not provide test pass rates, user-study scores, or benchmark comparisons.

## Link
- [https://arxiv.org/abs/2607.04948v1](https://arxiv.org/abs/2607.04948v1)
