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
- human-ai-interaction
relevance_score: 0.57
run_id: materialize-outputs
language_code: en
---

# Ask HN: Read‑only LLM tool for email triage and knowledge extraction?

## Summary
This is not a research paper, but a product request post describing the concept of a **read-only** LLM tool for email triage and knowledge extraction. The core requirement is to enable email classification, question-answer retrieval, and follow-up reminders without granting the model any write or send permissions.

## Problem
- Existing email filtering rules are too coarse to handle emails that fall into the “middle ground” between important and unimportant.
- Many AI email products require full mailbox control permissions, and even proactively send, archive, or modify content, which conflicts with the user's security boundary requirements.
- The user wants to extract decisions, tasks, deadlines, and stalled items from scattered email threads, but traditional email search struggles to support natural-language-level knowledge retrieval.

## Approach
- Proposes a **strictly read-only** LLM email assistant: it can only read and analyze emails, and cannot send, move, delete, archive, or modify any content.
- Uses an LLM to perform fine-grained triage of incoming mail, such as “important,” “maybe useful,” and “likely promo,” covering gray areas that rule-based filters struggle to handle.
- Organizes scattered email threads into a searchable knowledge base, supporting natural-language queries like “What were all the decisions about Project X across the last 3 months?”
- Extracts explicit tasks and deadlines from long email chains, and identifies threads that have stalled and need follow-up.
- Optionally emphasizes privacy-first design, such as running locally or allowing users to bring their own API key, to reduce the risk of data leakage.

## Results
- The text **does not provide any experiments, datasets, baselines, or quantitative metrics**, so there are no accuracy, recall, or efficiency improvement figures to report.
- The strongest concrete claim is the product boundary: achieving “zero write permissions,” meaning **no write access**—no sending, moving, deleting, or auto-archiving.
- The target capabilities described fall into three categories: email triage, knowledge retrieval, and follow-up/action item detection, but all are requirements descriptions and **no implemented results or comparative outcomes are shown**.
- The specific privacy requirements mentioned are “runs locally” or “bring your own API keys,” but again no performance or security evaluation results are provided.

## Link
- [https://news.ycombinator.com/item?id=47317429](https://news.ycombinator.com/item?id=47317429)
