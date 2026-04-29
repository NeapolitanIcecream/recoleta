---
source: arxiv
url: http://arxiv.org/abs/2604.23106v1
published_at: '2026-04-25T02:01:54'
authors:
- Siddeshwar Raghavan
- Tanwi Mallick
topics:
- scientific-code-generation
- multi-agent-systems
- knowledge-distillation
- code-intelligence
- llm-reasoning
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# No Test Cases, No Problem: Distillation-Driven Code Generation for Scientific Workflows

## Summary
MOSAIC is a training-free multi-agent system for scientific code generation when no input/output test cases exist. It replaces test-case-based verification with teacher-student distillation and a compact shared context, and it improves SciCode results across several LLM backbones.

## Problem
- Standard code-generation agents depend on I/O test cases to check and refine code, but scientific workflow tasks usually provide only a function signature and domain background.
- In scientific problems, building a valid test case often requires knowing the correct algorithm already, which creates a verification deadlock.
- This matters because scientific code needs executable programs, correct algorithms, and numerical precision across chained subproblems in domains such as physics, chemistry, biology, materials science, and mathematics.

## Approach
- MOSAIC uses a teacher-student distillation setup instead of execution feedback for semantic checking. The teacher reads a small non-overlapping validation subset with gold code and produces domain-specific rationale templates and pseudocode.
- A student-side Rationale Agent uses those templates as few-shot guidance to break a new problem into ordered substeps, then a Coding Agent writes Python for each step.
- A Consolidated Context Window (CCW) keeps only prior function signatures and one-line summaries, so later agents keep the needed history without carrying full code and long reasoning traces.
- A Debugger Agent runs the code for up to k repair rounds, but it is limited to syntax and import fixes rather than algorithmic validation, which separates syntactic grounding from semantic grounding.
- The system is LLM-agnostic, domain-bucketed, and uses separate memory per scientific domain to reduce cross-domain interference.

## Results
- On SciCode with GPT-4o, MOSAIC solves 12/65 main problems and 113/283 subproblems, versus the SciCode baseline at 7/65 and 94/283. The paper also states up to 24% accuracy gains across the five scientific domains.
- On SciCode with Claude Sonnet 4, MOSAIC reaches the best reported scientific result: 13/65 main problems and 118/283 subproblems, compared with the baseline at 9/65 and 109/283.
- On SciCode with Gemini 2.5 Flash, MOSAIC gets 11/65 main problems and 117/283 subproblems, compared with the baseline at 7/65 and 112/283.
- Domain examples on SciCode: with GPT-4o, physics improves from 48/145 to 56/145 subproblems and mathematics from 4/24 to 10/24; with Gemini 2.5 Flash, mathematics improves from 1/24 to 12/24.
- Ablation on SciCode (GPT-4o) shows the full system at 12/65 and 113/283 versus baseline 7/65 and 94/283. An unrestricted CCW that keeps all previous code drops performance to 4/65 and 57/283, which supports the compact-context design.
- On general code benchmarks, MOSAIC scores 92.53 on HumanEval, 84.90 on MBPP, and 24.71 on APPS. It ranks first on MBPP and APPS and second on HumanEval, behind CodeSIM at 93.60 on HumanEval.

## Link
- [http://arxiv.org/abs/2604.23106v1](http://arxiv.org/abs/2604.23106v1)
