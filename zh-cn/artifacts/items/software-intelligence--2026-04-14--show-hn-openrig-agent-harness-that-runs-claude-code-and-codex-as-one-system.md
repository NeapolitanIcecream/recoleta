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
OpenRig 是一个开源的本地系统，用来在一个共享拓扑中运行和管理一组编码代理，比如 Claude Code 和 Codex。它把重点放在多代理软件工作的编排、恢复、可见性和操作控制上。

## 问题
- 同时运行多个编码代理会带来会话分散、协作薄弱，以及崩溃或重启后的恢复能力差。
- 现有代理运行时通常绑定单一厂商或单一托管环境，这限制了混合代理团队和本地控制。
- 团队需要一种方式来定义代理角色、通信路径和生命周期规则，这样代理系统才能像软件一样被复现和管理。

## 方法
- OpenRig 用 YAML 中的 RigSpec 对象定义一个多代理团队，这些对象描述 pod、成员、边、连续性策略和共享文化规则。
- 它把每个代理启动在受管的 tmux 会话中，然后提供 CLI、本地守护进程、MCP 服务器和 React UI，用来检查、控制、消息传递、扩展、缩减、快照和恢复正在运行的拓扑。
- 它支持混合运行时，内置 Claude Code、Codex 和普通终端节点的适配器，因此一个 rig 可以组合多个编码代理。
- 它可以发现现有的 tmux 会话并把它们纳入管理，然后在关闭时保存完整拓扑，并在之后按名称恢复。
- 它通过 MCP 向代理暴露工具，这样代理可以用 `rig_up`、`rig_ps`、`rig_send` 和 `rig_chatroom_send` 等命令管理自己拓扑的一部分。

## 结果
- 该项目声称已经在全新的 macOS 虚拟机上完成了端到端演示，剩下的手动步骤只包括 Claude/OpenAI 的 OAuth 登录和权限提示。
- 随附的 demo rig 启动 **3 个 pod** 和 **8 个节点**，运行混合运行时，包括两个协调器、实现、QA、设计和两个审阅者。
- 该系统当前实现中暴露了 **40+ 个 CLI 命令**、**17 个 MCP 工具** 和 **52 个领域服务**。
- 它支持带快照和恢复的流程，并按节点报告恢复状态，比如 resumed、fresh 或 failed，但节选没有给出恢复速度、任务成功率或代码质量的基准数据。
- 它支持由服务驱动的 rig，举例中一个专门代理通过打包的 `secrets-manager` rig 管理一个 HashiCorp Vault 实例。
- 这段节选提供了产品和架构层面的主张，但没有给出与其他多代理编码系统或单代理基线的受控定量比较。

## Problem

## Approach

## Results

## Link
- [https://github.com/mvschwarz/openrig](https://github.com/mvschwarz/openrig)
