---
source: arxiv
url: http://arxiv.org/abs/2604.00917v1
published_at: '2026-04-01T13:58:30'
authors:
- Razvan Mihai Popescu
- David Gros
- Andrei Botocan
- Rahul Pandita
- Prem Devanbu
- Maliheh Izadi
topics:
- autonomous-coding-agents
- software-engineering
- github-pull-requests
- code-churn
- human-ai-collaboration
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Investigating Autonomous Agent Contributions in the Wild: Activity Patterns and Code Change over Time

## Summary
## 摘要
这篇论文研究自主编码代理如何参与真实的 GitHub 项目，以及它们提交的代码在合并后如何变化。作者使用一个新的数据集，涵盖五种代理和一组人类对照样本中的约 11.2 万个拉取请求，发现代理的使用正在增长，尤其是在低星标仓库中，而且代理编写的代码在后续阶段比人类编写的代码有更高的 churn。

## 问题
- 现有对编码代理的评估主要依赖基准测试、用户研究或小规模数据集，因此无法反映代理在真实协作式软件开发中的行为。
- 先前的实地研究通常只覆盖一种代理、少量 PR，或只关注热门仓库，这使得大规模比较代理行为变得困难。
- 代码生成只是软件工程的一部分；可维护性同样重要，因为代码在拉取请求合并后还需要长期保留并被继续修改。

## 方法
- 作者构建了一个 GitHub 数据集，包含 **2025 年 6 月至 8 月**的 **111,969 个拉取请求**，覆盖五种自主代理：**OpenAI Codex、Claude Code、GitHub Copilot、Google Jules 和 Devin**，以及一组匹配的人类编写 PR。
- 他们通过明确的 GitHub 信号识别代理 PR，例如分支前缀（`head:codex/`、`head:copilot/`）、机器人作者（`google-labs-jules[bot]`、`devin-ai-integration[bot]`），以及 PR 描述中的 Claude 水印文本。
- 数据集包含 PR，以及关联的 **commits、comments、reviews、issues 和 changed files**，每种代理对应的数量都达到数万，整体代码行数达到数百万。
- 他们从协作和活动指标上比较代理 PR 与人类 PR，包括合并频率、合并延迟、编辑的文件类型、变更规模、提交密度、评论、审查，以及仓库特征。
- 他们还对合并后代码的长期演化进行分析，使用 survival 和 churn 估计来衡量代理编写的代码后来有多少被保留或被重写。

## 结果
- 最终数据集包含 **111,969 个 PR**：**20,835 个 Codex**、**19,148 个 Claude Code**、**18,563 个 Copilot**、**18,468 个 Jules**、**14,045 个 Devin**，以及 **20,910 个 human** PR。
- 相关活动规模很大：例如，数据集包含 **102,037 个 human commits**、**82,755 个 Claude commits**、**69,896 个 Copilot commits**、**51,641 个 Devin commits**、**41,032 个 Jules commits** 和 **27,530 个 Codex commits**；changed files 数量从 Codex 的 **90,822** 到 Claude 的 **255,275** 不等。
- 论文认为，代理在开源项目中的活动正在增加，而且比早期研究所显示的更集中于 **low-star repositories**。
- 最主要的实质性发现是，**代理编写的贡献在时间推移中比人类编写的代码有更多代码 churn**，这说明其长期稳定性更低，或需要更多后续维护。
- 提供的摘录**没有给出实际的 churn、survival、merge-rate 或 latency 数值**，因此无法仅凭这段文本验证这些差异的量化幅度。
- 作为一项具体的研究资源，作者在 Hugging Face 上公开发布了该数据集，供后续关于 agentic software development 的研究使用。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.00917v1](http://arxiv.org/abs/2604.00917v1)
