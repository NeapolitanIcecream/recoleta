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
## 总结
这篇论文发现，一个多智能体 LLM 系统可以发现并修复部分企业 UI 测试，但它的自治修复循环经常产出不可执行的输出、薄弱断言，或缩小后的测试范围。

## 问题
- 当屏幕、选择器、导航路径和异步加载行为发生变化时，大型企业 UI 测试套件会失效。
- 手动修复无法扩展到大规模场景，只靠定位器修复又会漏掉语义漂移和新的测试目标。
- 这项研究之所以重要，是因为一次表面通过的自治测试运行可能掩盖覆盖范围流失或检查变弱。

## 方法
- 该系统使用五个代理：Explorer、Planner、Coder、Executor 和 Self-Correction。
- Explorer 结合 RAG、匿名化功能文档和运行时 DOM 快照来寻找可测试的 UI 功能。
- Planner 把每个功能转成测试场景；Coder 编写 Playwright TypeScript；Executor 运行测试并记录日志、状态、时长和 DOM 错误上下文。
- Self-Correction 使用 DOM 解析器、选择器验证器、认证检查、失败产物分析，以及一个基于 RAG 的历史失败存储来修改失败测试。
- 改进后的流程加入了有限重试、跳过列表过滤、基于相似度的去重，以及基于 RAG 的选择器反馈。

## 结果
- 先从文档中发现了 10 个屏幕上的 119 个可测试功能，然后每次运行再通过运行时 DOM 发现 15 到 30 个功能，合计约 140 个有效功能。
- 多轮 RAG 在完整功能发现上调用了 34 次 LLM，而硬编码查询基线只调用 11 次，约为 3 倍。
- 评估覆盖了 126 天内连续 300 份执行报告，共 636 次单个测试用例执行。
- 300 份报告中只有 187 份生成了可执行测试文件，113 份报告，即 37.7%，没有生成任何测试产物。
- 在测试用例执行中，204 次通过，占 32.1%；432 次失败，占 67.9%；42 份报告，即 14%，达到 COMPLETED 状态。
- 在场景家族层面，10 个家族中有 7 个收敛，即 70%；首次通过率是 10 个中的 1 个，即 10%；表中给出的平均收敛修复迭代数是 3.4 次，观察到的最大重试深度是 16。研究还报告了 300 份报告中的失败模式：方法或契约不匹配 132 次，导航或环境超时 120 次，选择器或就绪失败 96 次，断言不匹配 78 次，不可执行输出 113 次，可见性断言失败 72 次，浏览器或上下文关闭 48 次，以及幻觉出的 API 或选择器 36 次。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01471v1](https://arxiv.org/abs/2605.01471v1)
