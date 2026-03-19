---
source: hn
url: https://github.com/goshtasb/OmniGlass
published_at: '2026-03-02T23:51:00'
authors:
- goshtasb
topics:
- desktop-ai
- mcp-plugins
- screen-understanding
- sandboxed-execution
- local-llm
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: OmniGlass – Executable AI screen snips with kernel-level sandboxing

## Summary
OmniGlass 是一个把屏幕截图直接转成可执行操作的本地开源平台，而不是只给出聊天式回答。它强调零信任插件执行、内核级沙箱和本地 OCR/可选本地模型，以降低把屏幕内容交给 AI 时的安全风险。

## Problem
- 现有桌面 AI 工具通常只能“看图说话”，无法把识别出的上下文直接转成可执行工作流，导致从理解到操作之间仍需人工切换和复制粘贴。
- 直接让 AI 插件或桌面代理以用户权限运行有明显安全隐患：恶意插件或提示注入可能读取 SSH 密钥、`.env`、浏览器 Cookie 等敏感数据。
- 开发这类自动化能力通常要自己处理截图、OCR、提示工程和工具调用链，门槛高，不利于快速扩展生态。

## Approach
- 核心机制很简单：用户截图或输入文本，系统先在本地做 OCR，再把提取的文本送给 LLM，让模型判断内容类型并生成一组可执行动作菜单，用户点击后再真正执行。
- 整个管线是 `Screen/Input -> OCR -> LLM classification -> action menu -> execution`；其中执行既可走内置处理器，也可走 MCP 插件。
- 插件开发被简化为“接收结构化 JSON 后调用 API”：OmniGlass 负责前面的截图理解和提示流程，开发者主要写工具接口和权限声明即可。
- 安全上主打零信任执行：插件运行在内核级 `sandbox-exec` 沙箱中，并通过 manifest 声明网络等权限，降低插件获得完整用户权限的风险。
- 部署上强调本地与隐私：无 OmniGlass 中转服务器，OCR 在设备端完成；可直接调用 Claude/Gemini，也可离线运行本地 Qwen-2.5-3B（经 llama.cpp）。

## Results
- 文中宣称动作菜单可在 **1 秒内** 返回（LLM 完成分类并生成可执行菜单），这是其主要交互性能指标。
- 在无 API key 的离线模式下，使用 **Qwen-2.5-3B + llama.cpp** 可实现“完整管线”约 **6 秒** 完成，且**全程离线**。
- 插件开发效率的核心主张是：社区示例插件可做到 **整个插件约 100 行以内**，文中展示的 Slack 插件基本就是单个 `index.js` + manifest。
- 项目声称插件开发可在 **5 分钟** 内从零到可用，但这是文档中的开发体验承诺，不是严格实验结果。
- 没有给出标准学术数据集、准确率、成功率或与基线系统的定量对比；最强的具体结果主要是**<1 秒菜单返回、~6 秒本地离线全流程、内核级沙箱隔离**这些工程指标与安全主张。

## Link
- [https://github.com/goshtasb/OmniGlass](https://github.com/goshtasb/OmniGlass)
