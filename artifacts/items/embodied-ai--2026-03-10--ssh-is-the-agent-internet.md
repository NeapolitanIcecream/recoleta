---
source: hn
url: https://rolandsharp.com/ssh-is-the-agent-internet/
published_at: '2026-03-10T23:49:52'
authors:
- epscylonb
topics:
- ssh
- ai-agents
- agent-communication
- git-based-platform
- developer-infrastructure
relevance_score: 0.12
run_id: materialize-outputs
---

# SSH Is the Agent Internet

## Summary
这篇文章主张用 **SSH + git** 作为 AI agent 的原生互联网栈，而不是继续依赖为浏览器设计的 HTTP/API 体系。作者通过一个名为 **sshmail** 的原型展示：agent 只靠 SSH 命令、文件系统和仓库即可完成身份、通信与存储。

## Problem
- 文章认为现有 **HTTP/Web API** 栈是为浏览器和文档检索设计的，给 agent 做应用交互时引入了过多额外复杂度，如 OAuth、API key、JSON 协议、TLS 证书、重试与限流处理。
- 对 AI agent 来说，真正需要的基础能力只有 **身份认证、加密通信、持久化存储**；若继续沿用 Web 栈，会增加集成成本、脆弱性和维护负担。
- 这很重要，因为如果 agent 之间与 agent-服务之间的交互协议过重，就会拖慢自动化协作、发现、任务执行与数据可携带性。

## Approach
- 核心思路很简单：把 **SSH 当作 agent 的原生网络协议**。身份就是 SSH 密钥对，通信就是经过认证和加密的远程命令，存储就是通过 **git repo** 和文件系统完成。
- 作者实现了一个原型系统 **sshmail**：基于 **Wish**（Charmbracelet 的 SSH server framework）和 **SQLite**，用一个 SSH 服务器二进制提供发消息、收件箱、轮询、群组、房间和文件传输等能力。
- 客户端并不是必须的，因为“服务器就是 CLI”：用户或 agent 直接执行诸如 `ssh sshmail.dev send ajax "done"` 之类的命令即可交互，不需要 SDK、浏览器或专门安装包。
- 为了让 agent 更容易处理数据，消息可以同步成 **Markdown 文件**，而更大的愿景是每个 agent 拥有一个经 SSH 托管的 **git 仓库**，其中包含 profile、resume、blog、messages 等目录；拉取、提交、PR 就成为发现、申请、审核、协作的通用机制。
- 文章进一步设想把招聘、发布、博客、聊天、归档和备份都统一到 **SSH + git + SQLite** 之上，形成“GitHub + Slack + Substack，但没有 HTTP”的平台。

## Results
- 没有给出正式论文式基准、实验数据或统计指标，因此**没有量化结果**可用于和现有 HTTP/API 系统做严格比较。
- 最强的实证性主张是：**“Within hours of launching, AI agents were using sshmail autonomously”**，即系统上线数小时内就已有 AI agent 自主读写消息并回复，但未提供数量、任务成功率或对照实验。
- 原型已支持的具体功能包括：**direct messages、boards、private rooms、groups、file transfers**；实现形态为 **one binary, one deploy**，后端存储使用 **SQLite**。
- 文中给出的关键操作路径高度简化：例如发送消息只需一条 `ssh ... send ...` 命令；作者声称相比 HTTP 方案，可省去 **TLS cert、DNS、API endpoint、JSON serialization、auth token、token refresh、rate limit handling、client library** 等整套组件。
- 作者还声称 agent 已经通过该 SSH 通道完成了若干真实协作行为，如**发现彼此、提功能建议、讨论许可、提交 PR、压力测试群聊、构建 Web UI**，但这些仍属于案例式观察，不是系统化评测。

## Link
- [https://rolandsharp.com/ssh-is-the-agent-internet/](https://rolandsharp.com/ssh-is-the-agent-internet/)
