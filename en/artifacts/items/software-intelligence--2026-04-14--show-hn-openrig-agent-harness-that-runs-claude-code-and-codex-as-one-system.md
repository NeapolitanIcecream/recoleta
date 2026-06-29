---
source: hn
url: https://github.com/mvschwarz/openrig
published_at: '2026-04-14T23:46:40'
authors:
- mschwarz
topics:
- multi-agent-orchestration
- code-agents
- developer-tooling
- agent-runtime
- tmux-based-systems
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Show HN: OpenRig – agent harness that runs Claude Code and Codex as one system

## Summary
OpenRig is an open-source local system for running and managing a team of coding agents such as Claude Code and Codex in one shared topology. It focuses on orchestration, recovery, visibility, and operator control for multi-agent software work.

## Problem
- Running several coding agents at once creates session sprawl, weak coordination, and poor recovery after crashes or reboots.
- Existing agent runtimes are often tied to one vendor or one hosted environment, which limits mixed-agent teams and local control.
- Teams need a way to define agent roles, communication paths, and lifecycle rules so the agent system can be reproduced and managed like software.

## Approach
- OpenRig defines a multi-agent team in YAML with RigSpec objects that describe pods, members, edges, continuity policies, and shared culture rules.
- It starts each agent in a managed tmux session, then provides a CLI, local daemon, MCP server, and React UI to inspect, control, message, expand, shrink, snapshot, and restore the running topology.
- It supports mixed runtimes, with built-in adapters for Claude Code, Codex, and plain terminal nodes, so one rig can combine multiple coding agents.
- It can discover existing tmux sessions and adopt them into management, then save the full topology on shutdown and restore it later by name.
- It exposes agent-facing tools through MCP so agents can manage parts of their own topology with commands such as `rig_up`, `rig_ps`, `rig_send`, and `rig_chatroom_send`.

## Results
- The project claims an end-to-end demo that has been run on fresh macOS VMs, with the remaining manual steps limited to OAuth logins for Claude/OpenAI and permission prompts.
- The included demo rig starts **3 pods** and **8 nodes** with mixed runtimes, including two orchestrators, implementation, QA, design, and two reviewers.
- The system exposes **40+ CLI commands**, **17 MCP tools**, and **52 domain services** in its current implementation.
- It supports snapshot and restore with per-node restore status reporting such as resumed, fresh, or failed, but the excerpt gives no benchmark numbers for restore speed, task success rate, or coding quality.
- It supports service-backed rigs, with a concrete example where a specialist agent manages a HashiCorp Vault instance through a packaged `secrets-manager` rig.
- The excerpt provides product and architecture claims, but no controlled quantitative comparison against other multi-agent coding systems or against single-agent baselines.

## Link
- [https://github.com/mvschwarz/openrig](https://github.com/mvschwarz/openrig)
