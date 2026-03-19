---
source: hn
url: https://thenewstack.io/risk-mitigation-agentic-ai/
published_at: '2026-03-12T22:58:27'
authors:
- chhum
topics:
- agentic-ai
- api-testing
- contract-testing
- mocking-sandbox
- enterprise-ai-risk
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Before you let AI agents loose, you'd better know what they're capable of

## Summary
This article discusses why enterprises must clearly understand the true capabilities and risk boundaries of autonomous AI agents before deploying them. The core argument is that **contract-driven testing, shared mocks/sandboxes, and observability** can be used to verify what an agent will actually do before production, thereby reducing the risks of loss of control, injection attacks, and irreversible actions.

## Problem
- Enterprise-grade agents do more than generate text; they can **browse the web, call APIs, execute code, and modify files**. Early mistakes can cascade and amplify, and it is difficult to audit after the fact **what was done, when it was done, and why**.
- When agents consume external web pages, emails, and documents, they are vulnerable to **prompt injection**, which may lead to **data exfiltration, privilege escalation, and destructive actions** once connected to internal systems.
- Because agentic AI is still very new, enterprises lack mature best practices; without a capability catalog, sandboxing, and a testing feedback loop, organizations **do not know what an agent can actually do** and therefore cannot safely delegate authority.

## Approach
- The central method is to treat **behavior as the specification**: do not rely only on design intent, but observe real system behavior through testing before production and validate the agent’s actual action patterns across the toolchain.
- Adopt a **contract-first** approach: use formal specifications such as OpenAPI to define API capabilities, then automatically generate mock endpoints from the specification so the agent can first interact with interfaces that match the real structure inside a **safe sandbox**.
- Use open-source tools such as **Microcks + OpenAPI + Bruno** to maintain **shared, versioned sample data** and mocks, so API providers, consumers, and testers collaborate around the same contract and avoid drift between mocks and real services.
- Use **contract testing** to continuously send requests to real endpoints and check whether they still conform to the contract and whether backward compatibility has been broken; this ensures interface structure remains stable and consistent when moving from synthetic mocks to production.
- Further expose mock APIs as **MCP tool**s so LLMs/agents can call tools in a controlled environment, first understand the enterprise API menu and capability boundaries, and then gradually transition to production use.

## Results
- **BNP Paribas**: In its French retail banking line, **32 squads** and **500+ developers and testers** use Microcks, and the platform handles **2.5M+ API calls per week**.
- In the BNP case, mocking backend APIs for host systems enabled teams to develop and test in parallel, **reducing development and testing cycles by two-thirds (about 66%)**.
- Large adopters (such as **Amadeus**) reportedly achieved **significant development speed improvements** by shifting mocking and contract testing earlier, though the article does not provide more granular comparison figures.
- Microcks’ lightweight local binary starts in **under 200 milliseconds** and provides Testcontainers bindings for Java, Node, Go, and .NET for running full integration tests locally.
- The article does not provide standardized benchmark scores for agent security; the strongest concrete claim is that **shared sandbox + contract testing** can reduce risks caused by unrealistic mocks, dependency coupling, and direct production connections, while helping teams understand agent capability boundaries before real deployment.

## Link
- [https://thenewstack.io/risk-mitigation-agentic-ai/](https://thenewstack.io/risk-mitigation-agentic-ai/)
