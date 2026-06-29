---
source: arxiv
url: https://arxiv.org/abs/2605.03117v1
published_at: '2026-05-04T19:59:23'
authors:
- Shahd Seddik
- Fatemeh Fard
topics:
- software-engineering-agents
- automated-program-repair
- fault-localization
- program-analysis
- code-graphs
- data-flow-slicing
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# ARISE: A Repository-level Graph Representation and Toolset for Agentic Fault Localization and Program Repair

## Summary
ARISE adds a repository graph with statement-level def-use edges to an LLM repair agent. On SWE-bench Lite, it improves fine-grained localization and raises Pass@1 over SWE-agent.

## Problem
- Repository-level repair agents must find the right files, functions, and lines before they can patch a bug.
- Existing graph tools mostly track files, classes, functions, imports, calls, and references; they miss how variable values move inside a function.
- This matters because line- and function-level localization are a main failure point in SWE-bench-style repair.

## Approach
- ARISE builds a typed graph for Python repositories with Directory, Module, Class, Function, Method, and Statement nodes.
- It adds Contains, Imports, Calls, Inherits, and intra-procedural DataflowDefUse/DataflowUseDef edges.
- The data-flow pass scans each function body, records top-level statements, finds variable definitions and uses, and connects each use to the last preceding definition in the same function.
- The agent gets a three-tier API: structural navigation, data-flow slicing, and context bundling. The main tool returns backward, forward, or bidirectional slices for a chosen variable and statement.
- The evaluation uses SWE-agent with Qwen2.5-Coder-32B-Instruct on SWE-bench Lite.

## Results
- SWE-bench Lite contains 300 real GitHub issues from 11 Python repositories.
- Against unmodified SWE-agent, ARISE improves Function Recall@1 by 17.0 points.
- Against the same baseline, ARISE improves Line Recall@1 by 15.0 points.
- ARISE reaches 22.0% Pass@1, fixing 66/300 issues, a 4.7 percentage-point gain over SWE-agent. This implies the baseline fixed about 52/300 issues, or 17.3% Pass@1.
- Ablations attribute the gain to the data-flow graph; the tool-schema-only condition does not match it.
- The paper reports that Qwen2.5-Coder-32B-Instruct can use structured slice output directly, without a natural-language summary layer.

## Link
- [https://arxiv.org/abs/2605.03117v1](https://arxiv.org/abs/2605.03117v1)
