---
source: arxiv
url: http://arxiv.org/abs/2604.13100v1
published_at: '2026-04-10T09:30:08'
authors:
- Yi Lin
- Lujin Zhao
- Yijie Shi
topics:
- repo-level-code-generation
- multi-agent-software-engineering
- code-intelligence
- symbolic-contracts
- parallel-agent-orchestration
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Contract-Coding: Towards Repo-Level Generation via Structured Symbolic Paradigm

## Summary
## 摘要
Contract-Coding 是一种仓库级代码生成方法，它先把模糊的用户意图转换成结构化契约，再用该契约协调并行代码生成和验证。论文称，这种方法能减少跨文件混乱，并提高多文件软件任务的成功率。

## 问题
- 从模糊意图进行仓库级生成经常失败，因为智能体按顺序生成文件，必须携带越来越多的原始代码上下文。
- 早期设计错误会扩散到后续文件，长代码历史也会把重要的架构细节挤出模型的有效注意范围。
- 这对自主软件生产很重要，因为多文件项目需要一致的 API、文件结构和跨模块行为，而不只是局部有效的代码。

## 方法
- 系统首先把宽泛的用户请求转换成 **Language Contract**，这是一种结构化产物，用来记录需求、API、模块到文件的映射、类型签名和状态定义。
- 随后，代码生成被拆分为两步：先从意图推断契约，再在契约条件下生成每个文件，而不是依赖此前生成的原始代码。
- **Hierarchical Execution Graph (HEG)** 根据契约调度任务，因此当接口已经定义好时，多个模块实现可以并行运行。
- 验证器和契约审计器会检查生成代码是否符合契约、所需文件和符号是否存在，以及代码变更是否需要更新契约。
- 契约通过受约束的新增/更新操作来构建和修订，并检查无效图结构或签名不一致等问题。

## 结果
- 在 Greenfield-5 基准上，完整方法报告 **Gomoku** 成功率 **100%**，耗时 **136s**；**Plane Battle** 成功率 **100%**，耗时 **117s**；**City Sim** 成功率 **87%**，耗时 **257s**；**Snake++** 成功率 **80%**，耗时 **198s**；**Roguelike** 成功率 **47%**，耗时 **232s**。
- 与学术多智能体基线相比，在 **Roguelike** 上，Contract-Coding 报告成功率 **47%**，而 **OpenHands** 为 **30%**，**MetaGPT** 为 **10%**，**ChatDev** 为 **10%**，**FLOW** 为 **0%**。
- 与商业工具相比，在 **Roguelike** 上，它与 **Trae** 的 **47%** 持平，优于 **CodeBuddy** 的 **40%**，优于 **Lingma** 的 **33%**，低于 **Gemini Studio** 的 **63%**。
- HEG 消融显示成功率相同，但速度更慢：在 **Roguelike** 上，**Ours w/o HEG** 为 **47%**、耗时 **510s**，而 **Ours (Full)** 为 **47%**、耗时 **232s**；在 **Snake++** 上，成功率从 **78%**、耗时 **465s** 提升到 **80%**、耗时 **198s**。
- 论文称存在次线性的上下文效应：对于 **Roguelike** 任务，**8,857 tokens** 的代码仓库被压缩为约 **1,900 tokens** 的契约，压缩比约为 **4.6x**。
- 摘要还称在 Greenfield-5 上实现了 **47% functional success** 和 **near-perfect structural integrity**，但摘录中没有给出结构完整性的直接数值指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13100v1](http://arxiv.org/abs/2604.13100v1)
