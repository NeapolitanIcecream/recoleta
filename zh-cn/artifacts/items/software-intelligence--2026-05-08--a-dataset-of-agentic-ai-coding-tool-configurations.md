---
source: arxiv
url: https://arxiv.org/abs/2605.08435v1
published_at: '2026-05-08T19:58:27'
authors:
- Matthias Galster
- Seyedmoein Mohsenimofidi
- "Levi B\xF6hme"
- Jai Lal Lulla
- Muhammad Auwal Abubakar
- Christoph Treude
- Sebastian Baltes
topics:
- agentic-coding-tools
- code-intelligence
- software-engineering-dataset
- ai-configuration
- human-ai-collaboration
- github-mining
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# A Dataset of Agentic AI Coding Tool Configurations

## Summary
## 摘要
本文发布了一个经过整理的 GitHub 数据集，收录面向代理式 AI 编码工具的仓库级配置文件。它面向 Claude Code、GitHub Copilot、OpenAI Codex、Cursor 和 Gemini 等工具的控制方式研究。

## 问题
- 开发者现在会为编码代理编写项目专用的指令、规则、钩子和工具设置，但研究人员还没有一个覆盖多种工具、且规模足够大的整理数据集来收录这些内容。
- 这些数据缺口限制了对配置采用、上下文工程、AI 生成改动和真实仓库中人机协作的研究。
- 现有数据集主要关注 AI 生成代码、拉取请求或单一工具工件，因此无法捕捉跨工具和跨机制的原始配置内容。

## 方法
- 作者从 SEART GitHub Search 数据集中的 187,304 个 GitHub 仓库出发，按许可证、活跃度、语言、仓库状态、主题模式、提交次数、关注者数量和重定向情况进行筛选。
- 他们保留了 40,585 个仍在维护的仓库，然后用 README 内容、GitHub Linguist 文件摘要、外部链接摘要和 GPT-5.2 将其中 36,710 个判定为工程软件项目。
- 他们克隆了这些工程仓库，并按文档中的检测启发式方法识别 5 种工具和 8 种配置机制：Context Files、Skills、Subagents、Commands、Rules、Settings、Hooks 和 MCP 配置。
- 他们为每个工件保存了元数据，包括文件路径、创建日期、提交次数、首尾提交哈希；对 Context Files 还记录了语言和 AI 作者归属信号。
- 他们还扫描了包含配置工件的仓库中的 AI 共署提交，并发布了数据集、构建流程和网站。

## 结果
- 数据集包含 4,738 个带有至少一个检测到的配置工件的仓库，来源于 36,710 个工程软件仓库。
- 它包括 15,591 个配置工件，以及 18,167 个配置文件的完整内容。
- 它覆盖 5 种工具：Claude Code 出现在 2,525 个仓库中，GitHub Copilot 出现在 1,397 个，Cursor 出现在 466 个，Gemini 出现在 183 个，OpenAI Codex 出现在 53 个，另外还有 909 个只包含 AGENTS.md 的仓库。
- Context Files 是最主要的机制：4,463 个仓库中共有 9,470 个工件。其他数量分别是：Skills 2,430 个工件，分布在 547 个仓库；Commands 1,098 个，分布在 284 个；Rules 997 个，分布在 298 个；Subagents 884 个，分布在 273 个；Settings 472 个，分布在 447 个；MCP 138 个，分布在 124 个；Hooks 102 个，分布在 101 个。
- 数据集包含来自 3,392 个仓库的 148,519 个 AI 共署提交。
- 与作者之前的研究相比，覆盖范围从 2,853 个仓库扩大到 4,738 个仓库；改进后的分类流程将不确定案例从 2,204 个降到 152 个，文中报告为减少了 93%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08435v1](https://arxiv.org/abs/2605.08435v1)
