---
source: arxiv
url: http://arxiv.org/abs/2604.14228v1
published_at: '2026-04-14T17:59:37'
authors:
- Jiacheng Liu
- Xiaohan Zhao
- Xinyi Shang
- Zhiqiang Shen
topics:
- ai-agents
- coding-agents
- agent-architecture
- code-intelligence
- multi-agent-systems
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems

## Summary
## 概述
本文通过源代码分析 Claude Code，把它当作一项关于现代编码代理如何构建的研究。它认为，主要代理逻辑很简单，而系统的大部分复杂度集中在权限、上下文管理、可扩展性、委派和持久化上。

## 问题
- 论文研究的是，一个生产级编码代理应如何处理运行 shell 命令、编辑文件和使用外部服务等自主动作，同时不失去用户控制或安全性。
- 这很重要，因为代理式编码工具面对的是自动补全工具不会遇到的设计问题：权限控制、长链路可靠性、上下文窗口限制、可扩展性和多步执行。
- Anthropic 只在产品层面介绍了 Claude Code，但缺少细化的架构说明，所以本文尝试从公开的 TypeScript 源码中还原这些设计选择。

## 方法
- 作者分析了公开可用的 Claude Code 源码（版本 v2.1.88），并把系统拆分为主要组件和子系统层。
- 核心机制是一个简单循环：整理上下文、调用模型、读取工具使用请求、检查权限、运行获批工具、把结果反馈回去，然后重复，直到任务结束。
- 围绕这个循环，论文识别出具体的外围系统：一个带有 7 种模式和基于机器学习的自动模式分类器的权限系统、一个 5 层上下文压缩流水线、4 种可扩展机制（MCP、插件、技能和 hooks）、子代理委派机制，以及面向追加的会话存储。
- 论文还在多个设计维度上比较了 Claude Code 和 OpenClaw，说明部署上下文如何改变架构选择，例如按动作检查与边界级访问控制之间的差异。
- 分析框架由 5 项设计价值和 13 条设计原则构成，这些内容来自源码检查和被引用的 Anthropic 文档。

## 结果
- 论文认为主代理循环在结构上很简单：一个 `queryLoop()` 的 while 循环处理模型调用、工具分发，以及跨 CLI、SDK 和 IDE 接口的重复执行。
- 它报告说，基于对提取源码的社区分析，整个代码库中只有大约 **1.6%** 是 AI 决策逻辑，而大约 **98.4%** 是运行基础设施。
- 它识别出 **7** 个高层系统组件、**5** 个架构层、**13** 条设计原则、**7** 种权限模式、**5** 个上下文压缩阶段、**4** 种可扩展机制、最多 **54** 个内置工具（其中 **19** 个无条件、**35** 个有条件），以及 **27** 种 hook 事件类型（其中 **5** 种与安全相关、**22** 种与生命周期/编排相关）。
- 在上下文限制方面，论文指出 Claude Code 的设计围绕旧模型的 **200K** token 窗口和 Claude 4.6 模型的 **1M** token 窗口展开，并在每次模型调用前应用五个压缩阶段。
- 论文引用的是 Anthropic 的使用数据，而不是自己做基准测试：在 **132** 名工程师和研究员的内部调查中，约 **27%** 的 Claude Code 辅助任务是用户如果没有这个工具就不会尝试的任务。
- 摘要没有给出新的实验基准表，也没有提供与 SWE-bench、OpenHands 或 OpenClaw 等基线的直接定量对比；它最强的结论是架构性和描述性的，而不是基准驱动的。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.14228v1](http://arxiv.org/abs/2604.14228v1)
