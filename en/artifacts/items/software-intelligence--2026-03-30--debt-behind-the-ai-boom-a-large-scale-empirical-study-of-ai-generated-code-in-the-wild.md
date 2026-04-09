---
source: arxiv
url: http://arxiv.org/abs/2603.28592v1
published_at: '2026-03-30T15:38:05'
authors:
- Yue Liu
- Ratnadira Widyasari
- Yanjie Zhao
- Ivana Clairine Irsan
- David Lo
topics:
- ai-generated-code
- technical-debt
- code-quality
- static-analysis
- software-maintenance
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild

## Summary
This paper measures how much technical debt AI coding assistants add to real GitHub repositories after their code lands in production. The main finding is that AI-authored commits often introduce static-analysis issues, and a sizable share of those issues remain in the repository later.

## Problem
- Prior work showed quality and security problems in AI-generated code under controlled experiments, but it did not show what happens after that code is merged into real repositories.
- Teams need to know whether AI-added bugs, security issues, and maintainability problems are fixed quickly or stay in the codebase as technical debt.
- This matters because AI code is already common in production development, and persistent low-quality code raises future maintenance and review cost.

## Approach
- The authors build a large dataset of **304,362 verified AI-authored commits** from **6,275 GitHub repositories**, covering five major assistants: GitHub Copilot, Claude, Cursor, Gemini, and Devin.
- They identify AI-authored commits using explicit Git metadata such as bot accounts, author emails, author names, and co-author trailers, rather than a classifier or indirect proxy.
- For each AI-authored commit, they run static analysis on the code **before and after** the commit to attribute issues introduced or fixed by that specific change.
- The analysis uses Pylint and Bandit for Python, plus ESLint and njsscan for JavaScript and TypeScript, and tracks code smells, runtime bugs, and security issues.
- They then follow each introduced issue forward to the latest repository revision to see whether it still survives.

## Results
- The study finds **484,606 distinct AI-introduced issues** across **3,841 repositories** and **26,564 commits**. That means **61.2%** of studied repositories and **8.7%** of AI-authored commits had at least one introduced issue.
- **Code smells dominate** the issue mix: **431,850 issues (89.1%)**. The rest are **28,149 runtime bugs (5.8%)** and **24,607 security issues (5.1%)**.
- The paper states that **more than 15% of commits from every AI coding assistant** introduce at least one issue, though the excerpt does not provide the per-tool percentages.
- The most common code-smell rules include **broad exception handling (41,723; 8.6%)**, **unused variables or parameters (28,718; 5.9%)**, and **unused argument (24,444; 5.0%)**.
- The most common runtime bug is **undefined variable or reference: 23,091 issues (4.8%)**. Common security findings include **subprocess without shell check: 4,334 (0.9%)** and **try-except-pass: 4,040 (0.8%)**.
- On long-term persistence, **24.2% of tracked AI-introduced issues survive to the latest repository revision**, which supports the paper's claim that AI-generated code can create lasting maintenance cost in real projects.

## Link
- [http://arxiv.org/abs/2603.28592v1](http://arxiv.org/abs/2603.28592v1)
