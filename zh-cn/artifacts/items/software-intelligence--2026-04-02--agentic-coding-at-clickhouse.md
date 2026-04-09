---
source: hn
url: https://clickhouse.com/blog/agentic-coding
published_at: '2026-04-02T23:06:53'
authors:
- hodgesrm
topics:
- agentic-coding
- code-intelligence
- software-engineering
- developer-productivity
- multi-agent-systems
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic Coding at ClickHouse

## Summary
## 摘要
这篇文章认为，到 2025 年，在严格的人类审查和测试配合下，编码代理已经能在 ClickHouse 的日常工程工作中发挥作用，包括大型 C++ 代码库。它是一份经验报告，不是受控研究；证据来自一组内部使用案例，并附带具体的生产力描述。

## 问题
- 团队需要一个务实的判断，了解编码代理在真实软件工作中的帮助范围，而不是只看基准分数和“AI 会取代工程师”的宽泛说法。
- 像 ClickHouse 的 C++ 服务器这样大型、老旧、对安全敏感的代码库，会给代理带来困难任务：排查缺陷、重构、维护 CI、代码审查和功能开发。
- 主要风险是输出看起来合理但实际错误。没有审查、测试和工程师判断，代理会浪费时间或引入缺陷。

## 方法
- ClickHouse 主要在“Level 2”阶段使用 agentic coding：通过 CLI 或 IDE 代理读取代码、搜索日志、运行工具、构建和测试代码，并在人工指导下完成多步骤任务。
- 首选配置是 Claude Code 和 Codex CLI 这类 CLI 代理，因为它们可以规划、管理上下文、调用工具、检查日志、使用 GitHub、运行构建，并根据反馈反复修改。
- 工程师把代理用于具体工作流：样板代码修改、长期未处理的 pull request、合并冲突、代码移植、代码审查、缺陷和事故排查、不稳定测试修复、优化、原型和内部工具。
- 人工监督是方法的一部分。文章反复强调一个简单循环：说明任务，让代理修改或排查，用测试和 CI 验证，再审查 diff 或推理过程。
- ClickHouse 也开始在少量狭窄任务上使用有限的自主代理，例如修复不稳定测试和生成边界情况测试，但文章说，更长的自主循环仍然不够可靠。

## 结果
- 最强的量化结果来自 CI 清理：作者说在 1 月和 2 月，代理帮助产出了 **700 个 pull request** 来修复测试和 CI 问题，把发现数量从大约**每天 200 个**降到每 **10,000,000** 次测试约 **3 到 5 个**。
- 在代码移植方面，一个代理在 **36 小时**内修复了 Polyglot 项目中的 SQL 方言兼容性问题，其中 **23 小时是 API 时间**，成本约 **500 美元**；这些修改已被合并，并用于 ClickHouse 的需求。
- 对于一个复杂缺陷，文中称最终修复只是**一行改动**，模型推理大约用了 **1 小时**，单次会话成本低于 **30 美元**；作者说，确认修复仍然需要数月的进一步压力测试和模糊测试。
- 在事故排查方面，一名值班工程师表示，初步排查用 **1 天**完成，而原本需要 **3 到 4 天**，但同时提醒，代理仍会提出很多错误假设。
- 在优化方面，文章称一个代理在一台大型服务器上经过一夜运行后，把 ClickHouse 的构建速度提高了 **28%**；摘录中没有提供基准设置或基线细节。
- 对于自主修复不稳定测试，Groene.AI 代理据称在未获得进一步反馈前，约 **30% 到 50%** 的情况下能给出正确修复。文章还称，在过去半年里，ClickHouse 收到的真实漏洞赏金问题中，**100%** 都是通过编码代理发现的，但除了说真实问题的数量大约是**每年 10 个**之外，没有给出原始计数。

## Problem

## Approach

## Results

## Link
- [https://clickhouse.com/blog/agentic-coding](https://clickhouse.com/blog/agentic-coding)
