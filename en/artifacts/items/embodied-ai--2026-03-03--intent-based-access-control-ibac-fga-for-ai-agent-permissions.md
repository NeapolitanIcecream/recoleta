---
source: hn
url: https://ibac.dev
published_at: '2026-03-03T23:57:52'
authors:
- ERROR_0x06
topics:
- ai-agent-security
- prompt-injection
- access-control
- fine-grained-authorization
- tool-use
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Intent-Based Access Control (IBAC) – FGA for AI Agent Permissions

## Summary
IBAC is a permission control method for AI agents: instead of trying to make the model better at detecting prompt injection, it converts the user's explicit intent into fine-grained permissions and enforces checks before every tool call. The core claim is to turn prompt injection from a “detection problem” into an authorization problem where, even if the model is misled, it still cannot perform unauthorized actions.

## Problem
- AI agents are vulnerable to prompt injection when calling tools such as email, databases, and external APIs, causing the model to follow malicious instructions and perform actions not authorized by the user.
- Existing defenses often rely on input filtering, LLM judges, or output classifiers, but fundamentally still require the model to “detect attacks,” making them less stable, interpretable, or deterministic.
- This matters because once an agent is connected to real tools, unauthorized behavior can directly cause data leaks, incorrect operations, or security incidents.

## Approach
- Parse the user's **explicit intent** into FGA (fine-grained authorization) tuples, for example encoding “allow sending email to Bob” as a checkable permission relationship.
- Before every tool call, perform a deterministic authorization check based on these tuples; if the action falls outside the scope authorized by the intent, block it directly.
- There are only two integration points: **write FGA tuples after intent parsing** and **run checks before every tool call**.
- This mechanism does not depend on a custom interpreter, does not require a dual-LLM architecture, and does not require changes to the existing agent framework; the claimed overhead is only **one additional LLM call** plus the authorization check.

## Results
- The main performance numbers given in the text are: **one additional LLM call** and approximately **9ms** of authorization-check latency.
- The author claims the solution can be integrated and running in **minutes**, and requires only **two integration points / four deployment steps** (start OpenFGA, define the model, write tuples, check permissions).
- No standard datasets, benchmarks, or systematic quantitative results such as attack success rate are provided, so there are **no academic benchmark numbers to report**.
- The strongest specific claim is that even if prompt injection “completely compromises the LLM's reasoning,” unauthorized tool calls will still be deterministically blocked, making prompt injection “irrelevant” at the execution layer.

## Link
- [https://ibac.dev](https://ibac.dev)
