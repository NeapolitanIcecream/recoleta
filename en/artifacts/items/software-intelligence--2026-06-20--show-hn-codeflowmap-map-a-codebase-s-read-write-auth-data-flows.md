---
source: hn
url: https://github.com/man-consult/code-mapper
published_at: '2026-06-20T23:49:07'
authors:
- brian-m
topics:
- code-intelligence
- static-analysis
- llm-code-tools
- software-visualization
- developer-workflow
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Show HN: Codeflowmap – map a codebase's read/write/auth data flows

## Summary
Codeflowmap is an experimental codebase map that combines static analysis with optional LLM file annotation. It helps developers verify generated or unfamiliar code by showing imports, function calls, data reads and writes, config use, auth paths, and flow traces.

## Problem
- LLM-generated code can compile while still being hard to verify: reviewers need to know what it touched, what it reads and writes, and whether auth paths match the intended design.
- Unfamiliar repositories require slow manual tracing across imports, calls, writes, config, and auth checks.
- The problem matters because missed write paths or auth flows can create security, privacy, or maintenance risk during code review.

## Approach
- Static analysis builds the base graph without model calls: import edges come from module resolution, and TypeScript/JavaScript function call edges come from symbol resolution through the TypeScript Compiler API.
- The LLM adds per-file annotations for reads, writes, config, auth, and flows. The graph edges are not inferred by the model.
- The tool writes results to `<repo>/.codemap`, including a Markdown vault with one `.md` file per source file and `[[wikilinks]]` for real graph edges.
- The web UI supports Files and Functions views, node focus, upstream/downstream path highlighting, search, and filtering by flow type.
- Annotation can run locally through Ollama or through any OpenAI-compatible provider; cached annotations use file-content hashes so unchanged files are not resent.

## Results
- The excerpt reports no benchmark, accuracy score, runtime measurement, or user study, so it does not provide quantitative evidence of a breakthrough result.
- It claims deterministic graph generation with no token cost for the base graph, using real module resolution for imports and TypeScript symbol resolution for TS/JS call edges.
- Language coverage is partial: TS/JS get function-level call edges, while Python currently contributes import edges and symbols.
- The default local annotation model is `qwen2.5-coder:7b`, about `4.7 GB`, and is claimed to run on a `16 GB` laptop.
- Suggested model options include `devstral` `24B` for `32 GB+` machines and `qwen2.5-coder:3b` for `8 GB` machines.
- The tool requires Bun `≥ 1.0`; graph scanning can run without an LLM, while annotation may send full source files to a remote provider unless local Ollama is used.

## Link
- [https://github.com/man-consult/code-mapper](https://github.com/man-consult/code-mapper)
