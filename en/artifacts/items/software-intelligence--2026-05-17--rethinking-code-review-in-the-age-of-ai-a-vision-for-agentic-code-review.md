---
source: arxiv
url: https://arxiv.org/abs/2605.17548v1
published_at: '2026-05-17T17:04:21'
authors:
- "H\xFCseyin \xD6zg\xFCr Kamal\u0131"
- Erdem Tuna
- Vahid Haratian
- "Eray T\xFCz\xFCn"
topics:
- code-review
- ai-agents
- software-engineering
- human-ai-collaboration
- pull-requests
- llm-code-tools
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Rethinking Code Review in the Age of AI: A Vision for Agentic Code Review

## Summary
The paper argues that AI-assisted coding increases review load, so code review needs an agentic, human-controlled PR workflow rather than isolated automation tools. It proposes a five-stage process for carrying context across PR creation, augmentation, reviewer selection, review, and retrospective.

## Problem
- AI coding assistants can raise code production speed by more than 50%, which increases the amount of code that must pass through PR review.
- Current AI review support is split across narrow tasks such as reviewer recommendation, PR description generation, and comment suggestion, so context is lost between stages.
- Reviewers still face missing rationale, poor reviewer assignment, uneven feedback quality, privacy risks, bias, automation bias, and weak evaluation methods.

## Approach
- The core mechanism is a coordinated PR workflow with specialized agents assigned to different review tasks, while humans keep final control at key quality gates.
- The proposed workflow has five stages: PR Creation, PR Augmentation, Reviewer Selection, AI-Assisted Code Review, and PR Retrospective.
- Agents enrich PRs with rationale, issue links, summaries, risk signals, reviewer suggestions, and review support so later stages reuse earlier context.
- Human reviewers remain responsible for judgment, accountability, team knowledge, and merge decisions.
- The paper also gives a research agenda for reliability, transparency, privacy, bias, evaluation metrics, and human-AI authority boundaries.

## Results
- The paper reports no new benchmark, prototype evaluation, user study, or controlled experiment for the proposed agentic review workflow.
- Its main concrete claim is a five-stage agentic PR process designed to connect tasks that current tools handle separately.
- The motivation cites prior evidence that AI coding assistants accelerate individual coding tasks by more than 50%, while AI-generated contributions require more review iterations than human-written ones.
- The background cites Fagan inspections detecting up to 80% of errors before testing in some cases.
- The background cites Google resolving more than 1,000 issues flagged by FindBugs in review, 75% of GitHub projects mandating peer review for contributions, and over 90% of analyzed GitHub projects using CI services.
- The background cites Microsoft branch studies where long-lived branches delayed integration by nearly 9 additional days on average.

## Link
- [https://arxiv.org/abs/2605.17548v1](https://arxiv.org/abs/2605.17548v1)
