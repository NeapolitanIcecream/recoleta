---
source: hn
url: https://onedev.io/blogs/ai-teammates
published_at: '2026-07-12T23:44:18'
authors:
- timplant
topics:
- coding-agents
- software-engineering
- pull-request-automation
- ci-cd
- multi-agent-workflows
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# OneDev AI: Coding Agents as Teammates in Issues, Pull Requests, and CI

## Summary
OneDev AI embeds coding agents in issues, workspaces, pull requests, and CI/CD so they can implement, review, and revise software within the team's existing workflow. The article claims this connected workflow improves traceability, control, and automation, but it provides no measured evaluation.

## Problem
- External coding-agent chats separate requirements, implementation, review, and delivery, making context and accountability harder to maintain.
- Teams need a durable specification, controlled execution environment, and repeatable checks so agents can work on software without ad hoc instructions.
- The problem matters because AI-generated changes still require review, CI/CD validation, and a clear record of why the change was made.

## Approach
- Use issues as the source of truth, including requirements, acceptance criteria, attachments, comments, and design context.
- Let an AI user create an isolated workspace, inspect the repository, make changes on an issue branch, and open a linked pull request.
- Connect pull-request review to the issue, allowing the agent to leave line comments, respond to requested changes, and revise code after CI/CD failures.
- Apply project rules to route issues to agents, require agent reviews, and permit automatic merging when required reviews and CI/CD checks pass.

## Results
- No quantitative results, benchmark scores, datasets, or baseline comparisons are provided in the article.
- The strongest concrete claim is end-to-end integration across issues, Git repositories, workspaces, pull requests, reviews, packages, code search, and CI/CD.
- Agents can implement assigned issues, open pull requests, review changes, respond to feedback, and continue work after failed builds.
- Controlled workspaces and permission rules provide isolated execution and limit where agents can operate.
- Linked issues preserve the original requirement and discussion throughout implementation and acceptance.

## Link
- [https://onedev.io/blogs/ai-teammates](https://onedev.io/blogs/ai-teammates)
