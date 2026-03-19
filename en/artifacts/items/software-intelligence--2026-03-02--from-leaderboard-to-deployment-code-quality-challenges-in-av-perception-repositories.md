---
source: arxiv
url: http://arxiv.org/abs/2603.02194v1
published_at: '2026-03-02T18:54:28'
authors:
- Mateus Karvat
- Bram Adams
- Sidney Givigi
topics:
- code-quality
- autonomous-vehicles
- static-analysis
- software-security
- production-readiness
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# From Leaderboard to Deployment: Code Quality Challenges in AV Perception Repositories

## Summary
This paper examines the software quality gap that AV perception model repositories face when moving from “leaderboard-topping scores” to “deployable systems.” The authors conducted a large-scale static analysis of 178 repositories from the KITTI and NuScenes leaderboards and found that most code falls far short of production requirements in terms of errors, security, and maintainability.

## Problem
- The paper addresses the question: **do AV perception repositories with high leaderboard accuracy actually have the capacity for production deployment and long-term maintenance**; this matters because autonomous driving is a safety-critical system, and code defects can directly affect real-world road safety and compliance.
- Existing evaluations focus almost exclusively on detection accuracy and do not measure engineering quality such as code errors, security vulnerabilities, CI/CD, and maintainability, creating a clear disconnect between research code and industrial deployment.
- Previously, there had been a lack of **large-scale, systematic** empirical software quality analysis targeting public AV perception research repositories.

## Approach
- The authors collected and cleaned repositories from the KITTI and NuScenes 3D object detection leaderboards, ultimately obtaining **178 unique repositories**, with sizes ranging from **600 to 184.9k SLOC**.
- They used three types of static analysis tools for evaluation: **Pylint** for code errors, **Bandit** for security vulnerabilities, and **Radon** for SLOC and the maintainability metric **MI**.
- They defined “production-ready” in a simple way as: **0 critical errors + 0 high-severity security vulnerabilities**, and used this to determine whether each repository met the standard.
- They further analyzed correlations among code size, number of errors, number of vulnerabilities, MI, GitHub metrics, team size, and adoption of testing and **CI/CD**.
- They distilled prevention guidelines for the 5 most common types of security issues, focusing on patterns such as **unsafe torch.load, silent exception suppression, shell injection, eval, unsafe yaml load**.

## Results
- The **production readiness rate is only 7.3% (13/178)**; according to the conclusion section’s wording, **only 2.8%** of repositories are completely error-free and **6.7%** are completely free of security vulnerabilities, showing a clear disconnect between leaderboard performance and deployment readiness.
- **97.2%** of repositories have at least one error; the median number of errors is **29**, the mean is **55.7**, and the range is **0–1,263**. Pylint identified **1,612** total errors, of which **1,424** were critical errors, and **90.4%** of repositories had at least one critical error.
- **93.3%** of repositories have at least one security issue; the median number of vulnerabilities is **9**, with a range of **0–62**. Bandit found **2,031** security issues, including **403 high-severity (19.8%)**, **1,180 medium-severity (58.1%)**, and **448 low-severity (23.1%)**; **51.7%** of repositories contain high-severity vulnerabilities.
- Security issues are highly concentrated: the top **5** issue types account for **79.3%** of all vulnerabilities. The most common is **B614 unsafe PyTorch load: 713 occurrences, affecting 144 repositories (80.9%)**; this is followed by **B110 try-except-pass: 273 occurrences (38.8%)**, **B605 shell injection: 239 occurrences (44.4%)**, **B307 eval: 222 occurrences (59.6%)**, and **B602 shell=True: 163 occurrences (15.7%)**.
- The larger the repository, the more issues it has: **the number of errors and SLOC have Spearman ρ=0.453, p=0.0000**; **the number of security issues and SLOC have ρ=0.607, p=0.0000**. The higher the maintainability, the lower the density of security issues: **MI and security issue density have ρ=-0.547, p=0.0000**; error density is also negatively correlated: **ρ=-0.397, p<0.001**.
- **CI/CD is adopted by only 7.3% of repositories**, but adopters have higher average maintainability: **MI 73.0 vs 65.9**, **Mann-Whitney U=429, p=0.0003, r=0.600**. At the same time, GitHub stars show **no significant correlation** with the number of errors (**ρ=0.04, p=0.56**), indicating that “popularity” does not equal “deployability.”

## Link
- [http://arxiv.org/abs/2603.02194v1](http://arxiv.org/abs/2603.02194v1)
