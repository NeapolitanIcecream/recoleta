---
source: arxiv
url: https://arxiv.org/abs/2606.26721v1
published_at: '2026-06-25T07:57:33'
authors:
- Xinyu Zhang
- Weiwei Sun
topics:
- code-intelligence
- software-agents
- pull-requests
- human-ai-interaction
- software-governance
- multi-agent-software-engineering
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Knowledge-Based Pull Requests: A Trusted Workflow for Agent-Mediated Knowledge Collaboration

## Summary
## 摘要
KPR 将跨信任边界的 PR 改成知识交接：外部代码、测试和清理后的智能体交互轨迹先成为证据，然后由项目自有的智能体在目标仓库内重新生成代码。论文提出的是一种工作流，并配有一个小规模模拟试点，所以其主要主张集中在治理和评审控制上；摘录中没有给出已测量的生产力提升。

## 问题
- 智能体生成的 PR 会让代码编写成本下降，但把更难的工作留给维护者：理解意图、界定范围、判断架构适配、执行安全策略，以及承担长期所有权。
- 传统 PR 让外部补丁作为合并候选跨过信任边界；对于开源、企业、供应商、承包商和客户提交的变更，这种做法有风险。
- 原始智能体聊天记录噪声太多，可能包含过时说法、机密、无关尝试或不可信指令，因此把轨迹直接丢给评审不能降低评审者负担。

## 方法
- 外部协作者使用本地编码智能体探索变更、创建代码、运行测试并收集证据。
- 抽取智能体把本地 diff、测试、日志、清理后的轨迹、失败尝试和人工修正转成结构化 KPR 包，并为各项声明保留来源信息。
- 转换智能体把该包渲染成面向评审者的材料，例如简报、设计备忘录、风险清单、测试计划或实现简述。
- 协作者在提交前确认该包；项目评审者先对知识进行批准、拒绝或要求澄清，然后才进入任何代码合并路径。
- 项目自有的内部可信编码智能体在接收仓库内，基于项目上下文、测试、约定和安全策略重新生成候选代码；人工仍然负责评审并决定是否合并。

## 结果
- 试点覆盖 7 个已合并的公开 PR，并显示可以用真实 PR 材料构建 KPR 包。
- 试点在 3 种条件下对包进行压力测试：描述消融、diff 消融和合成投毒补丁条件。
- 论文没有报告评审时间、合并延迟、缺陷率或维护者工作量的实测下降。
- 论文引用 Njoku et al. 对 2,807 个仓库中 40,214 个 PR 的研究，其中包括 33,596 个由智能体编写的 PR，用来证明智能体 PR 已经影响集成结果。
- 论文还引用 SWE-chat，其中包含约 6,000 次编码智能体会话；智能体生成的代码有 44% 保留到用户提交中，用户在 44% 的轮次中提出反对意见。这支持了一个判断：除最终 diff 外，轨迹也包含有用的评审证据。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.26721v1](https://arxiv.org/abs/2606.26721v1)
