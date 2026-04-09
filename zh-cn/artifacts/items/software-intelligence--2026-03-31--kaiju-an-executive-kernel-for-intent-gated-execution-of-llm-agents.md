---
source: arxiv
url: http://arxiv.org/abs/2604.02375v1
published_at: '2026-03-31T21:38:28'
authors:
- Cormac Guerin
- Frank Guerin
topics:
- llm-agents
- tool-use
- agent-execution
- security-gating
- parallel-planning
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# KAIJU: An Executive Kernel for Intent-Gated Execution of LLM Agents

## Summary
## 摘要
KAIJU 是一种面向 LLM 智能体的执行层架构，它将规划与工具执行分离，并加入一个外部意图门控来授权工具调用。论文认为，这样可以减少上下文增长、支持并行执行，并阻止一些仅靠提示词无法防止的 ReAct 风格智能体失效模式和安全问题。

## 问题
- ReAct 风格的工具智能体会在多轮过程中累积完整历史，导致 token 呈二次增长：论文称总成本为 $O(n^{2}k)$，一个包含 7 个工具的任务约为 63K tokens，一个包含 18 个工具的任务约为 250K tokens。
- 模型在每一轮都保留对工具使用的控制权，因此在工具失败或只得到部分结果后，它可能提前停止、退回到参数化知识，或转而询问用户，而不是完成任务。
- 安全规则通常放在提示词或模型侧防护中。论文认为，这种做法难以应对幻觉、提示注入、上下文溢出和自适应攻击。

## 方法
- KAIJU 将智能体拆分为推理层和执行层。LLM 先生成一个依赖图计划，随后由 executive kernel 负责调度、依赖解析、工具分发、失败恢复和最终结果传递。
- 主要的安全机制是 Intent-Gated Execution (IGX)。每次工具调用都会根据四个变量进行检查：scope、intent、impact，以及来自外部权威的 clearance。
- 当依赖关系允许时，执行层会并行运行工具，并使用 `param_refs` 将前面节点的输出注入后续工具参数中，而不必强制进入完整的串行推理循环。
- 系统在执行期间通过三种模式自适应调整：在依赖波次边界进行反思的 Reflect、每完成 N 个节点后反思一次的 nReflect，以及为每个节点配备观察器的 Orchestrator。
- 工具调用失败时，会触发一个有范围限制的微规划器，添加替代节点，例如用新参数重试、改用其他工具或跳过，同时保持失败节点不可变，以便审计。

## 结果
- 在论文的示例中，支持并行函数调用的 ReAct 基线共进行了 9 次 LLM 调用、14 次工具执行，耗时 64.5 秒。
- 在同一查询上，Reflect 模式下的 KAIJU 共进行了 4 次 LLM 调用、10 次工具执行，耗时 41.8 秒，按墙钟时间计算约比 ReAct 快 1.54 倍。
- 论文称，由于规划开销，KAIJU 在简单查询上存在延迟劣势；在中等复杂度任务上会趋于接近；在需要并行收集数据的计算型查询上则有结构性优势。
- 论文称，token 复杂度从 ReAct 的 $O(n^{2}k)$ 改进为 Reflect 模式下的 $O(nkd)$，以及 Orchestrator 模式下的 $O(nk)$，其中 $d$ 是依赖深度。
- 与此前的 DAG 执行工作相比，论文称 LLM Compiler 相对串行 ReAct 的加速最高可达 3.7 倍，而作者观察到，在简单场景中增益接近这一水平，在复杂查询上约为 7 倍，在高度复杂查询上相对串行 ReAct 最高可达 18 倍。当前摘录没有给出这些数字对应的基准表或数据集细节。
- 一些结论是结构层面的，而不是基于基准测试：模型不会观察到门控拒绝，被阻止的工具会隐藏在执行层之后，授权是在编译后的代码中强制执行，而不是依靠提示词指令。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02375v1](http://arxiv.org/abs/2604.02375v1)
