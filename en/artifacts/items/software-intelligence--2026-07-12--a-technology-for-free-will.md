---
source: hn
url: https://ziyzhu.com/a-technology-for-free-will
published_at: '2026-07-12T22:28:06'
authors:
- ziyzhu
topics:
- local-agents
- personal-ai
- user-data-sovereignty
- agentic-proxy
- permissionless-access
- human-ai-interaction
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# A Technology for Free Will

## Summary
The essay proposes Mango, a mobile-first local AI agent that acts across websites using the user's existing access while keeping the device, data, and model under the user's control. It aims to reduce platform steering, preserve portable user memory, and make agent safety enforceable in client software.

## Problem
- Web services keep useful data and actions behind fragmented interfaces, logins, and limited APIs, forcing users and developers to follow platform-designed workflows.
- Cloud agents can centralize private context, model choice, and control, which may let providers shape the user's options and actions.
- This matters because an agent that mediates access to personal data and online services can affect user autonomy as well as convenience.

## Approach
- Run the agent locally on the user's phone or computer and let it use the user's existing browser or service access instead of waiting for platform APIs or MCP integrations.
- Store chats, memories, actions, and settings as portable plain-text files in a user-controlled folder, so another application or model can use the same data.
- Keep the model replaceable, allowing users to switch providers without moving their history or granting one provider permanent control.
- Add a deterministic client-side safety layer intended to prevent data leaks and unauthorized actions unless the user explicitly permits them.
- Present a single intent-driven interface that can read and act across several platforms while reducing ads, pop-ups, trackers, and recommendation surfaces.

## Results
- The Matcha Tennis example reportedly reduced court-booking time from about 2 minutes to 5 seconds and reached more than 1,000 users in Seattle.
- The author's Slack MCP server at Amazon became one of the company's most-used MCP servers within weeks and reached thousands of employees.
- A unified CLI for internal websites is reported to run about once per second on average and lets builders add integrations without waiting for each service owner.
- The essay provides no controlled benchmark, security audit, dataset evaluation, or comparison against existing agent systems for the proposed Mango design.
- The main claimed result is a product architecture: local execution, file-based memory, model portability, permissionless interface access, and client-enforced safety are presented as conditions for user-controlled personal AI.

## Link
- [https://ziyzhu.com/a-technology-for-free-will](https://ziyzhu.com/a-technology-for-free-will)
