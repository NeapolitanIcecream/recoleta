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
## 总结
RoboPlayground 是一个用于机器人操作评估的框架。用户用自然语言写任务，系统把任务转成可执行、可复现的定义。论文认为，这样能暴露固定、专家编写基准漏掉的失败模式，也让非专家更容易做评估。

## 问题
- 机器人操作通常用少数专家编写的固定基准来评估，任务实例和成功检查都写死了。
- 这种做法很难测试用户自己写的意图、约束和成功标准变化，尽管这些变化对机器人行为的真实评估很重要。
- 这种方式也限制了可访问性：新增评估任务通常需要基准专用代码和模拟器经验。

## 方法
- RoboPlayground 接收自然语言指令，并把它编译成结构化任务规格，包含明确的资产、初始化分布、成功谓词和释义。
- 系统使用固定任务模式，再加上基于 LLM 的合成步骤，生成符合标准环境接口的可执行任务代码。
- 一个多阶段验证流水线检查语法、API 使用、运行时执行和物理可实现性。目标状态在仿真稳定后必须仍然有效，失败任务会经过迭代修复。
- 该框架通过带版本的任务家族支持对现有任务做受控编辑。用户请求会被分类为 Tweak、Extend、Modify、Pivot 和 Fresh 等 steering 类别，并跨版本跟踪谱系。
- 论文把这套方法放到一个结构化的方块操作领域中，让语言变化映射到受控、可比较的任务变化。

## 结果
- 在包含 26 名参与者的用户研究中，RoboPlayground 的 SUS 得分为 **83.4 ± 6.9**，高于 Cursor 的 **68.8 ± 7.8** 和 GenSim 的 **52.5 ± 9.3**。差异具有统计显著性：对 GenSim 为 **p < 0.001**，对 Cursor 为 **p = 0.0017**。
- RoboPlayground 的认知负荷更低，为 **18.6 ± 7.7 NASA-TLX**；Cursor 为 **36.7 ± 10.4**，GenSim 为 **41.8 ± 9.0**。配对检验显示，对 Cursor 为 **p = 0.0019**，对 GenSim 为 **p = 0.0007**。
- 用户偏好也更支持 RoboPlayground：**69%** 的参与者整体选择它，Cursor 为 **23%**，GenSim 为 **8%**。平均可用性排名中，RoboPlayground 为 **1.3 ± 0.3**，另外两者分别为 **2.0 ± 0.2** 和 **2.7 ± 0.2**。
- 在基于语言定义的策略评估任务上，该框架显示，不同策略和任务之间的性能差异很大，而固定基准可能看不出来。示例成功率包括：**GR00T** 在 "Place Two Blocks on Patch" 上为 **96.0 ± 2.8**，**Qwen-OFT** 在 "Red Block Right Placement" 上为 **86.0 ± 4.9**，还有多个接近失败的案例，例如在 "Red Block Stacking" 和 "Color Block Alignment" 上，多种方法都是 **0.0 ± 0.0**。
- 最强的定性结论是：在语言定义的任务家族上评估策略，可以揭示语义变化和成功定义变化下的泛化失败，而这些问题在固定训练分布测试中看不出来。
- 摘要还声称，评估空间的多样性更多随贡献者多样性增长，而不是只随任务数量增长，但这段摘录没有给出该结果对应的量化表格。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05226v1](http://arxiv.org/abs/2604.05226v1)
