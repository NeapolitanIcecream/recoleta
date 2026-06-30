---
source: arxiv
url: https://arxiv.org/abs/2606.30549v1
published_at: '2026-06-29T16:47:46'
authors:
- Jessica Hutchison
- Ian Tyler Applebaum
- Kenneth Angelikas
- Kush Rakesh Patel
- Phuoc Nguyen
- Antonio Lazaro
- Nicholas Rucinski
- Rahad Arman Nabid
- Stephen MacNeil
topics:
- code-completion
- programming-education
- behavioral-signals
- attention-checks
- human-ai-interaction
- code-intelligence
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# To Tab or Not to Tab: Measuring Critical Engagement in AI Code Completion Tools Using Behavioral Signals and Attention Checks

## Summary
## 摘要
本文介绍了 Clover，这是一个 VS Code 代码补全扩展，用于记录学生如何接受、拒绝、编辑和查看 AI 建议。它使用有意设计的注意力检查来衡量初学编程者是否注意到 AI 生成的错误代码行。

## 问题
- 学生可能会在没有检查代码是否符合任务要求的情况下接受 AI 代码建议，这会影响学习和调试。
- 以往研究使用边想边说、屏幕录制、截图、眼动追踪和日志。这些方法能提供细节，但难以扩展到大量编程会话。
- 本文针对一个测量缺口：教师和研究人员需要行为信号，用来显示学生在真实编码工作中如何使用 AI 代码补全。

## 方法
- Clover 在 VS Code 中模拟 GitHub Copilot，包括光标处的单行建议和按 Tab 接受的行为。
- 系统记录的事件包括建议显示、Tab 接受、慢速接受、接受后修改、接受后删除、忽略、运行代码、停留时间和注意力检查失败。
- 注意力检查是有意误导的建议，例如在 `count++` 符合当前目标时给出 `count--`。接受这类建议计为注意力检查失败；拒绝则计为通过。
- 作者开展了一项线下研究，分析了 55 名 CS1 学生。他们完成一个 Java 降雨量问题，最多包含 26 个测试用例。
- 他们使用 Spearman 相关性分析会话级指标与任务表现、注意力检查失败率之间的关系。

## 结果
- 学生平均接受 18.4 条建议（SD 30.9），通过 Tab 接受 17.1 条建议（SD 31.0），慢速接受 1.3 条建议（SD 1.5），修改已接受建议 17.7 次（SD 29.8），删除已接受建议 0.6 次（SD 1.0），忽略 36.3 条建议（SD 13.3）。
- 平均停留时间为 12.2 秒（SD 8.1），范围为 1.7 到 39.1 秒。
- 学生平均运行代码 15.5 次（SD 12.6），范围为 0 到 52 次。
- 平均任务表现为 26 个测试中通过 10.4 个（SD 12.9）；55 名学生中有 22 人通过全部 26 个测试。
- 在测得的行为中，运行次数与任务表现的正相关最强，但效应不大（Spearman ρ = 0.26）。
- Tab 接受率与注意力检查失败率高度相关（ρ = 0.73，p < 0.001），停留时间与注意力检查失败率负相关（ρ = -0.26）。注意力检查失败率与较低任务表现弱相关（ρ = -0.17）。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.30549v1](https://arxiv.org/abs/2606.30549v1)
