---
source: hn
url: https://vinibrasil.com/my-coworker-iris-isnt-a-person/
published_at: '2026-06-28T22:30:26'
authors:
- vnbrs
topics:
- ai-coding-agent
- slack-agent
- code-intelligence
- human-ai-interaction
- developer-workflow
relevance_score: 0.79
run_id: materialize-outputs
language_code: en
---

# My coworker Iris isn't a person

## Summary
The article describes Iris, a Slack-based AI agent at CrewAI that handles small engineering tasks such as opening code PRs. Its main claim is practical: agents can reduce context switching for low-risk work, even when they are not reliable enough for complex engineering tasks.

## Problem
- Small software fixes can carry high workflow cost: the example fix needed 2 lines of logic but would have required 9 manual steps.
- Context switching matters because acknowledging a small task can create an open mental loop that interrupts ongoing work.
- For larger engineering work, autonomous agents can shift effort into review and supervision rather than saving time.

## Approach
- CrewAI provisioned Iris as an internal Slack agent built on CrewAI and connected to company tools.
- Engineers tag `@Iris` in Slack with a task request, such as asking for a whitespace trim fix.
- Iris can start crews, file Linear issues, run Claude Code, open GitHub PRs, and send emails.
- In the example, Iris found the correct handler, added trimming logic, added a newline test, and posted a PR link back in the Slack thread.

## Results
- The example task closed in about 3 minutes after the engineer tagged Iris.
- The task avoided a 9-step manual workflow for a 2-line logic change.
- Iris added a test for the newline case, so the PR covered the reported failure mode.
- The article gives no benchmark, dataset, controlled comparison, success rate, or production reliability metric.
- The strongest claim is that agent delegation helps with small, well-scoped engineering tasks by reducing context switching; it does not claim that Iris handles complex software work well.

## Link
- [https://vinibrasil.com/my-coworker-iris-isnt-a-person/](https://vinibrasil.com/my-coworker-iris-isnt-a-person/)
