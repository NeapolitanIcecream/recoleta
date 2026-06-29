---
source: arxiv
url: https://arxiv.org/abs/2606.13239v1
published_at: '2026-06-11T11:53:32'
authors:
- Jiaxin Ai
- Tao Hu
- Xuemeng Yang
- Shu Zou
- Hairong Zhang
- Daocheng Fu
- Yu Yang
- Hongbin Zhou
- Nianchen Deng
- Pinlong Cai
- Zhongyuan Wang
- Botian Shi
- Kaipeng Zhang
- Licheng Wen
topics:
- computer-use-agents
- com
- cad-automation
- software-foundation-model
- code-generation
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# ComAct: Reframing Professional Software Manipulation via COM-as-Action Paradigm

## Summary
## 摘要
ComAct 将专业软件控制重新定义为通过 COM 接口进行代码生成，这一点很重要，因为 GUI 代理在复杂的 CAD 软件中容易失效，而基于 API 的代理又很难覆盖商业工具。

## 问题
- 在真实的 CAD 工作流中，专业软件自动化会失效，因为 GUI 控制很脆弱，长链路操作中的错误会不断累积。
- 对很多商业应用来说，API 和 MCP 工具过于碎片化，或者根本不可用。
- 论文把工业 CAD 作为主要测试场景，因为它需要精确几何、长动作链和跨应用步骤。

## 方法
- 论文把 COM，也就是 Windows 上的软件对象模型，作为动作空间，SolidWorks、AutoCAD、Office 和 Adobe 应用都使用这一模型。
- 代理不再执行大量底层鼠标和键盘步骤，而是直接编写可执行的 Python COM 脚本。
- 论文构建了 ComCADBench，这是一个包含 1,000 个任务的基准，覆盖 SolidWorks、Inventor 和 AutoCAD，分为 400 个单任务案例和 600 个多任务案例。
- ComActor 分三个阶段训练：指令到代码的监督微调、基于执行反馈的多轮修正，以及使用基于 Chamfer Distance 的连续几何奖励进行 GRPO 强化学习。
- 论文使用 ComForge，这是一个容器化的 Windows 平台，提供 1,000+ 个并行的真实环境用于训练和评估。

## 结果
- ComCADBench 包含 1,000 个任务，覆盖 3 个 CAD 应用和 7 类活动，评估指标是代码有效率和任务成功率。
- 论文报告说，基于 GUI 的代理在这个基准上的成功率接近于零，而基于 COM 的执行带来了明显的即时提升。
- 在表 1 中，作者在列出的单任务和多任务设置上报告了 90.0/81.0、96.0/89.0、95.0/88.0、86.0/86.0、84.0/75.0、97.0/87.0、76.0/61.0、78.0/58.0、98.0/86.0 和 95.0/80.0 的结果，其中每个单元格都是代码有效率 / 任务成功率。
- 表中最强的基线在一个设置上达到 82.0/88.0，在另一个设置上达到 76.0/74.0，而很多其他基线在没有 few-shot 提示时都接近 0.0。
- 论文还声称该方法可推广到外部 CAD 基准，包括 Text2CAD 和 CADPrompt，但摘要片段没有给出这些基准的数值结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13239v1](https://arxiv.org/abs/2606.13239v1)
