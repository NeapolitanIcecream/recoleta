---
source: arxiv
url: http://arxiv.org/abs/2603.02194v1
published_at: '2026-03-02T18:54:28'
authors:
- Mateus Karvat
- Bram Adams
- Sidney Givigi
topics:
- autonomous-driving
- code-quality
- software-security
- static-analysis
- production-readiness
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# From Leaderboard to Deployment: Code Quality Challenges in AV Perception Repositories

## Summary
This paper examines the gap in autonomous driving perception repositories between achieving “high leaderboard scores” and being “deployable,” pointing out that academic code often has high accuracy but poor engineering quality. The authors conducted a large-scale static analysis of 178 public repositories from the KITTI and NuScenes leaderboards and found that very few repositories are truly close to production usability.

## Problem
- The problem the paper addresses is: **autonomous driving perception models are usually evaluated only by benchmark performance, while lacking systematic assessment of code errors, security vulnerabilities, maintainability, and deployment readiness**, which hinders their entry into safety-critical real vehicle systems.
- This matters because AV perception is **safety-critical software** and must satisfy standards such as ISO 26262 and SOTIF; if research code contains serious errors or vulnerabilities, deployment could lead to missed obstacle detection, incorrect classification, or runtime failure.
- Leaderboard rankings cannot reflect whether code is suitable for production, so high-performing research models often still need to be **rewritten from scratch** before deployment.

## Approach
- The authors collected repositories from the **KITTI and NuScenes 3D detection leaderboards** and, after deduplication and filtering, obtained **178 unique codebases**, with sizes ranging from about **600 to 184.9k SLOC**.
- They used three static analysis tools for evaluation: **Pylint** to check code errors and critical errors, **Bandit** to check security vulnerabilities and high-severity issues, and **Radon** to compute code size and the **Maintainability Index (MI)**.
- They defined the most basic standard for “**production-ready**” as: **zero critical errors + zero high-severity security vulnerabilities**, and used this to measure how far research repositories are from deployment.
- They further analyzed the relationships between **repository size, team characteristics, GitHub metrics, CI/CD usage**, and quality metrics, and distilled prevention guidelines for the most common security issues.
- The core mechanism is simple: **instead of looking only at model accuracy, evaluate these perception repositories like engineering software, using static analysis to batch-check whether they are safe, stable, and maintainable.**

## Results
- The central conclusion: **only 7.3% (13/178) of repositories meet the production-readiness standard**; in other words, **92.7%** of repositories fail on at least one of “critical errors or high-severity vulnerabilities.”
- **97.2%** of repositories have at least one Pylint error; only **5/178** are error-free. The median number of errors is **29**, the mean is **55.7**, and the range is **0–1,263**. In total, **1,612** errors were found, of which **1,424** were critical errors, and **90.4%** of repositories had at least one critical error.
- **93.3%** of repositories have at least one security vulnerability; only **12** repositories have zero vulnerabilities. The median number of security issues is **9**, with a range of **0–62**. A total of **2,031** vulnerabilities were found, including **403 high-severity (19.8%)**, **1,180 medium-severity (58.1%)**, and **448 low-severity (23.1%)**; high-severity issues affect **51.7%** of repositories.
- Security issues are highly concentrated: **the top 5 issue categories account for 79.3%** of all vulnerabilities. The most common issues include **B614 unsafe PyTorch loading 713 times, affecting 144 repositories (80.9%)**; **B110 try/except/pass 273 times (38.8%)**; **B605 shell injection 239 times (44.4%)**; **B307 eval injection 222 times (59.6%)**; **B602 shell=True 163 times (15.7%)**.
- The larger the repository, the more issues it has: **error count and repository size Spearman ρ=0.453, p=0.0000**; **security issue count and repository size ρ=0.607, p=0.0000**. Meanwhile, the higher the maintainability, the lower the security issue density: **MI and security issue density ρ=-0.547, p=0.0000**; it is also negatively correlated with error density: **ρ=-0.397, p<0.001**.
- **CI/CD adoption is only 7.3%**, but repositories using CI/CD have higher maintainability: **average MI 73.0 vs 65.9**, **Mann-Whitney U=429, p=0.0003, r=0.600**. Based on this, the paper argues that leaderboard performance is decoupled from production readiness, while introducing basic engineering practices and targeted security fixes can significantly narrow this gap.

## Link
- [http://arxiv.org/abs/2603.02194v1](http://arxiv.org/abs/2603.02194v1)
