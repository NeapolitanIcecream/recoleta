---
source: arxiv
url: https://arxiv.org/abs/2606.09182v1
published_at: '2026-06-08T08:20:50'
authors:
- Kehui Chen
- Yicheng Sun
- Jacky Keung
- Zhenyu Mao
- Xiaoxue Ma
topics:
- model-context-protocol
- llm-software-engineering
- enterprise-adoption
- tool-integration
- human-ai-interaction
- agent-systems
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Understanding How Enterprises Adopt the Model Context Protocol for LLM-Driven Software Engineering

## Summary
The paper studies how enterprises adopt the Model Context Protocol (MCP) for LLM-driven software engineering through interviews with 20 practitioners. It finds that MCP helps LLMs connect to tools, files, databases, and internal systems, but teams still struggle with standards, compatibility, state handling, security, and fault diagnosis.

## Problem
- Enterprises want LLMs to run multi-step software engineering work across tools and internal systems, but plain function calling and ad hoc agent setups often lose context, increase integration work, and create maintenance costs.
- Prior MCP research has focused on benchmarks, integration, and security designs, with limited evidence from real enterprise deployments.
- The problem matters because MCP adoption depends on operational fit: compatibility, governance, auditability, fault recovery, and how teams use it in daily development work.

## Approach
- The authors ran semi-structured interviews with 20 MCP practitioners from 8 companies in Internet and financial sectors: 9 FinTech participants and 11 Internet participants.
- Participants covered host, client, server, and user roles, including senior architects, software developers, business analysts, and algorithm designers.
- The study used 3 pre-interviews to refine a 31-question interview guide, then formal 90–120 minute video interviews, producing about 400,000 words of transcript data.
- The authors also ran 10 follow-up interviews of 30 minutes each and used open coding, with Cohen’s kappa of 0.89 between coders.
- MCP’s core mechanism is a shared protocol layer with Host, Client, Server, and Resource roles, so an LLM can call external tools and exchange task context through a standard interface instead of custom links for each tool.

## Results
- 20 of 20 participants, or 100%, said MCP was important to their work.
- 16 of 20 participants, or 80%, said MCP improved efficiency by simplifying the connection between LLMs and external tools.
- 15 of 20 participants, or 75%, said MCP improved work patterns, including internal task management and standardized task execution.
- 14 of 20 participants, or 70%, said MCP lowered the technical barrier for operation and development.
- 16 of 20 participants, or 80%, said LLM+MCP is slightly more complex than LLM function calling, but needs less long-term development effort and gives better maintainability.
- 20 of 20 participants, or 100%, said fast fault localization was the main obstacle in troubleshooting; reported adoption issues also included fragmented standards, poor compatibility with tools such as LangGraph and ADK, cross-component coordination problems, distributed state management, and security concerns around data leakage, access control, auditability, and compliance.

## Link
- [https://arxiv.org/abs/2606.09182v1](https://arxiv.org/abs/2606.09182v1)
