---
source: arxiv
url: http://arxiv.org/abs/2603.03683v1
published_at: '2026-03-04T03:22:26'
authors:
- Jue Huang
- Tarek Mahmud
- Corina Pasareanu
- Guowei Yang
topics:
- llm-code-generation
- concurrency
- benchmark
- model-checking
- java
- evaluation
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# CONCUR: Benchmarking LLMs for Concurrent Code Generation

## Summary
CONCUR 是一个专门评测大语言模型生成并发代码能力的基准，而不是像以往那样只测顺序代码。它将并发程序的正确性评估从表面相似度或普通单测，提升到基于模型检测的更严格验证。

## Problem
- 现有代码生成基准主要面向顺序程序，无法有效衡量 LLM 生成并发代码的能力。
- 并发程序更复杂，存在死锁、竞态、饥饿等顺序程序没有的错误；普通单元测试难以系统覆盖非确定性的线程交错。
- 因此，如果没有专门的并发基准，就会高估 LLM 在真实软件工程场景中的代码生成能力。

## Approach
- 构建 **CONCUR**：包含 **43** 个来自标准并发教材的基础题，并基于其中一部分生成并人工验证 **72** 个 mutant 变体，共 **115** 个问题实例。
- 每个任务都配有结构化 prompt、可执行的 Java 8 参考实现，以及统一的约束（单文件、无第三方库、必须有 `main`、限制线程数与迭代次数）。
- 评测流程分两步：先在 **Java 8** 环境编译，再用 **Java Pathfinder (JPF)** 做模型检测，系统枚举线程交错来发现并发错误。
- 框架通过监听器识别多类错误，包括 **Deadlock、Race Condition、Starvation、Uncaught Exception、No Entry Method、Single Thread、Termination Error**。
- 为控制状态爆炸，作者采用双重有界策略：任务设计层面限制线程/迭代；验证层面把 `search.depth_limit` 设为参考解最大执行深度的 **10 倍**，并设置统一超时（示例配置中为 **9000 ms**）。

## Results
- 基准规模上，CONCUR 提供 **115** 个并发代码生成任务，其中 **43** 个基础题 + **72** 个人工验证 mutant，明确覆盖锁、信号量、原子类、阻塞队列、线程池等多种并发机制。
- 评测范围上，作者使用 CONCUR 测试了 **23** 个当前主流 LLM（含闭源 API 与开源模型），并指出这些模型在并发代码生成上存在明显局限。
- 自动验证质量上，论文声称其基于 JPF 的错误检测框架在人工复核中达到 **92% precision**。
- 方法论结论上，作者明确指出常用代码评估指标 **CodeBLEU** 不能可靠反映并发程序正确性；文中摘录未给出更细的相关系数或具体数值对比。
- 文段未提供各模型在 CONCUR 上的完整通过率、按错误类型分布、或与现有 benchmark 的量化 head-to-head 数字；最强的定量主张主要是 **115 题规模、23 个模型、92% precision、深度上限为参考解 10 倍**。

## Link
- [http://arxiv.org/abs/2603.03683v1](http://arxiv.org/abs/2603.03683v1)
