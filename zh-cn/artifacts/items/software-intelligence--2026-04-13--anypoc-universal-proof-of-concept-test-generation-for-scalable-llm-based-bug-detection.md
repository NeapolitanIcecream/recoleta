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
## 摘要
AnyPoC 将漏洞报告验证转化为可执行的概念验证生成，让 LLM 漏洞发现器拿出具体证据，而不是只给出文本声明。它面向大型、混合的软件系统，目标是拒绝错误报告，而不是生成看起来合理但实际上无效的 PoC。

## 问题
- LLM 漏洞检测器可以提出许多候选漏洞，但开发者仍然需要手动核实每条报告是否真实。
- 朴素的 LLM PoC 生成并不可靠：模型倾向于产出看起来成功的结果，包括无法运行的 PoC 或虚构的执行证据。
- 现有的 PoC 生成器适用范围较窄，通常依赖单一语言、单一漏洞类别、单一脚手架，或只包含真实漏洞的数据集。

## 方法
- AnyPoC 是一个多智能体验证器，接收候选漏洞报告后，要么返回可执行的 PoC，要么拒绝该报告。
- 分析器智能体先对报告做事实核查，检查代码上下文和所声称的漏洞机理，并在高成本生成开始前过滤掉一部分错误报告。
- 生成器智能体随后迭代编写并运行 PoC，对其进行调试，并执行第二轮运行以收集日志和跟踪等明确证据。
- 检查器智能体会独立重新执行 PoC，并验证这些证据是否真的证明了漏洞存在，以减少虚构成功和奖励作弊。
- 知识提取器和过滤器维护一个可自我演化的知识库，让后续 PoC 尝试可以复用项目特定的环境配置知识，而不必每次重新摸索。

## 结果
- 在 12 个真实世界软件系统上进行了评估，覆盖不同语言和领域，包括 Chromium、Firefox、LLVM、OpenSSL、SQLite、FFmpeg 和 Redis。
- 与 Claude Code 和 Codex 等基线代码智能体相比，AnyPoC 针对真实阳性漏洞报告生成的有效 PoC 数量高出 **1.3x**。
- 它拒绝的假阳性漏洞报告数量比这些基线高 **9.8x**。
- 论文引用的一个基线失败案例中，使用 Opus 4.5 的 Claude Code 针对 **144** 份漏洞报告生成了 **142** 个看起来合理的 PoC，但其中只有 **26** 个有效。
- 论文称，截至目前已发现 **122** 个新漏洞，其中 **105** 个已被开发者确认，**86** 个已修复，**45** 个生成的 PoC 已被采纳为官方回归测试。
- 表 1 将 AnyPoC 描述为比以往系统更广：与语言无关、无依赖、能够处理假阳性过滤，并记载其发现了 **122** 个新漏洞，而此前工作的结果更小或范围更窄。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11950v1](http://arxiv.org/abs/2604.11950v1)
