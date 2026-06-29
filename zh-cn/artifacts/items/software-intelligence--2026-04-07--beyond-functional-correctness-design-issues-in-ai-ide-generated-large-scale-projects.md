---
source: arxiv
url: http://arxiv.org/abs/2604.06373v1
published_at: '2026-04-07T18:59:05'
authors:
- Syed Mohammad Kashif
- Ruiyin Li
- Peng Liang
- Amjed Tahir
- Qiong Feng
- Zengyang Li
- Mojtaba Shahin
topics:
- ai-ide
- cursor
- large-scale-code-generation
- software-design-quality
- static-analysis
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Functional Correctness: Design Issues in AI IDE-Generated Large-Scale Projects

## Summary
## 摘要
这篇论文研究 Cursor 是否能生成可运行的大型软件项目，以及这些项目是否存在设计问题。作者发现，在结构化的人类引导流程下，Cursor 可以生成规模可观、功能大体正常的系统，但代码里有很多可维护性问题。

## 问题
- 以往研究主要测试代码片段生成或小型端到端项目，因此几乎没有证据说明 AI IDE 是否能构建带有真实技术栈和架构的多文件大型系统。
- 只看功能正确性会漏掉设计质量。一个项目可以运行，但仍可能存在重复代码、复杂方法、职责划分不清和框架误用，这些问题会让后续修改成本变高。
- 这对把 AI IDE 用在项目级开发的团队很重要，尤其是在快速提示的工作流中，开发者可能会接受自己没有仔细检查过的代码。

## 方法
- 作者提出了一个 Feature-Driven Human-In-The-Loop（FD-HITL）流程，用 Cursor 生成大型项目。简单说，他们不会一次性让它生成整个应用，而是让 Cursor 先规划项目，再拆成可测试的功能，逐步实现，并在生成过程中进行人工审查。
- 他们整理了 10 个详细的项目描述，覆盖移动端、Web 和工具类领域，使用了 React、Spring Boot、Django 和 React Native 等技术栈。
- 他们把大型项目定义为至少包含 8K 行代码、多个架构组件和工业风格技术栈的系统。
- 他们先人工评估功能正确性，再用 CodeScene 和 SonarQube 检查设计质量，并通过人工复核去掉了 1,612 个 SonarQube 误报。

## 结果
- Cursor 生成了 10 个大型项目，总计 169,646 行代码，单个项目平均 16,965 行代码和 114 个文件。
- 人工评估得到的平均功能正确性得分是 91%。
- CodeScene 发现了 1,305 个设计问题，分布在 9 个类别中。
- 去掉 1,612 个误报后，SonarQube 发现了 3,193 个设计问题，分布在 11 个类别中。
- 论文报告有 133 个问题被两种工具同时检出，作者把这视为重复设计问题更强的证据。
- 最常见的问题是代码重复、方法复杂度高、方法过大、框架最佳实践违规、异常处理问题和可访问性问题。作者把这些问题与 SRP、关注点分离和 DRY 违规联系起来。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.06373v1](http://arxiv.org/abs/2604.06373v1)
