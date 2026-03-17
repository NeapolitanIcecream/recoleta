---
source: hn
url: https://rolandsharp.com/ssh-is-the-agent-internet/
published_at: '2026-03-10T23:49:52'
authors:
- epscylonb
topics:
- ssh
- agent-infrastructure
- git-based-workflow
- multi-agent-communication
- terminal-ui
relevance_score: 0.87
run_id: materialize-outputs
---

# SSH Is the Agent Internet

## Summary
这篇文章主张把 **SSH+git** 作为面向 AI agent 的原生互联网栈，用统一的密钥身份、加密命令通道和仓库式存储替代复杂的 HTTP/API/OAuth 体系。作者以 sshmail 为例，展示了 agent 已能通过纯 SSH 命令和文件系统接口自主通信、协作与扩展功能。

## Problem
- 文章要解决的问题是：现有 HTTP 互联网主要为浏览器和文档检索设计，给 agent 做应用通信时需要叠加 API、OAuth、CORS、TLS 证书、token、客户端库等大量复杂层。
- 这很重要，因为 agent 真正需要的核心只有 **身份、通信、存储**；如果基础栈过重，会抬高 agent 间协作、自动化执行和系统集成的成本。
- 作者认为当前 web 应用栈的大量复杂性并非 agent 必需，限制了更直接的机器到机器交互与自动化软件生产模式。

## Approach
- 核心机制非常简单：**身份=SSH 密钥对，通信=SSH 加密命令，存储=git 仓库/文件系统**。也就是把“调用 API”改成“执行 SSH 命令”，把“应用状态/消息”改成“仓库中的文件与历史”。
- 作者实现了一个原型平台 **sshmail**：基于 Wish（Charmbracelet 的 SSH server 框架）和 SQLite，用单二进制部署消息系统；用户或 agent 通过 `ssh sshmail.dev send ...`、`inbox`、`poll` 等命令交互。
- 文章进一步提出 SSH-native 平台愿景：每个 agent 拥有一个通过 SSH 托管的 git repo，里面包含 profile、resume、blog、messages 等目录；消息写入仓库，读取靠 pull，协作靠 PR。
- 在这个模型里，招聘、群聊、公告板、文件传输、博客发布等都被统一为 SSH 命令和 git 工作流，文件系统本身就是接口，无需 SDK 或专门客户端。

## Results
- 定量结果基本没有：文中**没有给出标准数据集、评测指标、成功率、延迟、吞吐或与 HTTP 系统的基准对比数字**。
- 最强的实证性主张是：**“Within hours of launching”**，平台上线数小时内 AI agents 就开始自主使用 sshmail 收发消息和协作，但未报告具体 agent 数量、任务数或成功率。
- 作者声称已经在原型中支持多种功能：**direct messages、boards、private rooms、groups、file transfers**，并通过纯 SSH 命令完成操作。
- 文中还声称 agents 已在该系统上完成了若干真实互动行为：**发现彼此、提功能建议、讨论许可证、提交 PR、发布 web UI、压力测试群聊**，但同样未附带量化统计。
- 文章的突破性主张不是性能提升数字，而是架构层面的简化：将“GitHub + Slack + Substack”式能力收敛到 **SSH、git、SQLite** 三件套上，并认为这更适合作为 agent-native 基础设施。

## Link
- [https://rolandsharp.com/ssh-is-the-agent-internet/](https://rolandsharp.com/ssh-is-the-agent-internet/)
