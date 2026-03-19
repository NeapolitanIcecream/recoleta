---
source: arxiv
url: http://arxiv.org/abs/2603.08616v1
published_at: '2026-03-09T16:59:30'
authors:
- Nils Loose
- Nico Winkel
- Kristoffer Hempel
- "Felix M\xE4chtle"
- Julian Hans
- Thomas Eisenbarth
topics:
- software-fuzzing
- java-testing
- llm-agents
- coverage-guided-testing
- program-analysis
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Coverage-Guided Multi-Agent Harness Generation for Java Library Fuzzing

## Summary
本文提出一个用于 **Java 库模糊测试 harness 自动生成** 的多智能体 LLM 系统，通过按需查询文档、源码和调用图来生成、修复并迭代改进 harness。其核心贡献是把覆盖率反馈做成“目标方法定向”的，并让智能体判断何时继续优化、何时停止，从而比现有基线得到更高覆盖和实际漏洞发现。

## Problem
- 论文要解决的是：**Java 库 fuzzing 需要高质量 harness，但手工编写很慢、很依赖 API 语义理解、初始化顺序和异常约定**。
- 这很重要，因为没有合适 harness，coverage-guided fuzzing 很难真正触达库代码深处，导致大量广泛部署的 Java 库测试不足。
- 现有自动方法要么依赖大量客户端代码、要么只看类型结构、要么只用固定阈值做反馈，难以处理隐式前置条件、复杂初始化和语义化的覆盖缺口判断。

## Approach
- 方法核心是一个 **五智能体 ReAct 流水线**：Research 负责理解目标 API，Generation 生成初始 harness，Patching 修复编译错误，Coverage Analysis 分析覆盖缺口，Refinement 迭代修改 harness。
- 与一次性把整个代码库塞进上下文不同，系统通过 **MCP 按需查询** Javadoc、源码索引和静态调用图，只取当前任务相关信息，避免上下文爆炸。
- 一个关键机制是 **method-targeted coverage**：只在目标方法执行期间开启 JaCoCo 记录，避免 harness 通过跑无关初始化代码“刷高”覆盖率。
- 另一个关键机制是 **agent-guided termination**：覆盖分析智能体查看未覆盖源码，判断这些缺口是可通过更好输入/调用序列弥补，还是本质上难以到达，从而决定继续 refinement 还是停止。
- 在最简单的层面，这个系统就是：**先研究 API，再写 harness，编不过就修，跑 fuzz 看哪里没覆盖，再有针对性改 harness，直到继续改也不值得**。

## Results
- 在 **6 个广泛部署的 Java 库、7 个目标方法** 上评测，这些库合计有 **115,000+ Maven dependents**。
- 相对 **OSS-Fuzz** 现有 harness，生成的 harness 在 **method-targeted coverage** 上取得 **26% 的中位数提升**。
- 在 **full package-scope coverage** 下，方法分别比 **OSS-Fuzz 高 6%**、比 **Jazzer AutoFuzz 高 5%**（中位数）。
- 生成成本较低：平均每个 harness **约 10 分钟**、**约 3.20 美元**，说明可用于持续 fuzzing 工作流。
- 在 **12 小时 fuzzing campaign** 中，生成的 harness 在已经接入 OSS-Fuzz 的项目里发现了 **3 个此前未报告的 bug**。
- 文中还指出一个未超过基线的例子是 **jackson-databind**：因为 OSS-Fuzz 基线 harness 在目标方法后还包含额外 fuzzing 逻辑，导致整体 coverage 更高。

## Link
- [http://arxiv.org/abs/2603.08616v1](http://arxiv.org/abs/2603.08616v1)
