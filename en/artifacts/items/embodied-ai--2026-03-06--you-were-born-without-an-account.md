---
source: hn
url: https://simplex.chat/why/
published_at: '2026-03-06T23:28:44'
authors:
- Cider9986
topics:
- privacy
- secure-messaging
- metadata-resistance
- decentralized-network
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# You were born without an account

## Summary
This is not a robotics or machine learning paper, but a manifesto about the idea of a de-identified communication network. It argues for building an encrypted messaging system that requires no accounts, usernames, or phone numbers, and in which the network itself does not know who is communicating.

## Problem
- Existing online communication platforms typically require accounts, phone numbers, usernames, or social relationships, thereby inherently exposing metadata about “who is communicating with whom.”
- Even if message contents are encrypted, platforms often still control identities and connection graphs, making privacy depend on platform goodwill rather than infrastructure-level guarantees.
- This centralized, identifiable communication model weakens the basic human freedom to “talk without being watched,” and therefore carries social and political significance.

## Approach
- The core idea is to build a communication network with **no accounts, no usernames, no phone numbers, and no user identities**.
- The network is responsible only for carrying encrypted messages, but **does not need to know who the communicating parties are**, structurally reducing leakage of identities and relationships.
- The mechanism emphasized in the text is not a “more trustworthy platform,” but rather **infrastructure that itself cannot record and betray user identity relationships**.
- At the simplest level: change the model from “register an identity before connecting to chat” to “establish a private connection first, then send messages,” while making the network layer see as few identity markers tied to individuals as possible.

## Results
- The provided text **does not give any quantitative experimental results**, and includes no datasets, metrics, baselines, or ablation comparisons.
- The strongest concrete claim is that the network can achieve **no phone numbers / no usernames / no accounts / no user identities**.
- Its claimed breakthrough is that the communication infrastructure can “connect people and carry encrypted messages without knowing who is connected.”
- The text also claims that this design can elevate privacy from a “platform feature” to a “default property,” but provides no technical proof or performance figures in support.

## Link
- [https://simplex.chat/why/](https://simplex.chat/why/)
