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
## 总结
这篇论文研究自主编程代理如何参与真实的 GitHub 项目，以及它们的代码在合并后如何变化。作者用一个新的数据集，覆盖约 112k 个 pull request，包含五种代理和一组人类对照样本。结果显示，代理使用在增长，尤其集中在低星标仓库里；与人类编写的代码相比，代理编写的代码后续 churn 更高。

## 问题
- 现有的编程代理评估很大程度依赖基准测试、用户研究或小数据集，所以看不到代理在真实协作软件工作中的表现。
- 以往的实地研究常常只覆盖一种代理、少量 PR，或者只看热门仓库，这让大规模比较代理行为变得困难。
- 代码生成只是软件工程的一部分；可维护性同样重要，因为 pull request 合并后，代码还要在后续时间里继续存活并被修改。

## 方法
- 作者构建了一个 GitHub 数据集，包含 **111,969 个 pull request**，时间范围为 **2025 年 6 月至 8 月**，覆盖五种自主代理：**OpenAI Codex、Claude Code、GitHub Copilot、Google Jules 和 Devin**，并加入一组匹配的人类编写 PR。
- 他们通过具体的 GitHub 信号识别代理 PR，例如分支前缀（`head:codex/`、`head:copilot/`）、机器人作者（`google-labs-jules[bot]`、`devin-ai-integration[bot]`），以及 PR 描述中的 Claude 水印文本。
- 数据集包含 PR 以及关联的 **commits、comments、reviews、issues 和 changed files**，每种代理对应的数量都在数万级，总计覆盖数百万行代码。
- 作者比较了代理 PR 和人类 PR 在协作与活动指标上的差异，包括合并频率、合并延迟、编辑的文件类型、改动规模、commit 密度、comments、reviews 和仓库特征。
- 他们还用生存率和 churn 估计做了一个纵向分析，观察合并后代码演化，衡量代理编写的代码有多少后来被保留或重写。

## 结果
- 最终数据集包含 **111,969 个 PR**：**20,835 个 Codex**、**19,148 个 Claude Code**、**18,563 个 Copilot**、**18,468 个 Jules**、**14,045 个 Devin**，以及 **20,910 个 human** PR。
- 关联的活动量很大：例如，数据集包含 **102,037 条 human commits**、**82,755 条 Claude commits**、**69,896 条 Copilot commits**、**51,641 条 Devin commits**、**41,032 条 Jules commits** 和 **27,530 条 Codex commits**；changed files 数量从 Codex 的 **90,822** 到 Claude 的 **255,275** 不等。
- 论文认为，开源项目中的代理活动正在增加，而且比早期研究显示的情况更集中在 **low-star repositories**。
- 核心实质性发现是，**代理编写的贡献在时间上对应更高的 code churn，超过人类编写的代码**，这说明其长期稳定性更低，或者后续维护更多。
- 这段摘要 **没有给出实际的 churn、survival、merge-rate 或 latency 数值**，所以无法只根据提供文本核实这些差异的具体大小。
- 作为可直接复用的研究资源，作者把数据集公开发布在 Hugging Face 上，供后续 agentic software development 研究使用。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.00917v1](http://arxiv.org/abs/2604.00917v1)
