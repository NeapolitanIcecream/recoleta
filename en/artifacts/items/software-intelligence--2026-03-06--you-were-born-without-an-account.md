---
source: hn
url: https://simplex.chat/why/
published_at: '2026-03-06T23:28:44'
authors:
- Cider9986
topics:
- privacy-preserving-messaging
- anonymous-communication
- metadata-resistance
- decentralized-network
- encrypted-messaging
relevance_score: 0.14
run_id: materialize-outputs
language_code: en
---

# You were born without an account

## Summary
This article advocates a **communication network with no accounts, no usernames, no phone numbers, and no user identities**, making it impossible for platforms to know “who is talking to whom.” Its core value is turning privacy from a matter of “platform promises” into a property of infrastructure that **cannot betray** it.

## Problem
- Modern online communication usually requires accounts, phone numbers, usernames, or social-graph binding, which means platforms inherently control users’ identities and communication relationship graphs.
- Even if message content is encrypted, platforms can often still track **who is communicating with whom, when they are communicating, and where they appeared**, enabling metadata surveillance and centralized control.
- This matters because “being able to speak privately without being watched” is a basic human freedom; if communication infrastructure collects identity and relationships by default, users lose sovereignty over their space for communication.

## Approach
- The core mechanism is to build a **communication network that does not rely on any account-based identity layer**: no phone numbers, usernames, accounts, or fixed user identifiers.
- The network is responsible only for connecting parties and delivering **encrypted messages**, while the design goal is that it does not know who the connected parties are and does not retain an identifiable social graph.
- The article emphasizes that this is not a privacy model where “the platform still holds custody but is more benevolent”; rather, by **eliminating identifiable identity at the architectural level**, the infrastructure itself becomes incapable of betraying users.
- Put simply: instead of placing your chats in “a locked room in someone else’s house,” you own the communication space yourself, and the platform has no master ledger to inspect.

## Results
- The strongest claim made is that it is possible to build a **communication network with no phone numbers, no usernames, no accounts, and no user identities of any kind**.
- The article claims that this network can **deliver encrypted messages without knowing who is connected to whom**, decoupling identity visibility from communication functionality.
- The text does not provide paper-style quantitative experimental results, benchmark datasets, or throughput/latency metrics; there are **no verifiable numerical performance comparisons**.
- Therefore, its “results” are primarily conceptual and architectural claims: elevating privacy from a product feature to a default infrastructure property, and returning communication sovereignty to users.

## Link
- [https://simplex.chat/why/](https://simplex.chat/why/)
