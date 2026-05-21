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
本文发布了一个经过整理的 GitHub 数据集，内容是智能体式 AI 编码工具的仓库级配置文件。该数据集面向研究人员，用于研究开发者如何引导 Claude Code、GitHub Copilot、OpenAI Codex、Cursor 和 Gemini 等工具。

## 问题
- 开发者现在会为编码智能体编写项目专用指令、规则、钩子和工具设置，但研究人员缺少一个经过整理的、多工具的大规模配置工件数据集。
- 缺少这些数据会限制对真实仓库中配置采用情况、上下文工程、AI 编写的变更以及人机协作的研究。
- 现有数据集主要关注 AI 生成代码、拉取请求或单一工具工件，因此没有覆盖不同工具和机制下的原始配置内容。

## 方法
- 作者从 SEART GitHub Search 数据集中的 187,304 个 GitHub 仓库开始，按许可证、活跃度、语言、仓库状态、主题模式、提交数量、关注者数量和重定向情况进行筛选。
- 他们保留了 40,585 个活跃维护的仓库，然后使用 README 内容、GitHub Linguist 文件摘要、外部链接摘要和 GPT-5.2，将其中 36,710 个分类为工程化软件项目。
- 他们克隆了这些工程化仓库，并按文档化的检测启发式规则识别 5 种工具和 8 种配置机制：Context Files、Skills、Subagents、Commands、Rules、Settings、Hooks 和 MCP configurations。
- 他们存储了每个工件的元数据，例如文件路径、创建日期、提交数量、首次和最后一次提交哈希；对于 context files，还存储语言和 AI 作者信号。
- 他们还扫描了包含配置工件的仓库，查找 AI 共同署名提交，并发布了数据集、构建流水线和网站。

## 结果
- 该数据集包含 4,738 个至少检测到一个配置工件的仓库，这些仓库来自 36,710 个工程化软件仓库。
- 数据集包含 15,591 个配置工件，以及 18,167 个配置文件的完整内容。
- 数据集覆盖 5 种工具：Claude Code 出现在 2,525 个仓库中，GitHub Copilot 出现在 1,397 个仓库中，Cursor 出现在 466 个仓库中，Gemini 出现在 183 个仓库中，OpenAI Codex 出现在 53 个仓库中，另有 909 个仓库仅包含 AGENTS.md。
- Context Files 是数量最多的机制：4,463 个仓库中有 9,470 个工件。其他数量为：Skills 在 547 个仓库中有 2,430 个工件，Commands 在 284 个仓库中有 1,098 个，Rules 在 298 个仓库中有 997 个，Subagents 在 273 个仓库中有 884 个，Settings 在 447 个仓库中有 472 个，MCP 在 124 个仓库中有 138 个，Hooks 在 101 个仓库中有 102 个。
- 数据集包含来自 3,392 个仓库的 148,519 次 AI 共同署名提交。
- 与作者此前的研究相比，范围从 2,853 个仓库扩大到 4,738 个仓库；改进后的分类流程将不确定案例从 2,204 个减少到 152 个，报告称减少了 93%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08435v1](https://arxiv.org/abs/2605.08435v1)
