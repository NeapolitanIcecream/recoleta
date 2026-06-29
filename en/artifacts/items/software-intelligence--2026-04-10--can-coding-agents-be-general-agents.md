---
source: arxiv
url: http://arxiv.org/abs/2604.13107v1
published_at: '2026-04-10T22:39:51'
authors:
- Maksim Ivanov
- Abhijay Rana
- Gokul Prabhakaran
topics:
- coding-agents
- business-process-automation
- enterprise-resource-planning
- agent-evaluation
- code-execution
- human-ai-interaction
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Can Coding Agents Be General Agents?

## Summary
This paper tests whether coding agents can handle general business workflows, not just software tasks. In an Odoo ERP case study, the agents handled simple tasks well but broke down on harder workflows where business rules had to stay aligned with code execution.

## Problem
- Current benchmarks split the problem in two: software benchmarks like SWE-Bench and Terminal-Bench test code and system skills, while tool-use and policy benchmarks like BFCL and $\tau$-bench simplify the execution layer.
- Real business automation needs both sides at once: understand business requests and policies, inspect live system state, decide what should happen, and then change the software state correctly.
- The paper asks whether coding agents can do this end to end in a realistic ERP, because users are already applying them to business work beyond software engineering.

## Approach
- The authors define generalization for coding agents as bidirectional translation between the business layer and the code layer: read the business goal, inspect the system with code, plan a business action, then write the changes back into the system.
- They build a case-study environment in **Odoo 19.0 Community Edition**, populated with realistic company data across sales, inventory, manufacturing, purchasing, and HR.
- Tasks are natural-language business workflows with explicit constraints and policy rules. Each scenario requires at least **2 interdependent decisions** and at least **2 interacting constraints**; harder scenarios require **5+ decisions** and **5+ constraints**.
- The agent gets only a **bash tool**, database credentials, a workspace, and examples of five Odoo data models. It must map the ERP and write scripts on its own. They test **GPT-5** and **Claude Sonnet 4.5** at maximum reasoning settings.
- Evaluation checks the final PostgreSQL state against ground-truth rubrics on **constraint resolution, resource optimization, traceability, and policy adherence**.

## Results
- On the first trial of **10 easy scenarios**, the Claude Sonnet 4.5 coding agent scored **above 80%** on the verifiers and reliably completed tasks such as creating sales orders, selecting the cheapest vendor, and generating invoices.
- The study evaluates **20 scenarios** across a difficulty range from **Easy to Hardest**. Performance drops as the number of constraints increases.
- The paper reports a qualitative model split: **GPT-5** often produced business plans comparable to or better than Claude Sonnet 4.5, but it made more incorrect API calls, which lowered its overall scores.
- For more complex scenarios, agents moved from feasible but suboptimal plans to outright failure on constraint satisfaction, with traceability also degrading as workflows became more involved.
- The paper identifies four recurring failure modes: **lazy code heuristics** for policy implementation, **business-layer hallucinations**, **ignored policy constraints**, and **overconfidence** where successful code execution is mistaken for correct business outcomes.
- The excerpt does not provide a full numeric score table by model and difficulty, so the strongest quantitative claims are **>80% on 10 easy scenarios** and a tested set of **20 scenarios** with clear degradation on harder tasks.

## Link
- [http://arxiv.org/abs/2604.13107v1](http://arxiv.org/abs/2604.13107v1)
