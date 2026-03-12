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
---

# Oly – Run AI agents, close your terminal, intervene when it needed from anywhere

## Summary
Oly 是一个面向长时间运行 CLI AI 代理的会话持久化 PTY 守护进程：即使关闭终端，代理也会继续运行，并在需要人工介入时通知你。它的价值在于把“盯着终端 babysit 代理”变成“异步监督+按需介入”，更适合真实的软件工程工作流。

## Problem
- 长时间运行的 CLI 代理在遇到 `y/n`、权限确认或不确定决策时会卡住，用户不得不一直保持终端开启并守在电脑前。
- 终端关闭通常意味着会话中断、上下文丢失或需要重新连接，降低了 AI 代理在实际开发中的可用性。
- 人类需要保留审批和干预权，但不应该为此持续同步等待；这对人机协作和多代理监督流程很重要。

## Approach
- 核心机制是一个**后台 PTY 守护进程**：它接管并持有代理会话，因此关闭本地终端后任务仍持续运行。
- 它会**缓冲并回放输出**，用户重新附着时可以看到期间发生了什么，避免丢失上下文。
- 它会**检测可能需要人工输入的状态**并发出通知，让用户只在关键时刻介入。
- 用户可通过命令或浏览器**远程注入输入**（如发送 `yes` 或回车），甚至无需重新附着完整终端。
- 系统支持**审计日志、外部认证网关接入、以及 supervisor agent 监督其他 agent 并向人升级决策**，形成“人始终在环但无需持续盯守”的机制。

## Results
- 文本**未提供标准学术基准或定量实验结果**，没有数据集、准确率、通过率、时延对比或消融数字。
- 论文/项目声称可让代理任务在**关闭终端后继续运行**，解决“运行 20 分钟、中途因 `y/n` 提示而卡住”的典型场景。
- 声称支持**不中断地远程介入**：例如通过 `oly input <id> --text "yes" --key enter` 直接向会话注入响应。
- 声称支持**浏览器访问与推送通知**，从而“from anywhere” 进行会话管理和人工审批。
- 声称具备**完整动作审计**与**无内建公网监听器**的部署方式，强调通过 Cloudflare Access、Tailscale 等外部认证代理实现受控暴露。
- 声称支持**多节点/次级节点会话管理**与“一个 agent 监督另一个 agent”的升级式工作流，但未给出成功率、效率增益或用户研究数字。

## Link
- [https://github.com/slaveOftime/open-relay](https://github.com/slaveOftime/open-relay)
