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
SmellBench 测试 LLM 编码智能体是否能在真实 Python 代码库中修复架构代码异味。论文发现，智能体可以修复一些真实异味，也能识别许多误报，但激进修复经常让代码库变差。

## 问题
- 架构代码异味会跨模块影响可维护性，所以修复它们需要设计层面的推理，不能只做局部缺陷补丁。
- 静态检测器会产生大量误报；在这个基准中，专家复审发现 65 个检测出的高严重级别异味里有 41 个是误报，占 63.1%。
- 现有 LLM 修复基准通常用失败测试作为判定依据，而架构异味需要对依赖、API 和设计意图作出判断。

## 方法
- 作者围绕 scikit-learn v1.7.2 中 65 个高严重级别 PyExamine 检测结果构建 SmellBench，覆盖 Scattered Functionality、Redundant Abstractions、Unstable Dependency、Improper API Usage 和 God Object 异味。
- 专家将每个异味标注为 False Positive、True Positive 或 Partially Valid，然后复审 715 个智能体-任务结果中的智能体改动。
- 每个智能体都会收到一个任务包，其中包含异味报告、受影响文件、受影响模块、针对该异味的操作手册和 few-shot 示例。
- 智能体通过基于 MCP 的任务循环工作：认领任务、检查并编辑代码、运行编译和导入检查，然后报告 Done、Accepted、Need More Work 或 Blocked。
- GEPA 使用简单和中等示例优化针对各类异味的操作手册，而高难度评估任务在提示优化期间保持未见。

## 结果
- 该基准包含 65 个高严重级别异味：20 个 Scattered Functionality、25 个 Redundant Abstractions、14 个 Unstable Dependency、4 个 Improper API Usage 和 2 个 God Object 案例。
- 专家标签包括 41 个 False Positive 案例、11 个 True Positive 案例和 13 个 Partially Valid 案例；总体误报率为 63.1%。
- 根据智能体改动后重新运行 PyExamine 的结果，最佳智能体在该基准上的解决率达到 47.7%。
- 智能体识别误报时，与专家判断的一致性最高达到 κ=0.94。
- 修复越激进，代码库净质量越容易受损：最激进的智能体引入了 140 个新异味。
- 专家标签可靠性报告为平均成对二次加权 Cohen’s κ_w=0.67；将标签合并为真实与非真实两类后，标注者在 81.5% 的案例上达成一致，Fleiss’ κ=0.45。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07001v2](https://arxiv.org/abs/2605.07001v2)
