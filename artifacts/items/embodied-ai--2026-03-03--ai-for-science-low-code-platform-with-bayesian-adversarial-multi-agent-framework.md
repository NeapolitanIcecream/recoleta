---
source: arxiv
url: http://arxiv.org/abs/2603.03233v1
published_at: '2026-03-03T18:25:00'
authors:
- Zihang Zeng
- Jiaquan Zhang
- Pengze Li
- Yuan Qi
- Xi Chen
topics:
- ai-for-science
- multi-agent-systems
- bayesian-optimization
- code-generation
- low-code-platform
relevance_score: 0.11
run_id: materialize-outputs
---

# AI-for-Science Low-code Platform with Bayesian Adversarial Multi-Agent Framework

## Summary
本文提出一个面向 AI for Science 的低代码平台，用贝叶斯对抗式多智能体框架来联合改进代码、测试用例和提示词，从而降低 LLM 幻觉与错误传播。其核心主张是：不必完全信任单个 LLM，也能更稳定地产生科学代码，并让较小模型获得接近或超过更大模型的表现。

## Problem
- 科学代码生成里，LLM 不仅会在代码上幻觉，也会在测试用例上出错；在多智能体系统中，这些错误会层层传递，导致最终结果不可靠。
- AI4S 任务通常要求复杂流程、领域约束和物理一致性，普通单元测试难以验证科学正确性，静态提示或自我修正方法往往不够。
- 领域专家常不会提示工程，原始需求可能含糊或带有隐式专业知识，容易让模型误解任务。

## Approach
- 框架使用 3 个角色：Task Manager 负责把用户自然语言需求整理成计划并生成/更新测试；Solution Generator 生成候选代码；Evaluator 给代码、测试和提示词打分。
- 它把“写代码”和“出测试”变成对抗式共进化：TM 像挑战者不断设计更能暴露缺陷的测试，SG 像求解者不断修复代码去通过这些测试。
- 关键不是完全依赖 LLM 裁决，而是用非 LLM 的贝叶斯更新规则，根据提示词历史表现分数 \(S_3\) 来更新下一轮采用哪些测试样例和参考代码，从而减少对单一底座模型可靠性的依赖。
- 为了避免把所有候选代码都真实执行，他们还用基于代码结构相似性的贝叶斯优化，借助 AST/代码嵌入来估计哪些候选更值得昂贵测试。
- 平台还包含面向非程序员科学家的低代码交互：先把模糊需求澄清并转成结构化计划、子任务和科学约束，再进入迭代生成。

## Results
- 在 **SciCode** 上，作者声称对多种底座模型都有稳定提升；最大相对提升达到 **87.1%**，对应 **Qwen3-8b** 的子问题解决率（without knowledge）从 **13.2%** 提升到 **24.7%**。
- 一个代表性结果是：**Qwen3-14b + 本框架** 在 SciCode 的无知识设定下子问题解决率达到 **30.6%**，与 **Qwen3-235B-A22b-Instruct** 基线的 **30.6%** 持平，作者据此声称小模型可匹敌大约 **16×** 规模的大模型。
- 在 **SciCode** 上，**Qwen3-32b + 本框架** 的无知识子问题解决率为 **33.0%**，高于 **Qwen3-235B** 基线的 **30.6%**；这对应摘要中的核心主张：借助该框架，**32B 开源模型可超过 235B 模型**（比较对象为未加框架的基线）。
- 其它 SciCode 结果也显示一致增益，例如 **GPT-4o** 子问题解决率从 **24.1% → 37.2%**（无知识，**+54.3%**），**Deepseek-v3** 从 **27.8% → 40.3%**（无知识，**+45.0%**），**Claude-sonnet-4** 从 **31.3% → 42.7%**（无知识，**+36.4%**）。
- 在 **ScienceAgentBench** 上，使用 **GPT-4o** 作为底座时，作者宣称达到新的 SOTA，尤其是 **Valid Execution Rate (VER)**：**90.2%**（without knowledge）和 **87.3%**（with knowledge），并称其在 **Success Rate** 与 **Code-Based Score** 上也处于领先。
- 文本未给出完整的 ScienceAgentBench 全表对比数值（表 2 被截断），因此除 VER 外，其他指标的精确基线差值无法从摘录中完整核验。

## Link
- [http://arxiv.org/abs/2603.03233v1](http://arxiv.org/abs/2603.03233v1)
