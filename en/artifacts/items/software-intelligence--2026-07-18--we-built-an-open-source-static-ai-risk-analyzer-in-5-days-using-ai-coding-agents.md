---
source: hn
url: https://github.com/ikaruscareer/SafeAI
published_at: '2026-07-18T22:24:40'
authors:
- ikaruscareer
topics:
- code-intelligence
- ai-agent-security
- static-analysis
- software-supply-chain
- mcp-security
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# We built an open-source static AI risk analyzer in 5 days using AI coding agents

## Summary
SafeAI is an open-source static analyzer that finds security, capability, and governance risks in AI-agent source code before deployment. It operates offline, produces deterministic risk scores and CI-compatible reports, and complements runtime testing rather than replacing it.

## Problem
- Conventional SAST, software-composition analysis, and infrastructure scanning do not directly identify agent-specific risks such as prompt injection, tool misuse, MCP exposure, capability sprawl, or missing governance controls.
- Detecting these issues before deployment matters because agents may expose shell, filesystem, database, or external-service capabilities through framework code and configuration.

## Approach
- Detects AI frameworks and agent capabilities through imports, configurations, dependencies, AST parsing, framework-specific object fingerprints, and fallback regular expressions.
- Maps detected capabilities to normalized risk categories and applies configurable rules with severity and weighting.
- Computes a deterministic category-weighted trust score from 0 to 100 and attaches evidence, confidence, resolved definitions, and provenance to findings.
- Runs entirely offline without executing agents or calling LLMs, then exports terminal, JSON, SARIF 2.1.0, and HTML reports for CI/CD integration.

## Results
- In the included scan example, SafeAI analyzed 12 files, detected the LangGraph and CrewAI frameworks plus 2 MCP assets, and produced an overall AI Risk Score of 73.
- The same scan reported 9 findings: 1 critical, 3 high, and 5 medium; examples included untrusted input interpolated into a prompt, detected shell execution, and missing MCP authentication.
- The tool supports detection for at least 8 named framework or platform integrations, including LangGraph, CrewAI, LangChain, Semantic Kernel, OpenAI Agents SDK, Microsoft Agent Framework, Azure AI Foundry, and Bedrock Agent.
- The provided material reports no independent benchmark, precision/recall evaluation, or comparative performance results; capability coverage is incomplete for some MCP-based capabilities, whose framework adapters are planned.

## Link
- [https://github.com/ikaruscareer/SafeAI](https://github.com/ikaruscareer/SafeAI)
