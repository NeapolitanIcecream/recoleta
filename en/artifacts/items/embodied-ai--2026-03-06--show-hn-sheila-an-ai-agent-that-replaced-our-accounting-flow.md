---
source: hn
url: https://soapbox.pub/blog/announcing-sheila/
published_at: '2026-03-06T23:08:29'
authors:
- knewter
topics:
- ai-agent
- workflow-automation
- accounting-automation
- human-in-the-loop
- tool-using-agents
relevance_score: 0.07
run_id: materialize-outputs
language_code: en
---

# Show HN: Sheila, an AI agent that replaced our accounting flow

## Summary
Sheila is an AI agent for accounting and payment operations, and the author claims it has replaced Soapbox’s entire accounting flow. The core contribution of the article is not a new model, but a practical pattern for building agents: use fine-grained scripts plus natural-language workflow instructions, and iterate continuously under human supervision.

## Problem
- The article aims to solve the problem that **AI agents struggle to reliably complete end-to-end workflows in real business settings**, especially accounting tasks that span multiple systems, such as invoice processing, payments, bookkeeping, and expense archiving.
- This matters because many existing agent platforms are closer to demo systems; once deployed in production, complex multi-step workflows, edge cases, and external system integrations make agents fragile.
- For small and medium-sized teams, accounting operations are repetitive, tedious, and frequent. If they can be automated reliably, it can significantly save human time and reduce process friction.

## Approach
- The core method is simple: **don’t start by building a complex autonomous system; instead, first build many small scripts that each perform only a single action**, such as checking a balance, initiating a payment, uploading a file, reading email, or writing to a spreadsheet.
- The author tested **50+ scripts** in total, making each script reliable on its own before having the agent chain them together in sequence during task execution.
- Then they wrote an approximately **600-line** `AGENTS.md` that describes the full workflows in natural language; when the user says “process invoices,” the agent reads the instructions and selects the appropriate scripts to execute.
- The system runs in OpenCode and uses a **human-in-the-loop** approach: the agent can draft emails and prepare payments, but a human watches in the terminal and confirms key actions.
- The author emphasizes a bottom-up, iterative development process: test scripts, discover edge cases, revise instructions, retest end-to-end, and stabilize the workflow through hundreds of feedback cycles.

## Results
- The strongest practical result claim is that Sheila has “**replaced our entire accounting flow**,” covering the full workflow for **contractor invoices, fiat payments (ACH/wire via Mercury), Bitcoin payments (Kraken/Lightning/Boltz), bookkeeping, expense tracking, P&L, and 1099 reports**.
- The article gives concrete implementation scale details including **50+ scripts** and an approximately **600-line AGENTS.md**, indicating that the system relies primarily on tool-like actions and text-based workflow orchestration rather than a single all-in-one agent.
- The author explicitly states that Sheila is **not fully autonomous**, but operates under human supervision in the terminal; therefore, the result is better understood as a “high-reliability semi-automated production system” rather than an unattended agent.
- The article **does not provide standard benchmarks, success rates, percentage time savings, cost reductions, error rates, or quantitative comparisons with other methods/platforms**.
- There is no public experimental data supporting the conclusion that “OpenCode is better suited than OpenClaw for real agents”; this is an experiential claim based on a single real-world deployment case.

## Link
- [https://soapbox.pub/blog/announcing-sheila/](https://soapbox.pub/blog/announcing-sheila/)
