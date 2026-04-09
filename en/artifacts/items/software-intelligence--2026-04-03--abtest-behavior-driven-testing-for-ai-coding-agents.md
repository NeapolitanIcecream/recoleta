---
source: arxiv
url: http://arxiv.org/abs/2604.03362v1
published_at: '2026-04-03T17:52:37'
authors:
- Wuyang Dai
- Moses Openja
- Hung Viet Pham
- Gias Uddin
- Jinqiu Yang
- Song Wang
topics:
- ai-coding-agents
- behavioral-testing
- fuzzing
- code-intelligence
- repository-grounded-evaluation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# ABTest: Behavior-Driven Testing for AI Coding Agents

## Summary
ABTest is a behavior-driven fuzzing system for AI coding agents. It turns real user failure reports into executable tests on real repositories and finds many new agent behavior failures that normal code benchmarks miss.

## Problem
- Existing coding-agent benchmarks focus on final task correctness in controlled tasks, so they miss process-level failures such as editing the wrong files, leaving partial state, or making false claims about workspace state.
- These failures matter because tools like Claude Code, Codex CLI, and Gemini CLI can directly modify repositories, run commands, and affect software correctness and safety in day-to-day development.
- The paper targets behavioral robustness during multi-step interaction, using real reported failures instead of synthetic benchmark prompts.

## Approach
- ABTest mines 400 user-reported, developer-confirmed coding-agent failures from GitHub issues and abstracts them into 47 reusable **Interaction Patterns** and 128 **Action Types**.
- It composes compatible pattern-action pairs into 647 fuzzing seed templates, where the pattern captures the user workflow and the action captures the concrete stressed operation such as file moves, rollback, patching, or command execution.
- It instantiates each seed into a repository-grounded, multi-step test case in an isolated workspace on a real repository, with explicit expected artifacts, file states, and verification steps.
- It runs these cases against coding agents, records prompts, command traces, file diffs, outputs, and other artifacts, then uses automated checks plus manual validation to detect behavioral anomalies.
- The core mechanism is simple: start from real bug reports, abstract the repeated workflow and action structure, generate many similar executable cases, and check whether the agent's behavior diverges from the requested workflow or repository state.

## Results
- Source data: 400 real failure reports mined from Claude Code, OpenAI Codex CLI, and Gemini CLI issue trackers.
- Pattern inventory: 47 Interaction Patterns and 128 Action Types, combined into 647 executable repository-grounded fuzzing cases.
- Across one execution of the 647-case bundle per evaluated configuration, ABTest flagged 1,573 behavioral anomalies; 642 were manually confirmed as new true anomalies, for 40.8% detection precision.
- Claude Code: 119 new anomalies with Claude 4.5 Haiku and 87 with Claude 3.5 Haiku.
- Codex CLI: 166 new anomalies with GPT-5.1-Codex-Mini and 95 with GPT-4o-mini.
- Gemini CLI: 175 new anomalies with Gemini 2.5 Flash-Lite.

## Link
- [http://arxiv.org/abs/2604.03362v1](http://arxiv.org/abs/2604.03362v1)
