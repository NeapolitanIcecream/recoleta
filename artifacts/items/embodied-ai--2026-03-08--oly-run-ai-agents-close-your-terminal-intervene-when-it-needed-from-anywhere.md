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
---

# Oly – Run AI agents, close your terminal, intervene when it needed from anywhere

## Summary
Oly 是一个面向长时运行 CLI 智能体的会话持久化 PTY 守护进程，让用户关闭终端后任务仍可继续，并在需要人工介入时从任意位置干预。它解决了“必须盯着终端 babysit agent”的实际工作流痛点，强调可审计、可远程、人在回路中的控制。

## Problem
- 长时间运行的 CLI 智能体在遇到 `y/n`、权限确认或不确定决策时会卡住，迫使用户保持终端开启并持续值守。
- 关闭终端会中断常规会话，导致上下文丢失、任务失败或需要重新附着才能继续操作。
- 这限制了人类监督多智能体/代理工作流的可用性，尤其是在需要异步审批、远程介入和审计记录的场景中。

## Approach
- 核心机制是一个**后台 PTY 守护进程**：它“拥有”并维持 agent 的终端会话，所以即使用户关闭终端，进程和交互上下文仍持续存在。
- 它会**缓冲并回放输出**，用户重新附着时可以看到先前日志，避免丢失上下文。
- 它会**检测可能需要人类输入的时刻**并发送通知，使用户只在关键节点介入，而不是全程盯守。
- 用户可以**不附着终端直接注入输入**（如发送 `yes` 或按 Enter），也可以真正附着接管；所有动作都被记录为审计日志。
- 远程访问不通过内置网络监听器暴露，而是通过用户自选的认证网关/隧道（如 Cloudflare Access、Tailscale）接入，强调安全控制和可部署性。

## Results
- 文本未提供标准论文式定量实验结果，因此**没有公开的准确率、成功率、延迟或基准对比数字**。
- 明确声称可支持多类 CLI agent / 工具：如 **Claude Code、Gemini CLI、OpenCode** 以及普通 CLI 程序。
- 支持**会话持久化**：关闭终端后会话继续运行，不因 shell 退出而终止。
- 支持**远程人工介入**：可通过 `oly input <id> --text "yes" --key enter` 在不附着终端的情况下恢复卡住任务。
- 支持**浏览器访问与推送通知**，并可通过认证代理 + 隧道从“任意位置”管理会话，但文中未给出吞吐、并发或可靠性数字。
- 支持**多节点/次级节点目标控制**（`--node <name>`）和完整审计日志，最强的具体主张是把人保留在回路中，但不必持续盯着 agent。

## Link
- [https://github.com/slaveOftime/open-relay](https://github.com/slaveOftime/open-relay)
