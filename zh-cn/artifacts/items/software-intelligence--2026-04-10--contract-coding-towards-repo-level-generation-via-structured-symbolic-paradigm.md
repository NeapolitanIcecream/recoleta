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
## 总结
Contract-Coding 是一种面向仓库级代码生成的方法，它先把含糊的用户意图转成结构化契约，再用这个契约协调并行代码生成和验证。论文声称，这样可以减少跨文件混乱，并提高多文件软件任务的成功率。

## 问题
- 从含糊意图进行仓库级生成时经常失败，因为代理会按顺序生成文件，而且必须携带越来越多的原始代码上下文。
- 早期的设计错误会扩散到后续文件，冗长的代码历史会把重要的架构细节挤出模型的有效注意范围。
- 这对自主软件生产很重要，因为多文件项目需要一致的 API、文件结构和跨模块行为，而不只是局部正确的代码。

## 方法
- 系统先把松散的用户请求转换成 **Language Contract**，这是一个结构化工件，记录需求、API、模块到文件的映射、类型签名和状态定义。
- 然后把代码生成分解为两步：先从意图推断契约，再在契约而不是之前生成的原始代码条件下生成每个文件。
- **Hierarchical Execution Graph (HEG)** 根据契约调度任务；当接口已经定义好时，多个模块实现可以并行运行。
- 验证器和契约审计器检查生成代码是否符合契约、所需文件和符号是否存在，以及代码变更是否需要更新契约。
- 契约通过受限的添加/更新操作构建和修订，并检查无效图结构或不一致签名等问题。

## 结果
- 在 Greenfield-5 基准上，完整方法在 **Gomoku** 上以 **136s** 达到 **100%** 成功率，在 **Plane Battle** 上以 **117s** 达到 **100%**，在 **City Sim** 上以 **257s** 达到 **87%**，在 **Snake++** 上以 **198s** 达到 **80%**，在 **Roguelike** 上以 **232s** 达到 **47%**。
- 在 **Roguelike** 上，与学术多智能体基线相比，Contract-Coding 的成功率为 **47%**，而 **OpenHands** 为 **30%**，**MetaGPT** 为 **10%**，**ChatDev** 为 **10%**，**FLOW** 为 **0%**。
- 在 **Roguelike** 上，与商业工具相比，它与 **Trae** 的 **47%** 持平，优于 **CodeBuddy** 的 **40%**，优于 **Lingma** 的 **33%**，但低于 **Gemini Studio** 的 **63%**。
- HEG 消融显示成功率相同，但速度更慢：在 **Roguelike** 上，**Ours w/o HEG** 用 **510s** 达到 **47%**，而 **Ours (Full)** 用 **232s** 达到 **47%**；在 **Snake++** 上，**78%**、**465s** 改进为 **80%**、**198s**。
- 论文声称存在次线性的上下文影响：在 **Roguelike** 任务中，**8,857 tokens** 的仓库被压缩为约 **1,900 tokens** 的契约，大约压缩 **4.6x**。
- 摘要还声称在 Greenfield-5 上达到 **47% functional success** 和 **near-perfect structural integrity**，但摘录没有给出结构完整性的直接数值指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13100v1](http://arxiv.org/abs/2604.13100v1)
