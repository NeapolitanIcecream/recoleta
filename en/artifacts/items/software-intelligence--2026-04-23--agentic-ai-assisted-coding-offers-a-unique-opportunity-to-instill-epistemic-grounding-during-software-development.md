---
source: arxiv
url: http://arxiv.org/abs/2604.21744v1
published_at: '2026-04-23T14:50:35'
authors:
- Magnus Palmblad
- Jared M. Ragland
- Benjamin A. Neely
topics:
- agentic-coding
- code-intelligence
- context-engineering
- scientific-software
- epistemic-grounding
- proteomics
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Agentic AI-assisted coding offers a unique opportunity to instill epistemic grounding during software development

## Summary
The paper proposes **GROUNDING.md**, a field-scoped document that gives coding agents explicit domain rules that override user and project instructions. The goal is to keep AI-generated scientific software valid when non-experts use agentic coding tools.

## Problem
- Agentic coding can produce software that matches a user request while breaking domain validity rules, such as incorrect false discovery rate (FDR) handling in proteomics.
- Existing context files like `plan.md`, project rules, and `SKILL.md` guide tasks and methods, but they do not enforce field-level scientific constraints.
- This matters because bespoke scientific software is becoming easier to generate, while validity checks still depend on expert knowledge that many users and agents may lack.

## Approach
- The authors define **GROUNDING.md** as a community-governed, field-scoped grounding document for agentic software development.
- It encodes two kinds of rules: **Hard Constraints (HCs)** for non-negotiable validity requirements and **Convention Parameters (CPs)** for community default choices that may change over time.
- The document is meant to load at inference time with highest priority, above `plan.md`, project rule files such as `AGENTS.md` or `CLAUDE.md`, and method files such as `SKILL.md`.
- The paper provides a draft proteomics version, `proteomics_GROUNDING.md`, with rules for functional correctness, algorithmic efficiency, interoperability, testing, validation, provenance, and QC.
- The intended agent behavior is to refuse requests that violate HCs, cite the violated rule, explain why the request is invalid, and suggest compliant alternatives.

## Results
- The paper reports **preliminary proof-of-principle testing** with **Claude Code v2.1.90** and **NVIDIA Nemotron-3-Super-120B-A12B-FP8** in isolated fresh sessions.
- Agent HC compliance was tested with **6 prompts** designed to violate different hard constraints; the stated success condition was refusal to generate non-compliant code plus citation of the relevant HC.
- The authors state that, in their tests, using the **system prompt** to load `GROUNDING.md` was **more consistent than XML tagging**.
- They also tested conflict with an **adversarial `CLAUDE.md`** that told the model to ignore scientific validity, and argue that `GROUNDING.md` should have first priority in the context hierarchy.
- The excerpt gives **no aggregate accuracy, refusal rate, pass/fail table, or benchmark metric**, so the evidence is qualitative rather than a measured performance study.
- Strong concrete claims include prevention of invalid requests such as overly broad modification searches, enforcement of proteomics validity rules like FDR constraints, and better documentation of provenance such as software versions and `GROUNDING.md` commit SHA.

## Link
- [http://arxiv.org/abs/2604.21744v1](http://arxiv.org/abs/2604.21744v1)
