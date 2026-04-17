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
这篇论文研究 Cursor 是否能生成可运行的大型软件项目，以及这些项目是否存在设计问题。作者发现，在结构化的人类引导流程下，Cursor 可以生成规模较大、功能大多正确的系统，但代码中带有许多可维护性问题。

## 问题
- 以往工作主要测试代码片段生成或小型端到端项目，因此关于 AI IDE 是否能用真实技术栈和架构构建大型多文件系统，现有证据很少。
- 仅看功能正确性会漏掉设计质量问题。一个项目可以运行，但仍然包含重复代码、复杂方法、职责分离不清和框架误用，这些都会让后续修改的成本变高。
- 这对使用 AI IDE 进行项目级开发的团队很重要，尤其是在快速提示式工作流下，开发者可能会接受自己没有仔细检查的代码。

## 方法
- 作者提出了一个用 Cursor 生成大型项目的 Feature-Driven Human-In-The-Loop（FD-HITL）流程。简单说，他们不会一次性要求生成整个应用，而是让 Cursor 先规划项目，再拆分成可测试的功能，逐步构建，并在人类审查下完成生成。
- 他们整理了 10 个详细的项目描述，覆盖移动、Web 和工具类领域，使用的技术栈包括 React、Spring Boot、Django 和 React Native。
- 他们将大型项目定义为至少有 8K 行代码、包含多个架构组件、并采用工业风格技术栈的系统。
- 他们先通过人工方式评估功能正确性，再用 CodeScene 和 SonarQube 检查设计质量，并通过人工复核移除了 1,612 个 SonarQube 误报。

## 结果
- Cursor 生成了 10 个大型项目，总计 169,646 行代码，平均每个项目 16,965 LoC 和 114 个文件。
- 人工评估给出的平均功能正确性得分为 91%。
- CodeScene 发现了 1,305 个设计问题，分布在 9 个类别中。
- SonarQube 在移除 1,612 个误报后，发现了 3,193 个设计问题，分布在 11 个类别中。
- 论文报告了 133 个被两种工具同时检测到的重叠问题，作者将其视为反复出现的设计问题的更强证据。
- 最常见的问题包括代码重复、高复杂度或复杂方法、大方法、违反框架最佳实践、异常处理问题和可访问性问题。作者认为这些问题与违反 SRP、关注点分离和 DRY 原则有关。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.06373v1](http://arxiv.org/abs/2604.06373v1)
