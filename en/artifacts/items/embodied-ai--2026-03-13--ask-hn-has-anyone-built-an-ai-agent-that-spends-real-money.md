---
source: hn
url: https://news.ycombinator.com/item?id=47371289
published_at: '2026-03-13T23:16:04'
authors:
- xodn348
topics:
- ai-agents
- autonomous-payments
- agentic-commerce
- browser-automation
- payment-infrastructure
relevance_score: 0.1
run_id: materialize-outputs
language_code: en
---

# Ask HN: Has anyone built an AI agent that spends real money?

## Summary
This is not a research paper, but a Hacker News help post discussing whether anyone has actually built an AI agent that can autonomously spend real money to shop. Its core value is that it clearly exposes the real-world deployment obstacles around payments, compliance, anti-automation measures, and legal risk.

## Problem
- The problem to solve is enabling an AI agent, after receiving user authorization, to autonomously complete the full purchase loop of browsing products, selecting items, and making an actual payment.
- This matters because it is a key step toward AI agents truly executing real-world tasks, involving payment networks, merchant websites, identity verification, and liability assignment.
- The main obstacles identified in the post include: card issuers ignoring individual developers, Stripe off-session payments being constrained by 3D Secure, e-commerce platforms blocking browser automation, and legal risks surrounding automated shopping.

## Approach
- The author is already working on an MCP server intended to connect AI agents to payment providers such as Stripe, PayPal, and virtual cards.
- The envisioned mechanism is simple: the user gives the agent a card or payment authorization first, and the agent then completes the flow of "find product — place order — pay" on its own.
- The post does not propose a new algorithm or model, but instead focuses on the systems integration layer: payment rails, browser automation, e-commerce checkout flows, and compliance feasibility.
- The text also cites Visa's "Intelligent Commerce" and Mastercard's "Agent Pay," indicating that major payment networks are pushing agentic commerce, while the developer tooling remains immature.

## Results
- No experiments, benchmarks, datasets, or quantitative results are provided; this is not a paper, but a request-for-input post.
- The strongest concrete claims are the current implementation bottlenecks: **Stripe off-session payments require 3D Secure**, **major e-commerce sites block browser automation**, and **Amazon v. Perplexity (2025-03-09) shows that there is real legal risk**.
- The industry signals mentioned in the text include: **Visa launched "Intelligent Commerce"** and **Mastercard launched "Agent Pay"**, suggesting that payment networks see promise in this direction.
- The author also raises a product viability question: whether users would trust AI to shop on their behalf using a **$500 prepaid card**, but reports no user experiments or deployment results.

## Link
- [https://news.ycombinator.com/item?id=47371289](https://news.ycombinator.com/item?id=47371289)
