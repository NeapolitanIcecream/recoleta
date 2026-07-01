---
source: hn
url: https://www.serval.com/serval-news/introducing-catalyst-automating-a-task-forever-should-be-easier-than-doing-it-manually-once
published_at: '2026-06-30T23:05:57'
authors:
- emot
topics:
- ai-agents
- it-automation
- workflow-generation
- human-in-the-loop
- code-generation
- enterprise-it
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Catalyst: Automating a task forever should be easier than doing it manually once

## Summary
Catalyst is a Serval product agent that turns a natural-language automation request into a drafted Serval setup, including integrations, permissions, triggers, workflows, skills, and dashboards. The main claim is that IT teams will automate more tasks when creating the automation takes less effort than doing the task once.

## Problem
- IT teams often skip automation because building it can take longer than handling one ticket, such as adding an email alias by hand.
- Serval says Workflow Builder reduced the workflow-writing part, but setup still required separate work across integrations, permissions, triggers, and routing.
- This matters because repeated IT requests create manual load, and unsafe agent changes can affect help desk behavior, access, and third-party systems.

## Approach
- Catalyst uses the same public documentation, user-facing endpoints, and permissions as the person chatting with it, so it can configure the same Serval resources that user can access.
- A file-system-based agent treats Serval resources as editable files: workflows as TypeScript, skills as Markdown, and integrations or policies as JSON-like data.
- The agent runs in a sandbox where it can search docs, execute commands, generate files, and write temporary workflows for reads or proposed changes.
- Catalyst stages proposed changes instead of applying them directly; users review changed resources in tabs and publish approved changes.
- Teams can require a second-person approval flow, and mutating actions against third-party systems require approval before execution.

## Results
- The article gives no benchmark evaluation, accuracy metric, latency metric, or controlled comparison against another automation agent.
- Serval says Workflow Builder ran in production for 1 year before Catalyst and made workflow creation easier than doing some tasks manually once.
- In the alias-request example, Catalyst targets 4 setup steps at once: integration connection, permissions, workflow creation, and skill/routing setup.
- Catalyst Beta stages changes for 3 resource types: Workflows, Skills, and Dashboards.
- The staging design supports second-person approval, where a different team member must approve before publication.
- Serval claims some customer deals closed in under 1 week because Catalyst could build common automations after an intro call.

## Link
- [https://www.serval.com/serval-news/introducing-catalyst-automating-a-task-forever-should-be-easier-than-doing-it-manually-once](https://www.serval.com/serval-news/introducing-catalyst-automating-a-task-forever-should-be-easier-than-doing-it-manually-once)
