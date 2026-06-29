---
source: arxiv
url: http://arxiv.org/abs/2604.06373v1
published_at: '2026-04-07T18:59:05'
authors:
- Syed Mohammad Kashif
- Ruiyin Li
- Peng Liang
- Amjed Tahir
- Qiong Feng
- Zengyang Li
- Mojtaba Shahin
topics:
- ai-ide
- cursor
- large-scale-code-generation
- software-design-quality
- static-analysis
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Beyond Functional Correctness: Design Issues in AI IDE-Generated Large-Scale Projects

## Summary
This paper studies whether Cursor can generate large software projects that work and whether those projects have design problems. The authors find that Cursor can produce sizable, mostly functional systems under a structured human-guided process, but the code carries many maintainability issues.

## Problem
- Prior work mostly tests snippet generation or small end-to-end projects, so there is little evidence on whether an AI IDE can build large multi-file systems with realistic stacks and architecture.
- Functional correctness alone misses design quality. A project can run and still contain duplication, complex methods, poor separation of concerns, and framework misuse that make later changes costly.
- This matters for teams using AI IDEs for project-scale development, especially under fast prompting workflows where developers may accept code they did not inspect closely.

## Approach
- The authors propose a Feature-Driven Human-In-The-Loop (FD-HITL) process for generating large projects with Cursor. In simple terms, they do not ask for the whole app at once; they make Cursor plan the project, split it into testable features, build it step by step, and get human review during generation.
- They curate 10 detailed project descriptions across mobile, web, and utility domains, using stacks such as React, Spring Boot, Django, and React Native.
- They define large-scale projects as systems with at least 8K lines of code, multiple architectural components, and industrial-style technology stacks.
- They evaluate functional correctness manually, then inspect design quality with CodeScene and SonarQube, including manual review to remove 1,612 SonarQube false positives.

## Results
- Cursor generated 10 large-scale projects totaling 169,646 lines of code, with an average of 16,965 LoC and 114 files per project.
- Manual evaluation gave an average functional correctness score of 91%.
- CodeScene found 1,305 design issues across 9 categories.
- SonarQube found 3,193 design issues across 11 categories after removing 1,612 false positives.
- The paper reports 133 overlapping issues detected by both tools, which the authors treat as stronger evidence of recurring design problems.
- The most common issues were code duplication, high or complex methods, large methods, framework best-practice violations, exception-handling issues, and accessibility issues. The authors link these to violations of SRP, separation of concerns, and DRY.

## Link
- [http://arxiv.org/abs/2604.06373v1](http://arxiv.org/abs/2604.06373v1)
