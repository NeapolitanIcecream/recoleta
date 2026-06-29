---
source: arxiv
url: https://arxiv.org/abs/2606.26924v1
published_at: '2026-06-25T12:02:18'
authors:
- Padmaraj Madatha
topics:
- llm-coding-agents
- code-governance
- agent-configuration
- software-supply-chain
- ide-agents
- human-ai-interaction
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# A Deterministic Control Plane for LLM Coding Agents

## Summary
The paper proposes Rel(AI)Build, a deterministic control plane for LLM coding-agent configurations. It treats prompts, permissions, and workflow state as managed artifacts with hashes, lockfiles, audit logs, pre-tool checks, and target-specific compilers.

## Problem
- LLM coding agents can read and write files and run shell commands, but their rule files, agent definitions, and IDE markdown configs often lack provenance, permission boundaries, and traceable change history.
- A study of 10,008 public GitHub repositories found repeated and weakly maintained agent configs, which matters because these files steer agents with high-impact access.
- Agent expertise is tied to tool-specific dialects such as Claude Code, Cursor, Copilot, Aider, Codex, and Windsurf, which makes shared policy hard to maintain across teams.

## Approach
- Rel(AI)Build adds a control plane above existing IDE coding harnesses. It does not replace model inference, code indexing, or the editing loop.
- It content-addresses agent resources with SHA-256, writes HMAC-stamped lockfiles, and records mutations in hash-chained JSONL audit logs.
- It assigns each agent a permission tier, checks tool allowlists before install or transform, and blocks risky commands and write paths before tool execution.
- It gates work through a phase state machine with requirement, file, and test trace artifacts. Trace linkage depends on agent cooperation and is audited after the fact.
- It compiles one canonical Markdown+YAML agent definition into seven IDE targets and detects prompt drift with Jaccard similarity.

## Results
- In 10,008 public GitHub repositories with 6,145 agent config files, 10.1% of tracked config paths were exact duplicates after fork adjustment, measured by SHA-256.
- Among duplicate clone pairs, 75.5% crossed organizational boundaries, which supports the claim that agent configs propagate as undeclared shared components.
- 58% of agent config files had a single commit. After age normalization, agent configs averaged 0.4 commits/month versus 0.6 commits/month for CI/CD workflows in the same repositories.
- Fewer than 1% of agent config files declared permission boundaries, compared with 33% of GitHub Actions workflows. The paper labels this result fragile because the parser found only 31 true positives.
- The corpus showed 3.18% credential-pattern hits and six agent-config dialects.
- Conformance tests with injected violations at N=10, N=15, and N=20 confirmed that the implementation enforces its stated invariants. The paper does not claim developer productivity gains; controlled developer outcomes are future work.

## Link
- [https://arxiv.org/abs/2606.26924v1](https://arxiv.org/abs/2606.26924v1)
