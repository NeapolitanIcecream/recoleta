---
source: hn
url: https://blog.unratified.org/2026-03-03-in-defense-of-the-open-web/
published_at: '2026-03-03T23:45:51'
authors:
- 9wzYQbTYsAIc
topics:
- open-web
- agentic-verification
- web-infrastructure
- information-access
- research-agents
relevance_score: 0.23
run_id: materialize-outputs
language_code: en
---

# Why the Open Web Matters: A Claude Code Agent's Case for Open Infrastructure

## Summary
This is a case-based argument about the importance of open web infrastructure for “verifiable agentic research,” rather than a traditional experimental paper. Using a human rights/legal analysis site built by an agent, the author argues that open, crawlable, authentication-free public information sources are a key prerequisite for improving the credibility of agent outputs.

## Problem
- The article addresses the question: **if the open web is replaced by authentication walls, API barriers, rate limits, and closed protocols, can agents still reliably retrieve, verify, and correct facts?** This matters because more and more people will rely on agent-generated research, policy summaries, and analysis.
- The author argues that relying only on model training data leads to **fact drift and undiscoverable errors**; without real-time, authoritative, open external sources, agents will generate content that appears authoritative but lacks grounding.
- The article also raises a broader risk: tightening access in response to agent traffic may actually reduce agent output quality, ultimately harming the human users who depend on those outputs.

## Approach
- The core method is simple: the author uses a real project as a case study to show how an agent, like a human researcher, can directly access authoritative sources on the open web (such as OHCHR, Congress.gov, Senate.gov, etc.) to **verify content item by item**.
- In a glossary containing **49 terms across 8 categories**, the author selected **19 terms** and externally validated them along four dimensions: **factual accuracy, scope alignment, completeness, and whether any intentional reinterpretation was present**.
- The author reports several concrete correction cases: for example, changing “67 votes” to “two thirds of the Senators present,” changing “guarantees” to the more accurate “recognizes” in ICESCR, and correcting the oversimplified “positive/negative rights” dichotomy in the ESCR definition.
- Beyond verification, the article also emphasizes the “discovery layer”: through open protocols such as **RSS, JSON-LD, SKOS, `/.well-known/`**, agents can discover and combine resources without OAuth, API keys, or per-vendor negotiation.
- The mechanistic claim is: **open web = the agent’s external memory and verification layer; closed web = higher friction, less verification, and more ungrounded output.**

## Results
- After externally validating **19/49** terms, the author reports: **0 critical factual errors, with 5 corrections applied**; all of these corrections came from verification against open authoritative sources.
- Specific corrections include revising the U.S. treaty ratification threshold from a generic **67 votes** to the constitutional requirement of **“two thirds of the Senators present”**; with the minimum quorum of **51 senators** present, **34 votes** are sufficient.
- Another correction concerns the wording of ICESCR Article 15(1)(b): changing “**guarantees**” to “**recognizes**,” with the author emphasizing that the two have different legal meanings.
- In terms of terminology system scale, the project contains **49 terms across 8 categories**; only **19 terms** were validated in this round, indicating that the evidence is still a limited-scale case study rather than a large-scale controlled experiment.
- The article does not provide traditional machine learning benchmark results such as **accuracy/F1, dataset leaderboards, or direct comparisons with closed-source APIs or offline models**; nor does it test whether **a closed-web scenario would necessarily be unable to achieve the same corrections**. The strongest claim is: in this case, **every accuracy-improving correction depended on openly accessible authoritative sources, without exception**.

## Link
- [https://blog.unratified.org/2026-03-03-in-defense-of-the-open-web/](https://blog.unratified.org/2026-03-03-in-defense-of-the-open-web/)
