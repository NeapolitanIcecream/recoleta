---
source: arxiv
url: http://arxiv.org/abs/2604.23509v1
published_at: '2026-04-26T03:06:16'
authors:
- Chen Yang
- Junjie Chen
topics:
- unit-test-generation
- business-logic-bugs
- code-intelligence
- llm-for-software-engineering
- requirements-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Uncovering Business Logic Bugs via Semantics-Driven Unit Test Generation

## Summary
SeGa generates unit tests from business requirements, not just code, to catch business logic bugs that code-centric test generators miss. It builds structured semantic entries from requirement documents, retrieves the parts relevant to a target method, and uses them to guide LLM test generation.

## Problem
- The paper targets **business logic bugs**: cases where code violates intended product rules, workflows, or policies even though the code may look valid and execute normally.
- Existing unit test generation methods are mostly **code-centric**. They focus on control flow, types, and execution behavior, so they often miss bugs tied to requirements written in PRDs.
- This matters in enterprise software because many correctness rules live in requirement documents, team conventions, and workflow constraints rather than in method signatures or local code structure.

## Approach
- SeGa first builds a **semantic knowledge base** from product requirement documents. It converts tables and figures into text, removes irrelevant document content, and extracts **functionalities** that group related requirements under one business intent.
- It stores each functionality in a structured **DSL**, so the requirements are less noisy and easier to retrieve than raw PRD text.
- For a focal method, a **semantic reasoning agent** inspects the method and nearby code, summarizes the method's intended behavior in plain language, and uses that summary to retrieve the most relevant functionality entries.
- SeGa then derives **business scenarios** from the retrieved functionality. Each scenario turns one relevant requirement into explicit preconditions, triggering action, expected outcomes, and semantic constraints.
- A **test generation agent** uses both the code context and these scenarios to generate unit tests, and a compilation-repair step fixes build issues so the tests can run in real repositories.

## Results
- Evaluation covers **4 industrial Go projects** with **60 real-world business logic bugs**.
- SeGa detects **29 bugs**, while CHATTESTER detects **7**, SymPrompt **7**, HITS **6**, and RATester **4**. That is **22 to 25 more bugs** than the compared LLM-based baselines.
- SeGa reports **0.73 precision**, versus **0.54** for CHATTESTER, **0.54** for SymPrompt, **0.55** for HITS, and **0.57** for RATester. The paper states this is a **26.9% to 34.3% precision improvement**.
- In deployment on **6 production repositories**, SeGa found **16 previously unknown business logic bugs**. Developers confirmed and fixed all 16.
- The paper also reports concrete false-positive sources: implausible inferred failure scenarios, ambiguous or incomplete requirement documents, and team-specific engineering conventions that were not visible to the model.

## Link
- [http://arxiv.org/abs/2604.23509v1](http://arxiv.org/abs/2604.23509v1)
