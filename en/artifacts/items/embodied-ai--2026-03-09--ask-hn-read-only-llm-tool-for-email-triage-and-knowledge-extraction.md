---
source: hn
url: https://news.ycombinator.com/item?id=47317429
published_at: '2026-03-09T23:53:01'
authors:
- maille
topics:
- email-triage
- knowledge-extraction
- read-only-ai
- privacy-first
- task-detection
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Ask HN: Read‑only LLM tool for email triage and knowledge extraction?

## Summary
This is not a research paper, but a Hacker News help post describing a need for a **read-only** email intelligence assistant: it would perform email categorization, knowledge retrieval, and follow-up item detection, while strictly having no write or send permissions. Its value lies in emphasizing a “safety-boundary-first” way of using email AI, avoiding existing products that over-automate or require full control of the inbox.

## Problem
- Existing email filtering rules struggle to handle the subtle signals in emails that fall “between important and unimportant,” making it hard for users to triage mail efficiently.
- Many AI email clients require full inbox control and may send, move, delete, or archive messages, which does not meet strict security-boundary requirements.
- Decisions, tasks, deadlines, and stalled threads are scattered across long email chains, making them difficult to retrieve and track in a unified way through natural-language queries.

## Approach
- The core idea is a **strictly read-only** LLM tool: it only reads email content and provides classification, summaries, retrieval, and reminder suggestions, but **cannot write, send, delete, modify, or archive** any email.
- Put simply: treat the inbox as a searchable knowledge base, not an autopilot system. The model is responsible for “understanding and labeling,” not for “taking actions.”
- Functionally, it includes three parts: categorizing new emails (such as important / maybe useful / likely promo), extracting knowledge from historical threads and supporting natural-language Q&A, and identifying stalled conversations along with tasks/deadlines.
- An optional requirement is privacy-first operation, such as running locally or allowing users to bring their own API key, to reduce the risk of email data leakage.

## Results
- The text **does not provide any experiments, datasets, baselines, or quantitative metrics**, so there are no reportable accuracy, recall, latency, or user-study results.
- The strongest concrete claim is at the requirements level: the system should enforce **0 write permissions**, meaning no sending, moving, deleting, or auto-archiving.
- Example target capabilities include answering cross-thread knowledge-retrieval questions such as: “What were all the decisions about Project X across the last 3 months?”
- It also claims the system should be able to identify “stalled threads that need follow-up” and extract explicit tasks and deadlines from long email chains, but it does not explain the implementation method or provide effectiveness metrics.

## Link
- [https://news.ycombinator.com/item?id=47317429](https://news.ycombinator.com/item?id=47317429)
