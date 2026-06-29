---
source: hn
url: https://blog.sshh.io/p/designing-software-for-software-factories
published_at: '2026-06-13T22:34:33'
authors:
- sshh12
topics:
- software-factory
- agentic-workflows
- code-intelligence
- automated-testing
- human-in-the-loop
- multi-agent-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Designing Software for Software Factories

## Summary
## 总结
这篇文章认为，软件工厂是一种由 AI 驱动的系统，它接收原始的客户需求和 bug 报告，把它们转成代码、测试并发布，只保留有限的人类审核。核心观点是，当代码库有清晰的契约、强测试层级，以及能让代理持续改进后续运行的反馈回路时，这套工厂最有效。

## 问题
- 软件团队希望 AI 处理更多开发流程，但大多数项目仍然依赖人来定义范围、拆分任务和验证改动。
- 当代码库缺少清晰契约、可测试性或足够结构时，AI 编码就会失效，代理也难以规划和验证工作。
- 人工门禁、共享的预发环境瓶颈，以及薄弱的反馈采集，会让循环变慢，并阻碍并行工作。

## 方法
- 将软件工厂定义为一种系统，它能接受客户生成的 RFE 和 bug 报告，完成方案设计和实现，测试改动，并在只保留退出处理和少量审核的人类介入下完成部署。
- 增加基于 Markdown 的项目契约，比如 AGENTS.md 文件，用来描述原则、架构边界、验证规则和考虑路线图的预期。
- 让每次改动都能被代理测试，并使用分层检查，包括 lint、类型检查、单元测试、安全扫描、集成测试、UI 级测试和发布监控。
- 让代理自己跑完整个测试循环，编写验证脚本，甚至在共享预发环境受阻时创建或重建测试环境。
- 把审核者反馈、代理轨迹、事故、指标和客户结果回流到系统中，让后续运行改进。

## 结果
- 这段摘录没有给出实验结果或基准测试表。
- 最有力的具体说法是，只要配上设计良好的测试夹具，现代模型就能写出“出乎意料地正确且复杂的软件”。
- 作者声称，只要契约设置得当，软件工厂可以做到“一天交付数万行代码”。
- 对于从零开始的项目，文章建议在最初 3–10k 行代码和最初几个端到端功能上与编码代理配对，作者说在现代开发速度下这大约需要 1–3 周。
- 对于存量系统，文章的说法是，把某个子组件重建或拆解到能让代理测试改动，成本可能低于继续让人类参与特性开发，但没有提供数值研究。
- 文章还说，在作者的经验里，完全自动化的二阶反馈回路效果不好，往往会产生“正反馈垃圾循环”。

## Problem

## Approach

## Results

## Link
- [https://blog.sshh.io/p/designing-software-for-software-factories](https://blog.sshh.io/p/designing-software-for-software-factories)
