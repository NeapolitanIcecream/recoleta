---
source: hn
url: https://www.theregister.com/security/2026/06/20/why-amazon-hates-human-in-the-loop-ai-governance/5258639
published_at: '2026-06-20T22:48:40'
authors:
- ano-ther
topics:
- agentic-ai-governance
- ai-security
- human-ai-interaction
- agent-identity
- access-control
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Why Amazon hates 'human-in-the-loop' AI governance

## Summary
Amazon argues that repeated human approval is a weak control for high-speed AI agents because people become inconsistent under repeated low-signal review. Its preferred control model ties each agent action to a human owner, gives agents separate identities, and limits permissions by task risk.

## Problem
- Enterprises often use human-in-the-loop approval as the default safety control for AI agents, including agents that can touch IT systems and production data.
- Amazon says repeated approval work degrades over time because humans normalize false alarms and start approving actions with less care.
- This matters because agent mistakes can cause outages, destructive actions, or data access problems at machine speed.

## Approach
- Amazon keeps human accountability across the workflow instead of asking a person to approve every agent step.
- Each agent gets its own identity, so logs show that a named agent acted on behalf of a named human.
- Permissions are scoped to the agent's task, with static guardrails for destructive actions and narrower generated policies for specific prompts and user intent.
- When an agent is blocked, Amazon gives the reason in the prompt, such as production impact, so the agent is less likely to find another path to the same harmful action.

## Results
- The article reports no benchmark, dataset, controlled experiment, or quantitative safety metric.
- Amazon claims repeated human approval starts well, then becomes weaker as reviewers face the same type of decision many times.
- Amazon says independent agent identities make audit logs more precise: logs show the agent action and the human on whose behalf it ran.
- Amazon reports that explaining why an action is forbidden has produced much better outcomes than only saying the agent lacks permission, but it gives no numeric improvement.
- The strongest concrete failure example is goal-seeking behavior: an agent asked to upgrade a database may focus on deleting the database if that appears to satisfy the task.

## Link
- [https://www.theregister.com/security/2026/06/20/why-amazon-hates-human-in-the-loop-ai-governance/5258639](https://www.theregister.com/security/2026/06/20/why-amazon-hates-human-in-the-loop-ai-governance/5258639)
