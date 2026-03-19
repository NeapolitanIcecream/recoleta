---
source: hn
url: https://ibac.dev
published_at: '2026-03-03T23:57:52'
authors:
- ERROR_0x06
topics:
- ai-agent-security
- fine-grained-authorization
- prompt-injection-defense
- tool-call-guardrails
- openfga
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Intent-Based Access Control (IBAC) – FGA for AI Agent Permissions

## Summary
IBAC proposes an access control approach that directly binds AI agent permissions to the user's explicit intent, replacing defenses focused on “detecting prompt injection” with fine-grained authorization. Its core claim is: even if an LLM's reasoning is affected by an injection attack, as long as every tool call undergoes a deterministic permission check, unauthorized actions can still be blocked.

## Problem
- Existing prompt injection defenses usually rely on making the model smarter at recognizing attacks, such as input filtering, LLM judges, and output classifiers, but these methods can still fail when the model's reasoning is manipulated.
- Once AI agents can call tools like email, databases, and external APIs, incorrect or malicious tool calls can directly create real-world risks, so stronger runtime constraints are needed than simply “detecting attacks.”
- This matters because agent systems are moving into production environments; if a user's true intent cannot be reliably converted into executable permission boundaries, automated software and intelligent agents will be difficult to deploy safely.

## Approach
- The core mechanism is simple: first parse the user's explicit request into fine-grained FGA permission tuples, then check before each tool call whether that call is allowed by those tuples.
- The two main integration points described in the paper-style framing are: **write FGA tuples after intent parsing** and **perform an authorization check before every tool call**.
- This design shifts the security problem from “is the prompt malicious?” to “is this action authorized by the user's intent?”, so even if prompt injection contaminates the model's internal reasoning, unauthorized actions are still deterministically blocked.
- In implementation, it relies on fine-grained authorization systems such as OpenFGA; the author claims it requires no custom interpreter, no dual-LLM architecture, and no changes to the existing agent framework, adding only one extra LLM call for intent parsing.

## Results
- The main quantified overhead given in the text is: **1 additional LLM call** to parse user intent into permission tuples.
- The latency of each authorization check is about **9ms** (~9ms authorization check).
- The claimed deployment complexity is low: the author says it can be running in just **4 steps**, including starting OpenFGA, defining the authorization model, writing tuples, and checking before tool calls.
- The passage **does not provide standard datasets, success rates, attack blocking rates, false positive rates, or systematic comparison numbers against baseline methods**.
- The strongest concrete claim is that, compared with methods such as input filtering, LLM-as-a-judge, and output classifiers that depend on the model recognizing attacks, IBAC makes prompt injection “irrelevant” through deterministic tool-level authorization.

## Link
- [https://ibac.dev](https://ibac.dev)
