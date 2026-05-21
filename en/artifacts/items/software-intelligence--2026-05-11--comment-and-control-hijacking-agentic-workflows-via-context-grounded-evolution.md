---
source: arxiv
url: https://arxiv.org/abs/2605.11229v1
published_at: '2026-05-11T20:45:31'
authors:
- Neil Fendley
- Zhengyu Liu
- Aonan Guan
- Jiacheng Zhong
- Yinzhi Cao
topics:
- agentic-workflows
- prompt-injection
- workflow-security
- llm-agents
- github-actions
- jailbreak-detection
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Comment and Control: Hijacking Agentic Workflows via Context-Grounded Evolution

## Summary
JAW finds and exploits hijackable LLM-agent workflows in GitHub Actions and n8n by combining workflow path analysis, runtime prompt tracing, capability probing, and payload evolution. The paper claims 4,174 hijackable GitHub workflows and 8 hijackable n8n templates, including cases that leak credentials.

## Problem
- Agentic workflows put attacker-controlled content, such as GitHub issue comments, into prompts for agents that may hold tokens, secrets, shell tools, APIs, or database access.
- Existing workflow scanners miss feasible agent-invocation paths and runtime prompt behavior; jailbreak work often assumes the attacker controls the full prompt, which does not match workflow templates.
- This matters because an outside user can steer a trusted workflow agent into credential exfiltration, unauthorized data access, or unwanted service requests.

## Approach
- JAW builds a Guarded Workflow Graph across workflow YAML, shell, JavaScript, Python, reusable actions, and n8n nodes, then solves path constraints to produce an event that reaches an agent call.
- It runs the workflow with canary-marked attacker fields and traces how those fields are transformed and inserted into the final model request.
- It profiles the agent's available tools and limits, such as command allowlists, path rules, sandboxing, environment filtering, and output channels.
- It evolves payloads against the recovered trigger conditions, prompt context, and tool limits so the same input can trigger the agent and drive an executable action chain.

## Results
- On real-world GitHub workflows and n8n templates, JAW found 4,174 hijackable GitHub workflows and 8 hijackable n8n templates.
- The findings covered 15 widely used GitHub Actions, including official actions for Claude Code, Gemini CLI, Qwen CLI, and Cursor CLI.
- The findings also covered 2 official n8n nodes.
- Reported impacts include credential leakage and arbitrary command execution when the agent has suitable runtime access.
- Vendors acknowledged and fixed multiple reports; the paper names GitHub, Google, Anthropic, and Snowflake as sources of bug bounties or acknowledgements.

## Link
- [https://arxiv.org/abs/2605.11229v1](https://arxiv.org/abs/2605.11229v1)
