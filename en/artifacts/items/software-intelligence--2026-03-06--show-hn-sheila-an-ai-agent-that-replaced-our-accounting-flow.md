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
- code-intelligence
- human-in-the-loop
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# Show HN: Sheila, an AI agent that replaced our accounting flow

## Summary
Sheila is an accounting AI agent built for real business operations, and the author claims it has replaced Soapbox’s entire contractor payment and bookkeeping workflow. The article’s core contribution is not a new model, but a demonstration of an engineering approach for building production-capable agents through fine-grained tool scripts + natural-language workflow documentation + human-in-the-loop iteration.

## Problem
- It is hard to get AI agents to truly take over **end-to-end business processes**; many platforms emphasize autonomy, multi-agent setups, and demo appeal, but lack a single agent that can run reliably in production.
- Accounting/payment workflows involve multi-system integration and high-risk operations, including invoice intake, bookkeeping, fiat/Bitcoin payments, archiving, tax reporting, and expense submission; manual handling is time-consuming and error-prone.
- This matters because if AI agents cannot work reliably in highly constrained, high-responsibility workflows like this, the value of an “AI agent platform” is hard to realize in actual business operations.

## Approach
- Build bottom-up with **OpenCode** in an empty project, rather than first writing complex hardcoded multi-step flows; the author says the v1 approach was “fragile and inflexible,” so v2 switched to a tool-oriented design.
- Break capabilities into **50+ fine-grained scripts**, with each script doing exactly one thing, such as reading email, checking balances, initiating payments, uploading files, or writing to spreadsheets, and test them one by one.
- Use a roughly **600-line `AGENTS.md`** to describe workflows in natural language; when the user gives a command like “process invoices,” the agent reads the instructions and chains together the appropriate scripts to complete the workflow.
- Maintain **human-in-the-loop** operation: the agent runs in the terminal, with the author supervising in real time; it can draft emails or prepare payments, but key actions are visible to a human before being sent.
- The core mechanism can be summarized simply as: **break a complex accounting workflow into many reliable small tools, then let the LLM call them in sequence according to the instructions, while humans repeatedly test and correct the system.**

## Results
- The author claims Sheila has already **replaced Soapbox’s entire accounting flow**, covering the full process for contractor invoice handling, fiat payments (ACH/wire via Mercury), Bitcoin payments (Kraken/Lightning/Boltz), bookkeeping, expense tracking, P&L, and 1099 reporting.
- The article gives specific engineering scale details: **v2 uses 50+ scripts**, the workflow instruction document is about **600 lines**, and it went through “**hundreds of**” rounds of human-machine iterative testing and correction.
- In terms of interaction outcome, the user only needs to ask in the terminal, “**what's the status?**” and the agent can summarize what is done, what is pending, and what needs attention, indicating cross-system workflow state integration capability.
- **No standard benchmark data or formal quantitative metrics are provided**; it does not report processing latency, success rate, error rate, percentage of labor saved, or reproducible experimental comparisons with other agent frameworks.
- The strongest concrete claim is that compared with the author’s earlier v1 “complex code flows,” v2’s “fine-grained scripts + AGENTS.md + human oversight” is more stable and more flexible in a real production accounting setting, and is already being used in company operations.
- The article also claims this pattern is transferable: by replacing the integration scripts, it can be reused for other business workflows; the code has been **open-sourced under AGPL**.

## Link
- [https://soapbox.pub/blog/announcing-sheila/](https://soapbox.pub/blog/announcing-sheila/)
