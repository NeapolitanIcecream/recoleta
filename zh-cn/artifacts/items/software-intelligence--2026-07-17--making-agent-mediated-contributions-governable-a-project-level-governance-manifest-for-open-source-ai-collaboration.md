---
source: arxiv
url: https://arxiv.org/abs/2607.15769v1
published_at: '2026-07-17T08:58:54'
authors:
- Jinjin Gao
- Luyang Li
- Shufen Guo
- Ligang He
- Xiaoning Sun
topics:
- open-source-governance
- coding-agents
- ai-contribution-review
- software-engineering
- human-ai-collaboration
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Making Agent-Mediated Contributions Governable: A Project-Level Governance Manifest for Open-Source AI Collaboration

## Summary
## 摘要
论文提出了 Agent Governance Manifest（AGM），这是一个托管在代码仓库中的框架，旨在依据项目规则，更便于评估由 AI 介导的开源贡献。该框架将证据准备工作更多地交给贡献者和代理，同时保留维护者对验证和接纳的决定权。

## 问题
- 编码代理生成贡献的速度可能超过维护者评估正确性、安全性、可维护性、证据和问责性的能力。
- 现有的代理可读指令和可追溯性记录，未能持续明确与具体贡献相关的风险、证据义务、问责状态或审查门槛。
- 这一问题之所以重要，是因为维护者必须在审查能力有限、且对 AI 介导变更掌握的信息不完整的情况下作出接纳决定。

## 方法
- 论文区分了三个治理层次：为仓库提供指导的代理可读性、记录 AI 介导工作的可追溯性，以及依据项目规则组织审查的可治理性。
- 论文将项目侧可治理基础设施定义为一套规则和决策安排，涵盖风险分类、证据义务、问责、审查门槛以及维护者的决策权。
- AGM 将这一模型实现为托管在代码仓库中的、机器和人均可读的边界资源，把贡献者侧的证据包和确认声明与维护者侧的验证门槛连接起来。
- 研究先对 50 个公开 GitHub 仓库进行诊断性审计，随后评估 AGM 支持的工作流在审查者侧和贡献者侧的表现。

## 结果
- 审计考察了 50 个仓库、23,237 个拉取请求和 19,884 个议题；结果显示，一般性的治理产物和代理可读指导广泛存在，但 AI 治理线索分布不均且相互割裂。
- 经审计的仓库中，没有一个提供覆盖整个项目的安排，能够在 AI 介导的贡献工作流中协调共享规则、贡献者准备义务、验证权以及维护者的决策权。
- 在审查者侧评估中，15 名参与者生成了 75 个任务级输出。在有 AGM 支持材料的条件下，准确恢复风险标签的结果为 37/38；没有 AGM 支持材料时为 15/37。
- 在 1–7 分量表上，AGM 条件下的感知审查支持度从 3.27 提高到 6.14。
- 在贡献者侧可行性检查中，15 名参与者完成了 45 个任务；所有最终材料包都正确表示了核心治理状态，其中 41 个通过了严格的结构验证。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.15769v1](https://arxiv.org/abs/2607.15769v1)
