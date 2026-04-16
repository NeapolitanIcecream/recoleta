---
source: arxiv
url: http://arxiv.org/abs/2604.05203v1
published_at: '2026-04-06T22:02:01'
authors:
- Saketh Ram Kasibatla
- Raven Rothkopf
- Hila Peleg
- Benjamin C. Pierce
- Sorin Lerner
- Harrison Goldstein
- Nadia Polikarpova
topics:
- ai-programming-agents
- code-intelligence
- human-ai-interaction
- software-engineering
- test-based-specification
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Decision-Oriented Programming with Aporia

## Summary
Aporia is a VS Code programming assistant built around explicit design decisions instead of free-form prompts and plans. The paper argues that this interaction style keeps developers involved in design and helps them understand what the agent actually implemented.

## Problem
- Coding agents reduce effort by letting developers specify goals at a high level, but the agent then fills in many design details on its own.
- Those hidden decisions can create "cognitive debt": developers lose track of system behavior and hold mental models that do not match the code.
- Existing prompt-generate-review workflows make it easy to accept agent choices without noticing key design branches such as policy, constraints, and edge cases.

## Approach
- The paper proposes **decision-oriented programming (DOP)**, where programmer-agent collaboration is organized around explicit, editable design decisions.
- Aporia implements this idea as a VS Code extension with a persistent **Decision Bank** that stores structured decisions the programmer can review, edit, or add to.
- A **questioner** agent asks yes/no design questions with optional comments to elicit decisions from the programmer; relevant code references are shown to ground the question in the codebase.
- A **planner** agent turns each accepted decision into a test suite, so each decision has an executable specification tied to code behavior.
- An **implementer** agent modifies the codebase using the goal, the Decision Bank, and the generated tests; the tests then validate whether the implementation matches the recorded decisions.

## Results
- The evaluation is a within-subjects user study with **14 programmers** comparing Aporia against **Claude Code** on feature additions to an existing Python codebase.
- The paper claims Aporia increased developer **engagement** in design: participants articulated **significantly more design decisions** and showed more continuous reflection during development. The excerpt does not report the exact count or test statistic.
- Aporia improved understanding accuracy: participants' mental models were **5x less likely to disagree with the code** than with the baseline agent.
- The introduction also reports a **79% lower likelihood of mismatches** between participants' mental models and the actual implementation compared with the baseline coding agent.
- The system is reported to help with both **exploration** and **validation** by turning decisions into checkable tests and by using the Decision Bank as a review checklist.
- The excerpt does not provide task-level accuracy, pass-rate, time, or productivity numbers beyond the user-study claims above.

## Link
- [http://arxiv.org/abs/2604.05203v1](http://arxiv.org/abs/2604.05203v1)
