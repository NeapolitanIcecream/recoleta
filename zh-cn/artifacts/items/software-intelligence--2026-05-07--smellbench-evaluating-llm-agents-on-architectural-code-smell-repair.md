---
source: arxiv
url: https://arxiv.org/abs/2605.07001v2
published_at: '2026-05-07T22:33:32'
authors:
- Ion George Dinu
- "Marian Cristian Mih\u0103escu"
- Traian Rebedea
topics:
- llm-agents
- code-intelligence
- automated-refactoring
- software-architecture
- code-smells
- benchmark
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair

## Summary
## 摘要
SmellBench 测试 LLM 编码代理能否修复真实 Python 代码库中的架构代码异味。论文发现，代理能修复一部分真实异味，也能识别许多误报，但激进修复常常会让代码库变得更差。

## 问题
- 架构代码异味会影响跨模块的可维护性，所以修复它们需要设计层面的推理，而不是局部 bug 补丁。
- 静态检测器会产生很多误报；在这个基准中，专家复核发现 65 个检测到的严重异味里有 41 个是误报，占 63.1%。
- 现有的 LLM 修复基准通常用失败测试作为判定标准，而架构异味需要对依赖、API 和设计意图作出判断。

## 方法
- 作者围绕 scikit-learn v1.7.2 中由 PyExamine 检出的 65 个严重级别异味构建了 SmellBench，覆盖 Scattered Functionality、Redundant Abstractions、Unstable Dependency、Improper API Usage 和 God Object 异味。
- 专家将每个异味标记为 False Positive、True Positive 或 Partially Valid，然后复核了 715 个代理-任务结果中的代码修改。
- 每个代理都会收到一份任务包，里面有异味报告、受影响文件、受影响模块、针对该异味的操作手册和 few-shot 示例。
- 代理通过基于 MCP 的任务循环处理任务：领取任务、检查并编辑代码、运行编译和导入检查，然后报告 Done、Accepted、Need More Work 或 Blocked。
- GEPA 使用 easy 和 medium 示例优化针对异味的操作手册，而 hard 级别的评估任务在提示优化期间保持不可见。

## 结果
- 该基准包含 65 个 hard 异味：20 个 Scattered Functionality、25 个 Redundant Abstractions、14 个 Unstable Dependency、4 个 Improper API Usage 和 2 个 God Object 案例。
- 专家标注结果为 41 个 False Positive、11 个 True Positive 和 13 个 Partially Valid；整体误报率为 63.1%。
- 最好的代理在基准上的解决率达到 47.7%，这个结果基于代理修改后重新运行 PyExamine 得出。
- 代理识别误报时，与专家判断的一致性最高达到 κ=0.94。
- 修复激进程度会损害代码库净质量：最激进的代理引入了 140 个新异味。
- 专家标注可靠性报告为平均两两 quadratic-weighted Cohen’s κ_w=0.67；当标注合并为 genuine 与 not genuine 时，标注者在 81.5% 的案例上达成一致，Fleiss’ κ=0.45。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07001v2](https://arxiv.org/abs/2605.07001v2)
