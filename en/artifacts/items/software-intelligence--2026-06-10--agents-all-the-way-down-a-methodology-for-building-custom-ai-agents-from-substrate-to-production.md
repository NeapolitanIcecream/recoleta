---
source: arxiv
url: https://arxiv.org/abs/2606.11869v1
published_at: '2026-06-10T09:44:54'
authors:
- Marc Alier Forment
- Juanan Pereira
- "Francisco Jos\xE9 Garc\xEDa-Pe\xF1alvo"
- "Mar\xEDa Jos\xE9 Casa\xF1 Guerrero"
topics:
- custom-ai-agents
- agent-engineering
- multi-agent-software-engineering
- llm-tool-use
- agent-evaluation
- cli-orchestration
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Agents All the Way Down; A Methodology for Building Custom AI Agents from Substrate to Production

## Summary
The paper proposes "Agents All the Way Down", a five-phase method for building custom AI agents inside real products. It focuses on turning prototypes made with general-purpose code agents into shipped CLI-based agents with scenario testing.

## Problem
- Engineers need agents that use private tools, product data, security rules, audit logs, and domain language inside their own applications.
- The paper argues that existing sources explain separate pieces such as function calling, MCP, CLIs, ReAct, Reflexion, and code agents, but do not connect them into one end-to-end build practice.
- The gap matters because custom agents need predictable cost, maintainable code, product integration, and testing beyond normal deterministic software tests.

## Approach
- P1 treats the LLM as a software component and organizes prompts around `tools -> system -> messages` so stable content stays cacheable and dynamic content stays in message history.
- P2 defines the building blocks: function calling, MCP, CLI tools, the liteshell pattern, agent loops, skills, characters, hooks, and scaffolding.
- P3 uses a general-purpose code agent such as Claude Code, OpenCode, or Cursor to prototype against the real application.
- P4 harvests the prototype's tools, prompts, skills, security checks, and instructions into a small custom agent loop shipped as a CLI, called the Turtle pattern.
- P5 uses a general-purpose agent to drive the custom agent through behavioral scenarios; this complements unit, integration, and end-to-end tests.

## Results
- The claimed method has 5 phases: 2 prerequisites, P1 and P2, followed by a repeated 3-step loop, P3 -> P4 -> P5.
- The main worked example is AAC for the LAMB educational platform: built in about 10 days by 1 developer with an AI pair-programmer, then deployed at 2 universities for about 200 educator-creators since April 2026.
- For CLI versus MCP cost, the paper cites a controlled matched-task benchmark reporting about 35x more tokens via MCP than via CLI, with hard-scenario completion reliability at 72% for MCP versus 100% for CLI.
- It cites a GitHub language-check case using about 44,026 tokens through a matching MCP server versus about 1,365 tokens through the `gh` CLI.
- It cites another GitHub MCP case where 93 exposed tools add about 55,000 registry tokens at session start, compared with about 200 tokens for the `gh` equivalent.
- The paper does not provide a controlled quantitative evaluation of the full five-phase method; its security benefit is presented as a design argument, with dependency-count and attack-surface measurement left for future work.

## Link
- [https://arxiv.org/abs/2606.11869v1](https://arxiv.org/abs/2606.11869v1)
