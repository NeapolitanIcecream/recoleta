---
source: arxiv
url: https://arxiv.org/abs/2606.04769v1
published_at: '2026-06-03T11:51:32'
authors:
- Yutao Shi
- Xiaohan Zhang
- Xiangjing Zhang
- Xihua Shen
- Hui Ouyang
- Huming Qiu
- Mi Zhang
- Min Yang
topics:
- mcp-security
- tool-calling
- code-intelligence
- agent-safety
- static-analysis
- llm-evaluation
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Description-Code Inconsistency in Real-world MCP Servers: Measurement, Detection, and Security Implications

## Summary
The paper studies description-code inconsistency in MCP servers: tool descriptions tell an LLM one behavior while the code does something else. It defines the bug class, builds DCIChecker to detect it, and measures it across real MCP servers.

## Problem
- MCP agents choose tools from names, schemas, and natural-language descriptions. During planning, the LLM usually cannot inspect the code that will run.
- When a description omits behavior, overstates capability, or hides side effects, the agent may pick the wrong tool, trigger unwanted state changes, waste resources, or leak data.
- MCP does not require a check that tool descriptions match implementations, so stale docs, vague specs, feature drift, and malicious descriptions can all mislead agents.

## Approach
- The paper defines DCI with 2 main families and 7 subtypes: mismatched functionality covers undeclared, overclaimed, misclaimed, and ambiguous behavior; undeclared side effects cover resource overuse, state mutation, and data leakage.
- DCIChecker extracts each tool's name, schema, description, and entry function from 4 common MCP registration patterns.
- It uses AST-based interprocedural analysis to build a code bundle for each tool: entry code, project-local helper functions followed to depth k=3, and sensitive API calls with resolved arguments when possible.
- It compares the description and code bundle with Direct-Reverse-Arbitration prompting: one prompt checks consistency, one prompt searches for inconsistency, and a third prompt resolves label or subtype disagreement.
- The implementation uses claude-sonnet-4-5-20250929-thinking with temperature 0, top-p 1.0, and a 4,096-token generation limit.

## Results
- The measurement covers 19,200 description-code pairs from 2,214 real-world MCP servers.
- DCIChecker reports DCI in 9.93% of pairs, about 1,907 inconsistent tools out of 19,200.
- The paper says DCI has a long-tail distribution: a small fraction of servers account for most problematic tools, but the excerpt does not give the exact fraction.
- Functional misrepresentation is reported as the dominant DCI class, with overclaimed functionality called out as common; the excerpt does not give subtype counts.
- The paper claims Direct-Reverse-Arbitration improves precision and recall over one-sided prompting, but the excerpt does not provide the exact precision, recall, or baseline numbers.
- Reported security effects include tool invocation failures, incorrect tool prioritization, unintended system behavior, and stronger tool poisoning attacks; the excerpt gives no attack success-rate numbers.

## Link
- [https://arxiv.org/abs/2606.04769v1](https://arxiv.org/abs/2606.04769v1)
