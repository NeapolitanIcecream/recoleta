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
- multi-agent-systems
- llm-code-generation
- fuzzing
- java-testing
- coverage-guided-testing
- program-analysis
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Coverage-Guided Multi-Agent Harness Generation for Java Library Fuzzing

## Summary
该论文提出了一个面向 Java 库模糊测试的多智能体 LLM 系统，可自动生成和迭代改进 fuzz harness。其关键在于按需查询程序信息、使用方法定向覆盖率做反馈，并以较低成本达到或超过现有基线。

## Problem
- 它解决的是**Java 库 fuzz harness 自动生成**问题：库代码要被 coverage-guided fuzzing 有效测试，必须先把随机字节转换成合法 API 调用，但手工编写 harness 很耗时且需要理解 API 语义、初始化顺序和异常契约。
- 这很重要，因为缺少高质量 harness 会直接限制库代码覆盖率与 bug 发现能力；而 Java 库在持续模糊测试基础设施中仍相对欠覆盖，但实际部署非常广。
- 现有方法要么依赖大量客户端代码、要么只看类型结构难以捕获隐式前置条件、要么缺乏对覆盖缺口的语义化解释，导致泛化性和迭代改进能力不足。

## Approach
- 核心方法是一个**五智能体 ReAct 流水线**：Research、Generation、Patching、Coverage Analysis、Refinement，各自负责调研 API、生成 harness、修复编译错误、分析覆盖缺口、再迭代优化 harness。
- 最简单地说：系统先“查文档和源码理解 API”，再“写出可编译 harness”，再“运行 fuzzing 看哪些目标代码没被打到”，最后“根据没覆盖到的源码继续改 harness”。
- 它不预先把整个代码库塞进提示词，而是通过 **MCP** 按需查询 Javadoc、源码和调用图，避免上下文爆炸，并让不同智能体只访问与其职责相关的工具。
- 论文提出 **method-targeted coverage**：只在目标方法执行期间记录覆盖率，避免 harness 通过调用无关初始化/工具代码“刷高”覆盖指标，使反馈更贴近目标 API 本身。
- 还提出 **agent-guided termination**：覆盖分析智能体读取未覆盖源码，判断缺口是可通过更多输入/路径探索弥补，还是已进入收益递减，从而决定是否停止 refinement。

## Results
- 在 **6 个广泛使用的 Java 库、7 个目标方法** 上评估，这些库合计有 **115,000+ Maven dependents**。
- 相比已有 **OSS-Fuzz** harness，生成的 harness 在**方法定向覆盖率**上取得 **26% 的中位数提升**。
- 在**包级/完整目标范围覆盖率**下，方法分别优于 **OSS-Fuzz 6%**、优于 **Jazzer AutoFuzz 5%**（中位数）。
- 生成成本较低：平均每个 harness 约 **10 分钟**、约 **$3.20**，说明可用于持续 fuzzing 工作流。
- 在 **12 小时** fuzzing 活动中，生成的 harness 在已接入 OSS-Fuzz 的项目里发现了 **3 个此前未报告的 bug**。
- 文中还指出，唯一未稳定超过基线的目标是 **jackson-databind**，原因是其 OSS-Fuzz 基线在目标方法执行后还包含额外 fuzzing 逻辑，抬高了整体覆盖率。

## Link
- [http://arxiv.org/abs/2603.08616v1](http://arxiv.org/abs/2603.08616v1)
