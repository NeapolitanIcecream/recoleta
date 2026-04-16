---
source: arxiv
url: http://arxiv.org/abs/2604.05226v1
published_at: '2026-04-06T22:42:05'
authors:
- Yi Ru Wang
- Carter Ung
- Evan Gubarev
- Christopher Tan
- Siddhartha Srinivasa
- Dieter Fox
topics:
- robot-evaluation
- manipulation-benchmarking
- language-driven-tasks
- generalization-testing
- human-in-the-loop
relevance_score: 0.8
run_id: materialize-outputs
language_code: zh-CN
---

# RoboPlayground: Democratizing Robotic Evaluation through Structured Physical Domains

## Summary
## 摘要
RoboPlayground 是一个用于机器人操作评测的框架。用户用自然语言编写任务，系统会将其转换为可执行、可复现的任务定义。论文认为，这种方式能暴露固定的专家编写基准遗漏的失败模式，也让非专家更容易进行评测。

## 问题
- 机器人操作通常用一小部分专家编写的固定基准来评测，任务实例和成功判定也都是硬编码的。
- 这种设置很难测试用户自己编写的意图、约束和成功标准的变化，而这些变化对真实评估机器人行为很重要。
- 它也限制了可访问性：新增评测任务通常需要针对基准编写代码，并具备模拟器方面的专业知识。

## 方法
- RoboPlayground 接收一条自然语言指令，并将其编译为结构化任务规范，其中包含明确的资产定义、初始化分布、成功谓词和释义。
- 系统使用固定的任务模式，并结合基于 LLM 的合成步骤，生成符合标准环境接口的可执行任务代码。
- 多阶段验证流程会检查语法、API 使用、运行时执行和物理可实现性。目标状态在模拟稳定后仍需保持有效，失败的任务会进入迭代修复流程。
- 该框架支持通过带版本的任务家族对现有任务进行受控编辑。用户请求会被归类为 Tweak、Extend、Modify、Pivot 和 Fresh 等引导类别，并在各版本间跟踪谱系。
- 论文在一个结构化的积木操作领域中实现了这一框架，使语言变化能够映射为可控且可比较的任务变化。

## 结果
- 在一项包含 26 名参与者的用户研究中，RoboPlayground 的 **83.4 ± 6.9 SUS** 高于 Cursor 的 **68.8 ± 7.8** 和 GenSim 的 **52.5 ± 9.3**。差异具有统计显著性：相对 GenSim 为 **p < 0.001**，相对 Cursor 为 **p = 0.0017**。
- RoboPlayground 的认知负荷更低，为 **18.6 ± 7.7 NASA-TLX**；Cursor 为 **36.7 ± 10.4**，GenSim 为 **41.8 ± 9.0**。配对检验结果为：相对 Cursor **p = 0.0019**，相对 GenSim **p = 0.0007**。
- 用户偏好也更倾向于 RoboPlayground：总体上有 **69%** 选择它，Cursor 为 **23%**，GenSim 为 **8%**。平均可用性排名中，RoboPlayground 为 **1.3 ± 0.3**，另外两者分别为 **2.0 ± 0.2** 和 **2.7 ± 0.2**。
- 在基于语言定义的策略评测任务上，该框架显示出不同策略和任务之间存在很大的性能差异，而固定基准可能掩盖这种差异。示例成功率包括：**GR00T 96.0 ± 2.8** 在 "Place Two Blocks on Patch" 上，**Qwen-OFT 86.0 ± 4.9** 在 "Red Block Right Placement" 上；也有多个接近失败的案例，例如多种方法在 "Red Block Stacking" 和 "Color Block Alignment" 上都是 **0.0 ± 0.0**。
- 文中最强的定性结论是：在语言定义的任务家族上评测策略，可以发现由语义变化和成功定义变化带来的泛化失败，而这些问题在固定训练分布测试中不会显现。
- 摘要还声称，评测空间的多样性更多取决于贡献者的多样性，而不只是任务数量；但给出的摘录没有提供支持这一结果的底层定量表格。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05226v1](http://arxiv.org/abs/2604.05226v1)
