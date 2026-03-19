---
source: arxiv
url: http://arxiv.org/abs/2603.03085v1
published_at: '2026-03-03T15:28:50'
authors:
- Marion Wiese
- Kamila Serwa
- Eva Bittner
topics:
- technical-debt
- software-process
- action-research
- backlog-management
- engineering-practice
relevance_score: 0.45
run_id: materialize-outputs
language_code: en
---

# A Practical Guide for Establishing a Technical Debt Management Process (Preprint)

## Summary
This paper proposes a practical guide for establishing Technical Debt Management (TDM), distilled from a replicated action research study across 3 teams, summarizing common practices, typical challenges, and practical recommendations. Its value lies in turning scattered technical debt research methods into a process template that teams can adopt directly.

## Problem
- Software teams often adopt solutions that are beneficial in the short term but hinder long-term evolution, i.e., technical debt; without systematic management, the cost of future changes, risk, and maintenance burden continue to accumulate.
- Although there is extensive research on technical debt management, practical transfer remains insufficient, and there is a lack of a reusable, cross-company “standard-style” setup process and best practices.
- Teams especially struggle to answer: **which TDM methods should be adopted, how to implement them, what common obstacles will arise, and whether the process actually improves technical debt awareness.**

## Approach
- The authors replicated their previously proposed **5-step workshop method** and conducted **action research** in 3 teams, allowing the teams to select and trial TDM practices suited to them from existing research approaches.
- The study covered **15 workshops + 4 retrospectives**, while also observing team meetings over the long term to record how they identified, documented, prioritized, repaid, and prevented technical debt.
- To compare transferable practices, the authors analyzed the **commonalities and differences** in the final approaches adopted by each team, extracting starting-point “best practices” accepted by all teams.
- To evaluate changes in awareness, the authors combined **systematic observation, questionnaires, and TD-SAGAT interrupted awareness measurement** to check whether teams considered factors such as alternatives, benefits, drawbacks, risks, interest, affected components, and quality attributes during decision-making.
- Final outputs included a **white-paper-style guide** for practitioners and tool-support recommendations for defect tracking/issue system vendors.

## Results
- Scale of data: covering **3 teams, 20 participants, 108 meetings, 96 hours of observation, and a net research period of 30 months**; in total, **1132 discussion topics** were analyzed, and **240 TD-SAGAT data points** were collected in **28 meetings**.
- All teams adopted several shared practices: **establishing a TD champion/manager**, **adding a TD item type to the existing backlog**, recording similar attributes (such as **interest, contagiousness, resubmission date, and reminders to discuss drawbacks and risks**), and using these practices as the starting point for TDM best practices.
- The authors claim that the core practices that appeared consistently across teams include: **(1) a TD owner; (2) TD documentation attributes with specific values; (3) debiasing decisions using “alternatives + drawbacks + risks”; (4) prioritizing TD mainly against other TD rather than directly against feature requirements; (5) using a resubmission date for review.**
- There were also differences across teams: **prioritization methods and repayment approaches were not uniform**, indicating that these parts depend more on specific team contexts and are difficult to standardize into a single process.
- Common challenges included the need for **more concrete operational support**, a **simple method to identify TD from the backlog**, **guidance on how to start the process**, **external reminders in the early stage to sustain the process**, and help for teams to **articulate the consequences of TD**.
- Regarding effectiveness, the paper’s strongest quantitative conclusions are relatively limited; it explicitly claims that **overall TD awareness improves only when relevant attributes are added to issue types and ongoing reminders are established**. The excerpt does not provide more detailed unified effect sizes or significance comparisons with baselines/control groups.

## Link
- [http://arxiv.org/abs/2603.03085v1](http://arxiv.org/abs/2603.03085v1)
