---
source: arxiv
url: https://arxiv.org/abs/2607.07461v1
published_at: '2026-07-08T14:29:23'
authors:
- Yang Shi
- Jiaheng Fu
- Yihe Huang
- Ruixiang Wu
- Chengyao Sun
- Kaifeng Huang
topics:
- mcp-security
- llm-agents
- tool-use
- taint-analysis
- prompt-injection
- software-security
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Mitigating Taint-Style Vulnerabilities in MCP Servers via Security-Aware Tool Descriptions

## Summary
SpellSmith lowers taint-style exploit success in MCP servers by adding security guidance to MCP tool descriptions and adding a reflection step before tool use. The paper also reports a study of real MCP server vulnerabilities, where tainted input paths make up most disclosed cases.

## Problem
- MCP lets LLM agents call external tools, so a malicious prompt can push user-controlled text into commands, file paths, URLs, code, or database queries.
- This matters because 43 of 53 collected MCP server vulnerabilities, or 81.13%, are taint-style issues, and 75.47% are triggered during tool invocation.
- Code fixes are costly and uneven: repaired cases changed 203.6 lines, 5.5 functions, and 3.3 files on average, while 9.8% of repaired cases stayed exploitable.

## Approach
- SpellSmith reads MCP tool metadata, parameter meanings, and high-risk capabilities such as web access, file access, terminal execution, and database access.
- It builds a tool-level risk profile for possible taint-style failures, including SSRF, command injection, path traversal, code injection, and SQL injection.
- It rewrites the MCP tool Description field with security-aware instructions that tell the LLM which tool uses and parameter values are unsafe.
- It adds a self-reflection step before final tool execution so the LLM checks whether the planned invocation matches the authorized user intent and avoids unsafe arguments.

## Results
- The empirical study covers 100 GitHub MCP server projects, 1,856 MCP tools, and 53 vulnerability reports across 45 MCP servers.
- Security guidance is rare in existing metadata: 7.00% of top-level tool descriptions and 1.83% of parameter descriptions are security-aware.
- Taint-style vulnerabilities account for 43 of 53 cases, or 81.13%; command injection is the largest class with 27 cases, or 50.94%.
- Community response is slow: fixed vulnerabilities take 37.3 days on average, and unpatched vulnerabilities stay exposed for 92.3 days on average.
- On a benchmark of 792 malicious prompts, SpellSmith reports an attack success rate of 0.13% for taint-style vulnerability exploitation.
- The paper claims SpellSmith matches code-level mitigation effectiveness with lower repair cost and better reuse across vulnerability types, but the excerpt gives no exact comparative cost number for SpellSmith.

## Link
- [https://arxiv.org/abs/2607.07461v1](https://arxiv.org/abs/2607.07461v1)
