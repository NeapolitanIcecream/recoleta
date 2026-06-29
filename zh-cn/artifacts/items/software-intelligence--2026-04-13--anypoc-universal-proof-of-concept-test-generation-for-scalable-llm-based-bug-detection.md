---
source: arxiv
url: http://arxiv.org/abs/2604.11950v1
published_at: '2026-04-13T18:44:02'
authors:
- Zijie Zhao
- Chenyuan Yang
- Weidong Wang
- Yihan Yang
- Ziqi Zhang
- Lingming Zhang
topics:
- llm-bug-detection
- proof-of-concept-generation
- multi-agent-systems
- software-testing
- code-intelligence
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# AnyPoC: Universal Proof-of-Concept Test Generation for Scalable LLM-Based Bug Detection

## Summary
## 总结
AnyPoC 把漏洞报告验证变成可执行的概念验证生成，这样基于 LLM 的漏洞发现器就能提供具体证据，而不是只给出文字判断。它面向大型、混合的软件系统，目标是过滤掉错误报告，而不是生成看起来合理但实际上无效的 PoC。

## 问题
- LLM 漏洞检测器可以提出很多候选漏洞，但开发者仍然需要手动确认每条报告是否真实。
- 直接让 LLM 生成 PoC 不可靠：模型往往会产出看起来成功的结果，包括不能运行的 PoC 或幻觉出来的执行证据。
- 现有 PoC 生成器的适用范围很窄。它们常依赖单一语言、单一漏洞类别、单一脚手架，或者只包含真实漏洞的数据集。

## 方法
- AnyPoC 是一个多智能体验证器，接收候选漏洞报告后，要么返回可执行的 PoC，要么拒绝该报告。
- 分析器代理先核查报告，检查代码上下文和声称的漏洞机制，并在昂贵的生成开始前筛掉一部分错误报告。
- 生成器代理随后迭代编写并运行 PoC，调试它，再做一次执行，收集日志和跟踪等明确证据。
- 检查器代理独立重新执行 PoC，并验证这些证据是否真的说明了漏洞，这样可以减少幻觉式成功和 reward hacking。
- 知识提取器和过滤器维护一个持续演化的知识库，让后续 PoC 尝试复用项目特定的环境知识，而不用每次重新发现。

## 结果
- 在 12 个真实软件系统上评估，覆盖不同语言和领域，包括 Chromium、Firefox、LLVM、OpenSSL、SQLite、FFmpeg 和 Redis。
- 与 Claude Code 和 Codex 等基线编码代理相比，AnyPoC 针对真阳性漏洞报告生成的有效 PoC 多 **1.3x**。
- 它拒绝的假阳性漏洞报告比这些基线多 **9.8x**。
- 在文中引用的一个基线失败案例里，Claude Code 搭配 Opus 4.5 针对 **144** 份漏洞报告生成了 **142** 个看起来合理的 PoC，但只有 **26** 个有效。
- 论文称，截至目前已发现 **122** 个新漏洞，其中 **105** 个已由开发者确认，**86** 个已修复，**45** 个生成的 PoC 被采纳为官方回归测试。
- 表 1 将 AnyPoC 定位为比先前系统更广：不依赖特定语言、无需依赖项、能处理假阳性过滤，并记录了 **122** 个新漏洞，而先前结果更少或范围更窄。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11950v1](http://arxiv.org/abs/2604.11950v1)
