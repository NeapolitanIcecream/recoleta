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
## 摘要
这篇论文分析了 Claude Code 的源代码，把它作为一项关于现代编码代理如何构建的研究。论文认为，代理的主逻辑很简单，而系统的大部分复杂性集中在权限、上下文管理、可扩展性、委派和持久化上。

## 问题
- 论文研究了生产级编码代理应如何处理运行 shell 命令、编辑文件、使用外部服务等自主操作，同时不失去用户控制或安全性。
- 这很重要，因为代理式编码工具面临的是自动补全工具没有的设计问题：权限控制、长时程可靠性、上下文窗口限制、可扩展性和多步执行。
- Anthropic 在产品层面记录了 Claude Code，但详细的架构描述较少，因此论文尝试从公开的 TypeScript 源代码中还原这些设计选择。

## 方法
- 作者分析了公开可用的 Claude Code 源代码（版本 v2.1.88），并将系统映射为主要组件和子系统层级。
- 核心机制是一个简单循环：组装上下文、调用模型、读取任何工具使用请求、检查权限、运行获批工具、将结果反馈给模型，然后重复直到任务结束。
- 围绕这个循环，论文识别出一些具体的外围系统：一个具有 7 种模式并带有基于 ML 的自动模式分类器的权限系统、一个 5 层上下文压缩流水线、4 种可扩展机制（MCP、plugins、skills 和 hooks）、子代理委派，以及面向追加的会话存储。
- 论文还在多个设计维度上将 Claude Code 与 OpenClaw 做比较，以说明部署环境变化会如何改变架构选择，例如逐操作检查与边界访问控制的差别。
- 论文通过 5 个明确提出的设计价值和 13 条设计原则来组织分析，这些内容来自对源代码的检查和所引用的 Anthropic 文档。

## 结果
- 论文称，主代理循环在结构上很简单：一个 `queryLoop()` while-loop 就处理了模型调用、工具分发，以及在 CLI、SDK 和面向 IDE 的界面上的重复执行。
- 根据论文引用的社区对提取源代码的分析，代码库中只有约 **1.6%** 是 AI 决策逻辑，约 **98.4%** 是运行基础设施。
- 论文识别出 **7** 个高级系统组件、**5** 个架构层、**13** 条设计原则、**7** 种权限模式、**5** 个上下文压缩阶段、**4** 种可扩展机制、最多 **54** 个内置工具（**19** 个无条件、**35** 个有条件），以及 **27** 种 hook 事件类型（**5** 种与安全相关、**22** 种与生命周期/编排相关）。
- 在上下文限制方面，论文称 Claude Code 的设计围绕旧模型的 **200K** token 窗口和 Claude 4.6 模型的 **1M** token 窗口展开，并在每次模型调用前应用五个压缩阶段。
- 论文引用了 Anthropic 的使用数据，而不是给出自己的基准测试：在一项针对 **132** 名工程师和研究人员的内部调查中，大约 **27%** 的 Claude Code 辅助任务，是用户如果没有这个工具就不会尝试的任务。
- 摘录中没有提供新的实验基准表，也没有给出与 SWE-bench、OpenHands 或 OpenClaw 等基线的正面定量评估；其最强的论点是架构层面和描述性的，而不是由基准测试推动的。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.14228v1](http://arxiv.org/abs/2604.14228v1)
