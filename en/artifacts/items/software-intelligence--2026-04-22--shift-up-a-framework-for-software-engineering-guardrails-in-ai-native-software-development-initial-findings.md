---
source: arxiv
url: http://arxiv.org/abs/2604.20436v1
published_at: '2026-04-22T10:55:57'
authors:
- Petrus Lipsanen
- Liisa Rannikko
- "Fran\xE7ois Christophe"
- Konsta Kalliokoski
- Vlad Stirbu
- Tommi Mikkonen
topics:
- ai-native-development
- software-engineering-guardrails
- bdd-acceptance-testing
- agentic-coding
- architecture-traceability
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Shift-Up: A Framework for Software Engineering Guardrails in AI-native Software Development -- Initial Findings

## Summary
Shift-Up is a software engineering workflow for AI-native development that uses requirements, architecture artifacts, and executable tests to keep coding agents aligned. The paper reports early evidence that this structure changes developer work from reactive debugging toward planning, orchestration, and test-based validation.

## Problem
- Prompt-only "vibe coding" can produce fast prototypes, but the paper targets three recurring failures: architectural drift, weak traceability, and low controllability during agent-driven implementation.
- These failures matter because teams trade delivery speed for maintainability, rework, and lower confidence in what the generated system is actually doing.
- The paper asks whether classic software engineering artifacts can act as guardrails for coding agents instead of being treated as optional documentation.

## Approach
- Shift-Up turns software engineering artifacts into machine-readable inputs for the agent: a refined SRS, user stories, BDD-style acceptance tests in Robot Framework, C4 architecture models, and ADRs.
- In the reported case study, stakeholder input was refined into 68 user stories, then into 175 acceptance test cases, plus C4 and ADR artifacts, a 10-phase implementation roadmap, and GitHub issues tied to required tests.
- The implementation loop is simple: open the next issue, ask the agent to make a plan that follows the existing artifacts, let the agent implement, run the linked acceptance tests, and feed failures back into the next iteration until the tests pass.
- The evaluation compares three modes on a snack-bar web app: unstructured vibe coding, structured prompt engineering, and a partial Shift-Up workflow. No human wrote code; humans guided the agent through prompts.

## Results
- The paper gives mostly qualitative results. It does not report standard outcome metrics such as accuracy, pass-rate gains, defect counts, or time savings against a fixed baseline.
- Prompt-pattern analysis used 176 recorded prompts across the structured vibe coding and Shift-Up implementations. For Shift-Up, prompts were 62% "proceeding with the next step," 16% test execution, 9% developer-identified fixes, 7% acceptance of agent-proposed solutions, and 5% initiating the next plan step.
- In structured prompt engineering, 52% of prompts addressed issues found manually in the GUI or IDE, 27% were "proceeding with the next step," 5% were feature planning, 5% were new feature implementation, and 11% fell into other categories.
- The authors claim this shows a shift from reactive intervention in prompt engineering to strategic orchestration with automated validation in Shift-Up, with increased agent independence during implementation.
- Table 1 rates Shift-Up qualitatively as high upfront investment, high human control, rigid constraints, slower development speed, and guardrails based on BDD/TDD, C4, and ADRs; unstructured vibe coding is rated as the fastest for prototyping with low control.
- The paper only partially answers whether Shift-Up reduces agent drift. The authors say the small, common web-app domain likely did not expose enough drift to test that claim well.

## Link
- [http://arxiv.org/abs/2604.20436v1](http://arxiv.org/abs/2604.20436v1)
