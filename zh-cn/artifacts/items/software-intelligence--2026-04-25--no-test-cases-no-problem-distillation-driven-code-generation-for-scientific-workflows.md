---
source: arxiv
url: http://arxiv.org/abs/2604.23106v1
published_at: '2026-04-25T02:01:54'
authors:
- Siddeshwar Raghavan
- Tanwi Mallick
topics:
- scientific-code-generation
- multi-agent-systems
- knowledge-distillation
- code-intelligence
- llm-reasoning
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# No Test Cases, No Problem: Distillation-Driven Code Generation for Scientific Workflows

## Summary
## 摘要
MOSAIC 是一个无需训练的多智能体科学代码生成系统，用于没有输入/输出测试用例的场景。它用教师-学生蒸馏和紧凑的共享上下文替代基于测试用例的验证，并在多个 LLM 骨干模型上提升了 SciCode 的结果。

## 问题
- 标准代码生成智能体依赖 I/O 测试用例来检查和改进代码，但科学工作流任务通常只提供函数签名和领域背景。
- 在科学问题中，构造一个有效的测试用例往往已经需要知道正确算法，这会造成验证僵局。
- 这很重要，因为科学代码需要可执行的程序、正确的算法，以及在物理、化学、生物、材料科学和数学等领域的串联子问题中保持数值精度。

## 方法
- MOSAIC 不用执行反馈做语义检查，而是采用教师-学生蒸馏设置。教师读取一个小规模、互不重叠的验证子集及其金标准代码，并生成领域特定的推理模板和伪代码。
- 在学生侧，Rationale Agent 将这些模板作为少样本指导，把新问题拆解为有序子步骤，然后由 Coding Agent 为每一步编写 Python 代码。
- Consolidated Context Window (CCW) 只保留先前的函数签名和一行摘要，因此后续智能体能保留所需历史，而不必携带完整代码和长推理轨迹。
- Debugger Agent 最多运行 k 轮代码修复，但仅限于语法和导入修复，而不做算法验证，这样就把语法层面的约束与语义层面的约束分开了。
- 该系统不依赖特定 LLM，按领域分桶，并为每个科学领域使用独立记忆，以减少跨领域干扰。

## 结果
- 在 SciCode 上使用 GPT-4o 时，MOSAIC 解决了 65 个主问题中的 12 个、283 个子问题中的 113 个；SciCode 基线分别为 7/65 和 94/283。论文还称，在五个科学领域中的准确率提升最高可达 24%。
- 在 SciCode 上使用 Claude Sonnet 4 时，MOSAIC 达到论文报告的最佳科学任务结果：65 个主问题中解决 13 个，283 个子问题中解决 118 个；基线为 9/65 和 109/283。
- 在 SciCode 上使用 Gemini 2.5 Flash 时，MOSAIC 得到 11/65 个主问题和 117/283 个子问题；基线为 7/65 和 112/283。
- SciCode 的领域示例：使用 GPT-4o 时，物理子问题从 48/145 提高到 56/145，数学从 4/24 提高到 10/24；使用 Gemini 2.5 Flash 时，数学从 1/24 提高到 12/24。
- SciCode 上的消融实验（GPT-4o）显示，完整系统达到 12/65 和 113/283，而基线为 7/65 和 94/283。保留全部先前代码的无限制 CCW 会使结果降到 4/65 和 57/283，这支持了紧凑上下文设计。
- 在通用代码基准上，MOSAIC 在 HumanEval 上得分 92.53，在 MBPP 上得分 84.90，在 APPS 上得分 24.71。它在 MBPP 和 APPS 上排名第一，在 HumanEval 上排名第二，落后于 CodeSIM 的 93.60。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23106v1](http://arxiv.org/abs/2604.23106v1)
