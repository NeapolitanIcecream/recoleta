---
source: arxiv
url: https://arxiv.org/abs/2605.02455v1
published_at: '2026-05-04T10:58:22'
authors:
- Shuzhao Feng
- Boqi Chen
- Brett H Meyer
- Gunter Mussbacher
topics:
- repository-level-code-generation
- spec-driven-engineering
- llm-code-generation
- software-modeling
- gherkin-testing
- code-verification
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# LLM-Assisted Repository-Level Generation with Structured Spec-Driven Engineering

## Summary
SSDE uses structured specs such as Gherkin scenarios, domain models, and generated API signatures to guide LLMs in repository-level MVC code generation. The pilot study shows structured inputs often raise test pass rates over natural-language-only prompts, while many failures are static API or type errors that tooling could catch.

## Problem
- LLM code generation quality drops when moving from isolated functions or files to repository-level systems.
- Natural language prompts contain ambiguity and give weak support for verifying whether generated code matches requirements.
- Repository automation needs generated code that follows requirements, model APIs, constraints, and executable behavior across a system.

## Approach
- The method gives the LLM structured artifacts: Gherkin examples, Umple or Ecore domain models, generated model-layer class and function signatures, and a controller template.
- The LLM generates Python MVC controller business logic, which is combined with the generated model layer to form the backend system.
- The pilot uses 3 GitHub systems: Symboleo, CheECSEManager, and MeetingGroups, with 119 to 134 test cases per system.
- The study tests 5 LLMs: Claude Sonnet 4.5, Qwen 3 Coder 480B/A35B Instruct, GPT 5.1, GPT 5 Nano, and Llama 3.2 3B Instruct.
- Each LLM and input setup is run 10 times, then scored by Python unit-test pass rate and manual failure inspection.

## Results
- In Claude Sonnet 4.5 runs, Symboleo with Umple plus Gherkin plus domain model reached 99.1% ± 2.9% test pass rate, compared with 0.0% ± 0.0% for natural language with no model.
- For CheECSEManager with Umple, Claude reached 76.7% ± 0.0% with natural language plus signature model and 79.2% ± 0.3% with Gherkin plus signature model; Gherkin plus domain model fell to 25.7% ± 7.6%.
- For MeetingGroups with Umple, Claude improved from 81.6% ± 0.0% with natural language only to 85.0% ± 2.8% with natural language plus signature model.
- Across all LLMs, using generated model-layer signatures instead of domain models improved average test pass rate by 7.82 percentage points and reduced standard deviation by 2.47 points.
- Gherkin-plus-model inputs averaged 6.8 percentage points lower test pass rate than natural-language-plus-model inputs, but beat natural language in 14 of 30 LLM/tool/system combinations, with a mean gain of 7.7 points in those wins.
- Failure analysis found non-existent API calls at 49.0% of errors, data type mismatches at 20.2%, missing constraint validation at 11.5%, positional argument mismatches at 3.2%, and non-existent variables at 1.0%; the authors state that more than 70% of failures can be detected by static analysis.

## Link
- [https://arxiv.org/abs/2605.02455v1](https://arxiv.org/abs/2605.02455v1)
