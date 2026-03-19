---
source: hn
url: https://github.com/slaveOftime/open-relay
published_at: '2026-03-08T23:18:58'
authors:
- binwen
topics:
- cli-agent-ops
- human-in-the-loop
- session-persistence
- remote-intervention
- pty-daemon
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Oly – Run AI agents, close your terminal, intervene when it needed from anywhere

## Summary
Oly is a session-persistent PTY daemon for long-running CLI agents, allowing tasks to continue after the user closes the terminal and enabling intervention from anywhere when human input is needed. It addresses the practical workflow pain point of having to babysit an agent in the terminal, emphasizing auditable, remote, human-in-the-loop control.

## Problem
- Long-running CLI agents can get stuck when they encounter `y/n`, permission confirmations, or uncertain decisions, forcing users to keep the terminal open and remain on watch.
- Closing the terminal interrupts normal sessions, causing loss of context, task failure, or requiring reattachment before work can continue.
- This limits the usability of human-supervised multi-agent/agent workflows, especially in scenarios that require asynchronous approval, remote intervention, and audit records.

## Approach
- The core mechanism is a **background PTY daemon**: it "owns" and maintains the agent's terminal session, so even if the user closes the terminal, the process and interaction context continue to exist.
- It **buffers and replays output**, so when users reattach they can see prior logs and avoid losing context.
- It **detects moments when human input is likely needed** and sends notifications, so users intervene only at key points instead of watching continuously.
- Users can **inject input directly without attaching a terminal** (such as sending `yes` or pressing Enter), or fully attach and take over; all actions are recorded in audit logs.
- Remote access is not exposed through a built-in network listener, but instead accessed through user-selected authenticated gateways/tunnels (such as Cloudflare Access, Tailscale), emphasizing security control and deployability.

## Results
- The text does not provide standard paper-style quantitative experimental results, so there are **no public accuracy, success rate, latency, or benchmark comparison figures**.
- It explicitly claims support for multiple kinds of CLI agents/tools, such as **Claude Code, Gemini CLI, OpenCode**, as well as ordinary CLI programs.
- Supports **session persistence**: sessions continue running after the terminal is closed and are not terminated when the shell exits.
- Supports **remote human intervention**: stalled tasks can be resumed via `oly input <id> --text "yes" --key enter` without attaching a terminal.
- Supports **browser access and push notifications**, and sessions can be managed from "anywhere" through an authenticated proxy + tunnel, but the text does not provide throughput, concurrency, or reliability figures.
- Supports **multi-node/sub-node target control** (`--node <name>`) and complete audit logs; the strongest concrete claim is that it keeps humans in the loop without requiring them to continuously watch the agent.

## Link
- [https://github.com/slaveOftime/open-relay](https://github.com/slaveOftime/open-relay)
