---
source: hn
url: https://news.ycombinator.com/item?id=47371289
published_at: '2026-03-13T23:16:04'
authors:
- xodn348
topics:
- ai-agents
- autonomous-commerce
- payments-infrastructure
- browser-automation
- agentic-transactions
relevance_score: 0.81
run_id: materialize-outputs
language_code: en
---

# Ask HN: Has anyone built an AI agent that spends real money?

## Summary
This is not a formal paper, but rather a practical request-for-help post about the feasibility of an "AI agent that can autonomously spend real money." Its core value lies in clearly exposing real-world bottlenecks such as payments, risk control, compliance, and platform blocking, showing that although card networks are optimistic about this direction, developer infrastructure is still clearly lacking.

## Problem
- The problem to solve is: after receiving user authorization, enable an AI agent to autonomously complete the full loop of browsing products, selecting an order, and making a real payment.
- This matters because it is a key step from "can recommend" to "can execute," directly affecting the deployment of agent-based commerce, automated procurement, and more broadly executable AI assistants.
- The main current obstacles include card issuers not cooperating with individual developers, Stripe's 3D Secure restrictions on off-session payments, e-commerce sites blocking browser automation, and the legal risks of automation on major platforms.

## Approach
- The author is building an MCP server that connects AI agents to payment rails such as Stripe, PayPal, and virtual cards.
- The intended mechanism is simple: the user provides payment credentials once, and afterward the agent independently handles "find products → make decisions → pay."
- This approach depends on existing payment rails and browser automation rather than a new payment protocol, so it is directly constrained by payment authentication, anti-fraud systems, and website policies.
- The post also cites Visa's **Intelligent Commerce** and Mastercard's **Agent Pay** as industry signals, indicating that card networks are paving the way for "agentic spending," but developer-ready tools are still immature.

## Results
- No formal experiments, benchmark data, or quantitative results are provided; there are no figures for datasets, accuracy, success rate, or transaction conversion rate.
- The strongest concrete progress is that the author is "already building" an MCP payment service connecting Stripe, PayPal, and virtual cards, and has publicly shared the repository: `clawpay`.
- A key practical conclusion stated in the post is that **Stripe requires 3D Secure for off-session payments**, which makes it difficult for an agent to complete payment seamlessly within current e-commerce payment flows.
- Another concrete conclusion is that mainstream e-commerce platforms block browser automation, and **Amazon v. Perplexity (described in the post as March 9)** is viewed by the author as evidence that browser automation carries real legal risk.
- A positive industry-level signal is that **Visa Intelligent Commerce** and **Mastercard Agent Pay** have been launched, but the post provides no data on their availability, coverage, or developer adoption.

## Link
- [https://news.ycombinator.com/item?id=47371289](https://news.ycombinator.com/item?id=47371289)
