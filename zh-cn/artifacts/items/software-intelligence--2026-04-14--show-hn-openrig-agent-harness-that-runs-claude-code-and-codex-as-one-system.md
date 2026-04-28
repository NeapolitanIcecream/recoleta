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
language_code: zh-CN
---

# Show HN: OpenRig – agent harness that runs Claude Code and Codex as one system

## Summary
## 摘要
OpenRig 是一个开源本地系统，用于在一个共享拓扑中运行和管理一组编码代理，如 Claude Code 和 Codex。它重点解决多代理软件工作中的编排、恢复、可见性和操作控制。

## 问题
- 同时运行多个编码代理会导致会话蔓延、协作薄弱，以及在崩溃或重启后的恢复能力差。
- 现有代理运行时通常绑定单一厂商或单一托管环境，这限制了混合代理团队和本地控制。
- 团队需要一种方式来定义代理角色、通信路径和生命周期规则，使代理系统可以像软件一样被复现和管理。

## 方法
- OpenRig 用 YAML 中的 RigSpec 对象定义多代理团队，描述 pods、成员、边、连续性策略和共享文化规则。
- 它在受管的 tmux 会话中启动每个代理，然后提供 CLI、本地守护进程、MCP 服务器和 React UI，用于检查、控制、发送消息、扩展、缩减、快照和恢复运行中的拓扑。
- 它支持混合运行时，内置 Claude Code、Codex 和普通终端节点的适配器，因此一个 rig 可以组合多个编码代理。
- 它可以发现现有 tmux 会话并将其纳入管理，然后在关闭时保存完整拓扑，并在之后按名称恢复。
- 它通过 MCP 向代理暴露工具，使代理可以用 `rig_up`、`rig_ps`、`rig_send` 和 `rig_chatroom_send` 等命令管理其自身拓扑的一部分。

## 结果
- 项目声称提供了一个端到端演示，并且已在全新的 macOS VM 上跑通，剩余需要人工处理的步骤仅限于 Claude/OpenAI 的 OAuth 登录和权限提示。
- 附带的演示 rig 会启动 **3 个 pods** 和 **8 个节点**，使用混合运行时，包括两个 orchestrator、implementation、QA、design 和两个 reviewer。
- 当前实现提供 **40+ 个 CLI 命令**、**17 个 MCP 工具** 和 **52 个领域服务**。
- 它支持快照和恢复，并可按节点报告恢复状态，如 resumed、fresh 或 failed，但摘录没有给出恢复速度、任务成功率或编码质量的基准数据。
- 它支持由服务支撑的 rig，文中给出的具体例子是一个 specialist agent 通过打包的 `secrets-manager` rig 管理 HashiCorp Vault 实例。
- 摘录给出了产品和架构层面的说法，但没有提供与其他多代理编码系统或单代理基线的受控量化对比。

## Problem

## Approach

## Results

## Link
- [https://github.com/mvschwarz/openrig](https://github.com/mvschwarz/openrig)
