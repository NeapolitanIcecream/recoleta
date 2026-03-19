---
source: hn
url: https://github.com/slaveOftime/open-relay
published_at: '2026-03-08T23:18:58'
authors:
- binwen
topics:
- cli-agent-runtime
- human-in-the-loop
- session-persistence
- remote-intervention
- multi-agent-supervision
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Oly – Run AI agents, close your terminal, intervene when it needed from anywhere

## Summary
Oly is a session-persistent PTY daemon for long-running CLI AI agents: even if you close the terminal, the agent keeps running and notifies you when human intervention is needed. Its value is turning “babysitting an agent while staring at a terminal” into “asynchronous supervision + intervene on demand,” which is better suited to real software engineering workflows.

## Problem
- Long-running CLI agents can get stuck when they encounter `y/n`, permission confirmations, or uncertain decisions, forcing users to keep the terminal open and stay at their computer.
- Closing the terminal usually means the session is interrupted, context is lost, or reconnection is required, reducing the practicality of AI agents in real development work.
- Humans need to retain approval and intervention authority, but should not have to wait synchronously the whole time; this is important for human-AI collaboration and multi-agent supervision workflows.

## Approach
- The core mechanism is a **background PTY daemon**: it takes over and holds agent sessions, so tasks continue running after the local terminal is closed.
- It **buffers and replays output**, so when users reattach they can see what happened in the meantime and avoid losing context.
- It **detects states that likely require human input** and sends notifications, so users only intervene at critical moments.
- Users can **inject input remotely** via commands or a browser (such as sending `yes` or Enter), without even needing to fully reattach to the terminal.
- The system supports **audit logs, integration with external authentication gateways, and supervisor agents overseeing other agents and escalating decisions to humans**, creating a mechanism where “humans are always in the loop without needing to watch continuously.”

## Results
- The text **does not provide standard academic benchmarks or quantitative experimental results**; there are no datasets, accuracy figures, pass rates, latency comparisons, or ablation numbers.
- The paper/project claims it allows agent tasks to **keep running after the terminal is closed**, addressing the typical scenario where a task runs for 20 minutes and gets stuck midway on a `y/n` prompt.
- It claims to support **remote intervention without interruption**: for example, injecting a response directly into a session via `oly input <id> --text "yes" --key enter`.
- It claims to support **browser access and push notifications**, enabling session management and human approval “from anywhere.”
- It claims to provide **complete action auditing** and a deployment model with **no built-in public network listener**, emphasizing controlled exposure through external authentication proxies such as Cloudflare Access and Tailscale.
- It claims to support **multi-node/secondary-node session management** and an escalatory workflow where “one agent supervises another agent,” but provides no success-rate, efficiency-gain, or user-study metrics.

## Link
- [https://github.com/slaveOftime/open-relay](https://github.com/slaveOftime/open-relay)
