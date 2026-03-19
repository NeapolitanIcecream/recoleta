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
- software-engineering
- process-guideline
- action-research
- backlog-management
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# A Practical Guide for Establishing a Technical Debt Management Process (Preprint)

## Summary
This paper summarizes, through action research across 3 teams, how to implement a Technical Debt Management (TDM) process in enterprises, and distills a reusable starting point for best practices. Its core value is not in proposing a new algorithm, but in turning fragmented TDM research methods into executable organizational processes and implementation guidelines.

## Problem
- Software teams often adopt technical debt practices that are beneficial in the short term but increase maintenance costs in the long term; without systematic management, subsequent changes become slower, more expensive, and riskier.
- There is already a large body of TDM research, but a unified, transferable implementation guide across companies is lacking, making it difficult for practitioner teams to know where to start, which methods to use, and how to sustain execution.
- The paper also focuses on a key question: after establishing a TDM process, does the team's “awareness” of technical debt actually improve, since this directly affects the quality of day-to-day decisions.

## Approach
- It uses an **action research + 5-step workshop** method to replicate and compare the TDM implementation process across 3 teams; teams could independently choose which practices to adopt from candidate approaches presented in the research literature.
- The full study covers **15 workshops + 4 retrospectives**, observing **108 meetings, 96 hours**, over a period of **30 months**; in total, it analyzes **1,132 discussed items** and collects **240 TD-SAGAT awareness measurement data points**.
- Methodologically, it spans multiple TDM activities: technical debt identification, documentation, prioritization, repayment, prevention, and visualization, and compares which practices were accepted across different companies.
- The distilled common mechanism is simple: assign a **TD champion/manager**, add a dedicated TD item type to the existing backlog, record attributes such as **interest, contagiousness, resubmission date**, and require explicit discussion of **alternative solutions, drawbacks, and risks** during decision-making.
- It also uses TD-SAGAT and observation to track changes in “technical debt awareness,” evaluating whether establishing the process truly changes the team's discussion and decision-making habits.

## Results
- The paper claims to identify a cross-team starting point for TDM best practices adopted by all teams: **(1)** establish a TD champion/manager, **(2)** document debt using TD backlog items with specific attributes, **(3)** evaluate alternative solutions and their drawbacks/risks during decision-making, **(4)** prioritize TD mainly against other TD items rather than directly against feature requirements, and **(5)** use **resubmission date** for deferred review.
- The three teams were highly similar in documentation and prevention strategies: all reused their existing backlogs and added a TD issue type; shared attributes included **interest, contagiousness, resubmission date**, and fields reminding teams to discuss drawbacks/risks.
- The main quantitative results in terms of study scale are: covering **3 teams**, a **30-month net study period (43-month gross span)**, **108 meetings / 96 hours**, **1,132 discussed items**, **28 TD-SAGAT interruption measurements**, and **240 responses**, used to support its feasibility conclusions for the proposed process.
- Regarding effectiveness, the strongest concrete conclusion reported by the authors is: **technical debt awareness only increases overall when relevant attributes are added to the issue type and used as ongoing reminders**. However, the excerpt **does not provide clear before/after improvement percentages, statistical significance, or baseline comparison values**.
- The paper also summarizes recurring implementation difficulties across teams: teams needed more concrete operational support, simple backlog identification methods, guidance for starting the process, external reminder mechanisms in the early stage, and support to help members better articulate the consequences of TD.
- The final outputs include not only the research conclusions but also a **white paper/guide** for practitioners, and the paper recommends that issue tracking tool vendors natively support TD issue type and its attributes.

## Link
- [http://arxiv.org/abs/2603.03085v1](http://arxiv.org/abs/2603.03085v1)
