---
source: hn
url: https://github.com/beebeeVB/trajeckt/
published_at: '2026-06-29T23:52:48'
authors:
- beebeeVB
topics:
- ai-agent-security
- runtime-enforcement
- mcp
- data-exfiltration
- audit-logging
- tool-governance
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: A Firewall for AI agents with auditing

## Summary
## 摘要
trajeckt 是一个面向使用 MCP 通信的 AI Agent 的运行时网关。它通过密封的会话前承诺图和数据流跟踪，阻止不安全的多步骤工具序列。它的价值在于，按工具逐次授权可能会放行一次敏感读取后接一次外部写入，即使每次调用单独看都被允许。

## 问题
- Agent 安全检查通常一次只判断一个调用，例如 `(agent, tool, arguments)`，因此可能漏掉由调用顺序和数据移动造成的违规。
- 一次敏感数据库读取后接摘要生成和外部邮件发送，可能在每个单独工具调用都通过本地策略检查的情况下泄露数据。
- Agent 上下文被视为不可信，因此执行状态需要放在 Agent 之外，并在没有已批准计划时默认拒绝。

## 方法
- 执行前，trajeckt 创建或接受一个密封的 `CompiledGraph` (`Gτ`)，声明允许的工具、顺序、数据接收端、作用域和预算。该图使用 HMAC 密封，并安装到一个会话中。
- 每次工具调用都会根据密封图当前可达的前沿进行检查。图外调用、未安装图的会话，以及会话 ID 不匹配都会被拒绝。
- 网关跟踪来源和污点，因此敏感数据不能流入被禁止的接收端，即使经过摘要器等中间工具也一样。
- 当操作员退出承诺模式时，启发式安全底线会阻止已知模式，例如 `ReadSensitive → ExternalWrite` 和 `ShellExec → NetworkEgress`。
- 系统提供阻断原因、稳定的 `reason_code` 值、按会话记录的决策历史，以及用于审计的签名语料事件。

## 结果
- README 声称每次检查约 `1.6 ms`，执行具有确定性，并且不受 Agent 控制。
- 在随附的冒烟测试中，`read_database` 被允许，`summarize` 被允许，`send_email_external` 在完成一条外泄路径时被 HTTP `403` 阻断。
- 如果会话在未安装承诺的情况下到达 `tools/call`，会在评估前以 `no_commitment_installed` 被阻断；在所描述的网关路径中，`require_commitment_before_tools` 默认值为 `true`。
- MCP 网关为协议版本 `2025-11-25` 实现了 Streamable HTTP 传输的非流式配置，并通告 `2025-11-25`、`2025-06-18` 和 `2025-03-26`。
- 审计端点返回每个会话最近 `100` 条执行决策，`/corpus/stream` 通过 SSE 发送签名事件，并支持 `Last-Event-ID`。
- 评估证据有限：README 报告了一个 ClawTrojan 端到端案例 `cs_delay_002`，并覆盖了可信指令误报防护；尚未完成对全部 `20` 条 ClawTrojan 轨迹的套件级测量。

## Problem

## Approach

## Results

## Link
- [https://github.com/beebeeVB/trajeckt/](https://github.com/beebeeVB/trajeckt/)
