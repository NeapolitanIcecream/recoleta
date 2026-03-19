---
source: hn
url: https://blog.unratified.org/2026-03-03-in-defense-of-the-open-web/
published_at: '2026-03-03T23:45:51'
authors:
- 9wzYQbTYsAIc
topics:
- agentic-ai
- open-web
- web-verification
- knowledge-grounding
- machine-readable-protocols
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Why the Open Web Matters: A Claude Code Agent's Case for Open Infrastructure

## Summary
This article argues that the open web is the infrastructure for trustworthy agentic AI, because agents depend on publicly accessible authoritative web pages to discover information, verify facts, and correct errors. Using the construction of a human-rights-themed website as a case study, the author argues that once public information is closed off behind authentication walls, API keys, or rate limits, the quality of agent outputs will decline systematically.

## Problem
- The problem the article addresses is: **how agentic AI can obtain external knowledge that is verifiable, correctable, and discoverable**, rather than relying only on training data to generate content that appears authoritative but may drift.
- This matters because as AI is used for research, policy analysis, summarization, and recommendation generation, if public authoritative information is no longer open, **both humans and agents will lose reliable sources for factual calibration**.
- The author further points to a risk: closing the open web in response to agent traffic may instead lead to **worse AI content quality**, while pushing humans back to the same original web pages for manual verification.

## Approach
- The core mechanism is simple: let agents, like human researchers, directly access authoritative sources on the open web (such as OHCHR, Congress.gov, Senate.gov, and treaty texts) and compare content item by item, rather than trusting parametric memory.
- The author uses the construction of unratified.org as a case study: the site contains **49 terms**, of which **19 terms** were checked against external authoritative sources in the most recent development cycle across **4 dimensions**: factual accuracy, scope alignment, completeness, and whether any reinterpretation appeared intentional.
- Beyond verification, the article also emphasizes the “discovery layer”: through open protocols such as **/.well-known/agent-inbox.json, glossary.json, taxonomy.json, and RSS**, agents can traverse a site’s capabilities and semantic structure without authentication, API keys, or custom integrations.
- The author proposes two inferential hypotheses to explain system-level consequences: **H3 Jevons Explosion** (agents cause explosive growth in demand for web resources) and **H6 Quality Erosion** (if access is closed due to traffic, agent grounding is weakened, reducing average output quality).

## Results
- Of the **49 terms**, the author reports that **19 terms** have completed external verification; the result was **0 critical factual errors**, but **5 corrections** were identified and applied.
- One specific correction concerns the U.S. treaty ratification threshold: the original text described it as a **67-vote supermajority**, and after verification it was changed to the constitutional standard of **“two thirds of the Senators present”**; the author notes that if only **51 senators are present**, then **34 votes** would satisfy the threshold.
- Another correction concerns the wording of ICESCR Article 15: the original text described the right as **“guarantees”**, and after checking the treaty text it was changed to **“recognizes”**, because the two have different legal meanings.
- Regarding the definition of ESCR, the author says that after checking the OHCHR page, they corrected the Cold War-style dichotomy that treated economic, social, and cultural rights simply as “positive rights,” and added the previously omitted dimension of **“cultural rights.”**
- The article **does not provide experimental comparison metrics against alternative systems, closed-web settings, or benchmark models**, nor does it test the counterfactual of whether these 5 corrections would necessarily have been impossible if the web pages had been closed; the strongest specific claim is that, in this case, **every accuracy-improving correction depended on openly accessible authoritative sources, and the author says “without exception.”**
- In terms of research contribution, the most “novel” point is not a quantitative SOTA result, but the proposal and case-based argument that **the open web is a prerequisite infrastructure for trustworthy agentic AI**, rather than an optional distribution channel.

## Link
- [https://blog.unratified.org/2026-03-03-in-defense-of-the-open-web/](https://blog.unratified.org/2026-03-03-in-defense-of-the-open-web/)
