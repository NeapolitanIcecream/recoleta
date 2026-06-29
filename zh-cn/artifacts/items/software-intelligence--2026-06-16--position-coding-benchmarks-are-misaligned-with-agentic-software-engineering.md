---
source: arxiv
url: https://arxiv.org/abs/2606.17799v1
published_at: '2026-06-16T11:21:01'
authors:
- Maria I. Gorinova
- Macey Baker
- Amy Heineike
- Maksim Shaposhnikov
- Rob Willoughby
- Dru Knox
topics:
- coding-benchmarks
- agentic-software-engineering
- coding-agents
- swe-bench
- harness-evaluation
- code-intelligence
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering

## Summary
## 摘要
论文认为，当前的编码基准会为智能体式软件工程给出误导性信号。它们常把完整智能体配置的得分记成模型得分，评分也依赖范围狭窄的参考解，较少评估行为和代码质量要求。

## 问题
- 当前排行榜常把分数归给 LLM，但被测对象实际包括模型、智能体运行框架、工具、环境、任务设置和验证器。
- 单一参考评分可能否定有效的替代实现，也可能漏掉代码质量问题，例如抽象差、破坏项目约定或测试薄弱。
- 端到端分数对改进智能体系统的指导有限，因为它们不显示失败来自上下文、工具、任务拆解、验证器还是模型。

## 方法
- 论文把编码智能体描述为系统运行框架的一部分，该系统运行框架由任务、一个或多个智能体运行框架、环境、上下文和反馈信号组成。
- 论文把反馈分为内循环信号，例如测试和类型检查；中循环信号，例如审阅者请求和仿真；以及外循环信号，例如 PR 接受、回滚、事故和客户反馈。
- 论文分析了三类基准失效：模型与运行框架混淆、单一参考锚定、缺少组件级信号。
- 论文提出三项修复：要求提供模型、运行框架、环境和数据集版本的元数据；用行为验证器替代单一参考测试，允许多种有效解法形态；在端到端分数旁增加组件级评估。

## 结果
- 这是一篇立场论文，所以没有提出新基准，也没有报告新的受控实验结果。
- 在固定 Claude Opus 4.6 的 Terminal-Bench 上，报告成功率从 ForgeCode 的 79.8% ± 1.6 到 Claude Code 的 58.0% ± 2.9 不等；使用同一模型的不同运行框架之间相差 21.8 个百分点。
- 论文引用了实践者报告：在 SWE-Bench Verified 上更换脚手架时，Claude Opus 4.5 的结果会波动 4–10 个百分点；论文还引用了 OpenHands 在不同运行框架下使用可比模型取得 77.6% 的结果。
- 论文引用了 AI21 对超过 200,000 次 SWE-Bench 运行的结果，显示在固定模型和固定运行框架下，编排选择、容器分配和评估种子都会改变通过率。
- 论文引用了 SWE-Bench+ 的发现：issue 文本中有 32.67% 的解法泄漏，31.08% 的通过发生在测试不足的情况下。
- 论文引用的差分测试显示，7.8% 已解决的 SWE-Bench 风格补丁未通过开发者编写的测试，29.6% 与标准补丁的运行时行为不一致；论文还引用了 AIDev 数据，覆盖 61k 个代码库中 456k 个智能体编写的 PR，真实世界接受率为 35–64%，低于 SWE-Bench Verified 超过 70% 的头部数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.17799v1](https://arxiv.org/abs/2606.17799v1)
