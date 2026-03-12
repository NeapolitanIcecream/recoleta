---
source: hn
url: https://github.com/goshtasb/OmniGlass
published_at: '2026-03-02T23:51:00'
authors:
- goshtasb
topics:
- desktop-ai
- screen-understanding
- mcp-plugins
- sandboxing
- local-first
relevance_score: 0.06
run_id: materialize-outputs
---

# Show HN: OmniGlass – Executable AI screen snips with kernel-level sandboxing

## Summary
OmniGlass 是一个把“屏幕截图理解”直接连接到“可执行动作”的本地优先平台，而不只是返回文本回答。它强调零信任执行与插件化扩展，让用户从截图或文本输入直接触发自动化操作。

## Problem
- 现有桌面 AI 工具通常只能“看图后聊天”，不能把识别到的上下文安全地转化为可执行操作。
- 直接让插件或桌面代理以用户权限运行会带来严重安全风险，例如读取 SSH 密钥、环境变量或浏览器 Cookie。
- 开发这类自动化通常需要自己处理截图、OCR、提示工程和工具调用链，开发门槛高且不稳定。

## Approach
- 核心机制很简单：用户截图或输入文本后，系统先在本地做 OCR，再把提取文本送给 LLM 进行分类与动作生成，最后把候选操作作为按钮呈现，用户点击后执行。
- 执行层基于 MCP（Model Context Protocol）插件系统；插件开发者不需要写复杂提示词，而是接收结构化 JSON，然后调用目标 API。
- 安全上主打“零信任执行引擎”：插件通过内建处理器或沙箱化 MCP 插件运行，并宣称使用内核级 sandbox-exec 配置文件隔离权限。
- 隐私上强调本地优先：OCR 在设备端完成；没有 OmniGlass 服务器；API key 直接与模型提供商通信；也支持用 llama.cpp 本地运行 Qwen-2.5-3B 完成全离线流程。

## Results
- 声称从 OCR 文本送入 LLM 到返回动作菜单的延迟**低于 1 秒**，但未提供标准基准、测试条件或对比系统。
- 声称在**无 API key**场景下，可用本地 **Qwen-2.5-3B** 通过 llama.cpp 跑完整离线管线，耗时约 **6 秒**。
- 声称插件可非常轻量，社区示例定位为**100 行以内**即可实现多种工作流自动化；给出的 Slack 示例基本就是一个极简 MCP 工具与清单文件。
- 安全方面的最强具体声明是：若插件进程能够读取 `~/.ssh/id_rsa`，即说明出现严重漏洞；但文中**没有提供正式安全评测、攻击成功率、或与 Claude Desktop 等基线的量化比较**。

## Link
- [https://github.com/goshtasb/OmniGlass](https://github.com/goshtasb/OmniGlass)
