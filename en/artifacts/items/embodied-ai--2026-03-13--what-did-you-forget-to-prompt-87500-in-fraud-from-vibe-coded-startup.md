---
source: hn
url: https://qualitymax.io/vibe-check
published_at: '2026-03-13T23:58:41'
authors:
- qualitymax
topics:
- application-security
- ai-code-generation
- vibe-coding
- security-testing
- owasp
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# What Did You Forget to Prompt? $87,500 in Fraud from Vibe-Coded Startup

## Summary
This article is not an academic paper, but a case study and product marketing piece centered on security failures in “vibe-coded” startup applications. Its core argument is that AI coding driven only by prompts overlooks system security design, leading to real financial losses, data breaches, and costly rebuilds.

## Problem
- The problem the article addresses is that when founders use AI to quickly generate and launch products, they often treat prototypes as production systems, skipping security audits, architecture reviews, and basic protections, which results in vulnerabilities such as exposed frontend keys, missing authentication, XSS, and CSRF.
- This matters because the consequences are direct financial losses and compliance risks: examples in the article include **$87,500 in fraudulent transactions**, **$2,500 in Stripe fee losses**, **175 customers incorrectly charged $500 each**, and a forced shutdown after a medical data breach.
- The article emphasizes that AI can write “working code,” but it does not proactively think about the attack surface; if developers do not explicitly ask for security, the system may go live with fatal vulnerabilities.

## Approach
- The core method is simple: use an AI crawler called **QualityMax** to browse the application like an attacker, automatically scanning pages, API endpoints, and JavaScript bundles to look for exposed keys, missing authentication, missing security headers, and OWASP Top 10 vulnerabilities.
- The tool not only reports issues, but also provides severity levels, remediation guidance, and OWASP references, with the goal of enabling non-security experts to locate and fix problems.
- It also automatically generates **Playwright** security test scripts, turning these checks into repeatable tests that can run in CI/CD, so each deployment can be checked for reintroduced vulnerabilities.
- The article demonstrates this mechanism using a “simulated vulnerable fintech SaaS”: it recreates the common types of vulnerabilities seen in real vibe-coded startups after they were breached, then verifies whether the scanner and tests can detect all of them.

## Results
- The most prominent real-case figure in the article is that after a founder placed a **Stripe secret key** in the frontend, an attacker copied the key directly from the source code, resulting in **175 customers each being charged $500**, for a total of about **$87,500 in fraudulent transactions**; the founder said he absorbed **$2,500** in fees before rotating the key.
- For cleanup costs, the article gives experiential figures suggesting that fixing security debt often requires **4–8 months of re-architecture**, along with **$200K+** in rebuild costs, plus customer churn that is difficult to recover from.
- In its demo application, the author claims to have reproduced **24 vulnerabilities** in total, with scan results of **6 CRITICAL / 8 HIGH / 5 MEDIUM / 3 LOW**, covering exposed keys, an open admin backend, leaked APIs, XSS, and missing CSRF protections.
- The generated Playwright tests reportedly reached **25 tests, 25 failures**, meaning “every vulnerability was caught”; the article lists failed items including a Stripe key, a Supabase service role key, an OpenAI key, an unauthenticated admin panel, and missing CSP.
- The article also provides several anecdotal examples: finding exposed Stripe keys in **3** ProductHunt launches; someone built an MVP in 2 days but spent **3 months** cleaning up security debt; all of these are used to support the argument that “vibe coding” is systematically creating production security problems.
- However, it is important to note that the text does not provide a formal experimental design, public benchmarks, comparison methods, or peer-reviewed results, so these findings are better understood as case-based evidence and product claims rather than a rigorous academic evaluation.

## Link
- [https://qualitymax.io/vibe-check](https://qualitymax.io/vibe-check)
