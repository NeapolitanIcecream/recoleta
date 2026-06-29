---
source: hn
url: https://news.ycombinator.com/item?id=48522482
published_at: '2026-06-13T23:21:20'
authors:
- yells_jovially
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- human-ai-interaction
relevance_score: 0.71
run_id: materialize-outputs
language_code: en
---

# Atlassian "Data Contribution"

## Summary
The text argues that Atlassian’s “Data Contribution” policy lets Rovo train on customer content and raises privacy and IP concerns, especially for smaller organizations. It says Jira and Confluence data are unusually valuable because they combine company knowledge, work history, and recent operational detail.

## Problem
- Atlassian plans to use customer data to train Rovo, which raises privacy and intellectual property concerns.
- The rollout is uneven: smaller customers can opt out of data contribution only with manual steps, while Enterprise customers get a full opt-out.
- The text says Jira and Confluence contain high-value organizational knowledge, so the data exposure matters more than a normal SaaS telemetry policy.

## Approach
- It separates Atlassian’s collection into “Metadata” and “Data” and argues that the company’s “Metadata” bucket includes more than classical metadata.
- It points to examples such as story points, dates, SLAs, similarity scores, and readability scores as part of the data Atlassian can use.
- It explains why Jira and Confluence together create a strong training set: one holds plans, tasks, and execution history, while the other holds documentation and internal knowledge.
- It frames the policy as a one-way transfer where smaller organizations contribute process knowledge and IP to improve Atlassian’s AI products.

## Results
- No quantitative experimental results are provided in the excerpt.
- The concrete claim is that Atlassian has data from over 300k organizations and will use customer data to train Rovo unless customers opt out.
- The text says full opt-out is available only to Enterprise customers; for other customers, data opt-out is manual and metadata contribution remains on.
- It claims Atlassian’s metadata definition includes numeric fields and computed features, so the default contribution covers more than simple system logs.
- The main conclusion is a policy critique, not a measured technical result: the rollout creates privacy and IP risk and favors large enterprises over smaller customers.

## Link
- [https://news.ycombinator.com/item?id=48522482](https://news.ycombinator.com/item?id=48522482)
