---
source: arxiv
url: http://arxiv.org/abs/2604.11270v2
published_at: '2026-04-13T10:24:28'
authors:
- Islem Bouzenia
- Cristian Cadar
- Michael Pradel
topics:
- llm-agents
- software-analysis
- benchmarking
- code-intelligence
- multi-step-automation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Evaluating LLM Agents on Automated Software Analysis Tasks

## Summary
This paper studies whether LLM agents can set up and run real software analysis tools end to end on open-source projects. It introduces AnalysisBench, a benchmark for this task, and shows that a purpose-built agent reaches much higher verified success than adapted baseline agents.

## Problem
- Applying analysis tools to new projects is hard because the agent must set up both the tool and the target project, satisfy dependencies, generate required artifacts, and confirm that the tool actually analyzed the project.
- Prior agent evaluations focused on issue solving, repair, or environment setup, not end-to-end automated software analysis with tool-specific evidence checks.
- This matters because weak setup and validation block adoption of analyzers, fuzzers, symbolic execution tools, and profilers in practice.

## Approach
- The paper defines **automated software analysis** as a full pipeline: create an isolated container, install the analysis tool, build the target project, run the analysis, and produce project-specific evidence.
- It introduces **AnalysisBench**, a benchmark of 35 tool-project tasks covering 7 analysis tools and 10 open-source C/C++ and Java projects, with manually built reference setups and validation artifacts.
- The authors evaluate 4 agent architectures across 4 LLM backends: RAG-Agent, Mini-SWE-Agent, ExecutionAgent, and their custom **AnalysisAgent**.
- AnalysisAgent uses three main mechanisms: explicit workflow stages, one action per cycle with deterministic log condensation, and evidence-based completion checks with an LLM judge before stopping.
- Success is measured with manual verification of reproducible environments and tool-specific analysis outputs, not just whether the agent claims success.

## Results
- **AnalysisAgent + Gemini-3-Flash** achieves **94% verified success (33/35 tasks)**, compared with **77% (best baseline: ExecutionAgent + Gemini-3-Flash)**.
- Averaged across LLM backends, the best baseline reaches **57% verified success**, while **AnalysisAgent reaches 79%**, a **20 percentage point** gap.
- The internal validator accepted **131/140** AnalysisAgent submissions as successful, but only **111** were confirmed by manual verification, giving a **15% false-positive rate** for self-validation.
- Failed runs cost more: they consume **2.77×** more cycles and **1.27×** more cost than successful runs, so the higher success rate also improves total cost efficiency.
- The study reports that **whole-program analyses and symbolic execution** are the hardest tasks, and **Java toolchains** are harder than **C/C++** in this benchmark.
- Common baseline failures are concrete: stage mixing, poor root-cause extraction from long logs, and stopping after superficial signs such as `--help`, a toy run, or a project build without real analysis output.

## Link
- [http://arxiv.org/abs/2604.11270v2](http://arxiv.org/abs/2604.11270v2)
