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
MOSAIC 是一个无需训练的多智能体系统，用于没有输入/输出测试用例的科学代码生成。它用师生式蒸馏和紧凑的共享上下文取代基于测试用例的验证，并且在多个 LLM 基座模型上都提升了 SciCode 结果。

## 问题
- 标准代码生成代理依赖 I/O 测试用例来检查和修正代码，但科学工作流任务通常只提供函数签名和领域背景。
- 在科学问题中，要构造有效的测试用例，往往先得知道正确算法，这会造成验证死锁。
- 这很重要，因为科学代码需要可执行程序、正确算法，以及在物理、化学、生物、材料科学和数学等领域中跨多个串联子问题的数值精度。

## 方法
- MOSAIC 用师生式蒸馏代替执行反馈做语义检查。教师读取一个较小的、不重叠的验证子集，其中包含金标准代码，并生成领域相关的推理模板和伪代码。
- 学生侧的 Rationale Agent 用这些模板作少样本指导，把新问题拆成有顺序的子步骤，然后 Coding Agent 为每一步编写 Python 代码。
- Consolidated Context Window（CCW）只保留之前的函数签名和一句话摘要，这样后续代理能保留所需历史，同时不用带上完整代码和较长的推理轨迹。
- Debugger Agent 运行代码，最多进行 k 轮修复，但它只处理语法和导入修复，不做算法验证，这样把句法层面的对齐和语义层面的对齐分开。
- 该系统与具体 LLM 无关，按领域分桶，并为每个科学领域使用独立记忆，以减少跨领域干扰。

## 结果
- 在使用 GPT-4o 的 SciCode 上，MOSAIC 解决了 12/65 个主问题和 113/283 个子问题；SciCode 基线分别是 7/65 和 94/283。论文还指出，在五个科学领域上的准确率最高提升可达 24%。
- 在使用 Claude Sonnet 4 的 SciCode 上，MOSAIC 达到目前报告中的最佳科学结果：13/65 个主问题和 118/283 个子问题；基线分别是 9/65 和 109/283。
- 在使用 Gemini 2.5 Flash 的 SciCode 上，MOSAIC 解决了 11/65 个主问题和 117/283 个子问题；基线分别是 7/65 和 112/283。
- SciCode 的领域例子：在 GPT-4o 下，物理子问题从 48/145 提升到 56/145，数学从 4/24 提升到 10/24；在 Gemini 2.5 Flash 下，数学从 1/24 提升到 12/24。
- SciCode 的消融实验（GPT-4o）显示，完整系统为 12/65 和 113/283，而基线为 7/65 和 94/283。一个不受限制、保留全部历史代码的 CCW 会把性能降到 4/65 和 57/283，这支持紧凑上下文设计。
- 在通用代码基准上，MOSAIC 在 HumanEval 上得分 92.53，在 MBPP 上得分 84.90，在 APPS 上得分 24.71。它在 MBPP 和 APPS 上排第一，在 HumanEval 上排第二，落后于 HumanEval 得分 93.60 的 CodeSIM。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23106v1](http://arxiv.org/abs/2604.23106v1)
