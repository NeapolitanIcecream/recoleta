---
source: arxiv
url: https://arxiv.org/abs/2607.01087v1
published_at: '2026-07-01T15:44:15'
authors:
- James C. Davis
- Paschal C. Amusuo
- Tanmay Singla
- "Berk \xC7akar"
- Kirsten A. Davis
topics:
- agentic-software-engineering
- code-intelligence
- software-governance
- human-ai-interaction
- ai-coding-agents
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Cheap Code, Costly Judgment: A Case Study on Governable Agentic Software Engineering

## Summary
## 摘要
这篇论文研究一名工程师如何在 12 周的快速构建中让 AI 智能体编码工作保持可控。论文认为，稀缺工作转向了判断：发现反复出现的失败，并把它们转化为架构、测试、lint、验证器、关卡和智能体指令。

## 问题
- AI 编码智能体可以生成大量代码，但其输出不可靠，受上下文影响，在仓库规模上难以信任。
- 人工检查会拖慢高产量的智能体工作，而多智能体工作可能提高产出，却缺少明确的质量控制。
- 实际问题是如何在保持速度的同时，让智能体编写的系统可检查、可纠正、可维护。

## 方法
- 作者报告了一项第一人称案例研究：一名专家工程师在 12 周内通过 VS Code 使用 Claude，构建了一个面向 Office 和 PDF 文件的文档无障碍修复系统。
- 实证记录包括 88 条同步现场笔记、18,662 次提交、约 420 KLOC 生产代码，以及 1.16 MLOC 测试、lint、文档和智能体工具。
- 他们把每条现场笔记编码为一个关键事件，然后构建了一个经过 11 次迭代的编码手册。第二作者重新编码了 10 个抽样事件，在事件类别上匹配 10/10，在分类上匹配 6/7，在第三层编码上匹配 5/7。
- 核心机制是“失败 → 治理”：反复出现的智能体失败暴露出缺失的约束，工程师随后加入持久控制或架构变更，使后续智能体工作受到边界约束。
- 架构变更通过构造方式防止某些失败类别，例如类型化组件目录和有边界的接缝。控制措施在失败发生后检测问题，例如 lint、测试、验证器、关卡和中介器。

## 结果
- 该项目在 12 周内产出约 420 KLOC 生产代码，加上 1.16 MLOC 支持性产物，共有 18,662 次提交，并分析了约 160 万行活跃产物。
- 编码语料包含 88 个事件。工程反思占 72 个事件；最大类别是控制措施，共 35 个事件，其次是架构，共 20 个事件。
- 该案例报告了一个可运行系统，能够处理 Office 和 PDF 文件，并通过或改进无障碍检查。研究对象的课程幻灯片每套约 60 秒处理完成，成本约为每套 1 美元。
- 项目总成本约为 60K 美元：50K 美元薪资、2K 美元推理成本、6K 美元 Google Cloud 托管费用，以及 2K 美元 Claude 订阅费用。
- 论文主张的主要结果是一个可测试的治理转换过程模型，该模型基于案例，而非受控基准测试。论文没有声称提出新的模型架构，也没有给出编码智能体准确率的正面对比结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01087v1](https://arxiv.org/abs/2607.01087v1)
