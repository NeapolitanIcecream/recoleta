---
source: arxiv
url: https://arxiv.org/abs/2605.26017v1
published_at: '2026-05-25T16:35:36'
authors:
- Jian Fang
- Yingfei Xiong
topics:
- formal-verification
- llm-agents
- code-generation
- software-engineering
- interactive-theorem-proving
- risc-v
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Trustworthy Software Project Generation : a Case Study with an Interactive Theorem Prover

## Summary
The paper presents SPDDwL, an LLM-agent workflow that generates a runnable software project with a Rocq-verified pure core and C++ host integration. Its case study builds a RISC-V RV32I interpreter automatically from requirements.

## Problem
- LLM-generated projects can compile and pass available tests while still violating intended semantics, which matters for CPU interpreters and other code that implements state transitions.
- Verification can catch semantic errors, but LLM agents struggle to finish project-scale verified code when failed proof attempts give weak repair signals.
- Interactive theorem provers handle pure total functions, while deployed software also needs I/O and runtime effects, so the system must separate verified logic from host-side code.

## Approach
- A requirement-analysis agent turns natural-language requirements into a coding plan with data types, pure functions, host obligations, and formal properties.
- A coding agent generates Rocq functional definitions for the pure core, and a proving agent generates Rocq propositions and tactic proofs.
- Rocq checks the definitions and proofs; on failure, SPDDwL returns the proof state and diagnostics to the agents for repair.
- Accepted Rocq definitions are extracted to C++ with Crane and linked with a host layer that handles effects. The formal guarantee applies to the extracted core relative to its specifications.

## Results
- The case study implements all 47 instructions of the unprivileged RISC-V RV32I base as a CPU interpreter.
- With Claude Opus 4.7 and Rocq 9.0.1, SPDDwL completes the project within a 30-minute budget with no human intervention after requirements are supplied.
- The run produces 1,859 lines of verified Rocq and extracts 2,848 lines of C++.
- The interpreter passes 265 LLM-generated instruction tests covering the 47 instructions.
- A 12-hour AFL++ fuzzing run executes 98.2 million inputs and finds 0 crashes and 0 hangs.
- Under the same 30-minute configuration, a Dafny backend fails to complete verification; the paper attributes the Rocq result to explicit proof-state feedback that gives the agent repair information.

## Link
- [https://arxiv.org/abs/2605.26017v1](https://arxiv.org/abs/2605.26017v1)
