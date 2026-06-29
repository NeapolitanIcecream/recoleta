---
source: arxiv
url: https://arxiv.org/abs/2606.07448v1
published_at: '2026-06-05T16:51:25'
authors:
- Romain Robbes
- "Th\xE9o Matricon"
- Thomas Degueule
- Andre Hora
- Stefano Zacchiroli
topics:
- coding-agents
- github-mining
- ai-assisted-commits
- software-engineering
- code-intelligence
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Agentic Very Much! Adoption of Coding Agent in New GitHub Projects

## Summary
The paper finds much higher coding-agent adoption in GitHub projects created after the authors’ earlier study: 71.83% conservative adoption in new projects versus 26.46% in older projects.

## Problem
- The paper measures how often new GitHub projects use coding agents, because agent-written or agent-assisted code changes software production, project maintenance, and empirical software engineering data.
- Prior work measured adoption across older repositories; this paper checks whether projects created after 2025-08-29 show different adoption rates and commit patterns.
- The authors also test whether visible traces miss agent use, which matters because unsigned or hidden agent commits can make human-authored activity look larger than it is.

## Approach
- The study samples GitHub repositories with at least 100 commits, 5,000 lines of code, at least 10 stars, no forks, and creation dates after 2025-08-29. The main table reports 12,794 new projects and compares them with 127,670 older projects.
- It uses the same heuristics as the earlier “Agentic Much?” study: agent configuration or guidance files, ignored files such as agent artifacts in `.gitignore`, pull requests authored by known agents, and commits with known agent authors or co-authors.
- It computes file-level adoption, commit-level adoption, a conservative overall adoption estimate, a high estimate, and the share of detected AI-assisted commits among human plus AI-assisted commits.
- It also breaks adoption down by repository size, contributors, commits, issues, pull requests, age, programming language, GitHub topics, organization, tool, and contribution size.

## Results
- Conservative adoption is 71.83% for new projects, with 9,190 of 12,794 projects showing adoption, versus 26.46% for older projects, with 33,783 of 127,670 projects. The high estimate is 76.15% for new projects versus 32.89% for older projects.
- File-level adoption is 60.03% in new projects, with 7,680 of 12,794 projects, versus 14.70% in older projects, with 18,768 of 127,670 projects. Ignored-files-only signals are 11.81% in new projects versus 2.41% in older projects.
- Commit-only adoption without file traces is 29.53% in new projects, with 1,510 of 5,114 projects, versus 13.79% in older projects, with 15,015 of 108,902 projects.
- The detected AI-assisted commit ratio is much higher in new projects: the median is close to 30% versus 10% for older projects, and the upper quartile is around 75% versus around 25%.
- Claude Code is the most detected tool in both datasets. In new projects it appears in 6,443 projects, followed by Generic signals at 3,092, Copilot at 2,177, Codex at 1,231, Cursor at 1,064, and Gemini at 499. In older projects Claude Code appears in 16,897 projects and Copilot in 15,794.
- AI-assisted commits in new projects add more lines than in older projects: median added lines are 42 versus 30, and Q3 is 156 versus 110. Commits classified as human also grow from median 10 added lines in older projects to 29 in new projects, which the authors treat as evidence that some agent activity is undetected.

## Link
- [https://arxiv.org/abs/2606.07448v1](https://arxiv.org/abs/2606.07448v1)
