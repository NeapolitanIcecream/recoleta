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
## 总结
这篇文章认为，到 2025 年，编码代理在 ClickHouse 的日常工程工作中已经变得有用，包括大型 C++ 代码库，只要配合严格的人工审查和测试。它是一篇经验报告，不是受控研究，证据来自若干内部使用案例和具体的效率主张。

## 问题
- 团队需要一个实用视角，来看编码代理在真实软件工作中哪些地方有帮助，而不只是看基准分数和“AI 会取代工程师”的泛化说法。
- 像 ClickHouse 的 C++ 服务端这样庞大、历史悠久、对安全敏感的代码库，会给代理带来很难处理的任务：漏洞排查、重构、CI 维护、代码评审和功能开发。
- 主要风险是输出看起来合理但其实错误。没有审查、测试和工程师判断，代理会浪费时间，也可能引入 bug。

## 方法
- ClickHouse 主要在“Level 2”阶段使用编码代理：CLI 或 IDE 代理读取代码、搜索日志、运行工具、构建和测试代码，并在人工指导下处理多步骤任务。
- 首选配置是 Claude Code 和 Codex CLI 这类 CLI 代理，因为它们可以规划任务、管理上下文、调用工具、检查日志、使用 GitHub、运行构建并根据反馈迭代。
- 工程师把代理用在具体工作流里：样板代码修改、处理陈旧的 pull request、解决合并冲突、代码移植、代码审查、漏洞和事故排查、修复不稳定测试、优化、原型开发和内部工具。
- 人工监督是方法的一部分。文章反复强调一个简单循环：说明任务，让代理编辑或排查，用测试和 CI 验证，再审查 diff 或推理过程。
- ClickHouse 也开始在一些范围很窄的任务上使用有限的自治代理，比如修复 flaky test 和生成边界情况测试，但文章说，更长的自治循环仍然不够可靠。

## 结果
- 最强的量化结果是 CI 清理：作者说在 1 月和 2 月，代理帮助产出了 **700 个 pull request**，用于修复测试和 CI 问题，把发现数量从每天约 **200** 降到每 **10,000,000** 次测试约 **3 到 5**。
- 在代码移植上，一个代理在 **36 小时** 内修复了 Polyglot 项目中的 SQL 方言兼容性问题，其中 **23 小时** 是 API 时间，成本大约 **$500**；这些修改已经合并，并用于 ClickHouse 的需求。
- 对于一个复杂 bug，报告中的最终修复是一个 **一行修改**，模型推理时间大约 **1 小时**，单次会话成本低于 **$30**；作者说，后续确认仍需要数月的压力测试和 fuzz 测试。
- 在事故排查上，一名值班工程师说，初步排查用了 **1 天**，原本需要 **3 到 4 天**，但文章也提醒，代理仍会给出很多错误假设。
- 在优化上，文章称一个代理在一台大型服务器上经过整夜运行后，把 ClickHouse 的构建速度提升了 **28%**；摘录中没有提供基准设置或基线细节。
- 在自治的 flaky-test 修复上，Groene.AI 代理据称在进一步反馈前能在大约 **30% 到 50%** 的情况下给出正确修复。文章还声称，在过去半年里，ClickHouse 收到的 **100%** 真实漏洞赏金发现都由编码代理找到，但除去每年大约 **10 起** 真实发现这一说法外，没有给出原始数量。

## Problem

## Approach

## Results

## Link
- [https://clickhouse.com/blog/agentic-coding](https://clickhouse.com/blog/agentic-coding)
