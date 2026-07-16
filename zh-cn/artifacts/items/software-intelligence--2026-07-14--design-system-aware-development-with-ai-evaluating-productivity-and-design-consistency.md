---
source: arxiv
url: https://arxiv.org/abs/2607.13156v1
published_at: '2026-07-14T18:06:29'
authors:
- Luciane Silva
- Thayssa Rocha
- Nicole Davila
- Gustavo Pinto
topics:
- code-intelligence
- automated-software-production
- design-systems
- front-end-development
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Design-System-Aware Development with AI: Evaluating Productivity and Design Consistency

## Summary
## 总结
一项在工业环境中开展的受控实验发现，以企业设计系统为基础的 AI 辅助能够加快前端和移动界面的开发，并提高实现完整度。证据来自 49 名开发者，他们在 Angular、iOS 和 Android 平台上完成了两个基于设计稿的界面；但研究结果受限于单一企业环境和任务定义较为狭窄。

## 问题
- 通用 AI 编码工具缺乏内部设计系统的上下文，因此生成的结果可能在语法上有效，却在视觉上不一致，或不符合企业标准。
- 组织需要了解，在实际前端开发中，将 AI 与设计系统结合是否能够改善交付时间、设计还原度和工作流一致性。

## 方法
- 研究人员于 2025 年 6 月和 10 月分两个周期，在 Zup Innovation 开展了一项受控远程实验，共有 49 名专业开发者参与。
- 参与者使用三种工作流之一：手动开发、仅使用设计系统开发，或使用结合企业设计系统上下文的 StackSpot AI。
- 每名参与者在 Angular、iOS 或 Android 中实现两个高保真设计稿界面，并接受专家评审，同时按时间记录增量提交。
- 研究测量了交付时间、任务完整度、绩效差异，以及作为工作流摩擦间接指标的中断模式。

## 结果
- 在 Angular 中，AI 辅助的完成时间比手动基线低 69.4%，从 536.15 分钟降至 164.00 分钟；在 iOS 中低 46.7%，从 593.00 分钟降至 316.00 分钟；在 Android 中低 57.9%，从 387.75 分钟降至 163.25 分钟。报告称这些差异在统计上显著（p<0.05）。
- 与仅使用设计系统的开发相比，AI 辅助在 Angular 中快 24.4%，在 iOS 中快 15.5%，在 Android 中快 23.4%。
- 使用 AI 辅助时，平均任务完整度达到 96%；仅使用设计系统开发时为 85%，手动开发时为 68%。
- AI 组的完成时间差异更小：Angular、iOS 和 Android 的标准差分别为 42 分钟、51 分钟和 35 分钟，而设计系统组分别为 85 分钟、112 分钟和 75 分钟。
- 使用 AI 辅助时，中断时间更短且更为集中，范围为 0 至 90 分钟；手动组在一个数据集中记录到最长 195 分钟的中断。这支持工作流摩擦减少这一判断，但中断时间只是认知负荷的间接指标。
- 研究结果的普适性仍不确定，因为所有参与者都来自同一家巴西企业，任务仅涵盖两个预先定义的界面，而且完整度由专家评定，而不是通过自动化评估或多名评审者评估。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13156v1](https://arxiv.org/abs/2607.13156v1)
