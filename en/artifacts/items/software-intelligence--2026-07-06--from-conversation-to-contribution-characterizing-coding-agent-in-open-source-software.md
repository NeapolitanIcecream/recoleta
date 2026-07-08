---
source: arxiv
url: https://arxiv.org/abs/2607.05677v1
published_at: '2026-07-06T22:44:45'
authors:
- Zihan Fang
- Yueke Zhang
- Ningzhi Tang
- Collin McMillan
- Toby Jia-Jun Li
- Yu Huang
topics:
- ai-coding-agents
- open-source-software
- code-intelligence
- human-ai-interaction
- repository-mining
- software-engineering-agents
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# From Conversation to Contribution: Characterizing Coding Agent in Open-Source Software

## Summary
This paper studies how AI coding-agent chat logs connect to later open-source development activity. It links 13,360 chat sessions with GitHub histories and a developer survey, then reports adoption patterns, repository changes, and maintainability concerns.

## Problem
- AI coding assistants now support multi-turn code edits, terminal use, and project-aware changes, but most OSS studies only measure commits, pull requests, or static signals.
- OSS maintainers need to know how chat-based AI use affects contribution flow, review load, code maintenance, and trust.
- The missing link is the path from developer-AI conversations to later repository activity.

## Approach
- The authors collected 13,360 AI chat sessions with 79,172 user messages from 1,356 GitHub repositories using SpecStory chat logs for tools such as Cursor, GitHub Copilot, and Claude Code.
- After filtering inaccessible and trivial repositories, they analyzed 1,240 repositories, 12,108 retained AI-chat sessions, 657,971 commits, 9,510 pull requests, 12,747 issues, and 120,489 CI/check records.
- They classified chat purpose into seven labels, including Code Writing, Failure Reporting, Inquiry, Validation, and Workflow Control; the GPT-5 classifier had macro-F1 0.83 against a human-labeled set.
- They aligned each repository around its first observed AI chat and used before/after comparisons, interrupted time-series models, Wilcoxon tests, regressions, and concentration metrics such as HHI.
- They surveyed developers linked to the repositories: 589 delivered invitations produced 25 responses, a 4.2% response rate.

## Results
- AI use was heavier in smaller, less mature, and less collaborative repositories. The final dataset covered 1,240 repositories created between April 2013 and March 2026, with common primary languages TypeScript 25.8%, Python 22.8%, and JavaScript 12.9%.
- Code Writing was the main chat purpose: it accounted for 34.7% of sessions and was the dominant purpose in 53.9% of repositories.
- After AI adoption, projects tended to have more active contributors and lower contributor concentration, with reported significance p < .001; communication stayed concentrated among fewer participants.
- The paper reports no broad deterioration in observable code-quality signals or pull-request merge rates after adoption, based on bug/fix activity, test-touching commits, CI outcomes, issues, and pull requests.
- Developers saw other people’s AI-generated code as harder to maintain than their own, with p = .029, and viewed AI as making OSS contribution easier.
- Most surveyed developers, 68%, were willing to share chat histories, while concerns included appearing incompetent, adding reviewer burden, and exposing ideas to competitors.

## Link
- [https://arxiv.org/abs/2607.05677v1](https://arxiv.org/abs/2607.05677v1)
