---
source: hn
url: https://qualitymax.io/vibe-check
published_at: '2026-03-13T23:58:41'
authors:
- qualitymax
topics:
- application-security
- ai-generated-code
- vibe-coding
- security-testing
- playwright
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# What Did You Forget to Prompt? $87,500 in Fraud from Vibe-Coded Startup

## Summary
This article uses a public case to show that putting AI-generated prototype code directly into production without a security audit can quickly turn into real fraud and data exposure risk. The core claim is that automated security crawling plus generative testing can scan and block common vulnerabilities in "vibe-coded" applications before launch, like an attacker would.

## Problem
- The problem the article aims to solve is that founders use generative programming tools to quickly build and launch products, but often miss the most basic security design and auditing steps, allowing vulnerabilities such as exposed keys, missing authentication, XSS, and CSRF to go straight into production.
- This matters because the issue is not sophisticated attacks, but rather "low-barrier, high-loss" mistakes like plaintext keys in the frontend, open admin panels, and unauthenticated APIs, which can directly cause fraudulent charges, PII leaks, compliance incidents, and long-term rebuild costs.
- The article emphasizes that AI answers "the questions you ask," but does not automatically perform system-level security architecture thinking; therefore, prompt-driven development alone can easily mistake a runnable prototype for a product that is safe to operate.

## Approach
- The core method is simple: let QualityMax automatically crawl websites, APIs, and frontend JS bundles like an attacker would, looking for exposed keys, broken authentication, missing security headers, and OWASP Top 10 vulnerabilities.
- After finding issues, the system does not just provide a report; it also outputs vulnerability severity levels, remediation guidance, and corresponding OWASP references to help developers fix issues quickly.
- It can also automatically generate Playwright security test scripts and put these checks into CI/CD so that the same risks are re-validated on every deployment.
- By recreating patterns from real breached "vibe-coded" startup applications, the article shows how the tool can detect these common but fatal misconfigurations and implementation flaws before launch.

## Results
- The case in the article claims that a founder placed a **Stripe secret key** in the frontend, which an attacker copied directly from DevTools and abused, resulting in **175 customers each being charged $500**, while the founder reported losses of **$2,500 in Stripe fees**.
- The article also gives a broader description of losses: similar incidents can lead to **$200K+** in rebuild costs and **4–8 months** of system re-architecture; however, these are anecdotal claims rather than controlled experimental results.
- In its recreated demo application, the author claims there were **24 vulnerabilities**, with scan results of **6 CRITICAL, 8 HIGH, 5 MEDIUM, 3 LOW**, covering issues such as exposed keys, open admin panels, unauthenticated endpoints, XSS, and missing CSRF protection.
- For automated testing, the article gives an expected result of **25 tests, 25 failures**, and claims this means "every vulnerability caught"; however, note that this is a vendor-built demo and self-reported result, without an independent benchmark or third-party evaluation.
- The article also claims that an open admin panel could return **340 user records**, including names, email addresses, phone numbers, addresses, and partial SSNs, with **zero authentication required**, to illustrate the severity of the risk.
- It does not provide the standard datasets, comparison baselines, or statistical significance commonly seen in academic papers; the strongest evidence is multiple public incident cases plus a reproducible experimental demo environment.

## Link
- [https://qualitymax.io/vibe-check](https://qualitymax.io/vibe-check)
