---
source: arxiv
url: https://arxiv.org/abs/2605.01471v1
published_at: '2026-05-02T14:39:55'
authors:
- Hyukjoo Lee
topics:
- autonomous-testing
- test-repair
- llm-agents
- ui-testing
- multi-agent-systems
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Practical Limits of Autonomous Test Repair: A Multi-Agent Case Study with LLM-Driven Discovery and Self-Correction

## Summary
## 摘要
论文发现，多智能体 LLM 系统可以发现并修复一部分企业 UI 测试，但它的自主修复循环常产生不可执行输出、较弱的断言，或缩小测试范围。

## 问题
- 大型企业 UI 测试套件会在屏幕、选择器、导航路径和异步加载行为变化时失效。
- 人工修复难以扩展，只修复定位器会遗漏语义漂移和新的测试目标。
- 这项研究很重要，因为一次通过的自主测试运行可能掩盖覆盖率损失或检查变弱。

## 方法
- 系统使用五个智能体：Explorer、Planner、Coder、Executor 和 Self-Correction。
- Explorer 基于匿名化功能文档和运行时 DOM 快照进行 RAG，以发现可测试的 UI 功能。
- Planner 将每个功能转成测试场景；Coder 编写 Playwright TypeScript；Executor 运行测试，并记录日志、状态、耗时和 DOM 错误上下文。
- Self-Correction 使用 DOM 解析器、选择器验证器、身份认证检查、失败产物分析，以及由 RAG 支持的历史失败存储来修改失败测试。
- 改进后的工作流加入了有界重试、跳过列表过滤、基于相似度的去重，以及基于 RAG 的选择器反馈。

## 结果
- 功能发现从文档中在 10 个屏幕上找到 119 个可测试功能，随后每次运行又加入 15–30 个由运行时 DOM 发现的功能，总计约 140 个有效功能。
- 多轮 RAG 完整功能发现使用了 34 次 LLM 调用，而硬编码查询基线使用 11 次调用，调用量约为 3 倍。
- 评估覆盖 126 天内连续 300 份执行报告，包含 636 次单个测试用例执行。
- 300 份报告中只有 187 份生成了可执行测试文件，另有 113 份报告，即 37.7%，没有生成任何测试产物。
- 在测试用例执行中，204 次通过，即 32.1%；432 次失败，即 67.9%；42 份报告，即 14%，达到 COMPLETED 状态。
- 在场景族层面，10 个场景族中有 7 个收敛，即 70%；首次通过为 10 个中 1 个，即 10%；表格报告的平均收敛修复迭代次数为 3.4 次，观察到的最大重试深度为 16。研究还报告了 300 份报告中的失败特征：方法或契约不匹配 132 次，导航或环境超时 120 次，选择器或就绪失败 96 次，断言不匹配 78 次，不可执行输出 113 次，可见性断言失败 72 次，浏览器或上下文关闭 48 次，幻觉 API 或选择器 36 次。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01471v1](https://arxiv.org/abs/2605.01471v1)
